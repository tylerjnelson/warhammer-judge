#!/usr/bin/env python3
"""
collect_model_answers.py — run the eval_quality question set through the SHIPPED
retrieval pipeline ONCE per question, then fan the identical (system prompt + rules
context + question) prompt out to every chat-capable Groq model and record each full
answer verbatim. NO automated grading — correctness is judged by hand from the report.

Efficiency: chunks are assembled exactly once per question (retrieval.build_context,
the same call render_chat makes) and the resulting `messages` are reused for every
model, so the heavy reranker pipeline runs 45×, not 45×N-models.

Resilience: each (question, model) result is checkpointed to JSON as it lands, so the
run is resumable (re-running skips pairs already recorded) and an interrupt loses
nothing. 429s are retried with backoff honoring `retry-after` (per-model buckets, so
one model's limit never blocks another — see test_per_model_ratelimit.py).

Usage:
  python tests/manual/collect_model_answers.py --count 2     # smoke test (first 2 Qs)
  python tests/manual/collect_model_answers.py               # full set, all models
  python tests/manual/collect_model_answers.py --report-only # rebuild MD from JSON
"""
import argparse, json, logging, re, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

import app, config, retrieval, serving
from openai import OpenAI, RateLimitError
from tests.manual.eval_quality import SUITES, BUDGET, TOK

EDITION = "10e"
OUT_JSON = Path(__file__).resolve().parent / "model_eval_results.json"
OUT_MD   = Path(__file__).resolve().parent / "model_eval_report.md"

# Chat-capable text models on our Groq key. Excludes audio (whisper/orpheus),
# the prompt-guard / gpt-oss-safeguard classifiers (not Q&A models).
MODELS = [
    "qwen/qwen3-32b",          # current PROD
    "qwen/qwen3.6-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "allam-2-7b",
    # EXCLUDED — not viable grounded-RAG backends (verified 2026-06-24):
    #   groq/compound       → 413 Request Entity Too Large on our ~2800-tok context
    #                         (agentic tool-definition overhead leaves no room).
    #   groq/compound-mini  → internally routes to llama-3.3-70b-versatile (its 429
    #                         names that model), sharing that per-model bucket, so it
    #                         429s under load and adds nothing distinct.
]
MAX_OUT = config.MAX_OUTPUT_TOKENS


def strip_reasoning(raw: str) -> str:
    a = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    a = re.sub(r'<think>.*$', '', a, flags=re.DOTALL).strip()
    return a or raw


def ask(client, model, messages):
    """One completion with 429-aware backoff. Returns a result dict."""
    MAX_ATTEMPTS, WAIT_CAP = 4, 45        # never sit on a multi-minute retry-after
    for attempt in range(MAX_ATTEMPTS):
        t0 = time.time()
        try:
            r = client.chat.completions.create(
                model=model, messages=messages,
                max_completion_tokens=MAX_OUT, temperature=0.1,
            )
            raw = r.choices[0].message.content or ""
            return {
                "answer": strip_reasoning(raw), "raw_len": len(raw),
                "prompt_tokens": r.usage.prompt_tokens,
                "completion_tokens": r.usage.completion_tokens,
                "finish_reason": r.choices[0].finish_reason,
                "latency_s": round(time.time() - t0, 1),
                "attempts": attempt + 1, "error": None,
            }
        except RateLimitError as e:
            h = getattr(getattr(e, "response", None), "headers", {}) or {}
            wait = min(float(h.get("retry-after", 0) or 0) or 2 ** attempt, WAIT_CAP)
            if attempt == MAX_ATTEMPTS - 1:
                return {"answer": "", "error": f"rate_limited: {str(e)[:120]}",
                        "finish_reason": "error", "attempts": attempt + 1}
            time.sleep(wait + 0.5)
        except Exception as e:
            return {"answer": "", "error": str(e)[:200],
                    "finish_reason": "error", "attempts": attempt + 1}


def load_results():
    if OUT_JSON.exists():
        return json.loads(OUT_JSON.read_text())
    return {"meta": {}, "questions": []}


def build_report(data):
    lines = [f"# Model answer collection — {len(MODELS)} models",
             f"\nGroq models: {', '.join(MODELS)}",
             f"\nPipeline: retrieval.build_context → serving.build_messages (budget {BUDGET} tok). "
             f"max_completion_tokens={MAX_OUT}, temperature=0.1. Reasoning `<think>` stripped from answers.",
             "\n⚠ groq/compound[-mini] are agentic (may use tools/web), not pure grounded Q&A.\n"]
    for q in data["questions"]:
        lines.append("\n" + "=" * 100)
        lines.append(f"## [{q['idx']}] {q['suite']} · mp={'ON' if q['mp'] else 'OFF'} · ctx {q['ctx_tok']} tok")
        lines.append(f"\n**Q:** {q['query']}")
        lines.append(f"\n**Expected concepts (ground-truth anchors):** {q['groups']}\n")
        lines.append("<details><summary>rules context sent to every model</summary>\n")
        lines.append("```\n" + q["context"][:8000] + "\n```\n</details>\n")
        for m in MODELS:
            res = q["answers"].get(m)
            if not res:
                lines.append(f"\n### {m}\n_(not collected)_")
                continue
            tag = f"finish={res.get('finish_reason')} · {res.get('completion_tokens','?')} compl tok · {res.get('latency_s','?')}s"
            if res.get("error"):
                lines.append(f"\n### {m}\n`{tag}` ⚠ ERROR: {res['error']}")
            else:
                lines.append(f"\n### {m}\n`{tag}`\n\n{res['answer']}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=999, help="number of questions")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--concurrency", type=int, default=6, help="models in flight per question")
    ap.add_argument("--models", default="", help="comma list to restrict to (backfill)")
    ap.add_argument("--pace", type=float, default=0.0, help="seconds to sleep between questions")
    ap.add_argument("--out", default="", help="output filename stem (default model_eval_results); "
                                              "use a distinct stem to keep a prior run's baseline intact")
    args = ap.parse_args()

    global MODELS, OUT_JSON, OUT_MD
    if args.models:
        MODELS = [m.strip() for m in args.models.split(",") if m.strip()]
    if args.out:
        OUT_JSON = Path(__file__).resolve().parent / f"{args.out}.json"
        OUT_MD   = Path(__file__).resolve().parent / f"{args.out}.md"

    if args.report_only:
        OUT_MD.write_text(build_report(load_results()))
        print(f"Wrote {OUT_MD}")
        return

    app.get_reranker(); app.get_embedder()
    client = OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL)

    # Flatten questions (carry suite + mp + concept groups for the report).
    flat = []
    for suite, cases, mp in SUITES:
        for c in cases:
            flat.append((suite, c[0], c[1], mp))
    sel = flat[args.start:args.start + args.count]

    data = load_results()
    by_idx = {q["idx"]: q for q in data["questions"]}

    for i, (suite, query, groups, mp) in enumerate(sel, args.start + 1):
        q = by_idx.get(i)
        if q is None:
            chunks  = retrieval.build_context(query, edition=EDITION, mission_pack_mode=mp, resolution={})
            context = serving.format_rules_context(chunks, BUDGET)
            messages = serving.build_messages([], chunks, query, EDITION, mission_pack_mode=mp)
            q = {"idx": i, "suite": suite, "query": query, "mp": mp,
                 "groups": groups, "context": context, "ctx_tok": TOK(context),
                 "_messages": messages, "answers": {}}
            data["questions"].append(q)
            by_idx[i] = q
        else:
            # resuming: rebuild messages (not persisted) only if more models are pending
            chunks  = retrieval.build_context(query, edition=EDITION, mission_pack_mode=mp, resolution={})
            q["_messages"] = serving.build_messages([], chunks, query, EDITION, mission_pack_mode=mp)

        # collect a model if it's missing OR its prior result was an error (backfill)
        pending = [m for m in MODELS
                   if m not in q["answers"] or q["answers"][m].get("error")]
        print(f"[{i}/{len(flat)}] {suite:15} ({len(pending)} models) {query[:50]}", flush=True)
        if not pending:
            continue

        def run_one(m):
            r = ask(client, m, q["_messages"])
            print(f"    {m:42} {r.get('finish_reason'):8} "
                  f"{r.get('completion_tokens','?')!s:>4} tok  {r.get('latency_s','?')}s"
                  f"{'  ⚠'+r['error'][:40] if r.get('error') else ''}", flush=True)
            return m, r

        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            for m, r in ex.map(run_one, pending):
                q["answers"][m] = r

        # checkpoint after each question (drop the non-serializable messages).
        # Preserve the full model roster in meta even on a restricted backfill run.
        save = {"meta": {**data.get("meta", {}), "budget": BUDGET, "max_out": MAX_OUT},
                "questions": [{k: v for k, v in qq.items() if k != "_messages"}
                              for qq in data["questions"]]}
        OUT_JSON.write_text(json.dumps(save, indent=1))
        if args.pace and i < args.start + len(sel):
            time.sleep(args.pace)

    # Only regenerate the report on a full run; a restricted backfill would drop
    # the other models from the report. Run --report-only afterward to rebuild.
    if not args.models:
        OUT_MD.write_text(build_report(load_results()))
    print(f"\nDone. {OUT_JSON}")


if __name__ == "__main__":
    main()

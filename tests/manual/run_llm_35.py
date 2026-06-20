#!/usr/bin/env python3
"""
run_llm_35.py — run the 35-question pool through the LIVE LLM (Groq qwen3-32b) with
the real retrieval context, to inspect actual answers (not just retrieval).

Mirrors render_chat's fresh-query path exactly: retrieve → unit slice + seed → rerank
→ assemble → inject_sequence_neighbors → call_llm. Writes a markdown transcript.

TPM note: Groq free tier is 6K tokens/min (input+output, reasoning <think> billed too),
so calls are PACED (~--pace s apart) to avoid 429s. call_llm already auto-reduces on a
rate-limit hit; reduced answers are flagged by the app itself.

Usage:
  python tests/manual/run_llm_35.py --count 3            # smoke test (first 3)
  python tests/manual/run_llm_35.py --pace 55            # full 35, paced 55s apart
  python tests/manual/run_llm_35.py --start 3 --count 5  # a slice
"""
import argparse, logging, sys, time, warnings
from pathlib import Path
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app, config
from tests.manual.eval_30q import SUITES, BUDGET, TOK

EDITION = "10e"
OUT = Path(__file__).resolve().parent / "llm_35_report.md"


def final_chunks(query, mp_mode):
    """The assembled chunks render_chat would hand to call_llm."""
    expanded, where, _ = app.process_query(query, EDITION, mp_mode)
    raw   = app.retrieve(expanded, where, EDITION, n_results=config.RERANK_CANDIDATES)
    units = app.retrieve_unit_slice(query, EDITION, mp_mode, resolution={})
    rules = app.retrieve_rules_slice(expanded, EDITION, mp_mode, config.TOP_K_RULES * 2)
    rq    = expanded if config.RERANK_USE_EXPANDED else query
    pool  = raw + rules
    raw   = raw + app.seed_definitions(rq, pool, EDITION, mp_mode) \
                + app.seed_referenced_rules(rq, pool, EDITION, mp_mode)
    app.rerank_pools(rq, EDITION, mp_mode, raw, rules, units)
    app.rank_seeded_below_parents(raw + rules, EDITION, mp_mode)
    chunks = app.assemble_context(raw, rules, EDITION, mp_mode, unit_chunks=units)
    return app.inject_sequence_neighbors(chunks, EDITION)


import re

def llm_verbose(chunks, query, mp):
    """Call the model directly (not app.call_llm) so we can capture usage + the raw
    reasoning trace. Mirrors build_messages; keeps reasoning_format at the default
    (raw) so the billed <think> tokens are visible. Returns
    (stripped_answer, raw_content, usage, finish_reason)."""
    messages = app.build_messages([], chunks, query, EDITION, mission_pack_mode=mp)
    client   = app.get_llm_client()
    for attempt in range(3):                       # simple 429 backoff (no app.call_llm fallback here)
        try:
            r = client.chat.completions.create(
                model=config.LLM_MODEL, messages=messages,
                max_completion_tokens=config.MAX_OUTPUT_TOKENS, temperature=0.1,
            )
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < 2:
                time.sleep(35)
                continue
            raise
    raw    = r.choices[0].message.content or ""
    answer = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
    return (answer or raw), raw, r.usage, r.choices[0].finish_reason


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pace", type=float, default=55.0, help="seconds between LLM calls")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=999)
    args = ap.parse_args()

    app.get_reranker(); app.get_embedder()
    # flatten the pool with its suite + mp flag
    flat = [(s, q, c[2] if len(c) > 2 else {}, mp)
            for s, cases, mp in SUITES for c in cases for q in [c[0]]]
    sel = flat[args.start:args.start + args.count]

    OUT.write_text(f"# Live-LLM transcript — {config.LLM_MODEL} "
                   f"(max_completion_tokens={config.MAX_OUTPUT_TOKENS}, reasoning=raw/default)\n\n"
                   f"{len(sel)} questions · budget {BUDGET} tok · pace {args.pace}s\n\n")
    truncated = 0
    for i, (suite, query, checks, mp) in enumerate(sel, args.start + 1):
        chunks = final_chunks(query, mp)
        ctx_tok = TOK(app.format_rules_context(chunks, BUDGET))
        t0 = time.time()
        answer, raw, usage, finish = llm_verbose(chunks, query, mp)
        dt = time.time() - t0
        cut = (finish == "length")
        truncated += cut
        think_chars = len(raw) - len(answer)
        # transcript: usage (billed tokens incl reasoning) + raw reasoning (collapsed) + answer
        block = (f"## [{i}] {suite} · mp={'ON' if mp else 'OFF'} · {dt:.1f}s\n\n"
                 f"`billed: prompt={usage.prompt_tokens} completion={usage.completion_tokens} "
                 f"total={usage.total_tokens} · finish={finish}"
                 f"{'  ⚠ TRUNCATED' if cut else ''}` · ctx {ctx_tok} tok\n\n"
                 f"**Q:** {query}\n\n"
                 f"<details><summary>reasoning trace ({think_chars} chars, billed)</summary>\n\n"
                 f"```\n{raw[:6000]}\n```\n\n</details>\n\n"
                 f"**A:** {answer}\n\n---\n\n")
        with open(OUT, "a") as f:
            f.write(block)
        print(f"[{i}] {suite:9} {dt:5.1f}s  compl={usage.completion_tokens:4} "
              f"finish={finish:6} ans={len(answer):4}ch  | {query[:46]}")
        sys.stdout.flush()
        if i < args.start + len(sel):
            time.sleep(args.pace)
    print(f"\nTruncated (finish=length): {truncated}/{len(sel)}\nWrote {OUT}")


if __name__ == "__main__":
    main()

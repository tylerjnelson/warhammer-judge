#!/usr/bin/env python3
"""
backfill_until_done.py — resilient driver for the 3072-cap rerun of the two
reasoning models (qwen3.6-27b, gpt-oss-20b) that the Groq free-tier DAILY token
cap (TPD) keeps interrupting.

Why this exists: a 429 is rejected at admission and costs ZERO tokens (measured
~0.85s, before generation — see spec/free-llm-providers.md §5b), so polling while
daily-capped wastes time but not budget. Only successful calls draw down the daily
allowance. So we gate each backfill pass on a real-sized probe: if the probe 429s
(daily cap), sleep and retry later; if it succeeds, run one paced collection pass
to harvest whatever daily budget has freed. Repeat until both models reach 43/43
or the run-deadline (next-day rollover) passes.

Run in the background; it checkpoints through collect_model_answers.py's own
resumable JSON, so an interrupt loses nothing.
"""
import json, subprocess, sys, time
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from openai import OpenAI

# Retargeted 2026-07-04 at the uncapped (--tpm-room) run: the three reasoners whose DAILY
# caps (TPD/RPD) interrupt a single full pass (gpt-oss-120b & qwen3.6-27b hit the daily
# meter with the per-minute bucket still full; gpt-oss-20b usually finishes same-day).
OUT_STEM = "model_eval_uncapped"
# gpt-oss-120b/gpt-oss-20b/qwen3.6-27b reached 43/43 after overnight daily-cap rollover.
# Remaining straggler: llama-3.3-70b (100K TPD < ~127K needed for 43 Qs, so ≤~34/day — needs
# a multi-day harvest). allam-2-7b's 6 gaps are structural 413s (context window), uncollectable.
MODELS  = ["llama-3.3-70b-versatile"]
RESULTS = ROOT / f"tests/manual/{OUT_STEM}.json"
TARGET  = 43
PROBE_TOKENS    = 3000          # real-sized: a tiny probe passes on a sliver of daily budget (misleading)
IDLE_SLEEP      = 1800          # 30 min between probes while daily-capped
DEADLINE_HRS    = 48          # llama-3.3-70b needs ~1.5 days (100K TPD < ~127K for 43 Qs)

client = OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL, max_retries=0)


def coverage():
    d = json.loads(RESULTS.read_text())
    out = {}
    for m in MODELS:
        out[m] = sum(1 for q in d["questions"]
                     if q["answers"].get(m) and not q["answers"][m].get("error"))
    return out


def daily_available(model) -> bool:
    """True iff a real-sized call SUCCEEDS (daily budget actually usable)."""
    try:
        client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": "Reply with the single word OK."}],
            max_completion_tokens=PROBE_TOKENS, temperature=0)
        return True
    except Exception as e:
        print(f"    probe {model}: capped ({str(e)[:70]})", flush=True)
        return False


def missing_range():
    """Contiguous [start, count] covering the still-missing question indices, so a pass
    only re-walks the tail (already-answered ones inside the span are skipped fast) and we
    never burn the 120s pace / 4x retry backoff on the 40+ already-done cells. Returns
    (None, None) when nothing is missing."""
    d = json.loads(RESULTS.read_text())
    miss = sorted(q["idx"] for q in d["questions"]
                  for m in MODELS
                  if not (q["answers"].get(m) and not q["answers"][m].get("error")))
    if not miss:
        return None, None
    return miss[0] - 1, miss[-1] - miss[0] + 1     # --start is 0-based; idx is 1-based


def run_pass():
    start, count = missing_range()
    if start is None:
        return
    subprocess.run([sys.executable, str(ROOT / "tests/manual/collect_model_answers.py"),
                    "--models", ",".join(MODELS), "--out", OUT_STEM, "--tpm-room",
                    "--start", str(start), "--count", str(count),
                    "--pace", "8", "--concurrency", str(len(MODELS))])


def main():
    deadline = time.time() + DEADLINE_HRS * 3600
    p = 0
    while time.time() < deadline:
        # Crash-guard the whole body: a transient error (a subprocess hiccup, a JSON read
        # racing a checkpoint) must never kill a multi-day harvest — log and retry.
        try:
            cov = coverage()
            print(f"[{time.strftime('%H:%M:%S')}] coverage {cov}", flush=True)
            if all(v >= TARGET for v in cov.values()):
                print("COMPLETE", cov, flush=True)
                return
            # NO probe-gate: a 429 costs ZERO tokens, so attempt the tail directly —
            # failed calls are free and a success harvests freed daily budget straight
            # into a real answer instead of a throwaway probe.
            p += 1
            print(f"=== backfill pass {p} (tail from missing range) ===", flush=True)
            run_pass()
            if coverage() == cov:      # no progress -> daily-capped; wait for the trickle
                print(f"    no progress; sleeping {IDLE_SLEEP//60} min", flush=True)
                time.sleep(IDLE_SLEEP)
        except Exception as e:
            print(f"    !! pass error ({str(e)[:120]}); sleeping {IDLE_SLEEP//60} min", flush=True)
            time.sleep(IDLE_SLEEP)
    print("DEADLINE reached; final", coverage(), flush=True)


if __name__ == "__main__":
    main()

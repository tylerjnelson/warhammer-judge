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

MODELS  = ["qwen/qwen3.6-27b", "openai/gpt-oss-20b"]
RESULTS = ROOT / "tests/manual/model_eval_3072.json"
TARGET  = 43
PROBE_TOKENS    = 3000          # real-sized: a tiny probe passes on a sliver of daily budget (misleading)
IDLE_SLEEP      = 1800          # 30 min between probes while daily-capped
DEADLINE_HRS    = 24

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


def run_pass():
    subprocess.run([sys.executable, str(ROOT / "tests/manual/collect_model_answers.py"),
                    "--models", ",".join(MODELS), "--out", "model_eval_3072",
                    "--pace", "120", "--concurrency", "2"])


def main():
    deadline = time.time() + DEADLINE_HRS * 3600
    p = 0
    while time.time() < deadline:
        cov = coverage()
        print(f"[{time.strftime('%H:%M:%S')}] coverage {cov}", flush=True)
        if all(v >= TARGET for v in cov.values()):
            print("COMPLETE", cov, flush=True)
            return
        # gate on the bottleneck model (qwen3.6 is the most token-hungry / least covered)
        if daily_available(MODELS[0]):
            p += 1
            print(f"=== budget available -> backfill pass {p} ===", flush=True)
            run_pass()
        else:
            print(f"    daily-capped; sleeping {IDLE_SLEEP//60} min", flush=True)
            time.sleep(IDLE_SLEEP)
    print("DEADLINE reached; final", coverage(), flush=True)


if __name__ == "__main__":
    main()

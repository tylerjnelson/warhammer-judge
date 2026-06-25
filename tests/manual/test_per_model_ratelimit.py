#!/usr/bin/env python3
"""
test_per_model_ratelimit.py — empirically test spec/free-llm-providers.md §5:
"Groq rate limits are per-model, not account-wide ... exhausting one model's limit
does not lock you out of the others."

Method:
  1. Deliberately drive the PROD model (config.LLM_MODEL) into a 429 by firing many
     cheap requests concurrently (trips RPM, the fastest limit to hit).
  2. The instant PROD returns 429, fire ONE request at each ALT model on the SAME key.
     If §5 holds, the alts answer 200 while PROD is cooling down.
  3. Re-confirm PROD is still 429 (proves the alt success wasn't just PROD recovering).

This SPENDS a little free-tier quota on purpose. It does not multi-account or add keys
(both ToS-clean per §2/§5). Read-only against the codebase; no app state touched.

Usage:
  python tests/manual/test_per_model_ratelimit.py
  python tests/manual/test_per_model_ratelimit.py --max-fire 120 --concurrency 16
"""
import argparse, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

import config
from openai import OpenAI, RateLimitError

# Alt models on the same Groq key, each with its own per-model bucket (§5).
ALT_MODELS = ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]

PING = [{"role": "user", "content": "Reply with the single word: ok"}]


def client():
    return OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL)


def call(c, model):
    """One tiny completion. Returns (ok, status, detail, headers)."""
    try:
        r = c.chat.completions.create(
            model=model, messages=PING, max_completion_tokens=1, temperature=0,
        )
        return True, 200, (r.choices[0].message.content or "").strip(), {}
    except RateLimitError as e:
        h = getattr(getattr(e, "response", None), "headers", {}) or {}
        return False, 429, str(e)[:160], dict(h)
    except Exception as e:
        code = getattr(getattr(e, "response", None), "status_code", "ERR")
        return False, code, str(e)[:160], {}


def rl_headers(h):
    """Pull the Groq rate-limit headers worth seeing."""
    keys = ["retry-after", "x-ratelimit-limit-requests", "x-ratelimit-remaining-requests",
            "x-ratelimit-limit-tokens", "x-ratelimit-remaining-tokens",
            "x-ratelimit-reset-requests", "x-ratelimit-reset-tokens"]
    return {k: h[k] for k in keys if k in h}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-fire", type=int, default=150, help="max PROD requests to fire")
    ap.add_argument("--concurrency", type=int, default=12)
    args = ap.parse_args()

    prod = config.LLM_MODEL
    c = client()

    print(f"PROD model : {prod}")
    print(f"ALT models : {', '.join(ALT_MODELS)}")
    print(f"Base URL   : {config.LLM_BASE_URL}\n")

    # ── Phase 0: sanity — every model answers when fresh ─────────────────────────
    print("── Phase 0: baseline (all models fresh) ──")
    for m in [prod] + ALT_MODELS:
        ok, code, detail, _ = call(c, m)
        print(f"  {m:30} {code}  {detail!r}")
    print()

    # ── Phase 1: deliberately trip a 429 on PROD and KEEP it saturated ───────────
    # PROD's limit resets fast (retry-after ~1s), so a one-shot 429 would cool down
    # before we finish testing the alts. Instead a background flood fires PROD in a
    # tight loop for the whole window, so PROD stays 429 throughout Phases 2-3 — the
    # alt successes can't be dismissed as "PROD just recovered".
    import threading
    stop = threading.Event()
    flood_stats = {"fired": 0, "n429": 0, "headers": {}}
    flood_lock = threading.Lock()

    def flooder():
        cc = client()
        while not stop.is_set():
            ok, code, detail, headers = call(cc, prod)
            with flood_lock:
                flood_stats["fired"] += 1
                if code == 429:
                    flood_stats["n429"] += 1
                    flood_stats["headers"] = headers or flood_stats["headers"]

    print(f"── Phase 1: flooding {prod} with {args.concurrency} threads until 429 ──")
    threads = [threading.Thread(target=flooder, daemon=True) for _ in range(args.concurrency)]
    for t in threads:
        t.start()
    t0 = time.time()
    while time.time() - t0 < 30:
        with flood_lock:
            n429, fired = flood_stats["n429"], flood_stats["fired"]
        if n429:
            break
        time.sleep(0.1)
    if not flood_stats["n429"]:
        stop.set()
        print(f"  No 429 in {flood_stats['fired']} requests in 30s — limits higher than "
              f"expected; cannot test §5 without an active limit.")
        return
    headers = flood_stats["headers"]
    print(f"  429 reached after ~{fired} requests in {time.time()-t0:.1f}s; flood continues")
    rh = rl_headers(headers)
    if rh:
        print(f"  rate-limit headers: {rh}")
    print()

    # ── Phase 2: while PROD is HELD at its limit, hit each ALT on the SAME key ────
    print("── Phase 2: ALT models while PROD is held rate-limited (the §5 test) ──")
    alt_results = {}
    for m in ALT_MODELS:
        ok, code, detail, headers2 = call(c, m)
        alt_results[m] = (ok, code)
        verdict = "✓ answered" if ok else "✗ blocked"
        print(f"  {m:30} {code}  {verdict}  {detail!r}")
    print()

    # ── Phase 3: confirm PROD is STILL limited (flood still running) ──────────────
    print("── Phase 3: confirm PROD still limited (flood still active) ──")
    ok, code, detail, _ = call(c, prod)
    prod_still_limited = (code == 429)
    print(f"  {prod:30} {code}  {'still limited' if prod_still_limited else 'recovered/answered'}")
    stop.set()
    for t in threads:
        t.join(timeout=5)
    print(f"  (flood fired {flood_stats['fired']} reqs, {flood_stats['n429']} were 429)")
    print()

    # ── Verdict ──────────────────────────────────────────────────────────────────
    alts_ok = all(ok for ok, _ in alt_results.values())
    print("── VERDICT ──")
    if alts_ok and prod_still_limited:
        print("  ✓ CONFIRMED §5: PROD was 429 while every ALT answered 200 on the same "
              "key → limits are per-model, not account-wide. Model rotation is viable.")
    elif alts_ok and not prod_still_limited:
        print("  ~ PARTIAL: ALTs answered, but PROD recovered before Phase 3, so we can't "
              "fully rule out 'PROD just cooled down'. Re-run with more --concurrency to "
              "keep PROD saturated through Phase 2.")
    else:
        blocked = [m for m, (ok, _) in alt_results.items() if not ok]
        print(f"  ✗ REFUTED / inconclusive: ALT(s) blocked while PROD limited: {blocked}. "
              "This would indicate an account-wide or shared bucket — re-check before "
              "relying on §5 model rotation.")


if __name__ == "__main__":
    main()

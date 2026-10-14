#!/usr/bin/env python3
"""
grade_prod.py — mechanical first-pass gate over a single production model's answers,
to verify "prod answers every eval question accurately" after the rule-10 prompt fix.

This does NOT replace the hand-grade (the methodology in model_eval_graded.md reads each
answer against the context). It catches the objective failure modes automatically so the
manual read only has to adjudicate the genuinely subtle ones:

  • TRUNCATED   finish_reason == 'length'  (a severed ruling)
  • EMPTY       no answer text
  • REFUSED     "do not clearly address" while context was present
  • MISSING     an expected ground-truth anchor group absent from the ANSWER text
  • VP MISS     the two known Leviathan VP-math slips: Q11 must land on 5 VP (Tactical
                Assassination, NOT the 4 VP Fixed branch); Q12 must land on 6 VP
                (Bring It Down 20-wd monster: 2 +1 +1 +1 base +1 Tactical achieve-bonus).

Everything else is printed for the human read (each answer's opening ruling line).

Usage:
  python tests/manual/collect_model_answers.py --models "openai/gpt-oss-120b" --out model_eval_verify
  python tests/manual/grade_prod.py --in model_eval_verify --model "openai/gpt-oss-120b"

(Prod model is openai/gpt-oss-120b since 2026-07-21; the previous prod qwen/qwen3-32b was
retired when Groq closed it. The VP checks below are model-agnostic ground truth — gpt-oss-120b
resolves Q12 natively, without the rule-10 crutch qwen3-32b needed.)
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent

# Known exact-value expectations for the two questions prod slipped on at baseline.
# A pass requires the correct VP value to appear AND the wrong one to not be the ruling.
VP_EXPECT = {
    11: {"want": "5", "avoid_ruling": "4"},   # Tactical Assassination = 5 VP, not 4 (Fixed)
    12: {"want": "6", "avoid_ruling": "5"},   # Bring It Down 20-wd monster w/ Tactical = 6 VP
}

REFUSAL = re.compile(r"do not clearly address|recommend checking the official", re.I)


def ruling_line(answer: str) -> str:
    """The first substantive line — usually the [Ruling] that carries the VP number."""
    for ln in (l.strip() for l in answer.splitlines()):
        if ln and not ln.startswith(("#", "```")):
            return ln[:200]
    return answer[:200].replace("\n", " ")


def anchor_hit(answer: str, group: list) -> bool:
    """A group passes if ANY of its synonym strings appears in the answer (case-insens)."""
    low = answer.lower()
    return any(s.lower() in low for s in group)


ANSWER_KEY = {}   # per-question must / must_not regexes (11e set; see --edition)


def grade(q: dict, model: str) -> tuple[str, list]:
    res = (q.get("answers") or {}).get(model)
    if not res:
        return "NOT_COLLECTED", ["no result recorded"]
    if res.get("error"):
        return "ERROR", [res["error"]]
    ans = (res.get("answer") or "").strip()
    notes = []
    if res.get("finish_reason") == "length":
        notes.append("TRUNCATED (finish_reason=length)")
    if not ans:
        return "EMPTY", notes or ["empty answer"]
    if REFUSAL.search(ans):
        notes.append("REFUSED with context present")
    # anchor groups (ground-truth concepts that must surface in the ANSWER)
    for grp in q.get("groups", []):
        if not anchor_hit(ans, grp):
            notes.append(f"MISSING anchor {grp}")
    # known VP-value checks
    exp = VP_EXPECT.get(q["idx"])
    if exp:
        rl = ruling_line(ans)
        if exp["want"] not in ans:
            notes.append(f"VP MISS: expected {exp['want']}VP not found")
        elif exp["avoid_ruling"] and re.search(rf"\b{exp['avoid_ruling']}\s*VP\b", rl, re.I):
            notes.append(f"VP MISS: ruling line still shows {exp['avoid_ruling']}VP")
    key = ANSWER_KEY.get(q["idx"])
    if key:
        # Models emit typographic dashes ("1‑5", "fall‑back": U+2011/2010/2013) — fold
        # them to "-" so the answer-key patterns match the words, not the glyphs.
        ans = re.sub(r"[\u2010\u2011\u2012\u2013\u2014]", "-", ans)
        for pat in key.get("must", []):
            if not re.search(pat, ans, re.I):
                notes.append(f"FACT MISS: answer lacks /{pat}/")
        rl = ruling_line(ans)
        for pat in key.get("must_not", []):
            if re.search(pat, rl, re.I):
                notes.append(f"FACT MISS: ruling line states /{pat}/")
    status = "OK" if not notes else ("FLAG" if any(n.startswith(("TRUNC", "EMPTY", "VP MISS", "REFUS", "FACT MISS")) for n in notes) else "REVIEW")
    return status, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="model_eval_verify")
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--edition", default="10e",
                    help="11e: grade against eval_suites_11e.ANSWER_KEY instead of the 10e VP checks")
    args = ap.parse_args()

    global VP_EXPECT, ANSWER_KEY
    if args.edition == "11e":
        from tests.manual.eval_suites_11e import ANSWER_KEY as KEY_11E
        VP_EXPECT, ANSWER_KEY = {}, KEY_11E

    path = HERE / f"{args.inp}.json"
    if not path.exists():
        sys.exit(f"no {path} — run collect_model_answers.py --models '{args.model}' --out {args.inp} first")
    data = json.loads(path.read_text())
    qs = sorted(data["questions"], key=lambda q: q["idx"])

    counts = {"OK": 0, "REVIEW": 0, "FLAG": 0, "EMPTY": 0, "ERROR": 0, "NOT_COLLECTED": 0}
    print(f"\nGrading {args.model} over {len(qs)} questions ({path.name})\n" + "=" * 78)
    for q in qs:
        status, notes = grade(q, args.model)
        counts[status] = counts.get(status, 0) + 1
        mark = {"OK": "✓", "REVIEW": "·", "FLAG": "✗", "EMPTY": "✗", "ERROR": "E", "NOT_COLLECTED": "?"}[status]
        res = (q.get("answers") or {}).get(args.model) or {}
        tok = res.get("completion_tokens", "?")
        print(f"{mark} Q{q['idx']:<2} {q['suite']:<14} {str(tok):>4}tok  {ruling_line(res.get('answer','') or '')[:88]}")
        for n in notes:
            print(f"      ↳ {n}")
    print("=" * 78)
    print("  ".join(f"{k}={v}" for k, v in counts.items() if v))
    hard = counts["FLAG"] + counts["EMPTY"] + counts["ERROR"] + counts["NOT_COLLECTED"]
    print(f"\n{'PASS — no mechanical failures; do the manual read on any · REVIEW rows.' if hard == 0 else f'{hard} question(s) need attention (✗/E/?).'}")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()

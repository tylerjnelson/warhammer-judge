#!/usr/bin/env python3
"""
eval_segment_maxpool_ab.py — A/B probe for config.RERANK_SEGMENT_MAXPOOL.

Runs the REAL retrieval path (tests.verify.eval_retrieval.final_context) for every
test query with the flag OFF then ON, and diffs the ORDERED final chunks: rank
moves, chunks added/dropped, and the rerank score of the rank-1 chunk. Then runs
the hard retrieval gate in BOTH flag states so we can see whether the flag breaks
or preserves the 23-case regression.

Query set = the transcript Pile-In turn + eval_rerank_ab CASES + eval_retrieval
CASES/GAPS (deduped), i.e. the whole standing test set.
"""
import importlib, logging, sys, time, warnings
from pathlib import Path
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app, config
EV   = importlib.import_module("tests.verify.eval_retrieval")
ABm  = importlib.import_module("tests.manual.eval_rerank_ab")

EDITION = "10e"

def title(c):
    ls = [l for l in c["text"].splitlines() if l.strip()]
    return (ls[0].lstrip("# ").strip()[:38] if ls else "?")

def snapshot(query, mp_mode):
    """Ordered final chunks: [(title, category, rerank_or_cosine)]."""
    chunks = EV.final_context(query, EDITION, mp_mode)
    out = []
    for c in chunks:
        r = c.get("rerank")
        score = r if r is not None else c.get("similarity")
        out.append((title(c), c["metadata"].get("category", ""), round(score or 0.0, 3)))
    return out

def rank_of(snap, needle):
    for i, (t, _, _) in enumerate(snap):
        if needle.lower() in t.lower():
            return i + 1
    return None

# (query, mp_mode, optional needle to track its rank move)
QUERIES = [
    ("after i charge if i make the charge, how far can i pile in", False, "pile in"),
    ("my unit is in a land raider. if the land raider makes a normal move and "
     "then my unit gets out, can they charge", False, "assault ramp"),
    ("if a unit fell back, can it shoot and charge", False, "fall back"),
    ("when i pile in after a charge can i move into engagement range", False, "pile in"),
    ("after i shoot can i then charge the same unit", False, "charg"),
]
# fold in the standing sets (no needle)
for q, _want in ABm.CASES:
    QUERIES.append((q, False, None))
for case in EV.CASES:
    QUERIES.append((case["query"], False, None))
for case in EV.GAPS:
    QUERIES.append((case["query"], True, None))

def diff(off, on):
    """Human-readable diff between two ordered snapshots."""
    off_t = [t for t, _, _ in off]
    on_t  = [t for t, _, _ in on]
    added   = [t for t in on_t if t not in off_t]
    dropped = [t for t in off_t if t not in on_t]
    moved   = []
    for i, t in enumerate(on_t):
        if t in off_t:
            j = off_t.index(t)
            if i != j:
                moved.append((t, j + 1, i + 1))
    return added, dropped, moved

def run_ab():
    app.get_reranker(); app.get_embedder()
    print("=" * 80)
    print("A/B — RERANK_SEGMENT_MAXPOOL   off vs on   (ordered final context)")
    print("=" * 80)
    changed = unchanged = 0
    for query, mp, needle in dict.fromkeys(QUERIES):  # dedup, keep order
        config.RERANK_SEGMENT_MAXPOOL = False
        off = snapshot(query, mp)
        config.RERANK_SEGMENT_MAXPOOL = True
        t0 = time.time(); on = snapshot(query, mp); ms = (time.time() - t0) * 1000
        config.RERANK_SEGMENT_MAXPOOL = False

        segs = app.segment_query(query)
        added, dropped, moved = diff(off, on)
        any_change = bool(added or dropped or moved)
        changed += any_change; unchanged += (not any_change)

        print(f"\nQ: {query[:72]}")
        print(f"   segments({len(segs)}): {segs if len(segs) > 1 else '— single-clause (no-op)'}")
        if needle:
            print(f"   rank[{needle!r}]: off={rank_of(off, needle)}  on={rank_of(on, needle)}")
        if not any_change:
            print("   = no change")
        else:
            if moved:   print("   moved : " + "; ".join(f"{t!r} {a}->{b}" for t, a, b in moved))
            if added:   print("   +added: " + ", ".join(repr(t) for t in added))
            if dropped: print("   -drop : " + ", ".join(repr(t) for t in dropped))
            print(f"   ON top3: " + " | ".join(f"{t} ({s})" for t, _, s in on[:3]))
            print(f"   OFFtop3: " + " | ".join(f"{t} ({s})" for t, _, s in off[:3]))
        print(f"   on-latency {ms:.0f} ms")
    print(f"\n{'-'*80}\nchanged: {changed} | unchanged: {unchanged} | total: {changed+unchanged}")

def run_gate(flag):
    config.RERANK_SEGMENT_MAXPOOL = flag
    print(f"\n{'='*80}\nGATE  eval_retrieval.py  with RERANK_SEGMENT_MAXPOOL={flag}\n{'='*80}")
    rc = EV.run(EDITION, verbose=False)
    config.RERANK_SEGMENT_MAXPOOL = False
    return rc

if __name__ == "__main__":
    run_ab()
    off_rc = run_gate(False)
    on_rc  = run_gate(True)
    print(f"\n{'='*80}\nGATE SUMMARY  off: {'PASS' if off_rc==0 else 'FAIL'}  "
          f"on: {'PASS' if on_rc==0 else 'FAIL'}\n{'='*80}")
    sys.exit(on_rc)

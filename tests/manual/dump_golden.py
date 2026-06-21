#!/usr/bin/env python3
"""
dump_golden.py — behavioral oracle for the retrieval-pipeline refresh.
======================================================================
Drives the REAL shipped pipeline (mirrors render_chat / eval_quality.run_pipeline)
over the full standing query set and dumps, for every query, the ORDERED final
context with each chunk's scores (similarity, rerank, rank_score) + provenance
flags. Output is a deterministic JSON file used as the regression oracle: the
refresh is held byte-stable against it at every phase boundary.

Usage:
  python tests/manual/dump_golden.py            # writes spec/refresh-baseline/golden.json
  python tests/manual/dump_golden.py --out X     # custom path
  python tests/manual/dump_golden.py --compare spec/refresh-baseline/golden.json
                                                 # diff current pipeline vs a saved golden
"""
import argparse, json, logging, sys, warnings
from pathlib import Path
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app, config, retrieval  # noqa: E402

EDITION = "10e"

# Provenance-ish flags currently smeared across chunk dicts (pre-refresh). We
# record whichever are present so the oracle captures HOW a chunk got there, not
# just that it did.
PROV_FLAGS = ["unit_seed", "dep_seed", "seq_neighbor", "lexical",
              "dep_bridge", "dep_parent_keys"]


def _round(x):
    return None if x is None else round(float(x), 4)


def dump_chunk(c: dict) -> dict:
    m = c.get("metadata", {})
    text = c.get("text", "")
    title = text.splitlines()[0][:60] if text.splitlines() else ""
    rec = {
        "key": app.content_key(c),
        "title": title,
        "category": m.get("category"),
        "unit_name": m.get("unit_name"),
        "similarity": _round(c.get("similarity")),
        "rerank": _round(c.get("rerank")),
        "rank_score": _round(c.get("rank_score")),
    }
    prov = [f for f in PROV_FLAGS if c.get(f)]
    if prov:
        rec["prov"] = prov
    return rec


def final_context(query: str, mp_mode: bool) -> list[dict]:
    """The exact shipped fresh-query path — now the single retrieval.build_context
    engine (the same call render_chat makes), so the oracle tracks production."""
    return retrieval.build_context(
        query, edition=EDITION, mission_pack_mode=mp_mode, resolution={})


def collect_queries():
    """Every query in the standing suite, tagged with its toggle state."""
    import importlib
    er = importlib.import_module("tests.verify.eval_retrieval")
    eq = importlib.import_module("tests.manual.eval_quality")
    out = []  # (suite, query, mp_mode)
    for case in er.CASES:
        for state in ("on", "off"):
            if case.get(state) is not None:
                out.append((f"eval_retrieval/{case['layer']}", case["query"], state == "on"))
    for suite_name, cases, mp in eq.SUITES:
        for case in cases:
            out.append((f"eval_quality/{suite_name}", case[0], mp))
    return out


def build_golden():
    app.get_reranker(); app.get_embedder()
    queries = collect_queries()
    golden = []
    for suite, query, mp in queries:
        chunks = final_context(query, mp)
        golden.append({
            "suite": suite, "query": query, "mp_mode": mp,
            "chunks": [dump_chunk(c) for c in chunks],
        })
    return golden


def compare(saved_path: str):
    saved = json.loads(Path(saved_path).read_text())
    saved_by_q = {(g["query"], g["mp_mode"]): g for g in saved}
    current = build_golden()
    drift = 0
    rs_drift = 0
    for g in current:
        key = (g["query"], g["mp_mode"])
        ref = saved_by_q.get(key)
        if ref is None:
            print(f"NEW query (not in golden): {g['query'][:60]}")
            continue
        new_keys = [c["key"] for c in g["chunks"]]
        old_keys = [c["key"] for c in ref["chunks"]]
        if new_keys != old_keys:
            drift += 1
            print(f"\nDRIFT  [{g['suite']}] {g['query'][:70]}")
            print(f"   was ({len(old_keys)}): " +
                  ", ".join(f"{c['category']}:{c['title'][:22]}" for c in ref["chunks"]))
            print(f"   now ({len(new_keys)}): " +
                  ", ".join(f"{c['category']}:{c['title'][:22]}" for c in g["chunks"]))
        else:
            # same membership/order — check the effective sort key (rank_score) is stable
            old_rs = {c["key"]: c["rank_score"] for c in ref["chunks"]}
            for c in g["chunks"]:
                if c["key"] in old_rs and c["rank_score"] != old_rs[c["key"]]:
                    rs_drift += 1
                    print(f"RANK_SCORE drift [{g['suite']}] {c['title'][:30]}: "
                          f"{old_rs[c['key']]} -> {c['rank_score']}")
    print(f"\n{'='*72}\n{drift} queries with ORDER/MEMBERSHIP drift "
          f"+ {rs_drift} rank_score changes out of {len(current)}")
    return 1 if (drift or rs_drift) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "spec/refresh-baseline/golden.json"))
    ap.add_argument("--compare", default=None)
    args = ap.parse_args()
    if args.compare:
        sys.exit(compare(args.compare))
    golden = build_golden()
    Path(args.out).write_text(json.dumps(golden, indent=1, ensure_ascii=False))
    nchunks = sum(len(g["chunks"]) for g in golden)
    print(f"Wrote {args.out}: {len(golden)} queries, {nchunks} total chunks.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
eval_rerank_ab.py — recall/quality probe for the shipped Layer-3 retrieval path
(rerank + dependency seeding + ability→rule context seeding; spec/reranker.md).

Reranking + seeding are now unconditional in the pipeline (no toggle), so this is
a single-path report (not an A/B). For each canonical query it runs the REAL
pipeline and checks that the rules a surfaced chunk DEPENDS ON reach the budgeted
context:
  • definitions a rule references (engagement_range, unit_coherency, …)
  • core/mission-pack rules a unit/ability references by name (Deadly Demise, …)
and reports the seeded deps (with the gate score), WANT recall, rerank+seed latency,
and the final budgeted token count (must stay <= budget).

The hard pass/fail regression gate is tests/verify/eval_retrieval.py (run at the end).
"""
import logging, sys, time, warnings
from pathlib import Path
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app, config

EDITION = "10e"
MP_MODE = False
TOK     = lambda s: len(s) // config.TOKEN_CHAR_RATIO
BUDGET  = config.RULES_CONTEXT_TOKEN_BUDGET

# (query, rules the surfaced chunk depends on that should reach the budgeted context).
CASES = [
    ("how does Fall Back work", set()),
    ("how do saving throws work", set()),
    ("can I charge after advancing", {"engagement_range"}),
    ("do excess mortal wounds spill over to the next model", set()),
    ("who controls an objective marker", set()),
    ("I charged with one unit. My opponent has a unit with Fights First. Who fights first?", set()),
    ("how do normal moves work", {"engagement_range"}),
    ("what happens when a unit is below half strength", set()),
    ("how does the charge move work and what makes it fail", {"engagement_range", "unit_coherency"}),
    ("can a unit shoot after falling back", set()),
    # Unit-focused questions: the rule is CONTEXT the ability references by name
    # (seed_referenced_rules). Real units whose ability text names a USR.
    ("what does the Painboy's Dok's Toolz ability do", {"5_inflict_damage_sub0"}),       # Feel No Pain
    ("what happens to nearby units when a Lifta Wagon is destroyed", {"5_inflict_damage_sub1"}),  # Deadly Demise
    ("how does Vargard Obyron's Ghostwalk Mantle ability work", {"1_fights_first"}),     # Fights First
]

def norm(s):
    return " ".join(s.split())

def snippet(chunk):
    lines = [l for l in chunk["text"].splitlines()
             if l.strip() and not l.startswith("#") and not l.startswith("**")]
    return norm(" ".join(lines))[:60]

def stem_of(chunk, bc_to_stem):
    return bc_to_stem.get(chunk["metadata"].get("breadcrumb"))

def ctx_stems(chunks, ctx_norm, bc_to_stem):
    return {stem_of(c, bc_to_stem) for c in chunks
            if snippet(c) and snippet(c) in ctx_norm}

def run_pipeline(query, bc_to_stem):
    """The shipped retrieval path (mirrors render_chat): retrieve → seed (defs +
    referenced rules) → rerank → parent-cap → assemble → budget."""
    expanded, where, _ = app.process_query(query, EDITION, MP_MODE)
    raw    = app.retrieve(expanded, where, EDITION, n_results=config.RERANK_CANDIDATES)
    rules  = app.retrieve_rules_slice(expanded, EDITION, MP_MODE, config.TOP_K_RULES * 2)
    rq     = expanded if config.RERANK_USE_EXPANDED else query
    pool   = raw + rules
    seeded = (app.seed_definitions(rq, pool, EDITION, MP_MODE)
              + app.seed_referenced_rules(rq, pool, EDITION, MP_MODE))
    seeded_info = [(stem_of(c, bc_to_stem), c.get("dep_bridge")) for c in seeded]
    raw    = raw + seeded
    pool_n = len({app.content_key(c) for c in raw + rules})
    t0  = time.time()
    app.rerank_pools(rq, EDITION, MP_MODE, raw, rules)
    app.rank_seeded_below_parents(raw + rules, EDITION, MP_MODE)
    ms  = (time.time() - t0) * 1000
    chunks = app.assemble_context(raw, rules, EDITION, MP_MODE)
    final  = app.inject_sequence_neighbors(chunks, EDITION)
    ctx    = app.format_rules_context(final, BUDGET)
    return ctx_stems(final, norm(ctx), bc_to_stem), TOK(ctx), ms, pool_n, seeded_info

def run_report():
    bc_to_stem, _ = app.get_dep_index(EDITION)
    app.get_reranker(); app.get_embedder()      # warm so first timing isn't cold load
    print(f"{'='*78}\nSHIPPED RETRIEVAL PATH — {config.RERANK_MODEL}\n"
          f"pool={config.RERANK_CANDIDATES}  budget={BUDGET} tok  ({len(CASES)} queries)\n{'='*78}")

    hits = misses = balloons = wanted = 0
    for query, want in CASES:
        ctx, tok, ms, pool_n, seeded_info = run_pipeline(query, bc_to_stem)
        if tok > BUDGET:
            balloons += 1
        seed_str = ", ".join(f"{s}@{b:.2f}" for s, b in seeded_info) if seeded_info else "—"
        print(f"\nQ: {query}")
        print(f"   seeded      : {seed_str}")
        if want:
            wanted += 1
            got  = want & ctx
            miss = want - ctx
            if not miss:
                hits += 1
            else:
                misses += 1
            print(f"   WANT[{'ok' if not miss else 'MISS'}] got={sorted(got)}"
                  f"{'  missing='+str(sorted(miss)) if miss else ''}")
        print(f"   pool {pool_n} | rerank+seed {ms:.0f} ms | budget {tok}/{BUDGET}"
              f"{'  ⚠ OVER' if tok > BUDGET else ''}")

    print(f"\n{'-'*78}")
    print(f"WANT recall: {hits}/{wanted} | misses: {misses} | over budget (must be 0): {balloons}/{len(CASES)}")

def run_regression():
    """Hard gate: the 23-case retrieval eval must stay green on the shipped path."""
    print(f"\n{'='*78}\nREGRESSION — tests/verify/eval_retrieval.py\n{'='*78}")
    import importlib
    return importlib.import_module("tests.verify.eval_retrieval").run(EDITION, verbose=False)

if __name__ == "__main__":
    run_report()
    sys.exit(run_regression())

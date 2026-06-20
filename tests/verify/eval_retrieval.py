#!/usr/bin/env python3
"""
eval_retrieval.py — retrieval-quality eval harness for The Judge.
==================================================================
Asserts that the *final context* assembled for the LLM contains the expected
Core-Rules / mission-pack chunks, and that the mission-pack HARD INVARIANT
(spec/retrieval.md) holds in BOTH toggle directions:

  • toggle ON  → mission-pack chunks may rank (and are *required* for
    mission-pack-specific queries);
  • toggle OFF → mission-pack chunks are NEVER surfaced.

It drives the real app.py assembly path (process_query → retrieve →
retrieve_rules_slice → assemble_context → inject_sequence_neighbors), so it
measures what would actually reach the model — no reimplementation of ranking.

Run:
  python tests/verify/eval_retrieval.py            # 10e, all cases
  python tests/verify/eval_retrieval.py -v         # also print the final chunk list
  python tests/verify/eval_retrieval.py --edition 10e

Exit code is non-zero if any case fails — usable as a CI / pre-Layer-3 gate.

Seed cases are reconstructed from the failure modes recorded in
spec/retrieval.md (Core under-ranking, ordered-sequence isolation, card-deck
granularity, mission-pack toggle). Add real failing queries to CASES as they
surface — the schema is documented above CASES.
"""

import argparse
import logging
import sys
import warnings
from pathlib import Path

# ── Headless Streamlit: app.py calls st.set_page_config / @st.cache_resource at
#    import. In bare mode these warn but run; silence the noise. ────────────────
logging.getLogger("streamlit").setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import app  # noqa: E402  (after path insert)
import config  # noqa: E402


# ── Final-context assembly (mirrors render_chat's fresh-query path) ────────────

def final_context(query: str, edition: str, mp_mode: bool) -> list[dict]:
    """The chunks that would reach the LLM for a *fresh* (non-refined) query.

    Reproduces app.render_chat lines ~815-877: process_query → retrieve →
    retrieve_rules_slice → assemble_context → inject_sequence_neighbors. The
    ambiguity branch only gates the LLM call (not chunk content), so it is
    intentionally skipped here.
    """
    expanded, where, _ = app.process_query(query, edition, mission_pack_mode=mp_mode)
    raw   = app.retrieve(expanded, where, edition, n_results=config.RERANK_CANDIDATES)
    rules = app.retrieve_rules_slice(
        expanded, edition, mission_pack_mode=mp_mode,
        n_results=config.TOP_K_RULES * 2,
    )
    # Layer 3 — mirror render_chat: seed the rules a surfaced chunk depends on
    # (definitions + referenced rules), rerank the pool, parent-cap the seeded deps,
    # then assemble caps at TOP_K / budget.
    rerank_query = expanded if config.RERANK_USE_EXPANDED else query
    pool = raw + rules
    raw  = raw + app.seed_definitions(rerank_query, pool, edition, mp_mode) \
               + app.seed_referenced_rules(rerank_query, pool, edition, mp_mode)
    app.rerank_pools(rerank_query, edition, mp_mode, raw, rules)
    app.rank_seeded_below_parents(raw + rules, edition, mp_mode)
    chunks = app.assemble_context(raw, rules, edition, mission_pack_mode=mp_mode)
    return app.inject_sequence_neighbors(chunks, edition)


# ── Case schema ───────────────────────────────────────────────────────────────
# Each case has a `query` plus an optional `on:` block (toggle ON) and/or `off:`
# block (toggle OFF). Whichever blocks are present are run. Expectation keys in
# a block:
#   top_category : category of the rank-1 final chunk must equal this
#   category     : this category must appear somewhere in the final chunks
#   text_all     : every substring (case-insensitive) appears in final text
#   text_any     : at least one substring appears in final text
#   mp_required  : (ON only) the mission-pack category must appear
#   min_chunks   : final context has at least this many chunks
#   categories_subset : EVERY final chunk's category must be in this allow-list
#                       (G4 noise guard — a rules question must not pull
#                        datasheet/ability/stratagem chunks)
# UNIVERSAL INVARIANT (auto-applied, not declared): an `off:` run must contain
# ZERO mission-pack chunks. An `on:` run with mp_required must contain ≥1.

CASES = [
    # ── Layer 1: Core rules that previously lost to keyword-dense datasheets ──
    {
        "name": "Fall Back ranks Core top",
        "layer": "L1",
        "query": "how does Fall Back work",
        "on":  {"top_category": "Core_Rules", "text_all": ["fall back"]},
        "off": {"top_category": "Core_Rules", "text_all": ["fall back"]},
    },
    {
        "name": "Deep Strike surfaces Core",
        "layer": "L1",
        "query": "how does Deep Strike work",
        "on":  {"category": "Core_Rules", "text_any": ["deep strike", "deployment"]},
        "off": {"category": "Core_Rules", "text_any": ["deep strike", "deployment"]},
    },
    {
        # Sub-rule split (ingest): the bundled deployment_abilities file is split
        # per ALL-CAPS rule name, so Deep Strike is its own focused chunk rather
        # than a 1,555-tok bundle carrying Scouts/Infiltrators/Leader. Asserts the
        # split sub-chunk (by its synthesized header) reaches context.
        "name": "Deep Strike resolves to its own focused sub-chunk",
        "layer": "split",
        "query": "how does Deep Strike work",
        "on":  {"text_all": ["deployment abilities — deep strike"]},
    },
    {
        # Scraper off-by-one fix: Wahapedia renders these rules in self-titled
        # frameLight/Columns2 boxes that the old splitter dumped onto the PREVIOUS
        # h3, so Mortal Wounds was buried inside Invulnerable Saves (no own chunk)
        # and the LLM had to guess. It is now its own Core chunk.
        "name": "Mortal Wounds is its own chunk (scraper off-by-one fix)",
        "layer": "scrape",
        "query": "do excess mortal wounds spill over to the next model",
        "on":  {"category": "Core_Rules",
                "text_any": ["always applied one at a time",
                             "keep allocating damage to another model"]},
    },
    {
        # Same fix: the full Fall Back rule (incl. Desperate Escape + the
        # Battle-shock interaction) was buried in Advance Moves; fall_back_moves
        # held Moving Over Terrain text. The query that made #10 hallucinate now
        # surfaces the real rule.
        "name": "Fall Back carries Desperate Escape (scraper off-by-one fix)",
        "layer": "scrape",
        "query": "battle-shocked unit falls back desperate escape test",
        "on":  {"category": "Core_Rules",
                "text_any": ["fall back move by moving a distance",
                             "trigger one desperate escape test per phase"]},
    },
    {
        # G4 unit-name routing: a faction-less *rules* question used to retrieve
        # unfiltered (~54% datasheet/ability/stratagem noise, which fed the #10
        # hallucination). It must now be scoped to Core + mission-pack only.
        "name": "Rules question stays noise-free (G4 routing)",
        "layer": "route",
        "query": "battle-shocked unit holding an objective desperate escape falling back",
        "on":  {"categories_subset": ["Core_Rules", "Leviathan"],
                "text_any": ["objective control", "battle-shock"]},
        "off": {"categories_subset": ["Core_Rules"],
                "text_any": ["objective control", "battle-shock"]},
    },
    {
        # The other half of routing: a query that NAMES a datasheet is a unit
        # lookup and must still reach the broad (datasheet/ability) path.
        "name": "Unit lookup still reaches datasheets (G4 routing)",
        "layer": "route",
        "query": "how many wounds does a Terminator have",
        "on":  {"text_any": ["terminator"]},
    },
    {
        # G3 bare-Columns2 recovery: the Fight-phase activation-order rule
        # ("players alternate… starting with the player whose turn is not taking
        # place") lived in a bare Columns2/BreakInsideAvoid block the scraper
        # dropped — so #4 ("who fights first?") had no rule and answered
        # "simultaneously". Now captured into the Fight Phase chunk.
        "name": "Fight-phase activation order recovered (G3 bare-Columns2)",
        "layer": "scrape",
        "query": ("I charged with one unit. My opponent has a unit with Fights "
                  "First that I didn't charge. Who fights first, and can my "
                  "charging unit fight before theirs?"),
        "on":  {"text_all": ["whose turn is not taking place"]},
    },
    {
        "name": "Objective control (invariant pair)",
        "layer": "L1+INV",
        "query": "who controls an objective marker",
        # ON: mission-pack mission rules are relevant AND allowed → required.
        "on":  {"category": "Core_Rules", "mp_required": True,
                "text_any": ["objective"]},
        # OFF: only Core surfaces; zero mission-pack (auto invariant).
        "off": {"top_category": "Core_Rules", "text_any": ["objective"]},
    },

    # ── Track C: ordered sequences must travel together ──────────────────────
    {
        "name": "Saving throws pull sequence neighbors",
        "layer": "C",
        "query": "how do saving throws work",
        # seq±1 of saving_throw = allocate_attack / inflict_damage must appear.
        "on":  {"category": "Core_Rules",
                "text_all": ["saving throw"],
                "text_any": ["allocate", "inflict damage", "wound roll"]},
    },
    {
        "name": "Wound roll pulls sequence neighbors",
        "layer": "C",
        "query": "how do I make a wound roll",
        "on":  {"category": "Core_Rules",
                "text_all": ["wound roll"],
                "text_any": ["hit roll", "allocate"]},
    },

    # ── Track A: card-deck split → per-card granularity (mission-pack) ────────
    {
        "name": "Assassination resolves to its card (invariant pair)",
        "layer": "A+INV",
        "query": "Assassination secondary mission",
        "on":  {"top_category": "Leviathan", "mp_required": True,
                "text_all": ["assassination"]},
        # OFF: mission-pack gone entirely (auto invariant); no assertion on what
        # Core fallback returns.
        "off": {},
    },
    {
        "name": "Mission-pack secondary present ON / absent OFF",
        "layer": "INV",
        "query": "Bring It Down secondary mission points",
        "on":  {"mp_required": True},
        "off": {},
    },

    # ── Layer 3 (lexical/BM25 half, DONE): exact rule-name lookup ─────────────
    {
        "name": "Exact rule-name lookup surfaces parent chunk (BM25)",
        "layer": "L3-bm25",
        # "Big Guns Never Tire" lives *inside* core_rules_make_ranged_attacks.md
        # and is NOT in the top-60 dense candidates for its own name. The BM25
        # pass injects the parent chunk; before Layer 3's lexical half this failed.
        "query": "Big Guns Never Tire",
        "on":  {"category": "Core_Rules", "text_all": ["big guns never tire"]},
        "off": {"category": "Core_Rules", "text_all": ["big guns never tire"]},
    },
    {
        # G1: a *verbose* question that names a rule (here "engagement range")
        # buried among other concepts dilutes the dense score below threshold
        # (ER sim 0.34) AND falls outside BM25's length-biased top-k. The
        # full-corpus exact rule-name pass injects it. #9 in the live test.
        "name": "Exact rule-name lookup fires inside a verbose query (G1)",
        "layer": "L3-bm25",
        "query": ("Can my unit charge a unit on the second floor of a ruin "
                  "directly above me, and am I in engagement range vertically?"),
        "on":  {"text_all": ["1\" horizontally and 5\" vertically"]},
        "off": {"text_all": ["1\" horizontally and 5\" vertically"]},
    },
]

# ── KNOWN GAPS — Layer 3 (embedding-upgrade half) candidates ──────────────────
# These FAIL on the current stack (MiniLM + Layer 1/2 + the BM25 lexical half).
# The lexical half cannot help: they are conversational paraphrases that share no
# distinctive terms with the target rule, so BM25 correctly stays silent — only a
# stronger prose embedding (bge/e5) would lift the right chunk over threshold.
# Tracked as expected-failures (xfail): the suite does NOT fail on them, but flags
# loudly if one starts PASSING so we retire the gap. (The earlier BM25 gap,
# "Big Guns Never Tire", was closed by the lexical half and promoted to CASES.)
GAPS = [
    {
        "name": "Zero-keyword coherency paraphrase (embedding)",
        "layer": "L3-embed",
        "query": "my models are too far apart from each other",
        # Right chunk (Engagement Range / coherency) lands ~rank 51, sim 0.282 —
        # below SIMILARITY_THRESHOLD (0.35). A stronger embedding would lift it.
        "on": {"text_any": ["coheren", "engagement range"]},
    },
    {
        "name": "Zero-keyword line-of-sight paraphrase (embedding)",
        "layer": "L3-embed",
        "query": "shoot at something I cannot see",
        # core_rules_indirect_fire.md exists but the paraphrase scores it
        # ~sim 0.339, just under threshold; top hit is an unrelated Ability.
        "on": {"text_any": ["indirect fire", "line of sight"]},
    },
]


# ── Evaluation ────────────────────────────────────────────────────────────────

def _text_blob(chunks: list[dict]) -> str:
    return "\n".join(c["text"] for c in chunks).lower()

def check_block(chunks, block, mp_mode, mp_category):
    """Return list of failure strings ([] == pass) for one toggle run."""
    fails = []
    cats  = [c["metadata"].get("category") for c in chunks]
    blob  = _text_blob(chunks)

    # Universal invariant.
    if not mp_mode:
        leaked = [c for c in chunks if c["metadata"].get("category") == mp_category]
        if leaked:
            fails.append(f"INVARIANT: {len(leaked)} mission-pack chunk(s) leaked while toggle OFF")
    if mp_mode and block.get("mp_required"):
        if mp_category not in cats:
            fails.append(f"mp_required: no '{mp_category}' chunk in final context")

    if "top_category" in block:
        top = cats[0] if cats else None
        if top != block["top_category"]:
            fails.append(f"top_category: rank-1 is {top!r}, expected {block['top_category']!r}")
    if "category" in block and block["category"] not in cats:
        fails.append(f"category: {block['category']!r} absent (got {cats})")
    if "categories_subset" in block:
        allowed = set(block["categories_subset"])
        stray   = sorted({c for c in cats if c not in allowed})
        if stray:
            fails.append(f"categories_subset: noise categories present {stray} "
                         f"(allowed {sorted(allowed)})")
    for sub in block.get("text_all", []):
        if sub.lower() not in blob:
            fails.append(f"text_all: {sub!r} missing")
    if block.get("text_any"):
        if not any(s.lower() in blob for s in block["text_any"]):
            fails.append(f"text_any: none of {block['text_any']} present")
    if "min_chunks" in block and len(chunks) < block["min_chunks"]:
        fails.append(f"min_chunks: {len(chunks)} < {block['min_chunks']}")
    return fails


def run(edition: str, verbose: bool) -> int:
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    total = passed = 0
    print(f"\nRetrieval eval — edition {edition} · mission-pack category {mp_category!r}\n" + "=" * 72)

    for case in CASES:
        for state in ("on", "off"):
            block = case.get(state)
            if block is None:
                continue
            mp_mode = (state == "on")
            chunks  = final_context(case["query"], edition, mp_mode)
            fails   = check_block(chunks, block, mp_mode, mp_category)
            total  += 1
            ok      = not fails
            passed += ok
            mark    = "PASS" if ok else "FAIL"
            print(f"[{mark}] {case['layer']:7} {state.upper():3} · {case['name']}")
            if verbose or not ok:
                for c in chunks:
                    m = c["metadata"]
                    title = (c["text"].splitlines()[0][:34] if c["text"].splitlines() else "")
                    print(f"          {c['similarity']:.3f}  {m.get('category',''):11} {title}")
            for f in fails:
                print(f"        ↳ {f}")

    print("=" * 72)
    print(f"{passed}/{total} runs passed")

    # ── Known gaps (xfail): Layer 3 candidates ────────────────────────────────
    if GAPS:
        print("\nKnown gaps (Layer 3 candidates) — expected to fail until Layer 3 lands:")
        regressed = 0
        for case in GAPS:
            chunks = final_context(case["query"], edition, True)
            fails  = check_block(chunks, case["on"], True, mp_category)
            still_missing = bool(fails)
            status = "xfail (gap confirmed)" if still_missing else "XPASS ⚠ gap closed — retire it"
            print(f"  [{status:30}] {case['layer']:9} · {case['name']}")
            if not still_missing:
                regressed += 1
        if regressed:
            print(f"\n⚠  {regressed} known gap(s) now PASS — Layer 3 may be unnecessary for them; "
                  "review and move to CASES.")

    print()
    return 0 if passed == total else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Retrieval-quality eval for The Judge.")
    ap.add_argument("--edition", default="10e")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print final chunk list for every run, not just failures")
    args = ap.parse_args()
    sys.exit(run(args.edition, args.verbose))

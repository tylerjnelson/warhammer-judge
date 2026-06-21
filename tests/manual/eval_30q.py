#!/usr/bin/env python3
"""
eval_30q.py — 30-question retrieval-quality probe for the shipped Layer-3 path
(rerank + dependency seeding + ability→rule context seeding; spec/reranker.md).

Three non-trivial question sets, each pulling chunks from MULTIPLE parts of the
rules (so a single keyword-dense chunk can't satisfy them):

  • CORE      (10) — core-rules questions combining several mechanics
                     (mission-pack toggle OFF).
  • LEVIATHAN (10) — Leviathan mission-pack questions (toggle ON).
  • UNITS     (11) — named-unit / model interactions whose abilities reference a
                     core or mission-pack rule by name (toggle OFF) — these
                     exercise seed_referenced_rules (ability → rule context).

Grading: each question lists one or more CONCEPT GROUPS. A group is satisfied if
ANY of its substrings appears (case-insensitive) in the final budgeted context.
A question PASSES only when EVERY group is satisfied — i.e. all the distinct
ideas the answer needs actually reached the model. Every grading substring was
verified to exist in data/rule_blocks/10e before being added here.

This is a quality REPORT (per-question + per-group accuracy, seeded deps, latency,
token budget); the hard pass/fail regression gate stays tests/verify/eval_retrieval.py.

Run:  python tests/manual/eval_30q.py
"""
import logging, sys, time, warnings
from collections import Counter
from pathlib import Path
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app, config, retrieval

EDITION = "10e"
TOK     = lambda s: len(s) // config.TOKEN_CHAR_RATIO
BUDGET  = config.RULES_CONTEXT_TOKEN_BUDGET

# Each case: (query, [group, ...]) where a group is a list of acceptable
# substrings (text_any). PASS = every group satisfied.

CORE = [
    ("If a Battle-shocked unit that is below half-strength Falls Back, what tests "
     "does it take and can it still shoot or charge that turn?",
     [["desperate escape", "fall back"], ["battle-shock"], ["half-strength"]]),
    ("If I set up a unit using Deep Strike from Strategic Reserves, how far from "
     "enemy models must it arrive and can it charge that same turn?",
     [["deep strike"], ["strategic reserve"]]),
    ("When my unit makes a charge move over a barricade, can it end in Engagement "
     "Range with an enemy on the floor above, and does the barricade affect the move?",
     [["barricade"], ["engagement range"]]),
    ("How does Big Guns Never Tire let a Monster or Vehicle shoot while within "
     "Engagement Range, and what penalty applies to those ranged attacks?",
     [["big guns never tire"], ["engagement range"]]),
    ("If I shoot with an Indirect Fire weapon at a target I cannot see, what "
     "modifier applies to my hit rolls and does the target get the Benefit of Cover?",
     [["indirect fire"], ["benefit of cover", "cover"]]),
    ("How do Devastating Wounds interact with invulnerable saves and Feel No Pain — "
     "which of those can still be used against the damage?",
     [["devastating wounds"], ["invulnerable save"], ["feel no pain"]]),
    ("When a Transport is destroyed with units still embarked, how do the passengers "
     "disembark and can they take damage?",
     [["transport"], ["disembark"], ["destroyed"]]),
    ("Can a unit that Advanced still shoot Assault weapons, and is it allowed to "
     "declare a charge in the same turn?",
     [["assault"], ["advance"], ["charge"]]),
    ("In the Fight phase, when both players have units in combat and one unit has "
     "Fights First, what is the order in which units fight?",
     [["fights first"], ["whose turn is not taking place", "alternat", "pile in"]]),
    ("Does a Battle-shocked unit still control objective markers, and how does being "
     "below half-strength affect that unit?",
     [["battle-shock"], ["objective control", "objective marker"], ["half-strength"]]),
]

LEVIATHAN = [
    ("Using Tactical Missions in Leviathan, how does the Assassination Secondary "
     "Mission score when I destroy enemy Characters, and does a resurrected Character count?",
     [["assassination"], ["character"]]),
    ("Under Bring It Down with Tactical Missions, how many VP for destroying a "
     "20-wound Monster, and what is the maximum I can score from it?",
     [["bring it down"], ["wounds characteristic"]]),
    ("On the Take and Hold primary mission, how does VP scoring work in the second "
     "to fourth battle rounds versus the fifth battle round?",
     [["take and hold"], ["fifth battle round"]]),
    ("How are the attacker and defender determined in a Leviathan mission, and how "
     "does that affect deployment and the first turn?",
     [["attacker"], ["defender"]]),
    ("What is the Scorched Earth primary mission and how does burning an objective "
     "marker score VP at the end of the battle?",
     [["scorched earth"], ["burn"]]),
    ("In Leviathan, how do ruins affect movement and visibility, and can a unit end "
     "its move inside a ruin's walls?",
     [["ruin"]]),
    ("When are objective markers placed in a Leviathan mission, and how is control "
     "of an objective determined?",
     [["objective marker"], ["control"]]),
    ("What does the Engage on All Fronts secondary require across table quarters, "
     "and how do Battle-shocked units affect whether it is achieved?",
     [["engage on all fronts"], ["table quarter"]]),
    ("In the Secure No Man's Land secondary, how many VP do I score for controlling "
     "one versus two objective markers in No Man's Land?",
     [["no man's land"], ["secure"]]),
    ("How do Gambits work in a Leviathan game and when can I use one?",
     [["gambit"]]),
]

# UNITS schema: (query, concept-groups, checks). `checks` adds STRUCTURAL assertions on
# the named-unit chunks that reach the final context (not just text presence):
#   "distinct_units": N      → ≥N distinct named-unit datasheets represented (multi-unit)
#   "chunks_for": {name: N}   → ≥N chunks of that one unit (the per-unit 2-chunk path)
UNITS = [
    # ── 4 MULTI-UNIT: two named units must BOTH reach context (per-unit reservation
    #    must not let one unit sweep the other's slots). ───────────────────────────
    ("When Abaddon the Despoiler fights the Aberrants in melee, how do Abaddon's "
     "Devastating Wounds interact with the Aberrants' Feel No Pain?",
     [["abaddon"], ["aberrant"], ["devastating wounds"], ["feel no pain"]],
     {"distinct_units": 2}),
    ("When An'ggrath the Unbound is destroyed next to an Ork mob led by a Painboy, "
     "can the Painboy's Feel No Pain save against the Deadly Demise mortal wounds?",
     [["an’ggrath", "an'ggrath"], ["painboy"], ["deadly demise"], ["feel no pain"]],
     {"distinct_units": 2}),
    ("Compare the transport capacity of a Battlewagon and a Trukk, and what kinds of "
     "models each one is allowed to carry.",
     [["battlewagon"], ["trukk"], ["transport capacity", "transport"]],
     {"distinct_units": 2}),
    ("If a Callidus Assassin and Boss Snikrot both deploy using Infiltrators, how "
     "close to the enemy can each of them be set up?",
     [["callidus"], ["snikrot"], ["infiltrator"]],
     {"distinct_units": 2}),

    # ── 4 SINGLE-UNIT / TWO-CHUNK: needs BOTH the unit's datasheet AND a separate
    #    ability/section chunk → ≥2 chunks of that one unit must be reserved. ───────
    ("What melee weapons does Abaddon the Despoiler have on his datasheet, and what "
     "does his Dark Destiny ability do?",
     [["abaddon"], ["dark destiny"]],
     {"chunks_for": {"Abaddon The Despoiler": 2}}),
    ("What is the Battlewagon's transport capacity, and separately what does its "
     "'Ard Case ability do?",
     [["battlewagon"], ["transport capacity", "transport"], ["’ard case", "'ard case", "ard case"]],
     {"chunks_for": {"Battlewagon": 2}}),
    ("What is the Callidus Assassin's Movement characteristic, and what does her "
     "Acrobatic Escape ability do?",
     [["callidus"], ["acrobatic escape"]],
     {"chunks_for": {"Callidus Assassin": 2}}),
    ("What is the Trukk's transport capacity, and what does its Grot Riggers ability do?",
     [["trukk"], ["transport capacity", "transport"], ["grot riggers"]],
     {"chunks_for": {"Trukk": 2}}),

    # ── 3 SINGLE-UNIT (simple) ───────────────────────────────────────────────────
    ("Chief Librarian Mephiston has Fights First. If he is in combat with an enemy "
     "unit that also has Fights First, who fights first?",
     [["fights first"], ["mephiston"]],
     {}),
    ("How does the Aegis Defence Line fortification give units the Benefit of Cover, "
     "and how do models interact with it?",
     [["benefit of cover", "cover"], ["aegis"]],
     {}),
    # ABILITY→RULE seeding via an ABILITY parent (the hybrid seed_referenced_rules
    # path): Obyron's Ghostwalk Mantle NAMES "Fights First", which must seed the core
    # rule — the 4th group ("whose turn…"/"alternat"/"pile in") lives ONLY in that core
    # rule, not the ability, so it passes only if the seed actually reached context.
    ("While Vargard Obyron leads a unit, his Ghostwalk Mantle gives it Fights First — "
     "how does the Fights First rule resolve when both sides have it in the Fight phase?",
     [["obyron"], ["ghostwalk mantle"], ["fights first"],
      ["whose turn is not taking place", "alternat", "pile in"]],
     {}),
]

# ILLEGAL game states: the question describes a setup that VIOLATES a rule, so the only
# correct answer is "that is not a legal game state." This suite checks the RETRIEVAL
# PRECONDITION for that verdict — the rule that PROVES the illegality (and the unit(s)
# involved) must reach context; without it the model (system-prompt rule 8) cannot flag
# the violation. (The model's final wording is out of scope for this offline harness.)
ILLEGAL = [
    ("Can a 5-model Terminator Squad embark inside a Rhino transport?",          # Rhino: "cannot transport Terminator"
     [["cannot transport"], ["rhino"]],
     {"distinct_units": 2}),
    ("Can I set up a unit using Deep Strike just 3 inches away from an enemy unit?",  # must be >9"
     [["deep strike"], ["more than 9", "9\""]],
     {}),
    ("My unit Fell Back this turn — can that same unit then declare a charge this turn?",  # cannot
     [["fall back", "fell back"], ["declare a charge", "cannot shoot or declare"]],
     {}),
    ("Can my Space Marine unit embark inside an enemy Ork Trukk?",                # only a FRIENDLY transport
     [["embark"], ["friendly"]],
     {}),
    ("Can a single model in my 10-model unit end its move 4 inches away from every "  # coherency: within 2"
     "other model in that unit?",
     [["coherency"], ["within 2", "2\""]],
     {}),
]

# ARMY / DETACHMENT rules: the top-level faction rules (Abilities.csv army rules +
# Detachment_abilities.csv detachment rules) that ride the always-available rules
# slice (app.rules_where now allows Army_Rule / Detachment_Rule). Each names the rule
# so it cosine-lands in the rules-slice pool, then the reranker reserves it; the
# distinctive rule-name group proves the right chunk reached context, not a near-miss.
# (mission_pack OFF — faction rules are not mission-pack-gated.) See
# spec/army-detachment-rules.md.
ARMY_DETACHMENT = [
    ("What does the Space Marines army rule Oath of Moment do, and when do I pick "
     "the target?",
     [["oath of moment"], ["re-roll"], ["command phase"]]),
    ("What is the Ironstorm Spearhead detachment rule Armoured Wrath, and what can "
     "each Adeptus Astartes unit re-roll?",
     [["armoured wrath"], ["ironstorm spearhead"], ["re-roll one hit roll", "re-roll"]]),
    ("How does the Heretic Astartes army rule Dark Pacts work, and what test must the "
     "unit take?",
     [["dark pacts"], ["leadership test"], ["lethal hits", "sustained hits"]]),
    ("What does the T’au Empire army rule For the Greater Good do with Observer and "
     "Spotted units?",
     [["for the greater good"], ["observer"], ["spotted"]]),
    ("What does the Necrons Awakened Dynasty detachment rule Command Protocols do "
     "while a Character is leading the unit?",
     [["command protocols"], ["awakened dynasty"], ["hit roll"]]),
]

SUITES = [("CORE", CORE, False), ("LEVIATHAN", LEVIATHAN, True),
          ("UNITS", UNITS, False), ("ILLEGAL", ILLEGAL, False),
          ("ARMY_DETACHMENT", ARMY_DETACHMENT, False)]


def run_pipeline(query, mp_mode):
    """The shipped retrieval path (mirrors render_chat): retrieve → UNIT slice +
    seed (defs + referenced rules) → rerank → parent-cap → assemble (reserve rules +
    per-unit slots) → budget. Headless ⇒ no clarification, so resolution is empty and the
    unit slice pins each unit's sole army automatically (multi-faction → deduped/capped).
    Returns the context text, latency, seeded-dep names, and the distribution of named-
    unit chunks that actually reached the final context (unit_name → count)."""
    t0    = time.time()
    rctx  = retrieval.run(query, edition=EDITION, mission_pack_mode=mp_mode, resolution={})
    ms    = (time.time() - t0) * 1000
    final = rctx.result
    ctx   = app.format_rules_context(final, BUDGET)
    seeded = [c for c in rctx.main if c.get("dep_seed")]
    seeded_names = [s.get("dep_stem") or s["metadata"].get("breadcrumb", "?") for s in seeded]
    # Named-unit chunks that survived into final context (for structural checks).
    unit_keys = {app.content_key(c) for c in rctx.units}
    unit_dist = Counter(c["metadata"].get("unit_name") for c in final
                        if app.content_key(c) in unit_keys)
    return ctx, ms, seeded_names, unit_dist


def grade(ctx, groups):
    blob = ctx.lower()
    return [g for g in groups if not any(s.lower() in blob for s in g)]


def grade_checks(unit_dist, checks):
    """Structural assertions on named-unit chunks in final context. Returns failures."""
    fails = []
    if "distinct_units" in checks:
        n = len([u for u, c in unit_dist.items() if u and c > 0])
        if n < checks["distinct_units"]:
            fails.append(f"distinct_units: {n} < {checks['distinct_units']} "
                         f"(got {dict(unit_dist)})")
    for unit, need in checks.get("chunks_for", {}).items():
        if unit_dist.get(unit, 0) < need:
            fails.append(f"chunks_for[{unit}]: {unit_dist.get(unit, 0)} < {need}")
    return fails


def main():
    app.get_reranker(); app.get_embedder()      # warm so first timing isn't cold load
    total_q = sum(len(c) for _, c, _ in SUITES)
    print("=" * 80)
    print(f"{total_q}-QUESTION RETRIEVAL EVAL — {config.RERANK_MODEL}")
    print(f"pool={config.RERANK_CANDIDATES}  budget={BUDGET} tok  edition={EDITION}")
    print("=" * 80)

    # Whole-chunk context (no mid-chunk truncation): the budget is a SOFT target and
    # the boundary chunk is included whole, so totals overrun by up to one chunk.
    # CEILING is the hard sanity bound (budget + one large chunk); over it = a real
    # ballooning bug, not the accepted overrun.
    CEILING = BUDGET + 1100
    grand_pass = grand_total = grand_balloon = grand_maxtok = 0
    grp_pass = grp_total = 0

    for suite_name, cases, mp_mode in SUITES:
        print(f"\n{'#'*80}\n# {suite_name}  (mission_pack={'ON' if mp_mode else 'OFF'})  "
              f"— {len(cases)} questions\n{'#'*80}")
        s_pass = 0
        for case in cases:
            query, groups = case[0], case[1]
            checks = case[2] if len(case) > 2 else {}
            ctx, ms, seeded, unit_dist = run_pipeline(query, mp_mode)
            tok = TOK(ctx)
            missing  = grade(ctx, groups)
            chk_fail = grade_checks(unit_dist, checks)
            ok = not missing and not chk_fail
            s_pass += ok
            grp_pass += (len(groups) - len(missing))
            grp_total += len(groups)
            grand_maxtok = max(grand_maxtok, tok)
            if tok > CEILING:
                grand_balloon += 1
            mark = "PASS" if ok else "FAIL"
            qshort = query if len(query) <= 92 else query[:89] + "..."
            print(f"\n[{mark}] {qshort}")
            seed_str = ", ".join(seeded) if seeded else "—"
            print(f"      seeded: {seed_str}")
            if checks:
                print(f"      units in final: {dict(unit_dist) or '—'}")
            print(f"      groups {len(groups)-len(missing)}/{len(groups)} | "
                  f"rerank+cap {ms:.0f} ms | ctx {tok} tok (budget {BUDGET})"
                  f"{'  ⚠ OVER CEILING' if tok > CEILING else ''}")
            for g in missing:
                print(f"        ↳ MISSING any of: {g}")
            for f in chk_fail:
                print(f"        ↳ CHECK {f}")
        print(f"\n  {suite_name} score: {s_pass}/{len(cases)}")
        grand_pass += s_pass
        grand_total += len(cases)

    print(f"\n{'='*80}")
    print(f"OVERALL: {grand_pass}/{grand_total} questions fully satisfied  "
          f"| concept-groups {grp_pass}/{grp_total}  "
          f"| max ctx {grand_maxtok} tok (soft budget {BUDGET}) "
          f"| over ceiling {CEILING} (must be 0): {grand_balloon}")
    print("=" * 80)
    return 0 if grand_pass == grand_total else 1


if __name__ == "__main__":
    sys.exit(main())

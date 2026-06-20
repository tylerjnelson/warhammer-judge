#!/usr/bin/env python3
"""
sim_clarify.py — headless simulation of the TWO-STAGE unit-clarification state
machine (build_clarification_queue / next_clarification / apply_clarification).

Streamlit buttons can't be clicked in a test, so the UI logic is kept in pure
functions and the "clicks" are simulated here. Each ambiguous unit is resolved in
up to two rounds: faction first, then (only if that faction fields >1 variant)
which variant. A faction with a single variant auto-resolves with no second round.
This drives a query to completion one click at a time, asserting the queue advances
correctly, state is never lost, and single-faction / faction-pinned-but-unique /
no-unit queries never prompt.
"""
import logging, sys, warnings
from pathlib import Path
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import app

EDITION = "10e"
fails = []

def check(cond, msg):
    print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)

def drive(query, pick, sidebar=None, max_rounds=12):
    """Build the queue, then resolve every pending unit by calling `pick` for each
    question. `pick(kind, ref, army, choices) -> choice` simulates a button click;
    it must return one of `choices`. Returns the final state (or None)."""
    state = app.build_clarification_queue(query, EDITION, sidebar)
    print(f"\nQ: {query!r}  (sidebar={sidebar})")
    if state is None:
        print("   → no clarification needed")
        return None
    print(f"   pending: {[(u['ref'], u['stage']) for u in state['units']]}"
          f"   auto: {[(r['unit_name'], r['army']) for r in state['resolved']]}")
    rounds = 0
    while True:
        nxt = app.next_clarification(state)
        if nxt is None:
            break
        rounds += 1
        check(rounds <= max_rounds, "loop is bounded (no runaway)")
        if rounds > max_rounds:
            break
        if nxt[0] == "faction":
            _, ref, choices = nxt; army = None
        else:
            _, ref, army, choices = nxt
        choice = pick(nxt[0], ref, army, choices)
        check(choice in choices, f"{nxt[0]} pick {choice!r} for {ref} is offered "
                                 f"({choices})")
        state = app.apply_clarification(state, choice)
    print(f"   resolved: {[(r['unit_name'], r['army']) for r in state['resolved']]}")
    return state

def picker(plan):
    """Return a pick() that, on each call, pops the next planned choice from `plan`
    (a list of strings, in click order)."""
    it = iter(plan)
    return lambda kind, ref, army, choices: next(it)

def first(kind, ref, army, choices):
    """Strategy: always click the first offered choice (for integrity tests)."""
    return choices[0]

print("=" * 70)
print("TWO-STAGE CLARIFICATION — state-machine simulation")
print("=" * 70)

# 1) Generic chassis word, no faction → faction round lists ALL armies that field a
#    Land Raider; Custodes fields exactly one variant → auto-resolves to it (no
#    variant round). This is the bug the feature fixes.
print("\n--- Case 1: chassis word, faction with a single variant auto-resolves ---")
st = drive("my unit is in a land raider, can it charge",
           picker(["Adeptus Custodes"]))
check(st is not None, "chassis word triggers clarification")
if st:
    check(st["resolved"] == [{"ref": "Land Raider",
                              "unit_name": "Venerable Land Raider",
                              "army": "Adeptus Custodes"}],
          "Custodes → auto-resolved to Venerable Land Raider (one round only)")

# Re-check the faction round actually offered the full family (8 factions), proving
# Custodes / Chaos / variants are no longer boxed out.
fresh = app.build_clarification_queue("a land raider", EDITION)
kind, ref, armies = app.next_clarification(fresh)
check(kind == "faction" and "Adeptus Custodes" in armies
      and "Chaos Space Marines" in armies and len(armies) >= 8,
      f"faction round lists the whole family (got {len(armies)}: {armies})")

# 2) Same chassis, a faction with MANY variants → second (variant) round.
print("\n--- Case 2: chassis word, multi-variant faction prompts a variant round ---")
st = drive("land raider transport capacity",
           picker(["Space Marines", "Land Raider Crusader"]))
check(st is not None and st["resolved"] ==
      [{"ref": "Land Raider", "unit_name": "Land Raider Crusader",
        "army": "Space Marines"}],
      "SM → variant round → resolved to the chosen Land Raider Crusader")

# 3) Faction named IN the query → skip faction round, go straight to variant.
print("\n--- Case 3: faction in query → variant round only (skips faction) ---")
st = drive("Space Marines land raider transport", picker(["Land Raider Redeemer"]))
check(st is not None and st["units"] == []
      and st["resolved"] == [{"ref": "Land Raider",
                              "unit_name": "Land Raider Redeemer",
                              "army": "Space Marines"}],
      "in-query faction skips to variant round, resolves to the pick")

# 4) Sidebar faction pinned, that faction has a UNIQUE variant → no prompt at all.
print("\n--- Case 4: sidebar faction with a unique variant (no prompt) ---")
st = drive("land raider", picker([]), sidebar="Adeptus Custodes")
check(st is not None and st["units"] == []
      and st["resolved"] == [{"ref": "Land Raider",
                              "unit_name": "Venerable Land Raider",
                              "army": "Adeptus Custodes"}],
      "sidebar Custodes auto-resolves to Venerable Land Raider, no buttons")

# 5) Sidebar faction with MANY variants → variant round only.
print("\n--- Case 5: sidebar faction with many variants → variant round ---")
st = drive("land raider", picker(["Land Raider Excelsior"]), sidebar="Space Marines")
check(st is not None and st["resolved"] ==
      [{"ref": "Land Raider", "unit_name": "Land Raider Excelsior",
        "army": "Space Marines"}],
      "sidebar SM prompts which variant, resolves to the pick")

# 6) A specific variant NAME (leaf) that several factions field → faction round only.
print("\n--- Case 6: leaf datasheet, multi-faction → faction round only ---")
st = drive("Land Raider Crusader rules", picker(["Grey Knights"]))
check(st is not None and st["resolved"] ==
      [{"ref": "Land Raider Crusader", "unit_name": "Land Raider Crusader",
        "army": "Grey Knights"}],
      "leaf multi-faction unit asks faction once, resolves (no variant round)")

# 7) Single-faction unit → NEVER prompts (Abaddon is Chaos-only).
print("\n--- Case 7: single-faction unit (no prompt) ---")
st = drive("How does Abaddon the Despoiler's Devastating Wounds interact with invulns",
           picker([]))
check(st is None, "single-faction unit does not trigger clarification")

# 8) Pure rules question, no unit → no prompt.
print("\n--- Case 8: no unit named (no prompt) ---")
st = drive("how do saving throws work", picker([]))
check(st is None, "rules-only query does not trigger clarification")

# 9) Multi-unit query → each named unit resolved sequentially, state never lost.
print("\n--- Case 9: two units in one query, sequential resolution ---")
st = drive("how does a land raider fare against a rhino in melee", first)
if st is not None:
    refs = {r["ref"] for r in st["resolved"]}
    check("Land Raider" in refs and "Rhino" in refs,
          f"both named units resolved independently (refs={sorted(refs)})")
    check(st["units"] == [], "queue fully drained")
    check(all(r.get("army") for r in st["resolved"]),
          "every resolution carries a concrete army")
else:
    fails.append("Case 9: expected clarification for land raider + rhino")

# 10) Immutability: apply_clarification returns a NEW state (no mutation of input).
print("\n--- Case 10: apply_clarification does not mutate its input ---")
state = app.build_clarification_queue("a land raider and a rhino", EDITION)
if state:
    before = [dict(u) for u in state["units"]]
    nxt = app.next_clarification(state)
    choice = nxt[2][0] if nxt[0] == "faction" else nxt[3][0]
    _ = app.apply_clarification(state, choice)
    check([dict(u) for u in state["units"]] == before,
          "original units list untouched after apply (new state returned)")
else:
    fails.append("Case 10 setup: expected ambiguity for land raider + rhino")

print("\n" + "=" * 70)
print(f"{'ALL PASS' if not fails else f'{len(fails)} FAILURE(S)'}")
print("=" * 70)
sys.exit(1 if fails else 0)

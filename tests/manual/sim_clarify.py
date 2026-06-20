#!/usr/bin/env python3
"""
sim_clarify.py — headless simulation of the sequential unit-clarification state
machine (build_clarification_queue / next_clarification / apply_clarification).

Streamlit buttons can't be clicked in a test, so the UI logic is kept in pure
functions and the "clicks" are simulated here: build the queue for a query, then
drive it to completion one pick at a time, asserting the queue advances correctly,
state is never lost, and single-faction / faction-pinned / no-unit queries never
prompt. This validates Part 1 BEFORE the sourcing logic is wired in.
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

def drive(query, picks, selected_faction=None):
    """Simulate the render loop: build queue, then apply `picks` (a {unit: army}
    plan) one at a time the way a user clicking buttons would. Returns final state."""
    state = app.build_clarification_queue(query, EDITION, selected_faction)
    print(f"\nQ: {query!r}  (sidebar={selected_faction})")
    if state is None:
        print("   → no clarification needed")
        return None
    print(f"   initial queue: {state['queue']}")
    steps = 0
    while True:
        nxt = app.next_clarification(state)
        if nxt is None:
            break
        unit, opts = nxt
        # the simulated click: choose the army the test planned for this unit
        army = picks[unit]
        labels = [o[0] for o in opts]
        check(any(o[1] == unit and o[2] == army for o in opts),
              f"option for {unit}→{army} is offered (choices: {labels})")
        state = app.apply_clarification(state, unit, army)
        steps += 1
        check(unit not in state["queue"], f"{unit} removed from queue after pick")
        check(state["resolved"].get(unit) == army, f"{unit} recorded as {army}")
        check(steps <= len(picks) + 1, "loop is bounded (no runaway)")
    print(f"   resolved: {state['resolved']}  (after {steps} pick(s))")
    return state

print("=" * 70)
print("SEQUENTIAL CLARIFICATION — state-machine simulation")
print("=" * 70)

# 1) Two ambiguous units in one query → two sequential rounds, both recorded.
print("\n--- Case 1: multi-unit ambiguity (the Land Raider + Rhino case) ---")
st = drive("how does a Land Raider fare against a Rhino in melee",
           {"Land Raider": "Space Marines", "Rhino": "Grey Knights"})
check(st is not None and st["queue"] == [], "queue fully drained")
check(st is not None and st["resolved"] == {"Land Raider": "Space Marines",
                                            "Rhino": "Grey Knights"},
      "both units resolved independently (cross-faction matchup allowed)")

# 2) Single ambiguous unit → one round.
print("\n--- Case 2: single multi-faction unit ---")
st = drive("Land Raider transport capacity", {"Land Raider": "Grey Knights"})
check(st is not None and st["resolved"] == {"Land Raider": "Grey Knights"},
      "single unit resolved in one step")

# 3) Single-faction named unit → NEVER prompts (Abaddon is Chaos-only).
print("\n--- Case 3: single-faction unit (no prompt) ---")
st = drive("How does Abaddon the Despoiler's Devastating Wounds interact with invuln saves",
           {})
check(st is None, "single-faction unit does not trigger clarification")

# 4) Faction named in the query → resolve without asking.
print("\n--- Case 4: faction named in query (no prompt) ---")
st = drive("Space Marines Land Raider transport capacity", {})
check(st is None, "named faction in query pins resolution, no prompt")

# 5) Sidebar faction filter set → no prompt.
print("\n--- Case 5: sidebar faction pinned (no prompt) ---")
st = drive("Land Raider transport capacity", {}, selected_faction="Space Marines")
check(st is None, "sidebar faction pins resolution, no prompt")

# 6) Pure rules question, no unit → no prompt.
print("\n--- Case 6: no unit named (no prompt) ---")
st = drive("how do saving throws work", {})
check(st is None, "rules-only query does not trigger clarification")

# 7) Idempotency / no state loss: resolving unit A must not drop unit B's options.
print("\n--- Case 7: state integrity across the loop ---")
state = app.build_clarification_queue(
    "a Land Raider and a Rhino", EDITION)
if state:
    before_opts = dict(state["options"])
    state2 = app.apply_clarification(state, "Land Raider", "Space Marines")
    check(state2["options"] == before_opts, "options dict preserved after a pick")
    check(app.next_clarification(state2)[0] == "Rhino", "next unit is the remaining one")
    check(state["queue"] == ["Land Raider", "Rhino"],
          "apply returns a NEW state — original queue untouched (no mutation)")
else:
    fails.append("Case 7 setup: expected ambiguity for Land Raider + Rhino")

print("\n" + "=" * 70)
print(f"{'ALL PASS' if not fails else f'{len(fails)} FAILURE(S)'}")
print("=" * 70)
sys.exit(1 if fails else 0)

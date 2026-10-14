"""
eval_suites_11e.py — the 11th-edition question set for eval_quality.py /
collect_model_answers.py / grade_prod.py (select it with --edition 11e).

Same shape as the 10e SUITES in eval_quality.py: each case is
(query, [concept group, ...][, structural checks]) and a group is satisfied if ANY of
its substrings appears (case-insensitive) in the final budgeted context. Every
substring was checked against data/rule_blocks/11e when the set was written
(2026-10-14) — re-run `python tests/manual/eval_suites_11e.py` to re-verify after a
re-scrape.

The set leans on what CHANGED in 11e, so a model answering from 10e memory is caught:
cover worsens BS (not +1 save), Deep Strike is >8" (not 9"), hidden / gone to ground /
detection range, fall-back modes (desperate escape), assault/indirect shooting types,
emergency disembark, Chapter Approved force-disposition missions, Detachment Points,
quantity-tiered points, and Space Marines' Combat Doctrines (Oath of Moment is gone).

ANSWER_KEY (1-based question index, same numbering as collect_model_answers) holds
the ground-truth facts the ANSWER text must state ("must": regexes) or must not rule
("must_not": regexes checked against the ruling line) — grade_prod.py --edition 11e.
"""

CORE = [
    ("How does the benefit of cover work in 11th edition — what does it change about an "
     "attack, and when does a unit have it?",
     [["benefit of cover"], ["worsen the bs characteristic"], ["terrain area"]]),
    ("When is an infantry model hidden, and from how far away can enemy models see it?",
     [["is hidden while"], ["detection range"], ["15\""]]),
    ("What extra benefit does a hidden model get when it has gone to ground?",
     [["gone to ground"], ["subtract 3\""], ["dense terrain"]]),
    ("My unit is battle-shocked and engaged with an enemy unit. What happens if it falls "
     "back, and what can it do for the rest of the turn?",
     [["desperate escape"], ["hazard roll"], ["not eligible to shoot, declare a charge"]]),
    ("Can a unit that made an advance move shoot this turn, and if so with which weapons?",
     [["assault shooting"], ["[assault] weapons"], ["advance move"]]),
    ("How does shooting an Indirect Fire weapon at a target my unit cannot see work — "
     "which hit rolls fail, and does the target get the benefit of cover?",
     [["indirect shooting"], ["1-5 fails"], ["benefit of cover"]]),
    ("If a Transport is destroyed with a unit embarked inside it, how does that unit get "
     "out and what happens to it afterwards?",
     [["emergency disembark"], ["hazard roll"], ["battle-shocked"]]),
    ("When both players have Fights First units eligible to fight, in what order do "
     "units fight in the Fight phase?",
     [["fights first"], ["starting with the player whose turn it is"],
      ["resolve remaining combats"]]),
    ("How does a hazard roll work, and how many mortal wounds does a failed hazard roll "
     "inflict on a Vehicle unit?",
     [["hazard roll"], ["1-2"], ["3 mortal wounds"]]),
    ("How do Devastating Wounds interact with Feel No Pain?",
     [["devastating wounds"], ["feel no pain"], ["mortal wounds"]]),
    ("When can a unit in strategic reserves arrive on the battlefield, and how far from "
     "enemy units must it be set up?",
     [["ingress move"], ["second battle round"], ["more than 8\" horizontally"]]),
    ("How does Plunging Fire work?",
     [["plunging fire"], ["3\" or more in height"], ["towering"]]),
    ("What does it mean for a unit to be below half-strength, and which units have to "
     "take a battle-shock roll in the Command phase?",
     [["half-strength"], ["starting strength"], ["battle-shock roll"]]),
    ("How does a player control an objective, and what does it mean for an objective to "
     "be secured?",
     [["level of control"], ["secured"], ["oc characteristic"]]),
    ("How many Command Points does each player gain each turn in the Command phase?",
     [["gain core cp", "core cp"], ["1 command point"]]),
]

MISSIONS = [
    ("My Force Disposition is Take and Hold and my opponent's is Purge the Foe. What is "
     "my Primary Mission and how does it score?",
     [["immovable object"], ["central objectives"], ["5vp"]]),
    ("How do Force Disposition cards determine each player's Primary Mission?",
     [["force disposition"], ["primary mission"], ["secretly"]]),
    ("Using Fixed Secondary Missions, how many VP does Assassination score when I destroy "
     "one enemy Character model with 5 wounds?",
     [["assassination"], ["3vp fixed"], ["w of 4 or more"]]),
    ("Using Tactical Secondary Missions, how many VP does Bring It Down score when I "
     "destroy an enemy model with 12 wounds?",
     [["bring it down"], ["5vp tactical"], ["w of 10 or more"]]),
    ("What is the most VP I can score from Secondary Missions in a single battle round, "
     "and across the whole battle?",
     [["secondary missions"], ["up to 15vp per battle round"], ["45vp"]]),
    ("How do Tactical Secondary Missions work — when do I draw them, and can I discard "
     "them?",
     [["tactical secondary missions"], ["draw two secondary missions"], ["1cp"]]),
    ("What does the Mirrored World twist do?",
     [["mirrored world"], ["roll a d6"], ["primary mission"]]),
    ("How is it decided which player is the Attacker and which is the Defender?",
     [["attacker"], ["roll off"]]),
    ("How do I score the Plunder secondary mission?",
     [["plunder"], ["objective action"], ["5vp"]]),
    ("How many VP is a Battle Ready painted army worth, and what are the maximum VP from "
     "the Primary Mission?",
     [["battle ready"], ["10vp"], ["45vp"]]),
]

UNITS = [
    ("When my Vindicare Assassin uses Deadshot, can it shoot an enemy Lone Operative "
     "and an enemy hidden infantry unit 25 inches away?",
     [["deadshot"], ["lone operative"], ["detection range"]],
     {}),
    ("While Vargard Obyron leads a unit, his Ghostwalk Mantle gives it Fights First — "
     "how does that resolve when both sides have Fights First units?",
     [["obyron"], ["ghostwalk mantle"], ["fights first"],
      ["starting with the player whose turn it is"]],
     {}),
    ("Chief Librarian Mephiston has Lone Operative. Can an enemy unit 18 inches away "
     "shoot him?",
     [["mephiston"], ["lone operative"], ["within 12\""]],
     {}),
    ("If my Land Raider makes a Normal move, can the Intercessors embarked inside "
     "disembark and declare a charge that turn?",
     [["assault ramp"], ["assault disembark"], ["land raider"]],
     {"chunks_for": {"Land Raider": 1}}),
    ("My Callidus Assassin is still engaged at the end of the Fight phase — what can it "
     "do?",
     [["callidus"], ["acrobatic escape"], ["fall-back move"]],
     {}),
    ("What does the Ork Trukk's Pilin' Out ability let embarked units do, and can they "
     "charge afterwards?",
     [["trukk"], ["pilin"], ["rapid disembark"]],
     {}),
]

ILLEGAL = [
    ("Can a 5-model Terminator Squad embark inside a Rhino?",
     [["cannot transport terminator"], ["rhino"]],
     {"distinct_units": 2}),
    ("Can I set up a Deep Striking unit 6 inches away from an enemy unit?",
     [["deep strike"], ["more than 8\" horizontally"]],
     {}),
    ("My unit made an advance move this turn — can it declare a charge?",
     [["advance move"], ["not eligible to declare a charge"]],
     {}),
    ("Can I give two enhancements to the same Character unit?",
     [["enhancement"], ["more than one enhancement", "prevented from having two enhancements"]],
     {}),
    ("Can I include four Leman Russ Battle Tanks in a 2000-point Strike Force army?",
     [["unit limit"], ["strike force"]],
     {}),
    ("In an Incursion battle, can I take a 3DP detachment together with a 1DP "
     "detachment?",
     [["detachment points", "more than 2 dp"], ["3dp detachment as your only detachment"]],
     {}),
]

ARMY_DETACHMENT = [
    ("What is the Space Marines army rule in 11th edition, and how do its combat "
     "doctrines work?",
     [["combat doctrines"], ["assault doctrine"], ["once per battle"]]),
    ("How many Detachment Points does the Gladius Task Force cost, what is its force "
     "disposition, and what is its detachment rule?",
     [["gladius task force"], ["take and hold"], ["codex discipline"]]),
    ("How does the T'au Empire army rule For the Greater Good work with Observer and "
     "Spotted units?",
     [["for the greater good"], ["observer"], ["spotted"]]),
    ("What does the Heretic Astartes army rule Dark Pacts do, and what test does the "
     "unit take?",
     [["dark pacts"], ["leadership test"], ["lethal hits", "sustained hits"]]),
    ("What does the Orks Waaagh! army rule do — what happens while a unit is riled up?",
     [["waaagh"], ["riled up"], ["5+ insv"]]),
    ("What are the Detachment Points cost, force disposition and detachment rule of the "
     "T'au Kauyon detachment?",
     [["kauyon"], ["patient hunter"], ["reconnaissance"]]),
]

POINTS = [
    ("How many points do 20 Ork Boyz cost if they are the fourth unit of Boyz in my "
     "army?",
     [["boyz"], ["4th+ unit costs"], ["180 pts"]]),
    ("How many points is a Leman Russ Battle Tank, and how much does a lascannon add?",
     [["leman russ battle tank"], ["160 pts"], ["lascannon"]]),
    ("How many points does a Vindicare Assassin cost?",
     [["vindicare"], ["110 pts"], ["125 pts"]]),
    ("How many points is the Gunnery Honours enhancement, and can I take it more than "
     "once in my army?",
     [["gunnery honours"], ["upgrade"], ["up to three of the same upgrade"]]),
]

# (suite name, cases, mission_pack_mode) — the eval_quality.SUITES contract.
SUITES = [("CORE", CORE, False), ("MISSIONS", MISSIONS, True),
          ("UNITS", UNITS, False), ("ILLEGAL", ILLEGAL, False),
          ("ARMY_DETACHMENT", ARMY_DETACHMENT, False), ("POINTS", POINTS, False)]

# Ground truth for the ANSWER (grade_prod.py --edition 11e). Keys are 1-based question
# indices in SUITES order. "must": regexes that must appear in the answer (case-insens);
# "must_not": regexes that must NOT appear in the ruling line (the 10e-memory traps).
ANSWER_KEY = {
    1:  {"must": [r"worsen", r"\bBS\b|ballistic"], "must_not": [r"\+1 to (?:the )?sav"]},
    2:  {"must": [r"15\s*(?:\"|”|inch|in\b)"]},
    3:  {"must": [r"3\s*(?:\"|”|inch|in\b)"]},
    4:  {"must": [r"desperate escape", r"hazard"]},
    5:  {"must": [r"\[?assault\]?"]},
    6:  {"must": [r"1\s*[-–]\s*5", r"cover"]},
    7:  {"must": [r"emergency disembark", r"battle[- ]shock"]},
    8:  {"must": [r"whose turn"]},
    9:  {"must": [r"1\s*[-–]\s*2", r"3 mortal wounds"]},
    10: {"must": [r"feel no pain"]},
    11: {"must": [r"second battle round", r"8\s*(?:\"|”|inch|in\b)"],
         "must_not": [r"9\s*(?:\"|”|inch)"]},
    12: {"must": [r"\bBS\b|ballistic", r"towering"]},
    13: {"must": [r"starting strength"]},
    14: {"must": [r"\bOC\b|objective control", r"secured"]},
    15: {"must": [r"\b1\s*(?:CP|command point)"]},
    16: {"must": [r"immovable object", r"5\s*VP"]},
    17: {"must": [r"force disposition"]},
    18: {"must": [r"\b4\s*VP"], "must_not": [r"\b5\s*VP"]},
    19: {"must": [r"\b5\s*VP"], "must_not": [r"\b4\s*VP"]},
    20: {"must": [r"15\s*VP", r"45\s*VP"]},
    21: {"must": [r"\btwo\b|\b2\b", r"1\s*CP"]},
    22: {"must": [r"D6"]},
    23: {"must": [r"roll[- ]off"]},
    24: {"must": [r"5\s*VP"]},
    25: {"must": [r"10\s*VP", r"45\s*VP"]},
    26: {"must": [r"lone operative"]},
    27: {"must": [r"fights first"]},
    28: {"must": [r"12\s*(?:\"|”|inch|in\b)"]},
    29: {"must": [r"assault disembark"]},
    30: {"must": [r"fall[- ]back", r"D6"]},
    31: {"must": [r"rapid disembark"]},
    32: {"must": [r"\bno\b|cannot|not (?:able|allowed|legal|permitted)"]},
    33: {"must": [r"8\s*(?:\"|”|inch|in\b)"], "must_not": [r"9\s*(?:\"|”|inch)"]},
    34: {"must": [r"\bno\b|cannot|not eligible"]},
    35: {"must": [r"\bno\b|cannot|more than one enhancement"]},
    36: {"must": [r"\b3\b|three", r"\bno\b|cannot|not (?:able|allowed|legal|permitted)|exceed"]},
    37: {"must": [r"\bno\b|cannot|not (?:able|allowed|legal|permitted)|only detachment"]},
    38: {"must": [r"combat doctrines"], "must_not": [r"oath of moment"]},
    39: {"must": [r"\b3\b", r"take and hold", r"codex discipline"]},
    40: {"must": [r"observer", r"spotted"]},
    41: {"must": [r"leadership test"]},
    42: {"must": [r"riled up", r"5\+"]},
    43: {"must": [r"\b2\b", r"reconnaissance", r"patient hunter"]},
    44: {"must": [r"180"]},
    45: {"must": [r"160", r"175", r"\b5\b"]},
    46: {"must": [r"110", r"125"]},
    47: {"must": [r"\b15\b", r"three|\b3\b"]},
}


if __name__ == "__main__":
    # Re-verify every grading substring still exists somewhere in the 11e corpus.
    import glob
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent.parent
    blob = " ".join(Path(f).read_text(encoding="utf-8")
                    for f in glob.glob(str(root / "data/rule_blocks/11e/*.md"))).lower()
    n = bad = 0
    for suite, cases, _ in SUITES:
        for case in cases:
            n += 1
            for grp in case[1]:
                if not any(s.lower() in blob for s in grp):
                    bad += 1
                    print(f"MISSING  Q{n} [{suite}] group {grp}")
    assert sorted(ANSWER_KEY) == list(range(1, n + 1)), "ANSWER_KEY must cover every question"
    print(f"{n} questions · {bad} group(s) with no substring in the 11e corpus")

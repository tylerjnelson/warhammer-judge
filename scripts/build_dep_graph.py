#!/usr/bin/env python3
"""
build_dep_graph.py — DRAFT the Layer-2 Track-E dependency graph + GATE the
ratified artifact. No LLM, no network. Spec: spec/dependency-boost.md.

The runtime reads a HAND-RATIFIED artifact (data/dep_graph_<edition>.json). This
script does two things:

  1. DRAFT  — a deterministic name-scan over the core corpus, with the three fixes the plan calls for:
       • structural stoplist  — drop phase-pointers / navigation / passing mentions
       • conjugation handling — "Fell Back" -> fall_back_moves, "Advanced" -> advance_moves
       • spine ∪ procedure union — also scan the procedure chunks a spine names, so
         child-defined deps (unit_coherency, named in charging_with_a_unit not in
         charge_phase) are recovered.
     Written to data/dep_graph_<edition>.draft.json as a STARTING POINT for
     hand-ratification — it is NOT the runtime artifact.

  2. GATE   — load the ratified artifact and assert it reproduces the
     hand-validated charge/movement families (the self-validating gate). Also
     reports how close the raw draft gets, to guide future ratification.

Usage:  python scripts/build_dep_graph.py [edition]   (default 10e)
Exit code is non-zero if the ratified artifact fails the gate.
"""
import json, logging, re, sys, warnings
from pathlib import Path
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import app, config

EDITION = sys.argv[1] if len(sys.argv) > 1 else "10e"

# Hand-validated families (the hand-validated ESSENTIAL "spine -> core" set).
# The ratified artifact MUST cover these; the draft is scored against them.
GROUND_TRUTH = {
    "charge_phase": {"charging_with_a_unit", "engagement_range", "unit_coherency"},
    "1_move_units": {"normal_moves", "advance_moves", "fall_back_moves",
                     "remain_stationary", "engagement_range", "unit_coherency"},
}

# Common words that are ALSO chunk names but read as plain English — matching them
# manufactures phantom edges (the 87%-noise failure mode). Excluded from the vocab.
_STOP = {"units", "unit", "models", "model", "attacks", "attack", "weapons",
         "weapon", "fight", "advance", "charge", "moves", "abilities", "keywords",
         "profiles", "missions", "armies", "battlefield", "anti"}

# Structural stoplist: real chunk names that, when MENTIONED, are navigation /
# phase-pointers / passing references rather than definitions the rule depends on.
_STRUCTURAL_STOP = {
    "select_targets", "straight_lines", "destroyed", "2_reinforcements",
    "strategic_reserves", "terrain_features", "aircraft",
}
def _is_phase_pointer(stem):
    return stem.endswith("_phase") or re.match(r"^\d+_", stem) is not None

# Irregular / conjugated references: the prose says "Normal move" / "Fell Back" /
# "Advanced", not the bare stem.
_ALIAS = {
    "normal_moves":      r"normal moves?",
    "advance_moves":     r"\badvanced?\b",
    "fall_back_moves":   r"f(?:all|ell) back",      # "Fall Back" AND "Fell Back"
    "surge_moves":       r"surge moves?",
    "remain_stationary": r"remain(?:s|ed)? stationary",
    "1_move_units":      None,                        # spine: a phase, never a dep
}

def stem(cid): return cid[len("core_rules_"):] if cid.startswith("core_rules_") else cid
def body(text):
    return "\n".join(l for l in text.splitlines()
                     if not l.startswith("**") and not l.startswith("# "))

def build_vocab(core):
    vocab = {}
    for cid, doc, _ in core:
        s = stem(cid)
        if s in _ALIAS:
            pat = _ALIAS[s]
            if pat is None:
                continue
        else:
            phrase = re.sub(r"^\d+\s+", "", s.replace("_", " ").strip())
            if not phrase or phrase in _STOP:
                continue
            if len(phrase.split()) == 1 and (len(phrase) < 6 or phrase in _STOP):
                continue
            pat = r"\b" + re.escape(phrase).replace(r"\ ", r" ") + r"s?\b"
        vocab[s] = re.compile(pat, re.I)
    return vocab

def deps_of(s, doc, vocab):
    txt = body(doc)
    return {t for t, pat in vocab.items()
            if t != s and not _is_phase_pointer(t) and t not in _STRUCTURAL_STOP
            and pat.search(txt)}

def build_draft(core, vocab, doc_by_stem):
    draft = {}
    for cid, doc, _ in core:
        s = stem(cid)
        if _is_phase_pointer(s) and s not in GROUND_TRUTH:
            # phase spines still get a graph entry if they're known families;
            # otherwise skip numeric/phase stems as sources to cut nav noise.
            if not re.match(r"^\d+_", s):
                continue
        edges = deps_of(s, doc, vocab)
        # spine ∪ procedure union: one hop through the procedures this rule names.
        for child in list(edges):
            if child in doc_by_stem:
                edges |= deps_of(child, doc_by_stem[child], vocab)
        edges.discard(s)
        if edges:
            draft[s] = sorted(edges)
    return draft

def score(pred, truth):
    tp = len(pred & truth); fp = len(pred - truth); fn = len(truth - pred)
    p = tp / (tp + fp) if tp + fp else 1.0
    r = tp / (tp + fn) if tp + fn else 1.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f

def main():
    col  = app.get_collection(EDITION)
    data = col.get(where={"category": "Core_Rules"}, include=["documents", "metadatas"])
    core = list(zip(data["ids"], data["documents"], data["metadatas"]))
    doc_by_stem = {stem(cid): doc for cid, doc, _ in core}
    vocab = build_vocab(core)
    print(f"core chunks: {len(core)} | matchable terms: {len(vocab)}")

    draft = build_draft(core, vocab, doc_by_stem)
    draft_path = ROOT / f"data/dep_graph_{EDITION}.draft.json"
    draft_path.write_text(json.dumps(
        {"_meta": {"generated": "scripts/build_dep_graph.py",
                   "note": "DRAFT — hand-ratify into dep_graph_<edition>.json before use"},
         **draft}, indent=2), encoding="utf-8")
    print(f"draft written: {draft_path.relative_to(ROOT)}  ({len(draft)} source rules)\n")

    print("DRAFT vs hand-validated families (precision/recall of the raw scan):")
    for spine, truth in GROUND_TRUTH.items():
        got = set(draft.get(spine, []))
        p, r, f = score(got, truth)
        print(f"  {spine:16s} P={p:.2f} R={r:.2f} F1={f:.2f}  "
              f"missed={sorted(truth-got)}  extra={sorted(got-truth)}")

    # ── GATE: the RATIFIED artifact must cover every validated family ──────────
    ratified_path = ROOT / config.RULES_DEP_GRAPH_PATH.format(edition=EDITION)
    print(f"\nGATE — ratified artifact: {ratified_path.relative_to(ROOT)}")
    ratified = app.get_dep_graph(EDITION) if ratified_path.exists() else {}
    ok = True
    for spine, truth in GROUND_TRUTH.items():
        got = set(ratified.get(spine, []))
        missing = truth - got
        status = "OK" if not missing else f"FAIL missing={sorted(missing)}"
        if missing:
            ok = False
        print(f"  {spine:16s} {status}")
    # every dep stem in the ratified graph must resolve to a real chunk
    all_stems = {stem(cid) for cid, _, _ in core}
    for s, deps in ratified.items():
        for d in deps:
            if d not in all_stems and d not in doc_by_stem:
                print(f"  DANGLING edge {s} -> {d} (no such chunk)")
                ok = False
    print("\nGATE:", "GREEN ✓" if ok else "RED ✗")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

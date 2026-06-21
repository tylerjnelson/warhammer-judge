"""
clarify.py — unit/faction resolution + the chassis disambiguation state machine.
================================================================================
Moved out of app.py (Phase 5). Two concerns live here:

  • Unit/faction RESOLUTION (build_faction_keyword_map, detect_faction,
    build_unit_index, detect_unit, get_unit_name_resolver, resolve_named_units,
    find_unit_occurrences, unit_armies, is_chassis_base, _variant_signature,
    chassis_family) — also consumed by the retrieval path (process_query /
    retrieve_unit_slice), which import these back from app's namespace.
  • The two-stage (faction → variant) CLARIFICATION state machine
    (build_clarification_queue, next_clarification, apply_clarification,
    highlight_ref, apply_resolution_to_query).

A leaf module: depends only on config + indices (+ streamlit for @st.cache_resource,
pandas/glob lazily inside the cache builders). After Phase 1 the resolution helpers
read the cached indices, so nothing here does a per-call Chroma round-trip.
"""
import re
from collections import defaultdict
from pathlib import Path

import streamlit as st

import config
import indices

ROOT = Path(__file__).resolve().parent

@st.cache_resource
def build_faction_keyword_map(edition: str):
    import pandas as pd
    csv_dir  = ROOT / config.get_edition(edition)["csv_dir"]
    kw_map   = {}
    factions = {}
    kw_path = csv_dir / "Datasheets_keywords.csv"
    if kw_path.exists():
        df = pd.read_csv(kw_path, sep="|", encoding="utf-8-sig", dtype=str)
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        faction_rows = df[df["is_faction_keyword"].str.upper() == "TRUE"]
        for _, row in faction_rows.iterrows():
            kw_map[str(row["keyword"]).strip().lower()] = str(row["datasheet_id"]).strip()
    fac_path = csv_dir / "Factions.csv"
    if fac_path.exists():
        df = pd.read_csv(fac_path, sep="|", encoding="utf-8-sig", dtype=str)
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        for _, row in df.iterrows():
            name = str(row["name"]).strip()
            factions[name.lower()] = name
    return kw_map, factions

def detect_faction(query: str, factions: dict) -> str | None:
    q = query.lower()
    for fname_lower, fname in sorted(factions.items(), key=lambda x: -len(x[0])):
        if fname_lower in q:
            return fname
    return None

# Generic role / wargear words that appear *inside* datasheet names but are also
# everyday rules vocabulary ("when a Captain leads a squad", "models in the unit").
# A query containing only these is a RULES question, not a unit lookup — so they
# must never, on their own, route retrieval to the broad (datasheet) path.
_UNIT_STOPWORDS = {
    "captain", "captains", "lord", "lords", "sergeant", "lieutenant", "chaplain",
    "librarian", "warrior", "warriors", "guard", "guards", "squad", "squads",
    "team", "teams", "champion", "champions", "knight", "knights", "master",
    "warlord", "troupe", "brother", "brothers", "gunner", "leader", "hero",
    "character", "characters", "model", "models", "unit", "units", "infantry",
    "vehicle", "vehicles", "monster", "monsters", "weapon", "weapons", "armour",
    "heavy", "venerable", "ancient", "veteran", "veterans", "company", "command",
    "with", "and", "the", "of", "in", "on",
}

def _light_stem(t: str) -> str:
    """Strip a common inflectional suffix so 'burning'/'burned'/'burns' all reduce to
    'burn'. Deliberately crude (no linguistic stemmer dependency) — used only to match
    a query token against the rules-corpus vocabulary for unit-signal rejection."""
    for suf in ("ing", "ed", "es", "s"):
        if len(t) - len(suf) >= 3 and t.endswith(suf):
            return t[: -len(suf)]
    return t

@st.cache_resource
def build_unit_index(edition: str):
    """Distinctive unit-name lookup for query routing (NOT retrieval scoping).

    Returns (phrases, tokens):
      • phrases — full multi-word datasheet names (lowercased) for phrase match,
      • tokens  — single tokens distinctive enough to imply a specific datasheet
                  (not in _UNIT_STOPWORDS, length ≥ 5, not spread so thin across
                  datasheet names that they're effectively generic).
    A query that hits either is treated as a unit lookup; everything else is a
    rules question and gets scoped to Core + mission-pack (kills G4 noise).
    """
    import glob
    import pandas as pd
    from collections import Counter
    csv_path = ROOT / config.get_edition(edition)["csv_dir"] / "Datasheets.csv"
    phrases, token_df = set(), Counter()
    if csv_path.exists():
        df = pd.read_csv(csv_path, sep="|", encoding="utf-8-sig", dtype=str)
        for raw in df["name"].dropna():
            name = str(raw).strip().lower()
            toks = [t for t in re.split(r"[^a-z0-9]+", name) if t]
            if len(toks) > 1:
                phrases.add(name)
            for t in set(toks):
                token_df[t] += 1

    # Core-rules vocabulary: any token appearing in ≥2 core rule blocks is rules
    # language (battle, strike, deep, charge, guard, escape…), NOT a unit signal —
    # even though such words also sit inside datasheet names (Leman Russ *Battle*
    # Tank, *Strike* Squad). Subtracting this auto-handles the long tail a curated
    # stoplist would miss. Derived from on-disk blocks (cheap, edition-local).
    core_df  = Counter()
    glob_pat = str((ROOT / "data" / "rule_blocks" / edition / "core_rules_*.md"))
    for path in glob.glob(glob_pat):
        with open(path, encoding="utf-8") as f:
            seen = set(re.findall(r"[a-z0-9]+", f.read().lower()))
        for t in seen:
            core_df[t] += 1
    # ≥3 blocks, not ≥2: a unit-type word like "terminator" shows up in 1-2 core
    # example captions (the Deep Strike illustration), but genuine rules language
    # (battle=24, charge=12, strike=7) recurs widely. 3 cleanly splits them.
    core_vocab = {t for t, n in core_df.items() if n >= 3}

    # Mission-pack vocabulary: words that are MISSION language, not unit signals —
    # 'leviathan' (the pack name) sits only in the datasheet 'Leviathan Dreadnought',
    # 'burning' only in 'Burning Chariot', so without this they'd misfire a unit lookup
    # / unit slice on a pure mission question ("how does BURNING an objective score").
    # Any token in ≥1 mission-pack block (these blocks are far fewer than core) plus the
    # pack name itself is subtracted.
    mp_name  = config.get_edition(edition)["mission_pack"]["name"].lower()
    mp_vocab = set(re.findall(r"[a-z0-9]+", mp_name))
    mp_glob  = str((ROOT / "data" / "rule_blocks" / edition / f"{mp_name}_*.md"))
    for path in glob.glob(mp_glob):
        with open(path, encoding="utf-8") as f:
            mp_vocab |= set(re.findall(r"[a-z0-9]+", f.read().lower()))

    # Stem the MISSION-PACK vocab only, so a morphological variant in the query is still
    # recognised as mission language: the block says "burned", the query says "burning"
    # — both stem to "burn", so "burning" (→ datasheet "Burning Chariot") is rejected as
    # a unit signal. NOT applied to core_vocab: its ≥3-block threshold is tuned to keep
    # unit-type words like "terminator" (whose plural "terminators" sits in core
    # examples) AS unit signals — stemming core would wrongly drop them.
    mp_stems = {_light_stem(t) for t in mp_vocab}

    # Distinctive = long enough, not generic role vocab, not core-rules language, not
    # mission-pack language (literal or stemmed), not spread across many datasheets.
    tokens = {
        t for t, n in token_df.items()
        if len(t) >= 5 and t not in _UNIT_STOPWORDS
        and t not in core_vocab and t not in mp_vocab
        and _light_stem(t) not in mp_stems and n <= 40
    }
    return phrases, tokens

def detect_unit(query: str, edition: str) -> bool:
    """True if the query names a specific datasheet → it's a unit lookup, not a
    rules question. Matches a distinctive single token or a full multi-word name."""
    phrases, tokens = build_unit_index(edition)
    q = query.lower()
    q_tokens = set(re.findall(r"[a-z0-9]+", q))
    if q_tokens & tokens:
        return True
    return any(p in q for p in phrases)

# ── Unit-name resolution + sequential clarification (unit slice / disambiguation) ─
# detect_unit answers "is this a unit lookup?" (a bool, for routing). The functions
# below answer "WHICH datasheet(s)?" — needed to (a) source the unit's own chunks
# (retrieve_unit_slice) and (b) drive faction disambiguation BEFORE the heavy
# retrieval/rerank, deterministically from metadata rather than from whatever
# surfaced semantically (so a unit that doesn't embed near the query is still caught).

@st.cache_resource
def get_unit_name_resolver(edition: str):
    """Map a query to the specific datasheet name(s) it mentions. Returns
    (names, token_to_name):
      • names — datasheet names, LONGEST first, so substring matching prefers the
                most specific variant ('Land Raider Crusader' before 'Land Raider');
      • token_to_name — distinctive single tokens that resolve to exactly ONE
                datasheet ('snikrot'→'Boss Snikrot'). Tokens shared by several
                datasheets ('raider') are omitted — they need a full-name phrase or
                clarification, never a guess.
    Distinctiveness is reused from build_unit_index (stopwords + core-vocab stripped)."""
    import pandas as pd
    _, tokens = build_unit_index(edition)
    csv_path  = ROOT / config.get_edition(edition)["csv_dir"] / "Datasheets.csv"
    names = []
    if csv_path.exists():
        df = pd.read_csv(csv_path, sep="|", encoding="utf-8-sig", dtype=str)
        names = sorted({str(n).strip() for n in df["name"].dropna() if str(n).strip()},
                       key=len, reverse=True)
    tok2names = defaultdict(set)
    for nm in names:
        for t in set(re.findall(r"[a-z0-9]+", nm.lower())):
            if t in tokens:
                tok2names[t].add(nm)
    token_to_name = {t: next(iter(ns)) for t, ns in tok2names.items() if len(ns) == 1}
    return names, token_to_name

def resolve_named_units(query: str, edition: str) -> list[str]:
    """The specific datasheet name(s) a query mentions. Full-name substring match
    plus distinctive-single-token fallback; keeps only the most specific name when
    one matched name is a substring of another ('Land Raider' dropped when 'Land
    Raider Crusader' also matched)."""
    names, token_to_name = get_unit_name_resolver(edition)
    q = query.lower()
    found = {nm for nm in names if nm.lower() in q}
    for t in set(re.findall(r"[a-z0-9]+", q)) & token_to_name.keys():
        found.add(token_to_name[t])
    return sorted(n for n in found
                  if not any(n != m and n.lower() in m.lower() for m in found))

def find_unit_occurrences(query: str, edition: str) -> list[dict]:
    """Ordered occurrence SLOTS for the datasheet name(s) a query mentions, with
    positions and multiplicity preserved — unlike resolve_named_units, which returns a
    deduped set and loses the fact that the same chassis word can appear twice (the
    multi-occurrence case that this enables clarifying independently).

    Longest-match, left-to-right, consuming matched spans, so 'Land Raider' INSIDE
    'Land Raider Crusader' (or 'Chaos Land Raider') is not double-counted — the same
    substring-suppression intent as resolve_named_units, but applied per-occurrence
    instead of globally, so two genuinely separate mentions both survive.

    Returns [{id, ref, start, end}, ...] sorted by start; the same `ref` may appear in
    several slots. `id` is a stable per-query slot ordinal (keys the queue + buttons)."""
    names, token_to_name = get_unit_name_resolver(edition)
    q = query.lower()
    spans = []  # (start, end, ref)
    for nm in names:                                   # full-name occurrences
        low = nm.lower()
        start = q.find(low)
        while start != -1:
            spans.append((start, start + len(low), nm))
            start = q.find(low, start + 1)
    for t, nm in token_to_name.items():                # distinctive single tokens
        for m in re.finditer(rf"\b{re.escape(t)}\b", q):
            spans.append((m.start(), m.end(), nm))
    # Greedy: earliest start first, longest span at a tie; skip anything that overlaps
    # an already-claimed span (suppresses the shorter substring at the same position).
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    slots, consumed_end, sid = [], -1, 0
    for s, e, ref in spans:
        if s < consumed_end:
            continue
        slots.append({"id": sid, "ref": ref, "start": s, "end": e})
        consumed_end = e
        sid += 1
    return slots

def unit_armies(unit_name: str, edition: str) -> list[str]:
    """Distinct armies a datasheet name appears under — the faction-ambiguity axis.
    Reads the process-wide unit_army_map (A2) instead of a per-call Chroma round-trip."""
    return indices.unit_army_map(edition).get(unit_name, [])

# ── Chassis disambiguation (faction-first → variant) ──────────────────────────
# A "chassis" is a datasheet name that is a substring of OTHER datasheet names
# ("Land Raider" ⊂ "Land Raider Crusader", "Venerable Land Raider", …). A bare
# chassis word in a query (resolve_named_units returns the base name) must fan out
# to the whole family so the user can pick faction, then variant — instead of being
# silently pinned to the lone datasheet literally named "Land Raider" (GK/SM only).

def is_chassis_base(name: str, all_names: list[str]) -> bool:
    """True if `name` is a proper substring of some OTHER datasheet name — i.e. it is
    a shared chassis with more specific variants, not a leaf datasheet."""
    low = name.lower()
    return any(o != name and low in o.lower() for o in all_names)

def _variant_signature(unit_name: str, army: str, edition: str) -> str:
    """Stable hash of a datasheet's rules text (army-scoped), so two differently
    NAMED variants with identical rules collapse to one button. Reads the cached
    variant_signature_map (A2); a missing pair degrades to name-only dedup (the same
    fallback the old per-call .get took on an empty/failed fetch)."""
    return indices.variant_signature_map(edition).get((unit_name, army), unit_name)

@st.cache_resource
def chassis_family(ref: str, edition: str) -> dict:
    """{army: [variant datasheet names]} for the chassis a query reference names.

    For a chassis base ('Land Raider') the family is every datasheet whose name
    contains the base; for a leaf ('Land Raider Crusader', 'Abaddon …') it is just
    that one name. Within each army, variants whose rules are byte-identical are
    deduped (rules-signature) so a faction never shows two buttons for the same unit.
    """
    names, _ = get_unit_name_resolver(edition)
    low = ref.lower()
    family_names = ([n for n in names if low in n.lower()]
                    if is_chassis_base(ref, names) else [ref])
    by_army: dict = defaultdict(list)
    for nm in family_names:
        for army in unit_armies(nm, edition):
            by_army[army].append(nm)
    out = {}
    for army, variants in by_army.items():
        seen, deduped = {}, []
        for nm in sorted(set(variants)):
            sig = _variant_signature(nm, army, edition)
            if sig not in seen:
                seen[sig] = nm
                deduped.append(nm)
        out[army] = deduped
    return out

def _new_unit_state(ref: str, family: dict, pinned: str | None):
    """Per-reference clarification sub-state, or a finalized {ref,unit_name,army}
    resolution when no question is needed. Returns ("ask", unit_dict) |
    ("auto", resolution_dict) | ("skip", None)."""
    if pinned:
        if pinned not in family:
            return "skip", None          # pinned faction doesn't field this unit
        variants = family[pinned]
        if len(variants) <= 1:
            return "auto", {"ref": ref, "unit_name": variants[0], "army": pinned}
        return "ask", {"ref": ref, "family": {pinned: variants},
                       "stage": "variant", "army": pinned}
    armies = list(family)
    if len(armies) == 1:
        variants = family[armies[0]]
        if len(variants) <= 1:
            return "auto", {"ref": ref, "unit_name": variants[0], "army": armies[0]}
        return "ask", {"ref": ref, "family": family, "stage": "variant",
                       "army": armies[0]}
    return "ask", {"ref": ref, "family": family, "stage": "faction", "army": None}

def build_clarification_queue(query: str, edition: str,
                              selected_faction: str | None = None) -> dict | None:
    """Two-stage (faction → variant) disambiguation state for every chassis / multi-
    faction unit the query names. Runs BEFORE retrieval/rerank so the heavy work only
    happens once faction(s) and variant(s) are known. Returns None when nothing the
    query names needs disambiguating (single-faction leaf, no unit, …).

      {"query", "units": [{ref, family, stage, army}, ...],
       "resolved": [{ref, unit_name, army}, ...]}

    `units` are the pending prompts (in order); `resolved` accumulates the picks that
    needed no question (a faction that fields exactly one variant auto-resolves).
    """
    _, factions = build_faction_keyword_map(edition)
    pinned = None
    if selected_faction and selected_faction != "All Factions":
        pinned = selected_faction
    else:
        pinned = detect_faction(query, factions)

    names, _ = get_unit_name_resolver(edition)
    units, resolved = [], []
    # Iterate per OCCURRENCE (slot), not per unique name, so the same chassis mentioned
    # twice gets two independent prompts/resolutions. Each slot carries its id+span so
    # highlight targets the right word and the rewrite is offset-shift-immune.
    for slot in find_unit_occurrences(query, edition):
        ref = slot["ref"]
        # Only chassis bases or multi-faction leaves are ambiguous; a single-faction
        # leaf needs no prompt (retrieve_unit_slice derives its sole army).
        if not is_chassis_base(ref, names) and len(unit_armies(ref, edition)) <= 1:
            continue
        family = chassis_family(ref, edition)
        if not family:
            continue
        kind, payload = _new_unit_state(ref, family, pinned)
        slot_fields = {"slot_id": slot["id"], "start": slot["start"], "end": slot["end"]}
        if kind == "ask":
            units.append({**payload, **slot_fields})
        elif kind == "auto":
            resolved.append({**payload, **slot_fields})
    if not units and not resolved:
        return None
    return {"query": query, "units": units, "resolved": resolved}

def next_clarification(state: dict | None) -> tuple | None:
    """The next question to render, or None when no prompts remain.
      ("faction", ref, [army, ...])           — stage 1
      ("variant", ref, army, [unit_name, ...]) — stage 2
    """
    if not state or not state.get("units"):
        return None
    u = state["units"][0]
    if u["stage"] == "faction":
        return "faction", u["ref"], sorted(u["family"])
    return "variant", u["ref"], u["army"], list(u["family"][u["army"]])

def apply_clarification(state: dict, choice: str) -> dict:
    """Record a button click for the FIRST pending unit and advance (returns a NEW
    state). At the faction stage `choice` is an army; at the variant stage it is a
    datasheet name. A faction that fields exactly one variant resolves immediately."""
    units = [dict(u) for u in state["units"]]
    resolved = list(state["resolved"])
    u = units[0]
    # Carry the occurrence slot (id + span) onto the resolution so the inline rewrite
    # and unit slice can target the exact mention this pick was for.
    slot = {k: u[k] for k in ("slot_id", "start", "end") if k in u}
    if u["stage"] == "faction":
        variants = u["family"][choice]
        if len(variants) == 1:
            resolved.append({"ref": u["ref"], "unit_name": variants[0], "army": choice, **slot})
            units.pop(0)
        else:
            u["army"], u["stage"] = choice, "variant"
    else:  # variant stage
        resolved.append({"ref": u["ref"], "unit_name": choice, "army": u["army"], **slot})
        units.pop(0)
    return {**state, "units": units, "resolved": resolved}

def highlight_ref(query: str, ref: str, start: int | None = None,
                  end: int | None = None) -> str:
    """Mark the unit reference inside the query so the user sees WHICH word the
    clarification buttons are about. When the occurrence's span (start/end) is given,
    bold exactly THAT occurrence (so the second 'Land Raider' highlights on its own
    prompt); otherwise fall back to the first case-insensitive match of `ref`."""
    if start is not None and end is not None:
        return f"{query[:start]}**:blue[{query[start:end]}]**{query[end:]}"
    return re.sub(re.escape(ref), lambda m: f"**:blue[{m.group(0)}]**",
                  query, count=1, flags=re.IGNORECASE)

def apply_resolution_to_query(query: str, resolved: list) -> str:
    """Rewrite the query INLINE — replace each resolved chassis OCCURRENCE where it sits
    with the specific resolved datasheet + faction — rather than appending a trailing
    "specifically the …" (which leaves the generic word in place and over-weights the
    unit's own datasheet chunks at rerank).

    Offset-shift-immune: occurrences are keyed by their span (start/end) in the
    ORIGINAL string and the result is rebuilt in a single forward pass that only ever
    READS the original — so replacing one occurrence never invalidates a later one's
    span (the failure mode of count=1 replace-one-at-a-time). This is what makes the
    mirror case work: 'a Custodes Land Raider vs a Chaos Land Raider' rewrites BOTH
    mentions to their distinct (unit, army) pairs."""
    spanned = sorted((r for r in resolved if r.get("start") is not None
                      and r.get("end") is not None), key=lambda r: r["start"])
    if not spanned:                                    # legacy/no-span: name-based fallback
        out = query
        for r in resolved:
            out = re.sub(re.escape(r["ref"]), f'{r["unit_name"]} ({r["army"]})',
                         out, count=1, flags=re.IGNORECASE)
        return out
    out, prev = [], 0
    for r in spanned:
        out.append(query[prev:r["start"]])
        out.append(f'{r["unit_name"]} ({r["army"]})')
        prev = r["end"]
    out.append(query[prev:])
    return "".join(out)

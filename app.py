"""
app.py — The Judge: Warhammer 40K Rules Adjudicator
====================================================
Streamlit chat interface backed by ChromaDB RAG + Groq/Qwen LLM.

Run:
  streamlit run app.py --server.port 8501
"""

import json
import math
import sqlite3
import re
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

# `streamlit run app.py` executes this file as the module `__main__`, NOT `app`. The
# submodules (indices/retrieval) reach back here via a lazy `import app` at call time;
# without this line that import would not find the running script, so Python would
# import a SECOND copy of app.py as `app` and RE-EXECUTE the UI at the bottom
# (init_session/render_sidebar/render_chat) — surfacing as a StreamlitDuplicateElementId
# crash. Registering the running module under `app` makes those lazy imports resolve to
# THIS already-loaded instance. (Under the evals, `import app` runs first so `app` is
# already in sys.modules and this setdefault is a harmless no-op.)
import sys as _sys
_sys.modules.setdefault("app", _sys.modules[__name__])

import config
import indices
import retrieval
from chunk_model import Chunk, Provenance, content_key_text

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent
# Per-edition CSV dir is resolved from config.get_edition(edition)["csv_dir"].

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="The Judge",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Current user ──────────────────────────────────────────────────────────────

def get_current_user() -> str:
    try:
        user = st.context.headers.get("X-Remote-User", "").strip()
        if user:
            return user
    except Exception:
        pass
    return "unknown"

# ── ChromaDB (cached) ─────────────────────────────────────────────────────────

@st.cache_resource
def get_collection(edition: str):
    client = chromadb.PersistentClient(path=str(ROOT / config.CHROMA_DIR))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=config.EMBEDDING_MODEL
    )
    return client.get_collection(
        name=config.get_edition(edition)["collection"],
        embedding_function=emb_fn
    )

# ── Lexical (BM25) index — Layer 3 lexical half ───────────────────────────────

# Minimal stopword set so the term-overlap gate keys on meaningful words. Kept
# inline (no nltk dependency). "not"/"never"/"no" are deliberately NOT stopwords.
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "how", "what", "which", "who", "whom", "when", "where",
    "why", "can", "could", "should", "would", "will", "shall", "may", "might",
    "i", "me", "my", "we", "our", "you", "your", "it", "its", "they", "them",
    "to", "of", "in", "on", "at", "for", "and", "or", "as", "if", "that", "this",
    "these", "those", "with", "from", "by", "about", "into", "than", "then",
    "each", "other", "too", "so", "up", "out", "off", "over", "work", "works",
    "rule", "rules", "does", "got", "get",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")

def lexical_tokens(text: str) -> list[str]:
    """Lowercase word tokens used by both the BM25 index and query scoring."""
    return [t for t in _TOKEN_RE.findall(text.lower()) if len(t) > 1]

def content_terms(text: str) -> set[str]:
    """Non-stopword tokens — the set the term-overlap gate compares against."""
    return {t for t in lexical_tokens(text) if t not in _STOPWORDS}

def rule_display_name(meta: dict) -> str:
    """The rule's own name (leaf of the breadcrumb / rule_name), normalized to
    lowercase alphanumerics+spaces — used to spot an exact rule-name lookup."""
    raw  = meta.get("rule_name") or meta.get("breadcrumb") or ""
    leaf = raw.split(">")[-1]
    return re.sub(r"[^a-z0-9]+", " ", leaf.lower()).strip()

# B8: the operator set _meta_matches understands must stay in LOCKSTEP with what
# process_query / rules_where actually emit (those are the only `where` clauses that
# reach the lexical pass). This constant makes the coupling greppable: if a new
# operator is added to a where-builder, grep for this name to find the one place that
# must learn it. _where_operators() (below) extracts the ops a clause uses, so a test
# can assert process_query's output ⊆ _META_MATCHES_OPS instead of relying on memory.
_META_MATCHES_OPS = frozenset({"$or", "$and", "$ne", "$eq"})

def _where_operators(where: dict | None) -> set:
    """The set of $-operators a where-clause uses (recursively). For the B8 lockstep
    check: every operator process_query / rules_where can emit must be in
    _META_MATCHES_OPS, else _meta_matches would silently fail-closed on it."""
    ops: set = set()
    if not isinstance(where, dict):
        return ops
    for key, cond in where.items():
        if key.startswith("$"):
            ops.add(key)
        if isinstance(cond, dict):
            for op in cond:
                if op.startswith("$"):
                    ops.add(op)
        if isinstance(cond, list):
            for c in cond:
                ops |= _where_operators(c)
    return ops

def _meta_matches(meta: dict, where: dict | None) -> bool:
    """
    Evaluate a Chroma `where` clause against a single chunk's metadata in-memory,
    covering exactly the operators process_query / rules_where emit (_META_MATCHES_OPS:
    $or, $and, $ne, $eq, plus bare equality). Unknown operators fail CLOSED (return
    False) so a lexical hit is never injected past a filter we don't understand — this
    is what keeps the mission-pack HARD INVARIANT intact without a Chroma round-trip
    per query.
    """
    if not where:
        return True
    for key, cond in where.items():
        if key == "$or":
            if not any(_meta_matches(meta, c) for c in cond):
                return False
        elif key == "$and":
            if not all(_meta_matches(meta, c) for c in cond):
                return False
        elif isinstance(cond, dict):
            for op, operand in cond.items():
                if op == "$ne":
                    if meta.get(key) == operand:
                        return False
                elif op == "$eq":
                    if meta.get(key) != operand:
                        return False
                else:
                    return False  # unknown operator → fail closed
        else:
            if meta.get(key) != cond:
                return False
    return True

@st.cache_resource
def get_bm25_index(edition: str):
    """
    BM25 index over the SAME documents as the dense collection, so lexical and
    dense retrieval share one doc universe (and metadata). Built once per edition
    and cached. Returns (bm25, ids, docs, metas, doc_term_sets).
    """
    col  = get_collection(edition)
    data = col.get(include=["documents", "metadatas"])
    ids, docs, metas = data["ids"], data["documents"], data["metadatas"]
    tokenized      = [lexical_tokens(d) for d in docs]
    doc_term_sets  = [set(t) for t in tokenized]
    bm25 = BM25Okapi(tokenized)
    # Precompute each doc's normalized rule name once, so the exact rule-name pass
    # (full-corpus, BM25-rank-independent) is a cheap substring scan per query.
    names = [rule_display_name(m) for m in metas]
    return bm25, ids, docs, metas, doc_term_sets, names

def lexical_search(query: str, where: dict | None, edition: str, k: int) -> list[dict]:
    """
    BM25 retrieval over the edition corpus, restricted to the same `where`
    allow-set as dense retrieval (so the mission-pack HARD INVARIANT holds), then
    gated by query/document term overlap so paraphrases with no shared vocabulary
    are not injected. Returns chunk dicts with a synthesized cosine-band
    `similarity` (scaled by normalized BM25) and `lexical=True`.
    """
    q_terms = content_terms(query)
    if not q_terms:
        return []
    bm25, ids, docs, metas, doc_term_sets, names = get_bm25_index(edition)
    q_norm = " " + re.sub(r"[^a-z0-9]+", " ", query.lower()).strip() + " "

    hits     = []
    injected = set()

    # Pass 1 — exact rule-name lookup over the WHOLE corpus (independent of BM25
    # rank). A distinctive multi-word rule name appearing verbatim in the query is
    # a confident lookup; BM25's length bias can bury a short definition chunk
    # below the top-k even when the query names it (e.g. "...engagement range
    # vertically" inside a charge question — ER dense sim 0.34, BM25 rank >30).
    for i, name in enumerate(names):
        if len(name.split()) >= 2 and f" {name} " in q_norm and _meta_matches(metas[i], where):
            injected.add(i)
            hits.append(Chunk(text=docs[i], meta=metas[i], prov=Provenance.LEXICAL,
                              cosine=config.LEXICAL_SIM_CEIL))
            if len(hits) >= config.LEXICAL_INJECT_MAX:
                return hits

    # Pass 2 — BM25 top-k gated by term overlap (catches exact single-name lookups
    # and high-overlap matches dense missed; silent on paraphrases).
    scores = bm25.get_scores(lexical_tokens(query))
    order  = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    top    = scores[order[0]] if order and scores[order[0]] > 0 else 0.0
    if top <= 0:
        return hits

    for i in order:
        if scores[i] <= 0:
            break
        if i in injected:
            continue
        # Same isolation as dense: a lexical hit must satisfy the `where` clause
        # (mission-pack off ⇒ never injected). Evaluated in-memory on cached meta.
        if not _meta_matches(metas[i], where):
            continue
        overlap = len(q_terms & doc_term_sets[i]) / len(q_terms)
        if overlap < config.LEXICAL_MIN_OVERLAP:
            continue
        norm = scores[i] / top
        sim  = config.LEXICAL_SIM_FLOOR + (config.LEXICAL_SIM_CEIL - config.LEXICAL_SIM_FLOOR) * norm
        hits.append(Chunk(text=docs[i], meta=metas[i], prov=Provenance.LEXICAL,
                          cosine=round(sim, 3)))
        if len(hits) >= config.LEXICAL_INJECT_MAX:
            break
    return hits

# ── SQLite persistence ────────────────────────────────────────────────────────
# Moved to persistence.py (Phase 5). upsert_conversation is now session-agnostic
# (takes + returns conv_id); render_chat owns the session_state wiring.
from persistence import (                                              # noqa: E402
    db_connect, upsert_conversation, load_archived_conversations,
    load_conversation_messages,
)

# ── Query processor ───────────────────────────────────────────────────────────

SYNONYMS = {
    "invul":             "invulnerable save",
    "inv save":          "invulnerable save",
    "fnp":               "feel no pain",
    "sticky":            "sticky objectives",
    "saves":             "saving throws",
    "reserves":          "reinforcements",
    "overwatch":         "overwatch",
    "ap":                "armour penetration",
    "oc":                "objective control",
    "ds":                "deep strike",
    "deep strike":       "deep strike",
    "transhuman":        "transhuman physiology",
    "battleshocked":     "battle-shock",
    "battle shocked":    "battle-shock",
    "battleshock":       "battle-shock",
    "battle shock":      "battle-shock",
    "brick":             "unit",
}

# ── Unit/faction resolution + clarification state machine ─────────────────────
# Moved to clarify.py (Phase 5). Re-exported so process_query / retrieve_unit_slice /
# render_chat / the sidebar keep calling these by their original names.
from clarify import (                                                  # noqa: E402
    build_faction_keyword_map, detect_faction, build_unit_index, detect_unit,
    get_unit_name_resolver, resolve_named_units, find_unit_occurrences, unit_armies,
    is_chassis_base, chassis_family, build_clarification_queue, next_clarification,
    apply_clarification, highlight_ref, apply_resolution_to_query,
)


def expand_query(query: str) -> str:
    q = query
    for short, full in SYNONYMS.items():
        q = re.sub(rf'\b{re.escape(short)}\b', full, q, flags=re.IGNORECASE)
    return q

# Multi-word / unambiguous phrase triggers — safe as plain substring tests.
_CORE_PHRASE_TRIGGERS = [
    "core rule", "universal rule", "in every army", "basic rule",
    "all armies", "always active", "mission rule",
    "secondary mission", "primary mission", "tournament",
    "matched play", "victory points", "embark", "disembark", "riding in",
]
# D16: short/ambiguous tokens that, as bare substrings, re-scope retrieval on a
# COINCIDENTAL match ("vp" inside another token; "transport"/"inside"/"scoring"
# appearing incidentally). Matched on WORD BOUNDARIES so only the real word triggers.
_CORE_WORD_TRIGGERS = re.compile(r"\b(?:vp|scoring|transport|inside)\b", re.I)

def is_core_rules_query(query: str, edition: str) -> bool:
    q = query.lower()
    mp_name = config.get_edition(edition)["mission_pack"]["name"].lower()
    if mp_name in q:                       # the pack name is distinctive enough as a substring
        return True
    if any(t in q for t in _CORE_PHRASE_TRIGGERS):
        return True
    return bool(_CORE_WORD_TRIGGERS.search(q))

def process_query(query: str, edition: str, mission_pack_mode: bool = True):
    _, factions = build_faction_keyword_map(edition)
    expanded     = expand_query(query)
    faction      = detect_faction(query, factions)
    include_core = is_core_rules_query(query, edition)
    mp_category  = config.get_edition(edition)["mission_pack"]["category"]
    # Faction-less, non-core-trigger queries used to fall through to an UNFILTERED
    # retrieval (where=None) that floods rules questions with datasheet/ability/
    # stratagem noise (G4: ~54% of a rules question's context). Split that bucket:
    # a query that names a specific datasheet is a unit lookup (stay broad); every
    # other faction-less query is a rules question and is scoped to Core+mp.
    names_unit   = detect_unit(query, edition)

    # NOTE: isolation comes from the per-edition collection, NOT from a `where`
    # filter on edition — do not add {"edition": ...} here (see architecture §2).
    # Army/detachment rules are NOT scoped here — they reach context via the
    # name-gated retrieve_named_rules slice (folded into retrieve_rules_slice), which
    # mirrors the unit slice: a faction/detachment rule the query NAMES is reserved,
    # so it survives budget truncation without weakly-matched rules ballooning
    # unrelated questions (the cross-encoder saturates ~1.0 on off-topic rules, so a
    # name gate — not a rerank threshold — is the clean discriminator).
    # Where-clause truth table (B7 — the 5-way if/elif collapsed to the real cases;
    # the audit found the dropped arms byte-identical to ones that follow). Columns:
    # faction set? · include_core? · names_unit?  →  where
    #   ── toggle ON (mission-pack) ──
    #   faction · ─core · ─       → {army OR mp}              (faction rules + mp)
    #   faction · +core · ─       → {army OR Core OR mp}      (adds Core)
    #   ─       · ─     · unit     → None                      (broad datasheet lookup)
    #   ─       · *     · ─       → {Core OR mp}              (rules q; +core arm was identical)
    #   ── toggle OFF ──
    #   faction · *     · *       → {army AND ≠mp}            (both faction arms were identical)
    #   ─       · ─     · unit     → {≠mp}                     (broad lookup, minus mp = invariant)
    #   ─       · *     · ─       → {Core}                     (rules q; +core arm was identical)
    if mission_pack_mode:
        if faction and not include_core:
            where = {"$or": [{"army": faction}, {"category": mp_category}]}
        elif faction:  # faction and include_core
            where = {"$or": [{"army": faction}, {"category": "Core_Rules"}, {"category": mp_category}]}
        elif names_unit:
            # Unit lookup (incl. "Land Raider transport capacity"): go broad for
            # the datasheet — the guaranteed rules slice still injects the core
            # rule, so we get both without scoping away the unit.
            where = None
        else:  # rules question (include_core arm was identical to this else)
            where = {"$or": [{"category": "Core_Rules"}, {"category": mp_category}]}
    else:
        if faction:  # both include_core states were identical here
            where = {"$and": [{"army": faction}, {"category": {"$ne": mp_category}}]}
        elif names_unit:
            where = {"category": {"$ne": mp_category}}  # unit lookup → broad, minus mp (invariant)
        else:  # rules question (include_core arm was identical to this else)
            where = {"category": "Core_Rules"}

    return expanded, where, faction

# ── Retriever ─────────────────────────────────────────────────────────────────

def retrieve(query: str, where: dict | None, edition: str, n_results: int = None) -> list[dict]:
    """
    Retrieve chunks from ChromaDB.
    n_results defaults to config.TOP_K. Pass a larger value to get more
    candidates before deduplication.
    """
    collection = get_collection(edition)
    kwargs = dict(
        query_texts=[query],
        n_results=n_results or config.TOP_K,
        include=["documents", "metadatas", "distances"],
    )
    if where:
        kwargs["where"] = where
    where_fell_back = False
    try:
        results = collection.query(**kwargs)
    except Exception:
        # D17: don't crash on a malformed/over-complex where — but DON'T silently
        # widen scope past the HARD INVARIANT either. Re-query unfiltered, then
        # re-assert the same `where` in-memory below so a faction/category filter
        # can never leak past its intended scope unnoticed.
        kwargs.pop("where", None)
        where_fell_back = True
        import logging
        logging.getLogger(__name__).warning(
            "retrieve(): where-clause rejected by Chroma; re-querying unfiltered and "
            "re-asserting the filter in-memory. where=%r", where)
        results = collection.query(**kwargs)

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        # On the fallback path the query ran unfiltered, so honor the where-clause
        # here (same in-memory evaluator the lexical pass uses; fail-closed).
        if where_fell_back and not _meta_matches(meta, where):
            continue
        similarity = 1 - dist
        if similarity >= config.SIMILARITY_THRESHOLD:
            chunks.append(Chunk(text=doc, meta=meta, prov=Provenance.DENSE,
                                cosine=round(similarity, 3)))

    # Lexical (BM25) augmentation: catch exact rule-name hits dense missed. Add
    # only lexical-only chunks (those whose rules text isn't already present), so
    # this purely improves recall and never re-weights an existing dense hit.
    if config.HYBRID_LEXICAL:
        seen = {content_key(c) for c in chunks}
        for hit in lexical_search(query, where, edition, k=config.LEXICAL_CANDIDATES):
            key = content_key(hit)
            if key not in seen:
                seen.add(key)
                chunks.append(hit)
    return chunks

# ── Deduplication ─────────────────────────────────────────────────────────────

def content_key(chunk) -> str:
    """
    Stable hash of a chunk's *rules text* only — strips unit name / faction /
    category / source headers so identical rule text from different units (or
    the same chunk arriving via two different queries) collapses to one key.
    Delegates to the memoized chunk_model.content_key_text (A4). Accepts a Chunk
    (chunk["text"] → .text via the shim) or a bare {"text": ...} dict.
    """
    return content_key_text(chunk["text"])

def deduplicate_chunks(chunks: list) -> list:
    """
    Remove chunks whose rules text is substantively identical, keeping the
    first occurrence (callers sort by score first so the best survives).
    """
    seen   = set()
    result = []
    for chunk in chunks:
        key = content_key(chunk)
        if key not in seen:
            seen.add(key)
            result.append(chunk)
    return result

# ── Guaranteed rules slice + authority re-rank (Layer 1) ──────────────────────

def rules_where(edition: str, mission_pack_mode: bool) -> dict:
    """
    Where-filter for the guaranteed rules slice. Core Rules are always allowed;
    the mission-pack category is allowed ONLY when the toggle is on.
    HARD INVARIANT (spec/retrieval.md): toggle off => mission-pack never queried.
    """
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    if mission_pack_mode:
        return {"$or": [{"category": "Core_Rules"}, {"category": mp_category}]}
    return {"category": "Core_Rules"}

def retrieve_rules_slice(query: str, edition: str, mission_pack_mode: bool,
                         n_results: int) -> list[dict]:
    """
    Second, category-scoped retrieval that guarantees Core Rules (and, when the
    toggle is on, mission-pack rules) are represented even when the main query's
    semantic match favors datasheets. Below-threshold rules are still dropped by
    retrieve(), so irrelevant core rules are not force-injected.
    """
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    allowed     = {"Core_Rules"} | ({mp_category} if mission_pack_mode else set())
    chunks      = retrieve(query, rules_where(edition, mission_pack_mode),
                           edition, n_results=n_results)
    # Defensive: retrieve() silently drops its where-filter on error, so
    # re-assert the category allow-list here — this is what guarantees a
    # mission-pack chunk can never leak in while the toggle is off.
    sliced = [c for c in chunks if c["metadata"].get("category") in allowed]
    # Name-gated army/detachment rules ride the guaranteed rules slice (reserved by
    # assemble_context), so a NAMED faction/detachment rule survives budget truncation.
    return sliced + retrieve_named_rules(query, edition)


# Title prefixes the ETL gives the two faction-rule block types.
_RULE_TITLE_RE   = re.compile(r"^#\s*(?:Army|Detachment)\s+Rule:\s*(.+?)\s*$")
_RULE_DETACH_RE  = re.compile(r"\*\*Detachment:\*\*\s*([^|]+)")

def retrieve_named_rules(query: str, edition: str) -> list[dict]:
    """Guaranteed candidacy for an Army_Rule / Detachment_Rule the query NAMES — by
    rule name (e.g. "Oath of Moment", "Armoured Wrath") or detachment name (e.g.
    "Ironstorm Spearhead"). A metadata fetch + lexical gate, NOT semantic: the
    cross-encoder saturates ~1.0 on off-topic rules, so a rerank threshold can't
    separate them — but an unrelated query won't NAME a specific rule. Mirrors the
    unit slice. See spec/army-detachment-rules.md."""
    q = (query or "").lower()
    # (rule_name, detach_name, doc, meta) tuples PRE-PARSED once into
    # indices.named_rule_index (A1) — substring scan over a cached list, not a Chroma
    # round-trip + regex parse on ~343 docs per query.
    hits = []
    for name, detach, doc, meta in indices.named_rule_index(edition):
        if (len(name) >= 4 and name in q) or (len(detach) >= 5 and detach in q):
            # cosine 0.0 (not None) so boosted_score works pre-rerank — same
            # degraded-cosine convention the unit slice uses.
            hits.append(Chunk(text=doc, meta=meta, prov=Provenance.NAMED_RULE, cosine=0.0))
    return hits

# ── Guaranteed unit slice (datasheet candidacy for unit-named queries) ─────────

UNIT_SLICE_CATEGORIES = ("Datasheet", "Ability", "Datasheet_Section")

# Categories whose `army` metadata pins a chunk to a faction. Everything else
# (Core_Rules and the per-edition mission pack — incl. 11e's differently-named
# pack) is faction-agnostic and always kept. Inverting to an allowlist (rather
# than a denylist of agnostic categories) keeps the filter pure: no `edition`
# argument is needed to compute the mission-pack category name. Add any NEW
# faction-bearing category here. See spec/multi-unit-clarification-and-faction-scope.md (P2).
FACTION_SCOPED_CATEGORIES = set(UNIT_SLICE_CATEGORIES) | {"Army_Rule", "Detachment_Rule"}

def scope_to_resolved_armies(chunks: list[dict], resolved_armies: set) -> list[dict]:
    """Drop faction-bearing chunks whose faction isn't in `resolved_armies`; keep
    faction-agnostic chunks (Core_Rules, mission-pack) and anything not faction-
    scoped. No-op when `resolved_armies` is empty. Pure — no edition/config
    dependency. Army_Rule `army` may be a comma-joined multi-faction list
    (allied rules share an id), so membership is tested against the split set.

    A faction-bearing chunk with empty `army` yields an empty set → dropped; after
    P3 every unit/rule chunk has a populated `army`, so this only bites if P3 didn't
    land — the strict drop is the safe direction (never re-admit an unscoped chunk)."""
    if not resolved_armies:
        return chunks
    out = []
    for c in chunks:
        if c["metadata"].get("category", "") not in FACTION_SCOPED_CATEGORIES:
            out.append(c)                                   # agnostic → always keep
            continue
        army   = c["metadata"].get("army", "") or ""
        armies = {s.strip() for s in army.split(",") if s.strip()}
        if armies & resolved_armies:
            out.append(c)
    return out

def retrieve_unit_slice(query: str, edition: str, mission_pack_mode: bool,
                        resolution: list | dict | None = None) -> list[dict]:
    """Guaranteed candidacy for the datasheet(s) a query NAMES: a metadata fetch
    (NOT semantic) of each named unit's own chunks. A unit that doesn't embed near
    the query — Abaddon's stat block vs a 'Devastating Wounds' question — is still
    placed in the pool, where the reranker scores it and assemble_context reserves
    the best per-unit chunks into context (without forcing them to rank 1).

    Two sourcing modes:
      • RESOLVED (clarification done): `resolution` is a list of finalized
        {"unit_name", "army"} pairs — fetch exactly those (a chassis query resolves
        "Land Raider" → the specific "Venerable Land Raider"/"Adeptus Custodes").
      • DERIVED (no clarification needed): `resolution` is empty — fall back to the
        datasheet name(s) the query names, army pinned by the faction in the query or
        the unit's sole army; an unresolved multi-faction unit fetches all armies
        (dedup + the reserved-slot cap keep it bounded).

    similarity defaults to 0.0 (not None) so degraded cosine mode — reranker failed
    to load — still sorts these without a crash; they just rank low but stay present.
    """
    collection = get_collection(edition)
    cats       = {"$in": list(UNIT_SLICE_CATEGORIES)}

    # Build the (unit_name, army|None) fetch list.
    targets: list[tuple] = []
    if resolution:  # finalized list from the clarification flow
        targets = [(r["unit_name"], r.get("army")) for r in resolution]
    else:
        _, factions = build_faction_keyword_map(edition)
        q_faction   = detect_faction(query, factions)
        for unit in resolve_named_units(query, edition):
            armies = unit_armies(unit, edition)
            army   = q_faction or (armies[0] if len(armies) == 1 else None)
            targets.append((unit, army))

    out = []
    for unit, army in targets:
        where = ({"$and": [{"unit_name": unit}, {"army": army}, {"category": cats}]}
                 if army else {"$and": [{"unit_name": unit}, {"category": cats}]})
        try:
            res = collection.get(where=where, include=["documents", "metadatas"])
        except Exception:
            continue
        for doc, meta in zip(res["documents"], res["metadatas"]):
            out.append(Chunk(text=doc, meta=meta, prov=Provenance.UNIT_SLICE, cosine=0.0))
    return out

def boosted_score(chunk: dict, edition: str, mission_pack_mode: bool) -> float:
    """Relevance plus the authority tiebreak (mission-pack > core > rest).

    Relevance is the cross-encoder score (chunk['rerank'], 0..1) when the chunk was
    reranked; the bi-encoder cosine otherwise (e.g. a chunk that bypassed the
    reranker). The authority tiebreak stays deterministic — it encodes the
    mission-pack-overrides-core ordering, never delegated to a learned model.

    When the chunk WAS reranked we keep cosine as a sub-rerank FLOOR
    (max(rerank, W·cosine)): the cross-encoder tanks ~0 on general rules even when
    essential, and ranking by that alone discards the bi-encoder signal that still
    distinguishes a relevant rule from filler. W (RERANK_COSINE_FLOOR) is small
    enough that a blended cosine never leapfrogs a genuinely reranked chunk — it only
    re-orders the rules the reranker flattened to ~0. See config.RERANK_COSINE_FLOOR.

    B9: rank_seeded_below_parents stamps a `rank_override` (the parent-cap effective
    score) on a seeded dep — the cross-encoder rates a dependency ~0, so its rank is
    set from its parent, not its relevance. Honor that override directly; this removed
    the old back-out math (rerank = eff − authority) and a call site.
    """
    forced = chunk.get("rank_override")
    if forced is not None:
        return forced
    cos = chunk.get("similarity") or 0.0
    rer = chunk.get("rerank")
    relevance = max(rer, config.RERANK_COSINE_FLOOR * cos) if rer is not None else cos
    # Authority TIEBREAK (mission-pack > core > rest), folded inline (B9 — no longer a
    # standalone "subsystem"). Tiny by design: it only orders genuine ties without
    # overpowering relevance. The old flat cosine-band boosts were retired (they
    # leapfrogged more-relevant chunks in the compressed rerank band); rules now surface
    # as context by being *referenced* (seed_referenced_rules). See spec/reranker.md §8e.
    cat         = chunk["metadata"].get("category", "")
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    if mission_pack_mode and cat == mp_category:
        tiebreak = 2 * config.AUTHORITY_TIEBREAK
    elif cat == "Core_Rules":
        tiebreak = config.AUTHORITY_TIEBREAK
    else:
        tiebreak = 0.0
    return relevance + tiebreak

# ── Cross-encoder reranking (Layer 3, ranking half) ───────────────────────────

@st.cache_resource
def get_reranker():
    """Load the cross-encoder once (mirrors get_collection). Local ⇒ zero Groq TPM.
    Returns None on any load failure so the chat path degrades to cosine ranking
    rather than crashing. See spec/reranker.md."""
    try:
        from sentence_transformers import CrossEncoder
        return CrossEncoder(config.RERANK_MODEL)
    except Exception:
        return None


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


# Clause boundaries: subordinator/discourse markers + sentence punctuation. A
# compound rules question hangs its operative clause off one of these ("AFTER i
# charge … how far can i pile in", "IF the transport moves, can they charge").
_SEGMENT_SPLIT_RE = re.compile(
    r"[.;,]|\b(?:after|before|once|when|whenever|while|if|unless|assuming|"
    r"given that|provided|so that|in order to|then|and then|but)\b", re.I)
# The operative clause is the one phrased as a question (interrogative/modal head).
_INTERROG_RE = re.compile(
    r"^\s*(?:how|what|can|could|does|do|did|is|are|may|would|should|which|"
    r"when|where|will|whose|who)\b", re.I)

def segment_query(query: str) -> list[str]:
    """Split a query into clauses on subordinator/discourse markers + punctuation,
    keeping the interrogative-headed (operative) ones — pure heuristic, NO model.

    Returns [query] unchanged when no marker is found, so single-clause queries are
    untouched. When it DOES segment, the whole query is always appended as the last
    segment, so max-pool (rerank_pools) can only LIFT a chunk above its whole-query
    score, never demote it — the degradation guarantee. Operative clauses are capped
    at RERANK_SEGMENT_MAX to bound the cross-encoder cost."""
    q     = query.strip()
    parts = [p.strip() for p in _SEGMENT_SPLIT_RE.split(q) if p and len(p.strip()) > 3]
    if len(parts) <= 1:
        return [q]
    # D15: only take the segmented (up-to-3×-cross-encoder) path when a genuine
    # OPERATIVE (interrogative-headed) clause is actually found. A query that merely
    # contains a marker ("models in the unit, and the weapons they carry") but has no
    # interrogative clause is NOT a compound question — segmenting it on raw `parts`
    # paid 3× cost and ran the cluster tiebreak on structure that isn't there. No
    # interrogative clause ⇒ single whole-query pass (identical to OFF, zero added cost).
    interrog = [p for p in parts if _INTERROG_RE.search(p)]
    if not interrog:
        return [q]
    kept = interrog[:config.RERANK_SEGMENT_MAX]
    if q not in kept:                       # whole-query fallback ⇒ monotonic-safe
        kept.append(q)
    return kept

def rerank_pools(query: str, edition: str, mission_pack_mode: bool, *pools: list) -> None:
    """Stamp chunk['rerank'] = sigmoid(cross-encoder logit) on every UNIQUE chunk
    across the given candidate pools, scoring each once (deduped by content_key).

    With config.RERANK_SEGMENT_MAXPOOL the query is first SEGMENTED into clauses
    (segment_query) and each candidate is scored against EVERY segment, keeping the
    MAX — so a chunk that answers only the operative clause of a compound question
    ("how far can i pile in") is no longer buried by the framing clause it doesn't
    match. The whole query is always one segment, so the max is ≥ the single-query
    score for every chunk (never worse than OFF). No-op shape when the query has one
    clause (no marker) — identical to the legacy single-pass.

    No-op when the model fails to load or there are no candidates — callers fall
    back to cosine via boosted_score. Operates only on already-where-filtered
    candidates, so the mission-pack HARD INVARIANT holds by construction (a chunk
    that was never retrieved can't be reranked in). Mutates the chunk dicts in
    place; does not reorder (assemble_context sorts).
    """
    model = get_reranker()
    if model is None:
        return
    unique = {}
    for pool in pools:
        for c in pool:
            unique.setdefault(content_key(c), c)
    if not unique:
        return
    items = list(unique.values())
    keys  = list(unique.keys())

    segments = segment_query(query) if config.RERANK_SEGMENT_MAXPOOL else [query]
    if len(segments) == 1:
        logits       = model.predict([(segments[0], c["text"]) for c in items])
        score_by_key = {k: _sigmoid(float(s)) for k, s in zip(keys, logits)}
    else:
        # MxS pairs, one predict call (the model batches); max-pool the S segment
        # scores per candidate so it is judged on the clause it best answers, then
        # add W·(whole-query score) as a tiebreak so the saturated top cluster is
        # ordered by holistic relevance, not a noisy ~0.01 clause margin. The whole
        # query is always the LAST segment (segment_query guarantee).
        flat = model.predict([(seg, c["text"]) for c in items for seg in segments])
        S    = len(segments)
        W    = config.RERANK_SEGMENT_TIEBREAK
        score_by_key = {}
        for i, k in enumerate(keys):
            win = [_sigmoid(float(x)) for x in flat[i*S:(i+1)*S]]
            score_by_key[k] = max(win) + W * win[-1]      # maxpool + tiebreak(whole)
    for pool in pools:
        for c in pool:
            c["rerank"] = score_by_key[content_key(c)]


@st.cache_resource
def get_embedder():
    """The bi-encoder used for the span-bridge gate (same model the collection
    embeds with). Loaded once; reused for cheap sentence/query encodings."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(config.EMBEDDING_MODEL)


# Surface forms used to locate the sentence in a parent rule that NAMES a dep.
# Curated for the ratified graph's deps; falls back to the stem's words otherwise.
_DEP_SURFACE = {
    "normal_moves":         r"normal move",
    "advance_moves":        r"\badvanc",          # "Advance", "Advanced", "Advancing"
    "fall_back_moves":      r"f(?:all|ell) back",
    "remain_stationary":    r"remain(?:s|ed|ing)? stationary",
    "engagement_range":     r"engagement range",
    "unit_coherency":       r"coherency",
    "charging_with_a_unit": r"charge move|charging",
}

def _dep_surface_re(dep_stem: str):
    pat = _DEP_SURFACE.get(dep_stem) or re.escape(
        re.sub(r"^\d+\s+", "", dep_stem.replace("_", " ")).rstrip("s"))
    return re.compile(pat, re.I)

def _rule_sentences(text: str) -> list[str]:
    """Split a rule chunk into sentences (rules prose only, minus header lines)."""
    prose = "\n".join(l for l in text.splitlines()
                      if not l.startswith("#") and not l.startswith("**"))
    return [s.strip() for s in re.split(r"(?<=[.])\s+", prose) if len(s.strip()) > 15]

def _cos(a, b) -> float:
    denom = (float(a @ a) ** 0.5) * (float(b @ b) ** 0.5)
    return float(a @ b) / denom if denom else 0.0

_CHUNK_SENT_CACHE: dict = {}   # content_key -> (sentences, embeddings)

def _chunk_sentence_embeddings(chunk: dict):
    """Sentences of a chunk + their embeddings, cached by content_key. Works for any
    parent (a rule chunk for definitions, a unit/ability chunk for referenced rules)."""
    key = content_key(chunk)
    cached = _CHUNK_SENT_CACHE.get(key)
    if cached is None:
        sents = _rule_sentences(chunk["text"])
        embs  = get_embedder().encode(sents) if sents else []
        cached = (sents, embs)
        _CHUNK_SENT_CACHE[key] = cached
    return cached


# USRs that unit/ability chunks reference by name, as they appear in ability text
# (surface regex) -> a substring to resolve the actual rule chunk. Curated, high
# precision; extend as needed. Replaces the blanket authority boost for unit Qs.
_USR_RULES = {
    r"\bfall(?:s|ing)? back\b|\bfell back\b":  "fall back",
    r"\bdeep strike\b":                        "deep strike",
    r"\bfeel no pain\b":                       "feel no pain",
    r"\blone operative\b":                     "lone operative",
    r"\bengagement range\b":                   "engagement range",
    r"\bbattle.?shock(?:ed)?\b":               "battle shock",
    r"\bdeadly demise\b":                      "deadly demise",
    r"\bfights? first\b":                      "fights first",
    r"\bstealth\b":                            "stealth",
    r"\bprecision\b":                          "precision",
    r"\bscouts?\b":                            "scouts",
    r"\binfiltrators?\b":                      "infiltrators",
    r"\bbig guns never tire\b":                "big guns never tire",
    r"\bdevastating wounds\b":                 "devastating wounds",
    r"\bsustained hits\b":                     "sustained hits",
    r"\blethal hits\b":                        "lethal hits",
}

@st.cache_resource
def get_rule_name_index(edition: str):
    """[(surface_regex, rule_stem), …] for the USRs unit abilities reference by name.
    Resolves each curated keyword to a real rule chunk via the rule vocabulary, so a
    surfaced ability that names a USR can seed that rule as context."""
    _, seed = get_dep_index(edition)
    index = []
    for rx, key in _USR_RULES.items():
        stem = next((s for s, p in seed.items()
                     if key in rule_display_name(p["metadata"])), None)
        if stem:
            index.append((re.compile(rx, re.I), stem))
    return index


def _gate_and_build(dep_parents: dict, dep_bridge: dict, seed: dict,
                    allowed: set, present: set, gate: float) -> list:
    """Apply the relevance gate and build seed chunks (shared by both seeders).
    `dep_bridge` is the per-dep relevance signal — the span-bridge sentence score
    for definitions, the parent ability's relevance for referenced rules — and a dep
    is seeded only when it clears `gate`. Records sourcing parents (by content_key)
    + score so rank_seeded_below_parents can ride each dep just below its parent.
    Strongest first; bounded by DEP_BOOST_MAX_PER_QUERY."""
    out = []
    for d in sorted(dep_parents, key=lambda k: dep_bridge.get(k, -1.0), reverse=True):
        if dep_bridge.get(d, -1.0) < gate:
            continue
        payload = seed.get(d)
        if payload is None or payload["metadata"].get("category") not in allowed:
            continue
        cand = Chunk(text=payload["text"], meta=payload["metadata"],
                     prov=Provenance.DEP_SEED, cosine=0.0,
                     parent_keys=tuple(sorted(dep_parents[d])),
                     dep_bridge=round(dep_bridge[d], 3))
        if content_key(cand) in present:                    # already retrieved
            continue
        present.add(content_key(cand))
        out.append(cand)
        if len(out) >= config.DEP_BOOST_MAX_PER_QUERY:      # bound blast radius
            break
    return out


def seed_definitions(query: str, pool: list, edition: str, mission_pack_mode: bool) -> list:
    """Seed child-definition chunks a surfaced parent RULE references but doesn't
    contain (charge_phase → engagement_range, unit_coherency), from the ratified dep
    graph — SPAN-BRIDGE gated so only deps the *question* needs enter the pool.

    The span bridge: a dep reads as irrelevant to the query by direct similarity, so
    we never compare them. For each active parent we find the sentence(s) that NAME
    the dep and score the QUERY against them; the dep is seeded only when that bridge
    score ≥ SPAN_GATE_MIN — i.e. the question is about the part of the rule that
    invokes the dep. Depth-1; mission-pack filtered (HARD INVARIANT). See §8d."""
    graph = get_dep_graph(edition)
    if not graph:
        return []
    bc_to_stem, seed = get_dep_index(edition)
    allowed = _dep_boost_cats(edition, mission_pack_mode)
    present = {content_key(c) for c in pool}
    qv = indices.embed_query(query)            # encode-once (A3), shared by both seeders

    dep_parents: dict = {}   # dep_stem -> set(parent content_key)
    dep_bridge:  dict = {}   # dep_stem -> best cos(query, naming-sentence)
    for c in pool:
        if c["metadata"].get("category") not in allowed:
            continue
        if boosted_score(c, edition, mission_pack_mode) < config.SIMILARITY_THRESHOLD:
            continue
        pstem = bc_to_stem.get(c["metadata"].get("breadcrumb"))
        if pstem not in graph:
            continue
        sents, embs = _chunk_sentence_embeddings(c)
        for d in graph[pstem]:
            dep_parents.setdefault(d, set()).add(content_key(c))
            pat    = _dep_surface_re(d)
            naming = [e for s, e in zip(sents, embs) if pat.search(s)]
            if naming:
                dep_bridge[d] = max(dep_bridge.get(d, -1.0), max(_cos(qv, e) for e in naming))
    return _gate_and_build(dep_parents, dep_bridge, seed, allowed, present, config.SPAN_GATE_MIN)


def seed_referenced_rules(query: str, pool: list, edition: str, mission_pack_mode: bool) -> list:
    """Seed core/Leviathan rule chunks that surfaced UNIT/ABILITY chunks reference BY
    NAME, as the rules context needed to understand those abilities (and unit-vs-unit
    interactions). Parent = a surfaced non-rule chunk; dep = the USR it names.

    Gate depends on the PARENT TYPE (both require parent rel ≥ REFERENCED_PARENT_MIN):
      • ABILITY parent → parent-relevance IS the signal (a unit Q isn't phrased like the
        mechanic, so the rule surfaces because the ability granting it is relevant —
        "Obyron Fights First" bridges only 0.176 yet must seed Fights First). KEPT.
      • non-ability parent (Datasheet stat-block / Datasheet_Section / wargear) →
        SPAN-BRIDGE gated (query vs the naming sentence). Needed because the cross-
        encoder SATURATES (~1.0) on every chunk of a NAMED unit, so a unit's Datasheet
        passes the relevance pre-filter and would otherwise seed every weapon keyword in
        its wargear table ([SUSTAINED HITS], [DEADLY DEMISE]) on an unrelated question
        ("can it charge"). A wargear-table row scores ~0.1 against such a query → dropped.
    Capped below the parent by rank_seeded_below_parents. See §8e."""
    index = get_rule_name_index(edition)
    if not index:
        return []
    _, seed  = get_dep_index(edition)
    allowed  = _dep_boost_cats(edition, mission_pack_mode)
    mp_cat   = config.get_edition(edition)["mission_pack"]["category"]
    present  = {content_key(c) for c in pool}
    qv       = indices.embed_query(query)      # encode-once (A3), shared by both seeders

    dep_parents: dict = {}   # rule_stem -> set(parent content_key)
    dep_bridge:  dict = {}   # rule_stem -> gate score (parent rel for abilities, else span)
    for c in pool:
        cat = c["metadata"].get("category", "")
        if cat in ("Core_Rules", mp_cat):                 # parents here are non-rule only
            continue
        rel = boosted_score(c, edition, mission_pack_mode)
        if rel < config.REFERENCED_PARENT_MIN:            # only strongly-relevant parents
            continue
        matched = [(rx, rstem) for rx, rstem in index if rx.search(c["text"])]
        if not matched:
            continue
        if cat == "Ability":
            # ability parent: relevance of the ability is the gate (original §8e path)
            for _, rstem in matched:
                dep_parents.setdefault(rstem, set()).add(content_key(c))
                dep_bridge[rstem] = max(dep_bridge.get(rstem, -1.0), rel)
        else:
            # stat-block / wargear parent: require the QUERY to be about the naming
            # sentence, else a saturated Datasheet seeds its whole wargear keyword set.
            sents, embs = _chunk_sentence_embeddings(c)
            for rx, rstem in matched:
                dep_parents.setdefault(rstem, set()).add(content_key(c))
                naming = [e for s, e in zip(sents, embs) if rx.search(s)]
                if naming:
                    dep_bridge[rstem] = max(dep_bridge.get(rstem, -1.0),
                                            max(_cos(qv, e) for e in naming))
    return _gate_and_build(dep_parents, dep_bridge, seed, allowed, present,
                           config.SPAN_GATE_MIN)


def rank_seeded_below_parents(chunks: list, edition: str, mission_pack_mode: bool) -> None:
    """Override each seeded dep's effective score so it rides JUST BELOW the weakest
    parent that sourced it — the parent-cap, on the reranked parent score. The
    cross-encoder scores a seeded dep ~0 (it judges a *dependency*/referenced rule as
    irrelevant), so we replace that with a parent-derived score. Parents are matched
    by content_key (works for rule parents AND unit/ability parents). Mutates in
    place; call AFTER rerank_pools and BEFORE assemble_context. See §8d/§8e.

    B9: stamps `rank_override` (the effective score boosted_score returns directly),
    instead of the old back-out math that set rerank = eff − authority so the tiebreak
    would re-add to exactly eff. Cleaner, and the dep's raw `rerank` now stays at its
    true cross-encoder value (surfaced as the parenthetical in the source expander)."""
    score_by_key = {content_key(c): boosted_score(c, edition, mission_pack_mode)
                    for c in chunks if not c.get("dep_seed")}
    deps = [c for c in chunks if c.get("dep_seed")]
    # strongest-bridge dep first so the EPS ladder keeps a stable, sensible order
    for i, dep in enumerate(sorted(deps, key=lambda c: c.get("dep_bridge", 0), reverse=True)):
        ps = [score_by_key[k] for k in dep.get("dep_parent_keys", []) if k in score_by_key]
        if not ps:
            continue
        eff = min(ps) - config.RULES_BOOST_DEP - i * config.DEP_SCORE_EPS
        dep["rank_override"] = round(eff, 4)   # boosted_score(dep) == eff (below weakest parent)


def _reserve_unit_chunks(unit_chunks: list, reserved_keys: set, rank) -> list:
    """Per-unit reservation: group the named-unit slice by unit and keep each unit's
    best chunk (the query NAMING the unit is the relevance signal), plus its 2nd chunk
    unless that 2nd is legitimately irrelevant. Per-unit (not global) so one named unit
    can't sweep the slots from another in a multi-unit question.

    SELECTION SIGNAL = rerank (segment-maxpool). The cross-encoder SATURATES (~1.0) on
    every chunk of a named unit when the query names that unit prominently ("can my
    Venerable Land Raider charge" → Composition, Transport, Assault Ramp ALL ~0.9996).
    The OLD fix added the propagated whole-query cosine to break that tie toward the
    answer-bearing ability. But once RERANK_SEGMENT_MAXPOOL shipped, the reranker scores
    each chunk against the query's individual CLAUSES and keeps the max, so the operative
    section is lifted on rerank alone (Assault Ramp, Grot Riggers both verified). The
    cosine term then became a LIABILITY on compound questions: cosine is a whole-query
    signal that favors the DOMINANT clause's stat-block sections (which surfaced
    semantically) over a secondary clause's ability whose chunk never surfaced (cosine 0,
    e.g. Trukk's "Grot Riggers" behind "transport capacity"), starving the 2nd clause and
    sweeping both per-unit slots with the dominant topic. Ranking on the segment-aware
    rerank alone covers BOTH clauses (eval_30q 41/41, eval_retrieval 23/23, Assault Ramp
    still reserved).

    "Legitimately irrelevant 2nd" is judged RELATIVELY (within UNIT_SECOND_RATIO of the
    unit's own best) — BUT only when the best chunk's score is itself meaningful
    (≥ UNIT_SECOND_FLOOR). When the signal rates a unit's whole chunk set near-zero
    (a generic ability question — Snikrot's chunks 0.027/0.004), it cannot distinguish
    them, so the ratio would amplify pure noise into a spurious "6× worse" drop and lose
    a genuinely useful chunk (Snikrot's datasheet, which proves he HAS Infiltrators).
    Below the floor we keep both — same reasoning that sets the absolute gate to 0."""
    def sel(c):                                               # segment-aware rerank
        return rank(c)
    by_unit = defaultdict(list)
    for c in deduplicate_chunks(unit_chunks or []):
        if content_key(c) not in reserved_keys:
            by_unit[c["metadata"].get("unit_name", "")].append(c)
    keep = []
    for chunks in by_unit.values():
        chunks.sort(key=sel, reverse=True)
        chosen = chunks[:1]                                   # best chunk: always
        top    = sel(chosen[0])
        for c in chunks[1:config.UNIT_CHUNKS_PER_UNIT]:       # up to the per-unit cap
            indistinct = top < config.UNIT_SECOND_FLOOR       # signal indifferent → keep
            if indistinct or sel(c) >= config.UNIT_SECOND_RATIO * top:
                chosen.append(c)
        keep.extend(chosen)
    return keep

def _tier_unit_chunks(units_keep: list, rank) -> tuple[list, list]:
    """Split the per-unit reservation into (firsts, seconds): each named unit's single
    best chunk goes to `firsts`, every other reserved chunk of that unit to `seconds`.
    Lets assemble_context protect one chunk per unit ahead of any unit's extras, so the
    token budget can't drop a unit's only representation while keeping another's 2nd."""
    by_unit: dict = {}
    for c in units_keep:
        by_unit.setdefault(c["metadata"].get("unit_name"), []).append(c)
    firsts, seconds = [], []
    for chunks in by_unit.values():
        ranked = sorted(chunks, key=rank, reverse=True)
        firsts.append(ranked[0])
        seconds.extend(ranked[1:])
    return firsts, seconds

def assemble_context(main_chunks: list, rules_chunks: list, edition: str,
                     mission_pack_mode: bool, unit_chunks: list | None = None) -> list:
    """
    Merge the main semantic results with the two guaranteed slices, governed by the
    TOKEN budget rather than a hard chunk count:
      • reserve up to TOP_K_RULES slots for the best rules chunks,
      • reserve up to UNIT_CHUNKS_PER_UNIT chunks PER named unit (2nd gated relatively),
      • fill the remainder up to the TOP_K *target* with the best main chunks above
        REST_GATE.
    Reservations may push the total past TOP_K (a multi-unit question needs the room);
    the hard ceiling is RULES_CONTEXT_TOKEN_BUDGET, applied later by
    format_rules_context. Output is ordered RESERVED-FIRST (each group by score) so the
    guaranteed rules/units survive budget truncation; discretionary fill packs last and
    is dropped first. Simple single-topic queries still come out at ~TOP_K — lean on
    purpose for multi-turn TPM headroom.
    """
    rank = lambda c: boosted_score(c, edition, mission_pack_mode)

    rules_sorted    = sorted(deduplicate_chunks(rules_chunks), key=rank, reverse=True)
    guaranteed      = rules_sorted[:config.TOP_K_RULES]
    reserved_keys   = {content_key(c) for c in guaranteed}

    # Propagate the semantic COSINE of any unit-slice chunk that ALSO surfaced in the
    # main pool onto its slice copy (the metadata fetch leaves slice chunks at 0.0), so a
    # unit chunk that the cross-encoder rates near-zero can still clear boosted_score via
    # its RERANK_COSINE_FLOOR floor. (This used to also break _reserve_unit_chunks' slot
    # ties, but that now ranks on the segment-aware rerank alone — see its docstring — so
    # this only feeds the cosine floor.) No-op for sections that never surfaced (stay 0.0).
    cos_by_key: dict = {}
    for c in main_chunks:
        s = c.get("similarity")
        if s is not None:
            k = content_key(c)
            cos_by_key[k] = max(cos_by_key.get(k, 0.0), s)
    for c in (unit_chunks or []):
        k = content_key(c)
        if k in cos_by_key:
            c["similarity"] = max(c.get("similarity") or 0.0, cos_by_key[k])

    units_keep    = _reserve_unit_chunks(unit_chunks, reserved_keys, rank)
    reserved_keys |= {content_key(c) for c in units_keep}

    # A named unit's OTHER sections all rerank ~1.0 (saturated) and would sweep the
    # discretionary `rest` slots with stat-block fluff (Transport, Composition) over
    # genuinely different content. The unit is already represented by its reserved
    # slice — which now reserves the RIGHT section (cosine-aware, above) — so bound the
    # unit's TOTAL footprint by dropping its extra sections from the fill.
    capped_units = {c["metadata"].get("unit_name") for c in units_keep
                    if c["metadata"].get("unit_name")}

    # Tier the reservation so a multi-unit question can't let one unit box another
    # out: every named unit's BEST chunk (+ the guaranteed rules) rides the protected
    # front tier, and each unit's SECOND chunk rides a back tier. format_rules_context
    # fills in this order and drops whole chunks past the budget, so the sacrifice is a
    # unit's secondary detail (Abaddon's Dark Pacts) — never another unit's only chunk
    # (Aberrants' Feel No Pain, which the cross-encoder rates ~0 and would otherwise
    # sort dead last). Within each tier, order by rank.
    # Order: each named unit's BEST chunk FIRST (the unit slice exists because these
    # chunks rank ~0 under the cross-encoder, so ranking them against the rules would
    # bury them), then the guaranteed rules, then each unit's SECOND chunk. The budget
    # therefore sacrifices a unit's secondary detail / a low rule before any named
    # unit's only representation — no unit boxes another out of context.
    unit_firsts, unit_seconds = _tier_unit_chunks(units_keep, rank)
    reserved   = (sorted(unit_firsts,   key=rank, reverse=True)
                  + sorted(guaranteed,    key=rank, reverse=True)
                  + sorted(unit_seconds,  key=rank, reverse=True))
    rest_slots = max(0, config.TOP_K - len(reserved))         # target TOP_K, not a cap
    main_sorted = sorted(deduplicate_chunks(main_chunks), key=rank, reverse=True)
    rest = [c for c in main_sorted
            if content_key(c) not in reserved_keys
            and rank(c) >= config.REST_GATE
            and c["metadata"].get("unit_name") not in capped_units][:rest_slots]

    # Reserved-first so the 2800-token budget (format_rules_context) truncates the
    # discretionary fill before any guaranteed rule/unit chunk.
    result = reserved + rest
    # Stamp the EFFECTIVE ordering score (cosine-floored rerank + authority tiebreak)
    # so the source expander can surface the number that actually drove the order —
    # within-tier this is the sort key; across tiers the layout is reserved-first.
    for c in result:
        c["rank_score"] = round(rank(c), 4)
    return result


# ── Sequence neighbour injection (Layer 2 Track C) ────────────────────────────

def fetch_sequence_neighbors(group: str, seq: int, edition: str) -> list[dict]:
    """
    Fetch the seq±1 siblings of a curated rule sequence (config.RULES_SEQUENCES).
    These ordered steps live in separate rule-block files and rarely all match a
    query semantically, so when one step is retrieved we pull its neighbors to
    surface the full sequence (e.g. Saving Throw -> Wound Roll + Inflict Damage).
    """
    collection = get_collection(edition)
    try:
        results = collection.get(
            where={"$and": [
                {"section_group": group},
                {"seq": {"$in": [seq - 1, seq + 1]}},
            ]},
            include=["documents", "metadatas"],
        )
        # cosine=None (unscored); prov flips to SEQ_NEIGHBOR when inject_sequence_neighbors
        # actually places it after the sibling that pulled it in.
        return [
            Chunk(text=doc, meta=meta, prov=Provenance.DENSE, cosine=None)
            for doc, meta in zip(results["documents"], results["metadatas"])
        ]
    except Exception:
        return []

def inject_sequence_neighbors(chunks: list, edition: str) -> list:
    """
    For each retrieved chunk that belongs to a curated sequence, insert its
    seq-neighbors right after it (deduped). The token allocator in
    format_rules_context caps the total, so this never busts the budget.
    """
    if not chunks:
        return chunks
    existing = {content_key(c) for c in chunks}
    result   = []
    for chunk in chunks:
        result.append(chunk)
        meta = chunk["metadata"]
        group, seq = meta.get("section_group"), meta.get("seq")
        if not group or seq is None:
            continue
        for nb in fetch_sequence_neighbors(group, seq, edition):
            key = content_key(nb)
            if key not in existing:
                existing.add(key)
                # Sort/rank just below the sibling that pulled it in.
                nb["similarity"] = chunk["similarity"]
                # Mark provenance so the source expander can list this neighbor
                # directly after the parent that pulled it in (and label it).
                nb["seq_neighbor"] = True
                nb["dep_parent_keys"] = [content_key(chunk)]
                nb["rank_score"] = chunk.get("rank_score")   # rides with its parent
                result.append(nb)
    return result

# ── Dependency-aware definition boosting (Layer 2 Track E) ────────────────────

def _dep_stem(cid: str) -> str:
    """Chunk id -> dep-graph stem (the on-disk rule-block stem)."""
    return cid[len("core_rules_"):] if cid.startswith("core_rules_") else cid

def _dep_boost_cats(edition: str, mission_pack_mode: bool) -> set:
    """Categories eligible to source/seed a dependency boost — Core Rules always,
    the mission-pack category ONLY when the toggle is on. Mirrors rules_where, so
    the mission-pack HARD INVARIANT holds: toggle off ⇒ no mission-pack dep is ever
    seeded, and a core parent can never seed a mission-pack chunk."""
    mp = config.get_edition(edition)["mission_pack"]["category"]
    return {"Core_Rules"} | ({mp} if mission_pack_mode else set())

@st.cache_resource
def get_dep_graph(edition: str) -> dict:
    """Load the ratified dependency-graph artifact: stem -> [dep_stem, ...].
    Absent file ⇒ {} ⇒ the feature no-ops. Keys starting with '_' are metadata."""
    path = ROOT / config.RULES_DEP_GRAPH_PATH.format(edition=edition)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {k: v for k, v in raw.items() if not k.startswith("_")}

@st.cache_resource
def get_dep_index(edition: str):
    """Built once per edition from the rule-chunk universe:
      bc_to_stem: breadcrumb -> stem   (identify a surfaced chunk's stem)
      seed:       stem -> chunk payload (seed a missing dep into the pool by stem)
    Restricted to rule categories (Core_Rules + mission-pack) so only rules can be
    sourced or seeded."""
    col  = get_collection(edition)
    data = col.get(include=["documents", "metadatas"])
    mp   = config.get_edition(edition)["mission_pack"]["category"]
    bc_to_stem, seed = {}, {}
    for cid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        if meta.get("category") not in ("Core_Rules", mp):
            continue
        s = _dep_stem(cid)
        seed[s] = {"text": doc, "metadata": meta}
        bc = meta.get("breadcrumb")
        if bc and bc not in bc_to_stem:
            bc_to_stem[bc] = s
    return bc_to_stem, seed


# ── Prompt builder / serving / LLM call ───────────────────────────────────────
# Moved to serving.py (Phase 5). Re-exported into this namespace so existing call
# sites (and the evals that drive app.format_rules_context) keep working unchanged.
from serving import (                                                  # noqa: E402
    get_llm_client, system_prompt, mission_pack_context, estimate_tokens,
    format_rules_context, build_messages, call_llm, call_llm_reduced,
)

# ── Session state init ────────────────────────────────────────────────────────

def init_session():
    # Fail loudly at boot if a retrieval knob was nudged into an inconsistent
    # relationship (C14), before any query runs on a silently-degraded config.
    config.assert_invariants()
    defaults = {
        "messages":              [],
        "last_chunks":           [],
        "viewing_conv_id":       None,
        "selected_faction":      "All Factions",
        "current_conv_id":       None,
        "current_user":          get_current_user(),
        "edition":               config.default_edition(),
        "mission_pack_mode":     True,
        "refined_query":         None,
        "pending_clarification": None,
        "unit_resolution":       None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Warm the Layer-3 models (cross-encoder + span-bridge embedder) once at startup
    # so the first query doesn't pay the ~3.3 s cold load. @st.cache_resource means
    # this runs only on the first session; failures degrade gracefully (cosine path).
    try:
        get_reranker()
        get_embedder()
    except Exception:
        pass

# ── Per-edition theming ───────────────────────────────────────────────────────

def apply_edition_theme(edition: str):
    """Inject a per-edition accent color (sidebar border, title, primary buttons).
    Streamlit's static [theme] in config.toml cannot switch at runtime, so the
    edition differentiator is this CSS injection keyed on the active edition."""
    color = config.get_edition(edition)["accent_color"]
    st.markdown(f"""
        <style>
          :root {{ --edition-accent: {color}; }}
          [data-testid="stSidebar"] {{ border-right: 4px solid {color}; }}
          h1, .stCaption {{ color: {color}; }}
          .stButton button[kind="primary"] {{ background: {color}; }}
          /* st.code blocks force a horizontal scrollbar by default; wrap them so the
             source chunks read top-to-bottom while KEEPING the markdown syntax
             highlighting (the ** / # markers stay styled). */
          [data-testid="stCode"] pre, [data-testid="stCode"] code {{
            white-space: pre-wrap !important;
            overflow-wrap: anywhere;
            word-break: break-word;
          }}
        </style>
    """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.title("⚖️ The Judge")

        # ── Edition selector (resolved first — everything below is edition-scoped) ──
        codes   = config.active_editions()
        labels  = [config.get_edition(c)["label"] for c in codes]
        current = st.session_state.edition if st.session_state.edition in codes else codes[0]

        if len(codes) > 1:
            chosen_label = st.selectbox(
                "Edition",
                options=labels,
                index=codes.index(current),
                help="Switches rules data, retrieval, prompt, and history to the selected edition."
            )
            chosen = codes[labels.index(chosen_label)]
            # Detect the switch BEFORE reassigning, then reset the active chat so
            # contexts from different editions never mix.
            if chosen != st.session_state.edition:
                for key in ["messages", "last_chunks", "viewing_conv_id", "current_conv_id",
                            "refined_query", "pending_clarification", "unit_resolution"]:
                    st.session_state[key] = [] if key in ("messages", "last_chunks") else None
                st.session_state.edition = chosen
                st.rerun()
        else:
            # Only one active edition — render no dead selector. When 11th
            # activates, the selector appears automatically.
            st.session_state.edition = current

        edition = st.session_state.edition
        ed      = config.get_edition(edition)

        apply_edition_theme(edition)
        st.caption(f"Warhammer 40K · {ed['label']} Rules")
        st.caption(f"Logged in as **{st.session_state.current_user}**")

        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            for key in ["messages", "last_chunks", "viewing_conv_id", "current_conv_id",
                        "refined_query", "pending_clarification", "unit_resolution"]:
                st.session_state[key] = [] if key in ("messages", "last_chunks") else None
            st.rerun()

        st.divider()

        _, factions     = build_faction_keyword_map(edition)
        faction_options = ["All Factions"] + sorted(factions.values())
        selected = st.selectbox(
            "Faction Filter",
            options=faction_options,
            index=faction_options.index(st.session_state.selected_faction)
                  if st.session_state.selected_faction in faction_options else 0,
            help="Pre-filters retrieval to a specific faction for this session."
        )
        st.session_state.selected_faction = selected

        st.session_state.mission_pack_mode = st.toggle(
            ed["mission_pack"]["toggle_label"],
            value=st.session_state.mission_pack_mode,
            help="When on, mission-pack rules take precedence over Core Rules and are always included in retrieval."
        )

        st.divider()

        st.subheader("Past Conversations")
        archived = load_archived_conversations(st.session_state.current_user, edition)
        if not archived:
            st.caption("No archived conversations yet.")
        else:
            for conv_id, title, created in archived:
                created_dt = datetime.fromisoformat(created).strftime("%b %d %H:%M")
                if st.button(f"{created_dt} — {title}", key=f"conv_{conv_id}", use_container_width=True):
                    st.session_state.viewing_conv_id = conv_id
                    st.rerun()

# ── Main chat UI ──────────────────────────────────────────────────────────────

def render_clarification_buttons(state: dict) -> None:
    """Render the current clarification question + its choice buttons INSIDE the
    last assistant bubble. A click advances the queue and reruns. Rendering in-bubble
    (not floating at page bottom) is what keeps the buttons from lingering greyed
    behind the conversation after a pick."""
    nxt = next_clarification(state)
    if nxt is None:
        return
    query = state["query"]
    active = state["units"][0]                 # the slot this question is about
    if nxt[0] == "faction":
        _, ref, choices = nxt
        st.markdown(f"Which **army** fields this unit?")
    else:
        _, ref, army, choices = nxt
        st.markdown(f"Which **{ref}** — _{army}_?")
    st.markdown("> " + highlight_ref(query, ref, active.get("start"), active.get("end")))
    # Slot id keys the buttons so the SAME chassis prompted twice doesn't collide.
    slot_id = active.get("slot_id", 0)
    # Fixed 3-wide grid + full-width buttons → uniform sizing (no awkward gaps).
    for row_start in range(0, len(choices), 3):
        row = choices[row_start:row_start + 3]
        cols = st.columns(3)
        for col, choice in zip(cols, row):
            if col.button(choice, key=f"clarify_{nxt[0]}_{slot_id}_{ref}_{choice}",
                          use_container_width=True):
                st.session_state.pending_clarification = apply_clarification(state, choice)
                st.rerun()

def render_chat():
    user    = st.session_state.current_user
    edition = st.session_state.edition
    ed      = config.get_edition(edition)

    # ── Archived conversation viewer (read-only) ──────────────────────────────
    if st.session_state.viewing_conv_id is not None:
        messages = load_conversation_messages(st.session_state.viewing_conv_id, user)
        st.info("📜 Viewing archived conversation — read only.")
        if st.button("← Back to current chat"):
            st.session_state.viewing_conv_id = None
            st.rerun()
        for msg in messages:
            if not msg.get("content", "").strip():
                continue
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        return

    # ── Active chat ───────────────────────────────────────────────────────────
    st.title(f"⚖️ The Judge · {ed['label']}")
    st.caption(f"Ask any Warhammer 40,000 {ed['label']} rules question.")

    # pending_clarification is the two-stage queue {query, units, resolved}; while a
    # question is pending we render its buttons INSIDE the last assistant bubble
    # (render_clarification_buttons) rather than floating them at page bottom.
    pending      = st.session_state.pending_clarification
    asking       = bool(pending) and next_clarification(pending) is not None
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            is_last = i == len(st.session_state.messages) - 1
            if msg["role"] == "assistant" and is_last:
                if asking:
                    render_clarification_buttons(pending)
                elif st.session_state.last_chunks and not pending:
                    render_source_expander(st.session_state.last_chunks)

    # A question is on screen (in-bubble) — wait for the click; the rerun it triggers
    # re-enters here. Don't render the chat input or run the pipeline yet.
    if asking:
        return

    # ── Queue drained → hand off to the pipeline once ─────────────────────────
    # refined_query suppresses re-prompting; unit_resolution pins each unit's
    # (datasheet, army). The query is rewritten INLINE so the resolved unit replaces
    # the generic chassis word where it sits (mirrors-safe vs a trailing addendum).
    if pending:
        _state = pending
        st.session_state.refined_query   = apply_resolution_to_query(
            _state["query"], _state["resolved"])
        st.session_state.unit_resolution = _state["resolved"]
        st.session_state.pending_clarification = None

    # ── Determine active input ────────────────────────────────────────────────
    active_input = None
    if st.session_state.refined_query:
        active_input = st.session_state.refined_query
        st.session_state.refined_query = None

    user_input = st.chat_input("Ask a rules question...")
    if user_input:
        active_input = user_input

    if not active_input:
        return

    with st.chat_message("user"):
        st.markdown(active_input)

    # A refined query already carries its faction resolution (set when the
    # clarification queue drained); a fresh query is eligible for disambiguation.
    is_refined = (active_input != user_input)
    resolution = st.session_state.unit_resolution or {}
    st.session_state.unit_resolution = None

    # ── Disambiguation FIRST (deterministic, metadata-driven) ─────────────────
    # If a fresh query names any multi-faction unit with no faction pinned, ask —
    # sequentially, one unit per round — BEFORE the heavy retrieve/seed/rerank, so
    # that work runs only once the faction(s) are known. Replaces the old post-
    # retrieval detect_ambiguity gate, which could not see a unit that failed to
    # surface semantically.
    if not is_refined:
        clarify = build_clarification_queue(
            active_input, edition, st.session_state.selected_faction)
        if clarify and clarify["units"]:
            # At least one unit still needs a question — prompt and wait.
            st.session_state.pending_clarification = clarify
            st.session_state.messages.append({"role": "user", "content": active_input})
            st.session_state.messages.append({"role": "assistant",
                "content": "⚖️ **Clarification needed** — more than one option fields "
                           "this unit. Which did you mean?"})
            st.session_state.last_chunks = []
            st.session_state.current_conv_id = upsert_conversation(
                st.session_state.messages, user, edition, st.session_state.current_conv_id)
            st.rerun()
            return
        elif clarify and clarify["resolved"]:
            # Everything the query named auto-resolved (e.g. a pinned faction fields
            # exactly one variant) — no question needed; pin the slice and proceed.
            resolution = clarify["resolved"]

    # ── Retrieval engine ──────────────────────────────────────────────────────
    # The whole query→context pipeline (route → retrieve dense/unit/rules → scope →
    # seed → rerank → parent-cap → assemble → sequence-neighbors) now lives in
    # retrieval.build_context as one declarative PIPELINE of pure stages. render_chat
    # just hands it the active query + the session-shaped state and renders the result;
    # the stage ORDER (and its hard sequencing constraints) is enforced there by the
    # list, not by comment. See spec/retrieval-pipeline-refresh.md §4.
    chunks = retrieval.build_context(
        active_input, edition=edition,
        mission_pack_mode=st.session_state.mission_pack_mode,
        selected_faction=st.session_state.selected_faction,
        resolution=resolution,
    )

    # ── No ambiguity — call LLM ───────────────────────────────────────────────
    with st.chat_message("assistant"):
        with st.spinner("Adjudicating..."):
            answer = call_llm(
                st.session_state.messages, chunks, active_input, edition,
                mission_pack_mode=st.session_state.mission_pack_mode,
            )
        st.markdown(answer)
        if chunks:
            render_source_expander(chunks)

    st.session_state.messages.append({"role": "user",      "content": active_input})
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_chunks = chunks
    st.session_state.current_conv_id = upsert_conversation(
        st.session_state.messages, user, edition, st.session_state.current_conv_id)
    st.rerun()

# ── Source expander ───────────────────────────────────────────────────────────

def _is_child(c: Chunk) -> bool:
    """A chunk pulled in BY a parent (so it should display right after it): a seeded
    definition/referenced rule or an injected sequence neighbor. Switches on the typed
    `prov` (C12) instead of probing a bag of optional boolean keys."""
    return c.prov in (Provenance.DEP_SEED, Provenance.SEQ_NEIGHBOR)


def _source_label(c: Chunk) -> str:
    """How this chunk entered the candidate pool: the cosine when it was a semantic
    hit, otherwise the provenance that pulled it in. Reads the typed `prov` (C12); the
    cosine=None vs 0.0 distinction (C13) is now explicit, not an overloaded sentinel."""
    if c.prov is Provenance.UNIT_SLICE:   return "unit slice (named unit)"
    if c.prov is Provenance.NAMED_RULE:   return "named army/detachment rule slice"
    if c.prov is Provenance.DEP_SEED:     return "dependency seed (child)"
    if c.prov is Provenance.SEQ_NEIGHBOR: return "sequence neighbor (child)"
    if c.prov is Provenance.LEXICAL:      return f"lexical `{c.cosine}`"
    if c.cosine is None:                  return "metadata fetch"
    if c.cosine == 0.0:                   return "metadata fetch (cosine `0.0`)"
    return f"cosine `{c.cosine}`"


def _rerank_label(c: dict) -> str:
    """The EFFECTIVE ranking score that ordered this chunk — boosted_score, i.e.
    max(cross-encoder rerank, W·cosine) + authority tiebreak (config.RERANK_COSINE_FLOOR).
    This is the number the chunk was actually sorted by. When it diverges from the raw
    cross-encoder value (the reranker tanked a rule to ~0 and cosine set the floor) the
    raw value is shown in parens so the divergence stays visible."""
    rs  = c.rank_score
    rer = c.rerank
    if rs is None:                                          # defensive: never assembled
        if rer is None:
            return "not reranked" + (" (sequence neighbor)"
                                     if c.prov is Provenance.SEQ_NEIGHBOR else "")
        return f"`{round(rer, 3)}`"
    if rer is not None and abs(rer - rs) > 0.01:           # cosine floor lifted it
        return f"`{rs}`  (cross-encoder `{round(rer, 3)}`)"
    return f"`{rs}`"


def render_source_expander(chunks: list):
    # Listed in the SAME order the chunks are sent to the LLM (assemble_context →
    # inject_sequence_neighbors), so the [i] indices here match the [i] labels in the
    # rules context the model receives. Children (dep_seed / sequence neighbors) are
    # marked ↳ but kept in their context position, not regrouped under their parent.
    with st.expander("📖 View Source Chunks", expanded=False):
        for i, chunk in enumerate(chunks, 1):
            meta   = chunk["metadata"]
            indent = "↳ " if _is_child(chunk) else ""       # mark children as nested
            # Join only the populated fields with " · " — core-rule chunks carry no
            # army (so a fixed 3-slot template printed "Name · · Core_Rules"), and
            # name falls back to category, so dedup drops the repeated category.
            name   = meta.get("unit_name") or meta.get("category") or "Rule"
            header = " · ".join(dict.fromkeys(
                f for f in (name, meta.get("army"), meta.get("category")) if f))
            st.markdown(f"**[{i}]** {indent}{header}")
            st.markdown(f"Source: {_source_label(chunk)}  ·  Rerank: {_rerank_label(chunk)}")
            st.code(chunk["text"][:600] + ("..." if len(chunk["text"]) > 600 else ""),
                    language="markdown")
            if i < len(chunks):
                st.divider()

# ── Entry point ───────────────────────────────────────────────────────────────

init_session()
render_sidebar()
render_chat()
"""
indices.py — process-wide cached indices for the retrieval engine.
==================================================================
Every per-query Chroma scan and redundant embed the audit flagged (A1/A2/A3)
moves behind `@st.cache_resource` here. The collection is static between ingests
(an ingest restarts the app), so these caches are valid for the whole process
lifetime.

Import-safety: this module imports `app` LAZILY inside each builder, so there is
no import-time cycle (app.py imports indices at top; indices touches app only at
call time, by which point both modules are fully loaded). `@st.cache_resource`
degrades to a plain cache when there is no Streamlit script context, so the
builders are valid for the headless evals too.

Builders (all keyed by `edition`, built once):
  • named_rule_index   — replaces the per-query full scan + regex in
                         retrieve_named_rules (A1)
  • unit_army_map      — replaces every uncached unit_armies round-trip (A2)
  • variant_signature_map — replaces the per-call .get in _variant_signature (A2)
  • embed_query        — encode the query once per turn, shared by both seeders (A3)
"""
from functools import lru_cache

import streamlit as st

import config


@st.cache_resource
def named_rule_index(edition: str) -> list[tuple]:
    """[(name, detach, doc, meta), ...] for every Army_Rule / Detachment_Rule, with
    the rule name and detachment name PRE-PARSED and lowercased. Built once from a
    single col.get over the two categories (mirrors get_dep_index); the per-query
    retrieve_named_rules then collapses to substring tests over this list instead of
    a Chroma round-trip + regex parse on ~343 docs every query.

    Order is preserved from col.get so the produced hit order is identical to the
    pre-cache scan."""
    import app
    coll = app.get_collection(edition)
    try:
        got = coll.get(
            where={"$or": [{"category": "Army_Rule"}, {"category": "Detachment_Rule"}]},
            include=["documents", "metadatas"],
        )
    except Exception:
        return []
    index = []
    for doc, meta in zip(got.get("documents", []), got.get("metadatas", [])):
        lines    = doc.splitlines()
        m_name   = app._RULE_TITLE_RE.match(lines[0]) if lines else None
        name     = m_name.group(1).strip().lower() if m_name else ""
        m_detach = next((app._RULE_DETACH_RE.search(l) for l in lines[:3]
                         if app._RULE_DETACH_RE.search(l)), None)
        detach   = m_detach.group(1).strip().lower() if m_detach else ""
        index.append((name, detach, doc, meta))
    return index


@st.cache_resource
def unit_army_map(edition: str) -> dict:
    """{unit_name: [armies]} — the distinct armies each datasheet name appears under
    (the faction-ambiguity axis). Built from ONE full-collection metadata scan, so a
    fan-out over a chassis family does zero per-name Chroma round-trips. Identical to
    calling unit_armies() per name (sorted distinct non-empty armies)."""
    import app
    from collections import defaultdict
    coll = app.get_collection(edition)
    try:
        data = coll.get(include=["metadatas"])
    except Exception:
        return {}
    by_unit: dict = defaultdict(set)
    for meta in data["metadatas"]:
        unit = meta.get("unit_name")
        army = meta.get("army")
        if unit and army:
            by_unit[unit].add(army)
    return {u: sorted(a) for u, a in by_unit.items()}


@st.cache_resource
def variant_signature_map(edition: str) -> dict:
    """{(unit_name, army): rules-signature} for the variant-dedup in chassis_family.
    Built from one full col.get; the signature is the md5 over the sorted content_keys
    of that (unit, army)'s UNIT_SLICE_CATEGORIES chunks — byte-identical to the old
    per-call _variant_signature. Missing keys ⇒ the pair is absent here and the caller
    degrades to name-only dedup (same as the old except-branch)."""
    import app
    import hashlib
    from collections import defaultdict
    coll = app.get_collection(edition)
    try:
        data = coll.get(include=["documents", "metadatas"])
    except Exception:
        return {}
    slice_cats = set(app.UNIT_SLICE_CATEGORIES)
    docs_by_pair: dict = defaultdict(list)
    for doc, meta in zip(data["documents"], data["metadatas"]):
        if meta.get("category") in slice_cats:
            docs_by_pair[(meta.get("unit_name"), meta.get("army"))].append(doc)
    out = {}
    for pair, docs in docs_by_pair.items():
        keys = sorted(app.content_key({"text": d}) for d in docs)
        if keys:
            out[pair] = hashlib.md5("".join(keys).encode()).hexdigest()
    return out


@lru_cache(maxsize=256)
def embed_query(query: str):
    """The bi-encoder embedding of a query, memoized for the turn (and process). The
    two seeders previously each called get_embedder().encode([query]) on the same
    string — two SentenceTransformer encodes per turn. This collapses them to one.
    Deterministic, so process-level caching is correct. Returns the 1-D vector."""
    import app
    return app.get_embedder().encode([query])[0]

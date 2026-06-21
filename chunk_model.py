"""
chunk_model.py — the typed Chunk + provenance enum (audit C12/C13).
===================================================================
The audit's #2 smell: a chunk had no type. Provenance and scoring state were
smeared across ad-hoc optional dict keys (`unit_seed`, `dep_seed`, `seq_neighbor`,
`lexical`, …) that every consumer re-probed, and `similarity` was an overloaded
sentinel (float / 0.0 = degraded metadata-fetch / None = unscored).

`Chunk` gives provenance ONE typed field (`prov: Provenance`) and names the scoring
fields explicitly. To make the migration safe in this large monolith, Chunk also
exposes a **back-compat mapping shim** (`__getitem__` / `get` / `__setitem__` /
`__contains__`) translating the legacy keys to attributes — so the eval harnesses,
the Streamlit source-expander, and the golden dumper keep working unchanged while the
engine moves onto the typed form. The bag-of-keys is gone from STORAGE; only the read
surface stays compatible.

Named `chunk_model` (not `chunk`) to avoid shadowing Python's stdlib `chunk` module.
"""
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
import hashlib
import re


class Provenance(Enum):
    """HOW a chunk entered the candidate pool — the single typed replacement for the
    scattered boolean keys the audit (C12) flagged."""
    DENSE       = "dense"        # semantic hit from the vector query
    LEXICAL     = "lexical"      # BM25 name/phrase hit
    UNIT_SLICE  = "unit_slice"   # metadata fetch for a named datasheet
    NAMED_RULE  = "named_rule"   # metadata fetch for a named army/detachment rule
    DEP_SEED    = "dep_seed"     # definition / referenced-rule seeded by a parent
    SEQ_NEIGHBOR = "seq_neighbor"  # seq±1 sibling of a curated ordered sequence


@lru_cache(maxsize=8192)
def content_key_text(text: str) -> str:
    """Stable md5 of a chunk's *rules text* only — strips unit/faction/category/source
    headers so identical rule text collapses to one key. Memoized by text (A4): the key
    is a pure function of the text, so every repeat across the 25 call sites is a dict
    lookup. Header-stripping is unchanged, so dedup is byte-identical."""
    lines = text.splitlines()
    content_lines = [
        l for l in lines
        if not l.startswith("#")
        and not l.startswith("**Unit:**")
        and not l.startswith("**Faction:**")
        and not l.startswith("**Category:**")
        and not l.startswith("**Source:**")
    ]
    content = re.sub(r'\s+', ' ', " ".join(content_lines)).strip()
    return hashlib.md5(content.encode()).hexdigest()


# ── Legacy-key ↔ attribute translation (the back-compat shim) ──────────────────
# Read getters: legacy key -> function(chunk) -> value. Provenance booleans are
# DERIVED from `prov` (so the four old keys collapse to one typed field).
_GETTERS = {
    "text":            lambda c: c.text,
    "metadata":        lambda c: c.meta,
    "similarity":      lambda c: c.cosine,
    "rerank":          lambda c: c.rerank,
    "rank_score":      lambda c: c.rank_score,
    "rank_override":   lambda c: c.rank_override,
    "dep_bridge":      lambda c: c.dep_bridge,
    "dep_parent_keys": lambda c: list(c.parent_keys) if c.parent_keys else [],
    "unit_seed":       lambda c: c.prov is Provenance.UNIT_SLICE,
    "dep_seed":        lambda c: c.prov is Provenance.DEP_SEED,
    "seq_neighbor":    lambda c: c.prov is Provenance.SEQ_NEIGHBOR,
    "lexical":         lambda c: c.prov is Provenance.LEXICAL,
}

def _set_seq_neighbor(c, v):
    if v:
        c.prov = Provenance.SEQ_NEIGHBOR

# Write setters: legacy key -> function(chunk, value).
_SETTERS = {
    "similarity":      lambda c, v: setattr(c, "cosine", v),
    "rerank":          lambda c, v: setattr(c, "rerank", v),
    "rank_score":      lambda c, v: setattr(c, "rank_score", v),
    "rank_override":   lambda c, v: setattr(c, "rank_override", v),
    "dep_bridge":      lambda c, v: setattr(c, "dep_bridge", v),
    "dep_parent_keys": lambda c, v: setattr(c, "parent_keys", tuple(v)),
    "seq_neighbor":    _set_seq_neighbor,
}


@dataclass(eq=False)
class Chunk:
    text: str
    meta: dict
    prov: Provenance = Provenance.DENSE
    cosine: float | None = None        # bi-encoder similarity; None = never scored
    rerank: float | None = None        # cross-encoder sigmoid; None = not reranked
    rank_score: float | None = None    # effective sort key, stamped by assemble
    rank_override: float | None = None # parent-cap forced score (seeded deps; B9)
    parent_keys: tuple = ()            # sourcing parents (DEP_SEED / SEQ_NEIGHBOR)
    dep_bridge: float | None = None    # the per-dep relevance signal that seeded it

    @property
    def key(self) -> str:
        """Memoized content_key (A4)."""
        return content_key_text(self.text)

    # ── back-compat mapping shim ───────────────────────────────────────────────
    def __getitem__(self, k):
        if k in _GETTERS:
            return _GETTERS[k](self)
        raise KeyError(k)

    def get(self, k, default=None):
        if k not in _GETTERS:
            return default
        val = _GETTERS[k](self)
        return val if val is not None else default

    def __setitem__(self, k, v):
        if k in _SETTERS:
            _SETTERS[k](self, v)
        else:
            raise KeyError(f"Chunk has no writable legacy key {k!r}")

    def __contains__(self, k):
        return k in _GETTERS and _GETTERS[k](self) is not None

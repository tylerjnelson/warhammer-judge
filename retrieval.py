"""
retrieval.py — the pure retrieval engine (importable without Streamlit).
========================================================================
The audit (C10/C11) found the real controller living inside render_chat as a
70-line inline block whose ~10 ordered stages — with hard sequencing constraints
(seed BEFORE rerank, parent-cap AFTER rerank but BEFORE assemble) — were enforced
only by comment, and that the engine could not be imported without dragging in
Streamlit.

This module fixes both: the stages are lifted into pure functions driven by one
declarative ordered list (`PIPELINE`), so the sequencing IS the list order, and
`build_context()` is a pure function — query in, ordered chunk list out, no
Streamlit, no st.session_state (everything session-shaped is passed in). app.py's
render_chat now calls build_context() and renders the result; the evals import it
directly instead of monkey-driving the render function.

Behavior is held byte-stable against spec/refresh-baseline/golden.json: this is a
cut of the inline controller into a function, not a re-tune. `app` is imported
lazily (app.py imports retrieval at top) so there is no import-time cycle.
"""
from dataclasses import dataclass, field

import config


@dataclass
class RetrievalContext:
    """Mutable carrier threaded through the PIPELINE stages, so stages stop passing
    four parallel lists (main/units/rules + the resolved-army set) around by hand.

    Inputs (set by the caller):
      query              — the RAW user query (post-clarification rewrite); the unit
                           slice and the reranker key off this, NOT the expanded form.
      edition, mission_pack_mode, selected_faction, resolution — session-shaped state.
    Filled by stages:
      expanded/where     — route_query (process_query output + faction override)
      rerank_query       — the query string the cross-encoder + seeders score against
      main/units/rules   — the three candidate pools (was chunks_raw/unit_raw/rules_raw)
      result             — the final ordered context handed to the LLM
    """
    query: str
    edition: str
    mission_pack_mode: bool
    selected_faction: str = "All Factions"
    resolution: list | dict | None = None

    expanded: str = ""
    where: dict | None = None
    rerank_query: str = ""
    main: list = field(default_factory=list)
    units: list = field(default_factory=list)
    rules: list = field(default_factory=list)
    result: list = field(default_factory=list)

    @property
    def resolved_armies(self) -> set:
        res = self.resolution if isinstance(self.resolution, list) else []
        return {r["army"] for r in res if r.get("army")}


# ── Stages (each takes the context, mutates it; order is the PIPELINE list) ─────

def route_query(ctx: RetrievalContext) -> None:
    """process_query → (expanded, where, faction); apply the session faction override
    when the auto-route left `where` open; pick the rerank query (raw vs expanded)."""
    import app
    ctx.expanded, ctx.where, _ = app.process_query(
        ctx.query, ctx.edition, mission_pack_mode=ctx.mission_pack_mode)
    if ctx.selected_faction != "All Factions" and ctx.where is None:
        ctx.where = {"army": ctx.selected_faction}
    ctx.rerank_query = ctx.expanded if config.RERANK_USE_EXPANDED else ctx.query


def retrieve_dense(ctx: RetrievalContext) -> None:
    """Wide dense (+ BM25) candidate pool for the reranker to sort."""
    import app
    ctx.main = app.retrieve(ctx.expanded, ctx.where, ctx.edition,
                            n_results=config.RERANK_CANDIDATES)


def retrieve_units(ctx: RetrievalContext) -> None:
    """Guaranteed metadata slice for the datasheet(s) the query NAMES (army pinned by
    `resolution`) — keyed on the raw query."""
    import app
    ctx.units = app.retrieve_unit_slice(ctx.query, ctx.edition,
                                        ctx.mission_pack_mode, ctx.resolution)


def retrieve_rules(ctx: RetrievalContext) -> None:
    """Guaranteed Core (+ mission-pack when ON) rules slice + name-gated army/detachment
    rules, so rules are represented even when the semantic match favors datasheets."""
    import app
    ctx.rules = app.retrieve_rules_slice(
        ctx.expanded, ctx.edition, mission_pack_mode=ctx.mission_pack_mode,
        n_results=config.TOP_K_RULES * 2)


def scope_resolved(ctx: RetrievalContext) -> None:
    """P2 faction allowlist: once clarification resolved the named unit(s) to a faction
    set, drop a different faction's same-named unit/rule from the broad pools BEFORE the
    cap. No-op when nothing resolved. units are already resolution-scoped by construction."""
    import app
    armies = ctx.resolved_armies
    if armies:
        ctx.main  = app.scope_to_resolved_armies(ctx.main, armies)
        ctx.rules = app.scope_to_resolved_armies(ctx.rules, armies)


def seed_dependencies(ctx: RetrievalContext) -> None:
    """Seed the rules a surfaced chunk depends on (definitions + referenced rules), span-
    bridge gated, into the main pool BEFORE rerank."""
    import app
    pool = ctx.main + ctx.rules
    ctx.main = (ctx.main
                + app.seed_definitions(ctx.rerank_query, pool, ctx.edition, ctx.mission_pack_mode)
                + app.seed_referenced_rules(ctx.rerank_query, pool, ctx.edition, ctx.mission_pack_mode))


def rerank(ctx: RetrievalContext) -> None:
    """Segment-maxpool cross-encoder over all three pools (deduped by content_key)."""
    import app
    app.rerank_pools(ctx.rerank_query, ctx.edition, ctx.mission_pack_mode,
                     ctx.main, ctx.rules, ctx.units)


def cap_seeded_below_parents(ctx: RetrievalContext) -> None:
    """Override each seeded dep's score to ride just below its reranked parent (the
    cross-encoder rates a dependency ~0). AFTER rerank, BEFORE assemble."""
    import app
    app.rank_seeded_below_parents(ctx.main + ctx.rules, ctx.edition, ctx.mission_pack_mode)


def assemble(ctx: RetrievalContext) -> None:
    """Reserve rules + per-unit slots, fill toward TOP_K, order reserved-first under the
    token budget."""
    import app
    ctx.result = app.assemble_context(
        ctx.main, ctx.rules, ctx.edition,
        mission_pack_mode=ctx.mission_pack_mode, unit_chunks=ctx.units)


def inject_sequence_neighbors(ctx: RetrievalContext) -> None:
    """Pull seq±1 siblings of any curated ordered sequence a final chunk belongs to."""
    import app
    ctx.result = app.inject_sequence_neighbors(ctx.result, ctx.edition)


# The sequencing constraints the audit found buried in comments are now the literal
# order of this list (seed BEFORE rerank; cap AFTER rerank BEFORE assemble). Reordering
# is a one-line move with an obvious blast radius; each stage is independently testable
# via stage(ctx) on a constructed context.
PIPELINE = [
    route_query,
    retrieve_dense,
    retrieve_units,
    retrieve_rules,
    scope_resolved,
    seed_dependencies,
    rerank,
    cap_seeded_below_parents,
    assemble,
    inject_sequence_neighbors,
]


def run(query: str, *, edition: str, mission_pack_mode: bool,
        selected_faction: str = "All Factions",
        resolution: list | dict | None = None) -> RetrievalContext:
    """Drive the full PIPELINE and return the populated context (result + all three
    pools). Use this when you need the intermediate pools (e.g. the eval harness's
    per-unit / seeded-dep reporting); use build_context when you only want the result."""
    ctx = RetrievalContext(
        query=query, edition=edition, mission_pack_mode=mission_pack_mode,
        selected_faction=selected_faction, resolution=resolution)
    for stage in PIPELINE:
        stage(ctx)
    return ctx


def build_context(query: str, *, edition: str, mission_pack_mode: bool,
                  selected_faction: str = "All Factions",
                  resolution: list | dict | None = None) -> list:
    """Pure: query in, ordered chunk list out. No Streamlit, no session state.

    Mirrors render_chat's former inline controller exactly (the production retrieval
    path, WITH the unit slice). The evals and the golden oracle drive THIS instead of
    reproducing the stage wiring by hand."""
    return run(query, edition=edition, mission_pack_mode=mission_pack_mode,
               selected_faction=selected_faction, resolution=resolution).result

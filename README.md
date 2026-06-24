# ⚖️ Warhammer 40,000 Rules Adjudicator

A private, RAG-powered chat app that answers Warhammer 40,000 rules questions from the *actual* rules text — never the model's memory. Ask a natural-language question ("can a unit that Fell Back still shoot?", "how far can my Land Raider Crusader pile in?") and the app retrieves the governing rule chunks, hands *only* those to an LLM, and returns a cited ruling. If the supporting rule isn't in the retrieved context, the Judge says so rather than guess.

> 🚧 **Work in progress.** Actively evolving — retrieval tuning, coverage, and the 11th-edition path are all still moving.

## What it handles

- Core / universal rules and mission-pack (matched-play) rules, where the pack overrides Core
- Datasheet lookups, army & detachment rules
- Illegal-state detection (a question premised on an impossible board state is flagged before it's answered)
- Compound questions ("after I charge, how far can I pile in?") where the operative clause is buried under framing

## Two constraints shape everything

1. **Free-tier LLM (~6K tokens/min, shared across the window).** Context is hard-budgeted to ~2,800 tokens, so quality has to come from *retrieval precision* rather than stuffing the prompt. The budget is soft at the edge — whole rules are never cut mid-text — and the prompt is split into a cacheable instruction prefix and a volatile rules block to keep per-call token cost down.
2. **CPU-only host.** Embeddings and reranking run locally (a tiny cross-encoder), costing zero LLM tokens, which keeps the scarce token budget for the answer.

## How a query is adjudicated

The retrieval engine is a pure pipeline of ordered stages; the order *is* the contract (e.g. dependency seeding must happen before reranking).

1. **Route** — classify the query (unit lookup vs. rules question vs. faction-scoped) and pick the search filter.
2. **Retrieve** three pools in parallel: a wide **dense** (semantic) pool augmented by a **BM25 lexical** pass for exact rule-name hits; a guaranteed **unit slice** (a metadata fetch of any named datasheet, so a unit that doesn't embed near the question still reaches the pool); and a guaranteed **rules slice** (Core + mission pack + name-gated army/detachment rules).
3. **Scope** — once a unit is resolved to a faction, drop other factions' same-named units.
4. **Seed dependencies** — pull in the rules a surfaced rule depends on (e.g. a charge rule that leans on *Engagement Range*), gated so only genuinely relevant dependencies are added.
5. **Rerank** — a local cross-encoder rescores the merged pool. For compound questions it scores each candidate against *every* clause and keeps the best, so the chunk answering the operative clause isn't buried by framing.
6. **Assemble** — reserve slots for the best rules and for each named unit, fill the rest by score, and order reserved-first so the token budget truncates only discretionary fill. Curated multi-step sequences (e.g. the attack sequence) pull in their neighbors so the whole ordered rule surfaces together.

## Disambiguation before the heavy work

A chassis name like *Land Raider* maps to several datasheets across several factions. Rather than guess, a two-stage (faction → variant) clarification step runs *first*, deterministically from metadata. Faction is resolved per unit — "my Ork Boyz vs. a Space Marine Land Raider" keeps both units instead of silently dropping one — and the resolved choice rewrites the query inline before retrieval.

## Editions as a first-class dimension

A new edition shares no rules data with the current one, so each edition gets its own data and its own vector collection; isolation comes from the separate collections, and only code is shared. 11th edition is wired in but dormant until data is ready — launching it is data + a config flag, not a code change.

## Stack

Streamlit · ChromaDB (local) · `sentence-transformers` embeddings + a local cross-encoder reranker · Groq-hosted LLM · SQLite for conversation history · data sourced from Wahapedia (CSV exports + an HTML scrape) through an incremental, self-reconciling ingest pipeline.

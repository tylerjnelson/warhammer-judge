"""
config.py — LLM Provider Configuration
=======================================
All LLM settings live here. Swapping providers is a one-line change.
API keys are loaded from .env — never hardcoded here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Provider ──────────────────────────────────────────────────────────────

LLM_PROVIDER = "groq"                           # groq | gemini | deepseek | mistral
LLM_MODEL    = "openai/gpt-oss-120b"
LLM_BASE_URL = "https://api.groq.com/openai/v1"
LLM_API_KEY  = os.getenv("GROQ_API_KEY")

# ── Groq free-tier rate limits (active model) ─────────────────────────────────
# Full reference: https://console.groq.com/docs/rate-limits
# Limits are per-ORGANISATION; whichever threshold is hit FIRST wins. The binding
# constraint for us is TPM — tokens per MINUTE, combined input + output. It is
# NOT a per-request cap: multiple calls in the same minute SHARE the budget, and
# every turn re-sends the system prompt + growing history, all of which counts.
#
#   openai/gpt-oss-120b (active):  RPM 30 · TPM 8K · TPD 200K
#
# HISTORY (2026-07-21): the previous prod model `qwen/qwen3-32b` was RETIRED when
# Groq CLOSED it on the free tier (usage no longer available). gpt-oss-120b was
# the co-best model in every accuracy eval we ran (43/43, `model_eval_graded.md`)
# and — unlike qwen3-32b — needs NO rule-10 prompt crutch to resolve Q12, so it
# is the clean successor. qwen3-32b must not be reintroduced; it is unavailable.
#
# gpt-oss-120b is a *reasoning* model: its reasoning trace is billed as output
# tokens against TPM even though app.py strips it before display — so part of the
# 8K/min is spent on reasoning we discard. See spec/retrieval.md. Note gpt-oss's
# TPM is higher than qwen's old 6K, but its 200K TPD is 2.5x LOWER — watch the
# DAILY budget under sustained load.
#
# Recommended switches if TPM/TPD pressure or the reasoning tax becomes limiting
# (config-only change — same Groq base_url; A/B quality on real queries first):
#   llama-3.3-70b-versatile ............ TPM 12K · TPD 100K · instruct, no
#       reasoning tax; but 100K TPD is fragile at eval scale (see §5 caveats).
#   meta-llama/llama-4-scout-17b-16e-instruct  TPM 30K · TPD 500K · instruct;
#       most headroom, but lower accuracy (~39/43; flips FNP-vs-mortal-wounds).
# Staying on openai/gpt-oss-120b.

# ── Fallback (uncomment to switch) ───────────────────────────────────────────
# LLM_PROVIDER = "gemini"
# LLM_MODEL    = "gemini-2.5-flash"
# LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
# LLM_API_KEY  = os.getenv("GEMINI_API_KEY")

# ── Alt fallback ──────────────────────────────────────────────────────────────
# LLM_PROVIDER = "deepseek"
# LLM_MODEL    = "deepseek-chat"
# LLM_BASE_URL = "https://api.deepseek.com/v1"
# LLM_API_KEY  = os.getenv("DEEPSEEK_API_KEY")

# ── Retrieval ─────────────────────────────────────────────────────────────────

TOP_K              = 8       # TARGET chunk count — kept lean on purpose so a multi-turn
                             # exchange leaves TPM headroom. A soft target, NOT a hard
                             # cap: the per-category reservations below may push past it;
                             # the only HARD ceiling is RULES_CONTEXT_TOKEN_BUDGET (2800).
TOP_K_RULES        = 4       # guaranteed slots reserved for Core_Rules / mission-pack
# ── Named-unit reservation (per unit, not global) ─────────────────────────────
# Reserved by metadata (retrieve_unit_slice), so a unit that doesn't embed near the
# query (Abaddon vs 'Devastating Wounds') still reaches context. PER-UNIT so one named
# unit can't sweep the slots from another in a 2-unit question.
UNIT_CHUNKS_PER_UNIT = 2     # cap of reserved chunks per NAMED unit
UNIT_RERANK_SATURATION = 0.05  # the cross-encoder SATURATES (~1.0, near-tied) on every
                             # chunk of a prominently-named unit, so its rerank can't pick
                             # the answer-bearing section from stat-block fluff. Within
                             # this band of a unit's TOP rerank, treat chunks as tied and
                             # break by cosine (semantic match to THIS query) instead;
                             # outside it, trust rerank. Must sit above the saturated noise
                             # floor (Land Raider spread 0.027 → all tied → cosine finds
                             # Assault Ramp) and below a genuine rerank gap (Trukk: segment
                             # rerank lifts "Grot Riggers" 0.13 clear of fluff → rerank wins).
UNIT_SECOND_RATIO    = 0.3   # keep a unit's 2nd chunk only if its rerank score is within
                             # this ratio of the unit's OWN best chunk. Relative, not
                             # absolute: the cross-encoder rates a unit's stat-block ~0
                             # for a generic ability question, so an absolute floor would
                             # drop the name-bearing chunk. "2nd is legitimately
                             # irrelevant" = far weaker than this unit's best (Abaddon
                             # Datasheet 0.845 vs Keywords 0.037 → drop; Aberrants 0.0002
                             # vs 0.0001 → reranker indifferent → keep).
UNIT_SECOND_FLOOR    = 0.1   # ...but ONLY apply that ratio when the unit's best chunk is
                             # itself meaningfully relevant (≥ this). Below it the reranker
                             # can't tell the unit's chunks apart, so the ratio amplifies
                             # noise into a spurious drop — keep both (Snikrot top 0.027:
                             # ratio would drop his datasheet 0.004, losing the proof he
                             # has Infiltrators). 0.845 Abaddon stays above → ratio holds.
UNIT_KEYWORD_MATCH_FLOOR = 0.99  # rerank floor for a named unit's ABILITY chunk when the
                             # query names a rules-keyword (Feel No Pain, Deadly Demise,
                             # Fights First, …) that the ability ALSO names. The tiny
                             # cross-encoder demonstrably MIS-scores a unit's own abilities:
                             # for "can the Painboy's Feel No Pain save …" it rates the
                             # offensive 'Hold Still' 0.96 (shares the query's 'mortal
                             # wounds' tokens) and the actual FNP-GRANTING 'Dok's Toolz'
                             # 0.01 (which literally says "Feel No Pain 5+"), so the unit
                             # slice reserved the wrong ability and dropped the answer. An
                             # explicit query↔ability keyword match is higher-precision than
                             # the reranker, so floor the matched ability above the reranker's
                             # false top (0.96) → it wins the unit's reserved slot + front
                             # tier. Scoped to the unit slice + Ability chunks (see
                             # boost_named_ability_matches), so it can't promote the dozens
                             # of OTHER units' generic 'Feel No Pain' chunks in the dense pool.
REST_GATE            = 0.0   # rerank floor for DISCRETIONARY (non-reserved) fill chunks,
                             # so spare budget isn't packed with low-relevance noise.
                             # Tunable; 0.0 = current behavior (off).
SIMILARITY_THRESHOLD = 0.3   # discard chunks below this cosine similarity (lowered
                             # 0.35→0.3 to widen the candidate pool the reranker sorts)

# ── Production sends NO completion cap ────────────────────────────────────────
# DECISION (2026-07-04): production OMITS max_completion_tokens entirely. The decision
# is model-agnostic and still governs the current prod model (openai/gpt-oss-120b, TPM
# 8000); the measurements below were taken live against the then-prod model (retired
# qwen/qwen3-32b, TPM limit 6000) — the mechanics (admission-reservation) are identical:
#   • The cap is ADMISSION-RESERVED, not billed-only. The server reserves
#     (input + max_completion_tokens) against the 6000/min TPM wall BEFORE generating and
#     413s if that reservation exceeds 6000. So a cap of 3072 made 7/43 real questions
#     (input 2900-3300 tok) 413 → call_llm_reduced SHED context; 8192 413s EVERY call.
#     Consumption still bills only actual generated tokens — the RESERVATION is the harm.
#   • OMITTING the cap reserves the INPUT ONLY. Proved: a no-cap call dropped remaining-
#     tokens by just the ~33 input tokens at admission; the two worst 413'ers (Q21
#     input=3406, Q40 input=3172) both ADMIT and finish=stop with no cap. So dropping the
#     cap ELIMINATES the output-413/shed class — full context always reaches the model —
#     and leaves nothing to truncate: finish=length can now only occur at the model's ~40K
#     context window, which a rules answer never approaches (longest ever seen: 1383 tok).
#   • The cap's ONLY real benefit was a runaway-reasoning hard stop (gpt-oss-120b is a
#     heavier reasoner than the old qwen3-32b, so this matters more now, not less). That
#     backstop is now a wall-clock LLM_REQUEST_TIMEOUT, which bounds a pathological loop
#     WITHOUT reserving any TPM at admission.
# See spec/free-llm-providers.md §5c.
#
# MAX_OUTPUT_TOKENS is retained ONLY for the EVAL harnesses (collect_model_answers.py,
# run_llm_35.py): when fanning the question set across reasoning ALTERNATES (qwen3.6-27b,
# gpt-oss-20b) a cap usefully bounds their <think>. Production (serving._complete) does NOT
# read it. Bump it in the harness if an alternate needs room — it never touches prod.
MAX_OUTPUT_TOKENS  = 2048   # EVAL-HARNESS ONLY; production omits max_completion_tokens

# Wall-clock ceiling (seconds) on ONE completion HTTP request — the runaway backstop that
# replaces the output cap. Legitimate reasoning answers finish well under this (measured
# generation ≤ ~80s incl. <think>); a large value only catches a pathological loop that
# would otherwise run to the model's context window. Passed to the OpenAI client
# (serving.get_llm_client). Bounds one HTTP request only; the reset-aware 429 sleep is
# separate and additive.
LLM_REQUEST_TIMEOUT = 240

# ── Reset-aware 429 handling (serving.call_llm) ───────────────────────────────
# A 429 rate_limit_exceeded is transient: it costs no generated tokens and the token
# bucket refills within the minute, so the correct move on a per-minute (TPM) breach is
# to WAIT the reset window and retry the FULL request — preserving context/quality —
# rather than shedding context up front. The server tells us EXACTLY how long: serving
# reads the reset from the 429 headers and waits the MAX of (x-ratelimit-reset-tokens,
# retry-after) plus a small margin, so we never retry BEFORE the bucket actually refills
# (which would just earn another 429). We never guess and never wait a blind full minute.
#
# The reported reset is also an exact TPM-vs-TPD discriminator: a per-minute token bucket
# physically refills in ≤~60s, so any reset ≤ RATE_LIMIT_MAX_WAIT is a real TPM breach we
# wait out; a larger reset is the DAILY (TPD) cap (hundreds of seconds) → fall through to
# context-shedding / a clear message so a live user is never blocked for minutes.
# MEASURED (2026-07-04, a live TPM 429): reset-tokens=40.47s, retry-after=21s,
# remaining-tokens=1953/6000 — a real per-minute reset is TENS of seconds, NOT the 1-9s
# the plan assumed, so MAX_WAIT is set to a full minute window (60) to wait out any TPM
# breach rather than shed it. See spec/free-llm-providers.md §5b. NOTE: the SDK default
# max_retries silently masks 429s as multi-second hangs and hides the reset headers, so
# serving.get_llm_client sets max_retries=0 — we own the wait and read the reset ourselves.
RATE_LIMIT_MAX_WAIT = 60   # reset ceiling: wait out any TPM breach (≤~60s); shed the daily cap
RATE_LIMIT_RETRIES  = 1    # full-context wait-and-retry attempts on a bounded (TPM) 429

# ── Per-call token budget (Layer 2) ───────────────────────────────────────────
# The real cap on what reaches the model is a TOKEN budget, not a chunk count
# (TOP_K only bounds candidates). Sized so a multi-turn exchange fits 2-3 calls
# inside the 6K/min TPM window.
#
# OVERFLOW BEHAVIOR (2026-06-20): this is a SOFT target, not a hard cut. format_rules_
# context adds WHOLE chunks (rules first) and never truncates a rule mid-text — the
# chunk that crosses the budget is included in full, then assembly stops. So a rule is
# never reduced to a misleading header (which caused the model to mis-cite / refuse).
# Consequence: the actual context overruns the budget by up to one chunk. Most chunks
# are ~300 tokens, but a few core-rule/datasheet chunks run 600-900, so the MEASURED
# worst case across the 35-question eval is ~3667 tokens (vs the 2800 target). This is
# accepted: 3.7K input + ~1.3K output still fits the 6K/min TPM ceiling per call. If
# the overrun ever needs bounding, cap the boundary-chunk SIZE (drop it whole, never
# slice) rather than reinstating mid-chunk truncation.
RULES_CONTEXT_TOKEN_BUDGET = 2800   # SOFT per-call target (see overflow behavior above)
MAX_HISTORY_MESSAGES       = 6      # prior turns re-sent each call — trim proactively
TOKEN_CHAR_RATIO           = 4      # ~chars per token, cheap budget estimate

# ── Curated cross-file rule sequences (Layer 2 Track C) ───────────────────────
# The scraper flattened the source section hierarchy, so ordered multi-step
# rules that live in separate rule-block files can't be auto-grouped. Re-link
# them here: group name -> ordered list of rule-block file STEMS. ingest.py
# stamps members with section_group + seq; app.py's inject_sequence_neighbors
# pulls a hit's seq±1 siblings so the whole sequence surfaces together.
# Only fully-verified sequences belong here (every stem must exist on disk).
# 10e-specific; 11e needs its own map (or recovery via a Track B re-scrape).
RULES_SEQUENCES = {
    "10e": {
        # The Making Attacks sequence — the most-queried ordered rule in 40k.
        "making_attacks": [
            "core_rules_1_hit_roll",
            "core_rules_2_wound_roll",
            "core_rules_3_allocate_attack",
            "core_rules_4_saving_throw",
            "core_rules_5_inflict_damage",
        ],
    },
    "11e": {},
}

# Post-retrieval authority TIEBREAK (see spec/reranker.md §8e). The old flat
# additive boosts (+0.15/+0.10) were RETIRED: they were tuned for the cosine band
# but misbehave under reranking, where relevant chunks bunch at 0.95–0.999 — a 0.05
# flat differential there leapfrogs a *more*-relevant chunk (it let Leviathan mission
# cards sweep the Core objective rule). Rules now surface as CONTEXT by being
# *referenced* (seed_referenced_rules), not by a blanket boost, so authority is just
# a tiny tiebreak that orders genuine ties (mission-pack > Core) without overpowering
# relevance. Mission-pack only applies when the toggle is on; when off, mission-pack
# chunks are never retrieved at all (HARD INVARIANT — where-filter).
AUTHORITY_TIEBREAK       = 0.001   # mission-pack gets 2×, Core 1× — ties only

# The cross-encoder SATURATES (~1.0) on named-unit chunks and TANKS (~0.0) on
# general rules text even when it is adjudication-critical (a procedural overview
# like CHARGE PHASE, or a long passage whose decisive clause is buried — the model
# doesn't read them as a "direct answer"). When it zeros a batch of rules, ranking
# by rerank alone discards the bi-encoder's cosine signal, so a genuinely relevant
# rule (CHARGE PHASE cosine ~0.51) ties with deployment filler (cosine ~0.31) and
# can be crowded out of the reserved rule slots at random. RERANK_COSINE_FLOOR keeps
# cosine as a sub-rerank floor: relevance = max(rerank, W·cosine). W is small enough
# that a blended cosine (≤ W) never leapfrogs a genuinely reranked chunk (rerank
# 0.7+), it only re-orders the chunks the reranker flattened to ~0. See boosted_score.
RERANK_COSINE_FLOOR      = 0.4     # W; 0 restores pure-rerank ranking

# ── Dependency seeding params (used by the LIVE seed_definitions/seed_referenced_rules
#    path via rank_seeded_below_parents + _gate_and_build). The old HYBRID_DEP_BOOST
#    flag + inject_dependency_boosts() it gated were removed 2026-06-20 (superseded by
#    seed_definitions span-bridge seeding). These knobs remain live.
# Protective margin a seeded dependency sits BELOW the weakest parent that sourced
# it (rank_seeded_below_parents). Keeps a dep riding just under its parent — close
# enough to win leftover budget, never able to out-rank it. Larger = more conservative.
RULES_BOOST_DEP         = 0.02
DEP_BOOST_MAX_PER_QUERY = 5      # cap seeded deps per query (drop lowest-scoring extras)
DEP_SCORE_EPS           = 0.001  # tiny ladder step so multiple deps order deterministically
# Per-edition ratified dependency-graph artifact (stem -> [dep_stem, ...]). Loaded
# lazily; absent file ⇒ the feature simply no-ops. Hand-ratified, frozen once green.
RULES_DEP_GRAPH_PATH    = "data/dep_graph_{edition}.json"

# ── Cross-encoder reranking (Layer 3, ranking half) ───────────────────────────
# Bi-encoder cosine rewards keyword density over conceptual centrality (measured:
# "how do normal moves work" filled the budget with aircraft/flying edge chunks
# that repeat "Normal move", dropping the core constraints engagement_range /
# unit_coherency). A cross-encoder scores (query, passage) JOINTLY and reorders the
# candidate pool before assemble_context's TOP_K cap. Local model ⇒ ZERO Groq TPM
# (unlike an LLM reranker, which would spend the scarce 6K/min budget every turn).
# Always on (shipped 2026-06-19, no toggle). Full design: spec/reranker.md.
# Prod IS the no-AVX2 / no-GPU box, so the 2-layer model is FIXED — the 6-layer
# L-6 is unusable here (~20 s at 48 candidates). Do NOT swap to L-6 on this host.
RERANK_MODEL        = "cross-encoder/ms-marco-TinyBERT-L2-v2"  # ~26 ms/candidate on prod CPU
RERANK_CANDIDATES   = 48      # first-stage pool the reranker sorts (N=48 ≈ 1.25 s, accepted)
RERANK_USE_EXPANDED = False   # rerank against the RAW user query, not the synonym-expanded one

# ── Clause-segmented max-pool reranking (experimental) ────────────────────────
# A compound question ("after i charge … how far can i pile in") is lexically
# dominated by its framing clause, so the cross-encoder scores every candidate
# against a charge-blurred query and BURIES the chunk that answers the operative
# clause (Pile In: rerank 0.001, ranked last). When ON, rerank_pools SEGMENTS the
# query on subordinator/discourse markers (after/if/when/then/…) + punctuation and
# scores each candidate against EVERY segment, keeping the MAX — so a chunk is
# judged on the single clause it best answers, not the averaged blur. The WHOLE
# query is always one of the segments, so max can only LIFT a chunk above its
# single-query baseline, never demote it (monotonic-safe; worst case == OFF). Only
# fires when a marker is found (single-clause queries are untouched, zero added
# latency). Cost: up to (RERANK_SEGMENT_MAX+1)x cross-encoder passes on compound
# queries only. See the segment_query / rerank_pools docstrings.
RERANK_SEGMENT_MAXPOOL = True   # master switch (A/B-verified: target Pile-In 8→1,
                                # gate 23/23 on+off, 0 ranking regressions)
RERANK_SEGMENT_MAX     = 2      # max operative (interrogative-headed) clauses kept
                                # before the whole-query fallback segment is added
# Max-pool compresses the saturated top cluster (a compound query lifts EVERY
# clause's best chunk to ~0.99), so the rank-1 slot is then decided by a noisy
# ~0.01 margin — which can let a chunk that nails a SECONDARY clause out-rank the
# true subject ("when i pile in … into engagement range" demoted Pile In 1→5).
# Tiebreak: final score = maxpool + W·(whole-query score). W is small enough that a
# genuinely separated chunk (Pile In 0.96 vs 0.04) keeps its max-pool win, but large
# enough that within the 0.99-cluster the HOLISTIC whole-query relevance decides —
# restoring the real subject to #1. Only applies on the segmented (multi-clause)
# path; single-clause queries are a pure monotonic rescale (ranking unchanged).
RERANK_SEGMENT_TIEBREAK = 0.05

# Span-bridge gate for seeded child definitions (spec/reranker.md §8d). A dependency
# (engagement_range) reads as IRRELEVANT to the query by similarity, so we never
# compare them directly. Instead we find the sentence INSIDE the parent rule that
# names the dep ("...no model can move within Engagement Range...") and seed the dep
# only when the QUERY is similar to THAT sentence — i.e. the question is about the
# part of the rule that needs the dep. Gate = max cosine(query, naming-sentence).
SPAN_GATE_MIN       = 0.45    # bridging-sentence cosine floor to seed a dep (probe: keep≈0.52, drop≈0.34)
# For ability→rule context (seed_referenced_rules) the span-bridge is the WRONG gate:
# a unit question ("how does this ability work") isn't phrased like the rule mechanic,
# so query↔naming-sentence is low even when the rule IS needed context. The right
# signal is the PARENT ability's own relevance — if the ability surfaced strongly, the
# rule it grants is context. Gate on the ability's cosine relevance instead.
REFERENCED_PARENT_MIN = 0.45  # min parent (unit/ability) relevance to seed the rules it names

# ── Lexical (BM25) hybrid retrieval (Layer 3, lexical half) ───────────────────
# Dense MiniLM misses exact rule-name lookups for sub-rules diluted inside a
# parent chunk (e.g. "Big Guns Never Tire" lives inside make_ranged_attacks and
# never reaches the top-60 dense candidates for its own name). A BM25 pass over
# the same corpus, fused into retrieve(), catches these. No re-embed required.
# Lexical-only hits bypass the cosine SIMILARITY_THRESHOLD (their relevance is
# lexical, not semantic) but are gated by term-overlap so paraphrase noise with
# no shared terms is NOT injected — that tail is the embedding-upgrade half's job.
# The HARD INVARIANT still holds: lexical candidates are filtered by the same
# `where` clause as dense, so mission-pack chunks are never surfaced when off.
HYBRID_LEXICAL          = True   # master switch for the BM25 pass
LEXICAL_CANDIDATES      = 30     # BM25 top-k scored before gating
LEXICAL_INJECT_MAX      = 5      # max lexical-only hits injected per query
# A doc must contain (nearly) ALL of the query's content terms to be injected.
# This makes the pass fire on distinctive name/phrase lookups ("Big Guns Never
# Tire", "Lone Operative") — where the rule text holds every term — and stay
# silent on conversational paraphrases ("my models are too far apart"), which
# share only common words with noise and are the embedding-upgrade half's job.
LEXICAL_MIN_OVERLAP     = 0.8    # min fraction of query content-terms present in a doc
# Synthetic cosine-band score stamped on an injected lexical-only hit, scaled by
# its normalized BM25 score across [floor, ceil]. Kept modest (≤ ceil) so a
# lexical hit augments recall into the lower TOP_K slots WITHOUT displacing a
# strong dense+authority-boosted Core/mission-pack chunk from the top.
LEXICAL_SIM_FLOOR       = 0.40
LEXICAL_SIM_CEIL        = 0.55

# ── ChromaDB ──────────────────────────────────────────────────────────────────

CHROMA_DIR       = "chroma_db"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"

# ── Paths ─────────────────────────────────────────────────────────────────────

SQLITE_DB = "judge.db"

# ── Editions registry ─────────────────────────────────────────────────────────
# Edition is a first-class dimension: every pipeline script and the app resolve
# all paths, URLs, collection names, and labels from one entry here. Game data is
# fully separated per edition (own dirs, own manifests, own ChromaDB collection);
# only code/plumbing is shared. Cross-edition isolation is guaranteed by the
# separate collections — the `edition` chunk-metadata stamp is defense-in-depth
# only and must never be a hard dependency in a retrieval `where` filter.
#
# Invariant: exactly one edition has `default: True`; the set of `active`
# editions is a superset of the default. The default flip from 10e->11e is:
# set 11e.default=True and 10e.default=False (both remain active).

EDITIONS = {
    "10e": {
        "label":            "10th Edition",
        "active":           True,
        "default":          True,          # 10th is the default until 11th is promoted
        "wahapedia_base":   "https://wahapedia.ru/wh40k10ed",
        "core_rules_url":   "https://wahapedia.ru/wh40k10ed/the-rules/core-rules/",
        "mission_pack": {
            "name":         "Leviathan",
            "category":     "Leviathan",
            "prefix":       "leviathan",
            "url":          "https://wahapedia.ru/wh40k10ed/the-rules/leviathan/",
            "source":       "Wahapedia_Leviathan",
            "toggle_label": "Leviathan Matched Play",
            "priority":     2,             # Leviathan overrides Core Rules
        },
        "csv_dir":          "data/raw_csv/10e",
        "csv_archive_dir":  "data/raw_csv_archive/10e",
        "blocks_dir":       "data/rule_blocks/10e",
        "scrape_manifest":  "data/rule_blocks/10e/manifest.json",
        "ingest_manifest":  "data/ingest_manifest_10e.json",
        "hash_file":        "data/last_synced_hash_10e.txt",
        "collection":       "warhammer_rules_10e",
        "accent_color":     "#8a1f1f",     # 10th — deep red
    },
    "11e": {
        "label":            "11th Edition",
        "active":           False,         # flip True on release (Stage 2 §2.4)
        "default":          False,         # flip True to make 11th the default (Stage 2 §2.5)
        "wahapedia_base":   "https://wahapedia.ru/wh40k11ed",   # VERIFY exact slug on release
        "core_rules_url":   "<FILL: wh40k11ed core-rules URL>",
        "mission_pack": {
            "name":         "<FILL: 11e mission pack name>",
            "category":     "<FILL: e.g. MissionPack11e>",          # ChromaDB category label
            "prefix":       "<FILL: slug, e.g. mission_pack_11e>",  # rule-block filename prefix
            "url":          "<FILL: wh40k11ed mission pack URL>",
            "source":       "<FILL: e.g. Wahapedia_<Pack>>",
            "toggle_label": "<FILL: e.g. '<Pack> Matched Play'>",
            "priority":     2,
        },
        "csv_dir":          "data/raw_csv/11e",
        "csv_archive_dir":  "data/raw_csv_archive/11e",
        "blocks_dir":       "data/rule_blocks/11e",
        "scrape_manifest":  "data/rule_blocks/11e/manifest.json",
        "ingest_manifest":  "data/ingest_manifest_11e.json",
        "hash_file":        "data/last_synced_hash_11e.txt",
        "collection":       "warhammer_rules_11e",
        "accent_color":     "#1f4e8a",     # 11th — blue (distinct from 10th red)
    },
}


def get_edition(code: str) -> dict:
    """Return the EDITIONS entry for a code, raising KeyError on unknown codes."""
    return EDITIONS[code]


def active_editions() -> list[str]:
    """Return edition codes where active is True, default edition first."""
    codes = [c for c, e in EDITIONS.items() if e["active"]]
    return sorted(codes, key=lambda c: not EDITIONS[c]["default"])


def default_edition() -> str:
    """Return the single edition code whose 'default' is True."""
    return next(c for c, e in EDITIONS.items() if e["default"])


# ── Retrieval-knob interaction map + boot invariants (C14) ────────────────────
# The ~30 retrieval knobs above are individually justified but collectively tuned to
# one eval set, and their INTERACTIONS lived nowhere central. This is that central
# place. Grouped by pipeline STAGE (which knob affects which stage, and which knobs
# pull against each other):
#
#   ROUTING (process_query / is_core_rules_query)
#       — no numeric knobs; the where-clause truth table is in app.process_query.
#   RETRIEVAL (retrieve / lexical_search)
#       SIMILARITY_THRESHOLD ↓ widens the dense pool the reranker sorts; too low =
#         more noise for rerank to suppress. RERANK_CANDIDATES is that pool's size.
#       HYBRID_LEXICAL · LEXICAL_* gate the BM25 augmentation: LEXICAL_MIN_OVERLAP ↑
#         and [LEXICAL_SIM_FLOOR, LEXICAL_SIM_CEIL] together decide how aggressively a
#         lexical-only hit is injected and how high it can sort.
#   SEEDING (seed_definitions / seed_referenced_rules / rank_seeded_below_parents)
#       SPAN_GATE_MIN gates definition seeds; REFERENCED_PARENT_MIN gates ability→rule
#         seeds. RULES_BOOST_DEP + DEP_SCORE_EPS set how far BELOW its parent a seeded
#         dep rides (must stay > 0 so a dep never out-ranks its parent).
#         DEP_BOOST_MAX_PER_QUERY bounds blast radius.
#   RERANK (rerank_pools / boosted_score)
#       RERANK_COSINE_FLOOR (W) blends cosine UNDER the cross-encoder; must be < 1 so a
#         blended cosine can't leapfrog a genuinely reranked chunk. Segment-maxpool:
#         RERANK_SEGMENT_MAX clauses + RERANK_SEGMENT_TIEBREAK (whole-query weight).
#       AUTHORITY_TIEBREAK is a pure ~0.001 mission-pack>core ordering term — must stay
#         tiny so it never overpowers relevance.
#   RESERVATION (assemble_context)
#       TOP_K is the soft target; TOP_K_RULES reserves rule slots (must be < TOP_K).
#       UNIT_CHUNKS_PER_UNIT chunks per named unit; the 2nd is kept only if within
#         UNIT_SECOND_RATIO of the unit's best AND that best ≥ UNIT_SECOND_FLOOR
#         (FLOOR ≤ RATIO by construction). REST_GATE floors discretionary fill.
#   SERVING (format_rules_context / build_messages / call_llm)
#       RULES_CONTEXT_TOKEN_BUDGET is the SOFT hard-ceiling; MAX_HISTORY_MESSAGES bounds
#         re-sent history. Production sends NO output cap (see above) — LLM_REQUEST_TIMEOUT
#         is the runaway backstop; MAX_OUTPUT_TOKENS is eval-harness-only. On a 429,
#         RATE_LIMIT_MAX_WAIT/RATE_LIMIT_RETRIES wait a bounded TPM reset and retry
#         full-context; a large (daily) reset sheds context instead of blocking.

def assert_invariants() -> None:
    """Codify the relationships the tuning relies on, so a nudge that breaks an assumed
    invariant fails LOUDLY at boot instead of silently degrading retrieval. Called once
    at startup (app.init_session). Pure: no I/O, no model load."""
    inv = [
        ("0 <= RERANK_COSINE_FLOOR < 1",      0 <= RERANK_COSINE_FLOOR < 1),
        ("TOP_K_RULES < TOP_K",                TOP_K_RULES < TOP_K),
        ("UNIT_CHUNKS_PER_UNIT >= 1",          UNIT_CHUNKS_PER_UNIT >= 1),
        ("0 <= UNIT_SECOND_RATIO <= 1",        0 <= UNIT_SECOND_RATIO <= 1),
        ("0 <= UNIT_SECOND_FLOOR <= 1",        0 <= UNIT_SECOND_FLOOR <= 1),
        ("UNIT_SECOND_FLOOR <= UNIT_SECOND_RATIO (else the floor never bites)",
                                               UNIT_SECOND_FLOOR <= UNIT_SECOND_RATIO),
        ("0 < UNIT_KEYWORD_MATCH_FLOOR <= 1",  0 < UNIT_KEYWORD_MATCH_FLOOR <= 1),
        ("0 < SPAN_GATE_MIN < 1",              0 < SPAN_GATE_MIN < 1),
        ("0 < REFERENCED_PARENT_MIN < 1",      0 < REFERENCED_PARENT_MIN < 1),
        ("RULES_BOOST_DEP > 0 (a dep must ride strictly below its parent)",
                                               RULES_BOOST_DEP > 0),
        ("DEP_SCORE_EPS >= 0",                 DEP_SCORE_EPS >= 0),
        ("DEP_BOOST_MAX_PER_QUERY >= 1",       DEP_BOOST_MAX_PER_QUERY >= 1),
        ("RERANK_CANDIDATES >= TOP_K",         RERANK_CANDIDATES >= TOP_K),
        ("RERANK_SEGMENT_MAX >= 1",            RERANK_SEGMENT_MAX >= 1),
        ("0 <= RERANK_SEGMENT_TIEBREAK < 1",   0 <= RERANK_SEGMENT_TIEBREAK < 1),
        ("AUTHORITY_TIEBREAK >= 0 and small",  0 <= AUTHORITY_TIEBREAK < 0.05),
        ("0 <= LEXICAL_MIN_OVERLAP <= 1",      0 <= LEXICAL_MIN_OVERLAP <= 1),
        ("LEXICAL_SIM_FLOOR <= LEXICAL_SIM_CEIL", LEXICAL_SIM_FLOOR <= LEXICAL_SIM_CEIL),
        ("REST_GATE >= 0",                     REST_GATE >= 0),
        ("0 < SIMILARITY_THRESHOLD < 1",       0 < SIMILARITY_THRESHOLD < 1),
        ("exactly one default edition",        sum(1 for e in EDITIONS.values() if e["default"]) == 1),
        ("active editions ⊇ {default}",        EDITIONS[default_edition()]["active"]),
    ]
    broken = [name for name, ok in inv if not ok]
    if broken:
        raise AssertionError("config.assert_invariants violated: " + "; ".join(broken))
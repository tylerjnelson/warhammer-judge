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
LLM_MODEL    = "qwen/qwen3-32b"
LLM_BASE_URL = "https://api.groq.com/openai/v1"
LLM_API_KEY  = os.getenv("GROQ_API_KEY")

# ── Groq free-tier rate limits (active model) ─────────────────────────────────
# Full reference: https://console.groq.com/docs/rate-limits
# Limits are per-ORGANISATION; whichever threshold is hit FIRST wins. The binding
# constraint for us is TPM — tokens per MINUTE, combined input + output. It is
# NOT a per-request cap: multiple calls in the same minute SHARE the budget, and
# every turn re-sends the system prompt + growing history, all of which counts.
#
#   qwen/qwen3-32b (active):  RPM 60 · RPD 1K · TPM 6K · TPD 500K
#
# qwen3-32b is a *reasoning* model: its <think> traces are billed as output
# tokens against TPM even though app.py strips them before display — so part of
# the 6K/min is spent on reasoning we discard. See spec/retrieval.md.
#
# Recommended switches if TPM pressure / the reasoning tax becomes limiting
# (config-only change — same Groq base_url; A/B quality on real queries first):
#   llama-3.3-70b-versatile ............ TPM 12K · TPD 100K · instruct, no
#       reasoning tax; 2x per-minute headroom but 5x lower daily cap.
#   meta-llama/llama-4-scout-17b-16e-instruct  TPM 30K · TPD 500K · instruct;
#       5x per-minute AND full daily headroom, quality a notch below the 70B.
# Staying on qwen/qwen3-32b for now.

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

TOP_K              = 8       # chunks retrieved per query
TOP_K_RULES        = 4       # guaranteed slots reserved for Core_Rules / mission-pack
SIMILARITY_THRESHOLD = 0.35  # discard chunks below this cosine similarity

# Completion cap. Counts against the 6K/min TPM ceiling (and, for the reasoning
# model, includes <think> tokens we later strip). See the rate-limit block above
# and spec/retrieval.md for how this fits the per-call token budget.
MAX_OUTPUT_TOKENS  = 1000

# ── Per-call token budget (Layer 2) ───────────────────────────────────────────
# The real cap on what reaches the model is a TOKEN budget, not a chunk count
# (TOP_K only bounds candidates). Sized so a multi-turn exchange fits 2-3 calls
# inside the 6K/min TPM window. The allocator fills RULES_CONTEXT_TOKEN_BUDGET
# with retrieved chunks (rules first), truncating only at line boundaries.
RULES_CONTEXT_TOKEN_BUDGET = 2800   # tokens of retrieved rule context per call
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

# Post-retrieval authority boosts, added to cosine similarity at merge time so
# rules break ties against longer datasheet chunks, and mission-pack outranks
# Core Rules when the mission-pack toggle is ON. See spec/retrieval.md (Layer 1).
# The mission-pack boost is only applied when the toggle is on; when off,
# mission-pack chunks are never retrieved at all (HARD INVARIANT).
RULES_BOOST_MISSION_PACK = 0.15
RULES_BOOST_CORE         = 0.10

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
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
TOP_K_RULES        = 4       # for Core_Rules and Leviathan queries
SIMILARITY_THRESHOLD = 0.35  # discard chunks below this cosine similarity

# ── ChromaDB ──────────────────────────────────────────────────────────────────

CHROMA_DIR       = "chroma_db"
COLLECTION_NAME  = "warhammer_rules"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"

# ── Paths ─────────────────────────────────────────────────────────────────────

SQLITE_DB = "judge.db"
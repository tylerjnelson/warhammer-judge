"""
app.py — The Judge: Warhammer 40K Rules Adjudicator
====================================================
Streamlit chat interface backed by ChromaDB RAG + Groq/Qwen LLM.

Run:
  streamlit run app.py --server.port 8501
"""

import json
import sqlite3
import re
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
from openai import OpenAI

import config

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

def _meta_matches(meta: dict, where: dict | None) -> bool:
    """
    Evaluate a Chroma `where` clause against a single chunk's metadata in-memory,
    covering exactly the operators process_query / rules_where emit ($or, $and,
    $ne, equality). Unknown operators fail CLOSED (return False) so a lexical hit
    is never injected past a filter we don't understand — this is what keeps the
    mission-pack HARD INVARIANT intact without a Chroma round-trip per query.
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
            hits.append({"text": docs[i], "metadata": metas[i],
                         "similarity": config.LEXICAL_SIM_CEIL, "lexical": True})
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
        hits.append({
            "text": docs[i], "metadata": metas[i],
            "similarity": round(sim, 3), "lexical": True,
        })
        if len(hits) >= config.LEXICAL_INJECT_MAX:
            break
    return hits

# ── LLM client (cached) ───────────────────────────────────────────────────────

@st.cache_resource
def get_llm_client():
    return OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
    )

# ── SQLite helpers ────────────────────────────────────────────────────────────

def db_connect():
    conn = sqlite3.connect(ROOT / config.SQLITE_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user      TEXT,
            title     TEXT,
            messages  TEXT,
            created   TEXT,
            archived  TEXT
        )
    """)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(conversations)").fetchall()]
    if "user" not in cols:
        conn.execute("ALTER TABLE conversations ADD COLUMN user TEXT DEFAULT 'unknown'")
    if "edition" not in cols:
        conn.execute("ALTER TABLE conversations ADD COLUMN edition TEXT DEFAULT '10e'")
    conn.commit()
    return conn

def upsert_conversation(messages: list, user: str, edition: str):
    if not messages:
        return
    first = next((m["content"] for m in messages if m["role"] == "user"), "Untitled")
    title = first[:60] + ("..." if len(first) > 60 else "")
    conn  = db_connect()
    conv_id = st.session_state.get("current_conv_id")
    if conv_id is None:
        cursor = conn.execute(
            "INSERT INTO conversations (user, title, messages, created, archived, edition) VALUES (?, ?, ?, ?, ?, ?)",
            (user, title, json.dumps(messages), datetime.now().isoformat(), datetime.now().isoformat(), edition)
        )
        st.session_state.current_conv_id = cursor.lastrowid
    else:
        conn.execute(
            "UPDATE conversations SET messages = ?, archived = ? WHERE id = ? AND user = ?",
            (json.dumps(messages), datetime.now().isoformat(), conv_id, user)
        )
    conn.commit()
    conn.close()

def load_archived_conversations(user: str, edition: str):
    conn = db_connect()
    rows = conn.execute(
        "SELECT id, title, created FROM conversations WHERE user = ? AND edition = ? ORDER BY id DESC",
        (user, edition)
    ).fetchall()
    conn.close()
    return rows

def load_conversation_messages(conv_id: int, user: str):
    conn = db_connect()
    row = conn.execute(
        "SELECT messages FROM conversations WHERE id = ? AND user = ?",
        (conv_id, user)
    ).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return []

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

    # Distinctive = long enough, not generic role vocab, not core-rules language,
    # and not spread across a huge number of datasheets.
    tokens = {
        t for t, n in token_df.items()
        if len(t) >= 5 and t not in _UNIT_STOPWORDS and t not in core_vocab and n <= 40
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

def expand_query(query: str) -> str:
    q = query
    for short, full in SYNONYMS.items():
        q = re.sub(rf'\b{re.escape(short)}\b', full, q, flags=re.IGNORECASE)
    return q

def is_core_rules_query(query: str, edition: str) -> bool:
    mp_name = config.get_edition(edition)["mission_pack"]["name"].lower()
    triggers = [
        "core rule", "universal rule", "in every army", "basic rule",
        "all armies", "always active", mp_name, "mission rule",
        "secondary mission", "primary mission", "tournament",
        "matched play", "victory points", "vp", "scoring",
        "transport", "embark", "disembark", "inside", "riding in",
    ]
    return any(t in query.lower() for t in triggers)

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
    if mission_pack_mode:
        if faction and not include_core:
            where = {"$or": [{"army": faction}, {"category": mp_category}]}
        elif faction and include_core:
            where = {"$or": [{"army": faction}, {"category": "Core_Rules"}, {"category": mp_category}]}
        elif names_unit:
            # Unit lookup (incl. "Land Raider transport capacity"): go broad for
            # the datasheet — the guaranteed rules slice still injects the core
            # rule, so we get both without scoping away the unit.
            where = None
        elif include_core:
            where = {"$or": [{"category": "Core_Rules"}, {"category": mp_category}]}
        else:
            where = {"$or": [{"category": "Core_Rules"}, {"category": mp_category}]}  # rules question
    else:
        if faction and not include_core:
            where = {"$and": [{"army": faction}, {"category": {"$ne": mp_category}}]}
        elif faction and include_core:
            where = {"$and": [{"army": faction}, {"category": {"$ne": mp_category}}]}
        elif names_unit:
            where = {"category": {"$ne": mp_category}}  # unit lookup → broad, minus mp (invariant)
        elif include_core:
            where = {"category": "Core_Rules"}
        else:
            where = {"category": "Core_Rules"}  # rules question

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
    try:
        results = collection.query(**kwargs)
    except Exception:
        kwargs.pop("where", None)
        results = collection.query(**kwargs)

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        similarity = 1 - dist
        if similarity >= config.SIMILARITY_THRESHOLD:
            chunks.append({"text": doc, "metadata": meta, "similarity": round(similarity, 3)})

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

def content_key(chunk: dict) -> str:
    """
    Stable hash of a chunk's *rules text* only — strips unit name / faction /
    category / source headers so identical rule text from different units (or
    the same chunk arriving via two different queries) collapses to one key.
    """
    lines = chunk["text"].splitlines()
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
    return [c for c in chunks if c["metadata"].get("category") in allowed]

def boosted_score(chunk: dict, edition: str, mission_pack_mode: bool) -> float:
    """Cosine similarity plus an authority boost (mission-pack > core > rest)."""
    cat         = chunk["metadata"].get("category", "")
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    score       = chunk["similarity"]
    if mission_pack_mode and cat == mp_category:
        return score + config.RULES_BOOST_MISSION_PACK
    if cat == "Core_Rules":
        return score + config.RULES_BOOST_CORE
    return score

def assemble_context(main_chunks: list, rules_chunks: list, edition: str,
                     mission_pack_mode: bool) -> list:
    """
    Merge the main semantic results with the guaranteed rules slice:
      • reserve up to TOP_K_RULES slots for the best rules chunks,
      • fill the remaining slots with the best main (datasheet/ability) chunks,
      • order the final set by authority-boosted score.
    """
    rank = lambda c: boosted_score(c, edition, mission_pack_mode)

    rules_sorted    = sorted(deduplicate_chunks(rules_chunks), key=rank, reverse=True)
    guaranteed      = rules_sorted[:config.TOP_K_RULES]
    guaranteed_keys = {content_key(c) for c in guaranteed}

    main_sorted = sorted(deduplicate_chunks(main_chunks), key=rank, reverse=True)
    rest        = [c for c in main_sorted if content_key(c) not in guaranteed_keys]

    final = deduplicate_chunks(guaranteed + rest)[:config.TOP_K]
    return sorted(final, key=rank, reverse=True)

# ── Ambiguity detection ───────────────────────────────────────────────────────

def detect_ambiguity(chunks: list, query: str) -> list[tuple] | None:
    """
    Returns (label, unit_name, army) options if the query is ambiguous across
    multiple distinct units with genuinely different content. Returns None
    otherwise. Runs on RAW (pre-dedup) chunks so all variants are visible.
    Only considers Datasheet and Ability chunks — not Datasheet_Section,
    Stratagem, or rules chunks.
    """
    unit_chunks = [c for c in chunks
                   if c["metadata"].get("category") in ("Datasheet", "Ability")]
    if len(unit_chunks) < 2:
        return None

    units_seen = defaultdict(list)
    for chunk in unit_chunks:
        unit_name = chunk["metadata"].get("unit_name", "").strip()
        army      = chunk["metadata"].get("army", "").strip()
        if unit_name:
            units_seen[unit_name].append(army)

    query_words = [w for w in query.lower().split() if len(w) > 3]
    ambiguous   = []
    for unit_name, armies in units_seen.items():
        name_words = unit_name.lower().split()
        if any(w in query_words for w in name_words if len(w) > 3):
            if len(set(f"{unit_name}|{a}" for a in armies)) > 1 or len(armies) > 1:
                ambiguous.append(unit_name)

    if not ambiguous:
        return None

    options = []
    seen    = set()
    for chunk in unit_chunks:
        unit_name = chunk["metadata"].get("unit_name", "").strip()
        army      = chunk["metadata"].get("army", "").strip()
        label     = f"{unit_name} ({army})" if army else unit_name
        if label not in seen and any(amb.lower() in unit_name.lower() for amb in ambiguous):
            seen.add(label)
            options.append((label, unit_name, army))

    return options[:8] if len(options) >= 2 else None

# ── Unit section fetch ────────────────────────────────────────────────────────

def fetch_unit_sections(unit_name: str, army: str, edition: str) -> list[dict]:
    """
    Fetch Datasheet_Section chunks (Transport, Keywords, Composition, etc.)
    for a specific unit by name and army.

    These focused chunks exist in ChromaDB from ingest.py Pass 3 but won't
    always surface via semantic search when the query topic differs from the
    section content (e.g. a question about charging won't retrieve a Transport
    capacity section). This function injects them explicitly after clarification
    so the LLM always has transport capacity and keyword restrictions in context
    when ruling on unit-specific questions — enabling it to catch illegal game
    states per system prompt rule 8.
    """
    collection = get_collection(edition)
    try:
        results = collection.query(
            query_texts=[unit_name],
            n_results=5,
            where={"$and": [
                {"army":      army},
                {"category":  "Datasheet_Section"},
                {"unit_name": unit_name},   # exact match — prevents similar units bleeding in
            ]},
            include=["documents", "metadatas", "distances"],
        )
        return [
            {"text": doc, "metadata": meta, "similarity": round(1 - dist, 3)}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]
    except Exception:
        return []

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
        return [
            {"text": doc, "metadata": meta, "similarity": None}
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
                result.append(nb)
    return result

# ── Prompt builder ────────────────────────────────────────────────────────────

def system_prompt(edition: str) -> str:
    ed = config.get_edition(edition)
    mp = ed["mission_pack"]["name"]
    return f"""You are 'The Judge,' an expert Warhammer 40,000 {ed['label']} rules adjudicator.

Rules:
1. Answer ONLY using the provided rules context below.
2. If the context contains a {mp} or errata entry, it OVERRIDES any base Core Rule.
3. Always cite the specific rule name and source in your answer.
4. If you cannot find a definitive answer, say: 'The provided rules do not clearly address this — I recommend checking the official GW FAQ.' Do NOT speculate.
5. Structure complex answers as: [Ruling] → [Rule Citation] → [Reasoning].
6. CRITICAL: Never infer or extrapolate rules that are not explicitly stated in the context. If an ability says 'Normal move', it means Normal move only — do not assume it also applies to Advance moves, Fall Back moves, or any other move type unless the rule explicitly says so.
7. If a rule citation appears to be cut off or incomplete, say so explicitly rather than ruling based on partial text.
8. If a question contains an illegal game state (e.g. a unit embarked in a transport it cannot legally embark in, based on transport capacity or keyword restrictions in the provided context), identify and state the illegal premise before ruling on any other aspect of the question.
"""

def mission_pack_context(edition: str) -> str:
    mp = config.get_edition(edition)["mission_pack"]["name"]
    return (f"This app is used for {mp} matched play games. When rules conflict "
            f"between Core Rules and {mp}, {mp} rules take precedence.\n\n")

# ── Token budgeting (Layer 2) ─────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Cheap ~chars/token proxy — avoids a tokenizer dependency on the hot path."""
    return len(text) // config.TOKEN_CHAR_RATIO

def truncate_to_lines(text: str, token_budget: int, force_first: bool = False) -> str:
    """
    Trim text to fit token_budget, cutting only at line boundaries so a rule is
    never sliced mid-sentence (system-prompt rule 7). With force_first, always
    keep at least the first line even if it overflows — used only for the very
    first chunk so an otherwise-empty context still shows something.
    """
    if token_budget <= 0 and not force_first:
        return ""
    out, used = [], 0
    for line in text.split("\n"):
        cost = estimate_tokens(line) + 1
        if used + cost > token_budget and not (force_first and not out):
            break
        out.append(line)
        used += cost
    return "\n".join(out)

SEP        = "\n\n---\n\n"
SEP_TOKENS = len(SEP) // config.TOKEN_CHAR_RATIO + 1

def format_rules_context(chunks: list, token_budget: int) -> str:
    """
    Assemble the rules context within token_budget. Chunks arrive pre-ranked
    (rules first, via assemble_context); add whole chunks greedily, then
    line-truncate the boundary chunk to use the remaining budget. Lower-ranked
    chunks that don't fit are dropped rather than overrunning the budget — only
    the first chunk may overflow (so context is never empty).
    """
    if not chunks:
        return "No relevant rules found for this query."
    parts, used = [], 0
    for i, chunk in enumerate(chunks, 1):
        meta  = chunk["metadata"]
        label = f"[{i}] {meta.get('unit_name') or meta.get('category', 'Rule')} ({meta.get('army', '')})"
        block = f"{label}\n{chunk['text']}"
        sep   = SEP_TOKENS if parts else 0
        cost  = estimate_tokens(block) + sep
        if used + cost <= token_budget:
            parts.append(block)
            used += cost
            continue
        # Boundary chunk: fit whole leading lines into the remaining budget.
        remaining = token_budget - used - sep - estimate_tokens(label) - 1
        trimmed   = truncate_to_lines(chunk["text"], remaining, force_first=not parts)
        if trimmed:
            parts.append(f"{label}\n{trimmed}")
        break
    return SEP.join(parts) if parts else "No relevant rules found for this query."

def build_messages(conversation: list, chunks: list, user_query: str,
                   edition: str, mission_pack_mode: bool = True,
                   rules_budget: int | None = None,
                   history_messages: int | None = None) -> list:
    rules_budget     = config.RULES_CONTEXT_TOKEN_BUDGET if rules_budget is None else rules_budget
    history_messages = config.MAX_HISTORY_MESSAGES       if history_messages is None else history_messages

    # Stable, cacheable system prefix — instructions ONLY. Keeping the volatile
    # rules context OUT of this message lets Groq cache the prefix, so the Judge
    # instructions stop counting against TPM every call (spec/retrieval.md L2).
    mode_prefix    = mission_pack_context(edition) if mission_pack_mode else ""
    system_content = mode_prefix + system_prompt(edition)
    messages = [{"role": "system", "content": system_content}]

    # Prior turns are plain Q/A (rules context is never persisted to history),
    # but still a recurring per-call TPM cost — trim to the most recent few.
    for msg in conversation[-history_messages:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Volatile rules context rides in the final user message, budgeted.
    rules_context = format_rules_context(chunks, rules_budget)
    messages.append({
        "role": "user",
        "content": f"RULES CONTEXT (answer using ONLY this):\n{rules_context}\n\nQUESTION: {user_query}",
    })
    return messages

# ── LLM call ──────────────────────────────────────────────────────────────────

def _complete(messages: list) -> str:
    """Single Groq completion + reasoning-trace stripping. Raises on API error."""
    client   = get_llm_client()
    response = client.chat.completions.create(
        model=config.LLM_MODEL, messages=messages,
        max_tokens=config.MAX_OUTPUT_TOKENS, temperature=0.1,
    )
    raw    = response.choices[0].message.content
    answer = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
    return answer or raw

def call_llm(conversation: list, chunks: list, user_query: str, edition: str,
             mission_pack_mode: bool = True) -> str:
    messages = build_messages(conversation, chunks, user_query, edition, mission_pack_mode)
    try:
        return _complete(messages)
    except Exception as e:
        err = str(e)
        if "413" in err or "rate_limit_exceeded" in err or "tokens" in err.lower():
            if chunks:
                return call_llm_reduced(conversation, chunks, user_query, edition, mission_pack_mode)
            return "⚠️ This question requires too much context for the free tier. Try breaking it into smaller questions."
        return f"⚠️ LLM error: {err}\n\nCheck your API key and provider config in config.py."

def call_llm_reduced(conversation: list, chunks: list, user_query: str, edition: str,
                     mission_pack_mode: bool = True) -> str:
    """Retry with a sharply reduced budget when the 6K/min TPM ceiling is hit."""
    messages = build_messages(
        conversation, chunks[:3], user_query, edition, mission_pack_mode,
        rules_budget=config.RULES_CONTEXT_TOKEN_BUDGET // 3,
        history_messages=2,
    )
    try:
        return _complete(messages) + "\n\n*Note: Response was generated with reduced context due to API limits.*"
    except Exception:
        return "⚠️ This question requires too much context for the free tier. Try breaking it into a smaller question."

# ── Session state init ────────────────────────────────────────────────────────

def init_session():
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
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

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
                            "refined_query", "pending_clarification"]:
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
                        "refined_query", "pending_clarification"]:
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

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if (msg["role"] == "assistant"
                    and i == len(st.session_state.messages) - 1
                    and st.session_state.last_chunks
                    and not st.session_state.pending_clarification):
                render_source_expander(st.session_state.last_chunks)

    # ── Persistent clarification buttons ─────────────────────────────────────
    if st.session_state.pending_clarification:
        options, original_query = st.session_state.pending_clarification
        st.markdown("**Select a unit:**")
        for row_start in range(0, len(options), 3):
            row_options = options[row_start:row_start + 3]
            cols = st.columns(len(row_options))
            for col, (label, unit_name, army) in zip(cols, row_options):
                if col.button(label, key=f"clarify_{label}"):
                    st.session_state.pending_clarification = None
                    st.session_state.refined_query = f"{original_query} — specifically the {label}"
                    st.rerun()
        return

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

    # ── Process query ─────────────────────────────────────────────────────────
    expanded_query, auto_where, _ = process_query(
        active_input, edition, mission_pack_mode=st.session_state.mission_pack_mode
    )
    if st.session_state.selected_faction != "All Factions" and auto_where is None:
        auto_where = {"army": st.session_state.selected_faction}

    # Retrieve extra candidates so dedup still fills TOP_K slots after
    # collapsing identical chunks. Ambiguity detection runs on raw chunks
    # so all unit variants are visible for clarification buttons.
    chunks_raw = retrieve(expanded_query, auto_where, edition, n_results=config.TOP_K * 3)

    # Ambiguity check on raw chunks — only for fresh (non-refined) queries
    is_refined = (active_input != user_input)
    options    = None if is_refined else detect_ambiguity(chunks_raw, active_input)

    # Guaranteed rules slice: a second, category-scoped query for Core Rules
    # (and, only when the mission-pack toggle is on, mission-pack rules) so they
    # are represented even when the semantic match favors datasheets. When the
    # toggle is OFF, mission-pack chunks are never queried or surfaced.
    rules_raw = retrieve_rules_slice(
        expanded_query, edition,
        mission_pack_mode=st.session_state.mission_pack_mode,
        n_results=config.TOP_K_RULES * 2,
    )

    # Merge: reserve TOP_K_RULES slots for rules, fill the rest with the best
    # datasheet/ability matches, order by authority-boosted score.
    chunks = assemble_context(
        chunks_raw, rules_raw, edition,
        mission_pack_mode=st.session_state.mission_pack_mode,
    )

    # For refined queries, inject Datasheet_Section chunks (Transport capacity,
    # Keywords, etc.) for the selected unit. These have focused embeddings from
    # ingest Pass 3 but won't surface via semantic search when the query topic
    # differs from the section content. Injecting them guarantees the LLM has
    # transport restrictions in context to catch illegal game states (rule 8).
    if is_refined:
        match = re.search(r'specifically the (.+?) \((.+?)\)$', active_input)
        if match:
            unit_name      = match.group(1).strip()
            army           = match.group(2).strip()
            section_chunks = fetch_unit_sections(unit_name, army, edition)
            existing_ids   = {hashlib.md5(c["text"].encode()).hexdigest() for c in chunks}
            for sc in section_chunks:
                if hashlib.md5(sc["text"].encode()).hexdigest() not in existing_ids:
                    chunks.insert(0, sc)
            chunks = chunks[:config.TOP_K]

    if options:
        clarification_text = "⚖️ **Clarification needed** — multiple distinct units match your query. Which did you mean?"
        st.session_state.pending_clarification = (options, active_input)
        st.session_state.messages.append({"role": "user",      "content": active_input})
        st.session_state.messages.append({"role": "assistant", "content": clarification_text})
        st.session_state.last_chunks = chunks
        upsert_conversation(st.session_state.messages, user, edition)
        st.rerun()
        return

    # Track C: when a retrieved chunk is part of a curated ordered sequence, pull
    # its neighbors so the full sequence reaches the LLM. The token allocator
    # caps the total, so this can't bust the budget.
    chunks = inject_sequence_neighbors(chunks, edition)

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
    upsert_conversation(st.session_state.messages, user, edition)
    st.rerun()

# ── Source expander ───────────────────────────────────────────────────────────

def render_source_expander(chunks: list):
    with st.expander("📖 View Source Chunks", expanded=False):
        for i, chunk in enumerate(chunks, 1):
            meta = chunk["metadata"]
            st.markdown(
                f"**[{i}]** {meta.get('unit_name') or meta.get('category', 'Rule')} "
                f"· {meta.get('army', '')} · {meta.get('category', '')} "
                f"· similarity: `{chunk['similarity']}`"
            )
            st.code(chunk["text"][:600] + ("..." if len(chunk["text"]) > 600 else ""),
                    language="markdown")
            if i < len(chunks):
                st.divider()

# ── Entry point ───────────────────────────────────────────────────────────────

init_session()
render_sidebar()
render_chat()
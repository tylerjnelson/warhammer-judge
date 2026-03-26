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
from openai import OpenAI

import config

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT     = Path(__file__).resolve().parent
CSV_DIR  = ROOT / "data" / "raw_csv"

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
def get_collection():
    client = chromadb.PersistentClient(path=str(ROOT / config.CHROMA_DIR))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=config.EMBEDDING_MODEL
    )
    return client.get_collection(
        name=config.COLLECTION_NAME,
        embedding_function=emb_fn
    )

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
    conn.commit()
    return conn

def upsert_conversation(messages: list, user: str):
    if not messages:
        return
    first = next((m["content"] for m in messages if m["role"] == "user"), "Untitled")
    title = first[:60] + ("..." if len(first) > 60 else "")
    conn  = db_connect()
    conv_id = st.session_state.get("current_conv_id")
    if conv_id is None:
        cursor = conn.execute(
            "INSERT INTO conversations (user, title, messages, created, archived) VALUES (?, ?, ?, ?, ?)",
            (user, title, json.dumps(messages), datetime.now().isoformat(), datetime.now().isoformat())
        )
        st.session_state.current_conv_id = cursor.lastrowid
    else:
        conn.execute(
            "UPDATE conversations SET messages = ?, archived = ? WHERE id = ? AND user = ?",
            (json.dumps(messages), datetime.now().isoformat(), conv_id, user)
        )
    conn.commit()
    conn.close()

def load_archived_conversations(user: str):
    conn = db_connect()
    rows = conn.execute(
        "SELECT id, title, created FROM conversations WHERE user = ? ORDER BY id DESC",
        (user,)
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
def build_faction_keyword_map():
    import pandas as pd
    kw_map   = {}
    factions = {}
    kw_path = CSV_DIR / "Datasheets_keywords.csv"
    if kw_path.exists():
        df = pd.read_csv(kw_path, sep="|", encoding="utf-8-sig", dtype=str)
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        faction_rows = df[df["is_faction_keyword"].str.upper() == "TRUE"]
        for _, row in faction_rows.iterrows():
            kw_map[str(row["keyword"]).strip().lower()] = str(row["datasheet_id"]).strip()
    fac_path = CSV_DIR / "Factions.csv"
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

def expand_query(query: str) -> str:
    q = query
    for short, full in SYNONYMS.items():
        q = re.sub(rf'\b{re.escape(short)}\b', full, q, flags=re.IGNORECASE)
    return q

def is_core_rules_query(query: str) -> bool:
    triggers = [
        "core rule", "universal rule", "in every army", "basic rule",
        "all armies", "always active", "leviathan", "mission rule",
        "secondary mission", "primary mission", "tournament",
        "matched play", "victory points", "vp", "scoring",
        "transport", "embark", "disembark", "inside", "riding in",
    ]
    return any(t in query.lower() for t in triggers)

def process_query(query: str, leviathan_mode: bool = True):
    _, factions = build_faction_keyword_map()
    expanded     = expand_query(query)
    faction      = detect_faction(query, factions)
    include_core = is_core_rules_query(query)

    if leviathan_mode:
        if faction and not include_core:
            where = {"$or": [{"army": faction}, {"category": "Leviathan"}]}
        elif faction and include_core:
            where = {"$or": [{"army": faction}, {"category": "Core_Rules"}, {"category": "Leviathan"}]}
        elif include_core:
            where = {"$or": [{"category": "Core_Rules"}, {"category": "Leviathan"}]}
        else:
            where = None
    else:
        if faction and not include_core:
            where = {"$and": [{"army": faction}, {"category": {"$ne": "Leviathan"}}]}
        elif faction and include_core:
            where = {"$and": [{"army": faction}, {"category": {"$ne": "Leviathan"}}]}
        elif include_core:
            where = {"category": "Core_Rules"}
        else:
            where = {"category": {"$ne": "Leviathan"}}

    return expanded, where, faction

# ── Retriever ─────────────────────────────────────────────────────────────────

def retrieve(query: str, where: dict | None, n_results: int = None) -> list[dict]:
    """
    Retrieve chunks from ChromaDB.
    n_results defaults to config.TOP_K. Pass a larger value to get more
    candidates before deduplication.
    """
    collection = get_collection()
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
    return chunks

# ── Deduplication ─────────────────────────────────────────────────────────────

def deduplicate_chunks(chunks: list) -> list:
    """
    Remove chunks whose rules text is substantively identical.
    Hashes only content lines — strips unit name / faction / category
    headers so identical rule text from different units collapses to
    one chunk. The highest-similarity duplicate is always kept.
    """
    seen   = {}
    result = []
    for chunk in chunks:
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
        key     = hashlib.md5(content.encode()).hexdigest()
        if key not in seen:
            seen[key] = True
            result.append(chunk)
    return result

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

def fetch_unit_sections(unit_name: str, army: str) -> list[dict]:
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
    collection = get_collection()
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

# ── Prompt builder ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are 'The Judge,' an expert Warhammer 40,000 10th Edition rules adjudicator.

Rules:
1. Answer ONLY using the provided rules context below.
2. If the context contains a Leviathan or errata entry, it OVERRIDES any base Core Rule.
3. Always cite the specific rule name and source in your answer.
4. If you cannot find a definitive answer, say: 'The provided rules do not clearly address this — I recommend checking the official GW FAQ.' Do NOT speculate.
5. Structure complex answers as: [Ruling] → [Rule Citation] → [Reasoning].
6. CRITICAL: Never infer or extrapolate rules that are not explicitly stated in the context. If an ability says 'Normal move', it means Normal move only — do not assume it also applies to Advance moves, Fall Back moves, or any other move type unless the rule explicitly says so.
7. If a rule citation appears to be cut off or incomplete, say so explicitly rather than ruling based on partial text.
8. If a question contains an illegal game state (e.g. a unit embarked in a transport it cannot legally embark in, based on transport capacity or keyword restrictions in the provided context), identify and state the illegal premise before ruling on any other aspect of the question.
"""

LEVIATHAN_CONTEXT = "This app is used for Leviathan matched play games. When rules conflict between Core Rules and Leviathan, Leviathan rules take precedence.\n\n"

def build_messages(conversation: list, chunks: list, user_query: str,
                   leviathan_mode: bool = True) -> list:
    if chunks:
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            meta  = chunk["metadata"]
            label = f"[{i}] {meta.get('unit_name') or meta.get('category', 'Rule')} ({meta.get('army', '')})"
            context_parts.append(f"{label}\n{chunk['text'][:2000]}")
        rules_context = "\n\n---\n\n".join(context_parts)
    else:
        rules_context = "No relevant rules found for this query."

    mode_prefix    = LEVIATHAN_CONTEXT if leviathan_mode else ""
    system_content = mode_prefix + SYSTEM_PROMPT + f"\n\nRULES CONTEXT:\n{rules_context}"

    messages = [{"role": "system", "content": system_content}]
    for msg in conversation:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
    return messages

# ── LLM call ──────────────────────────────────────────────────────────────────

def call_llm(messages: list, chunks: list = None) -> str:
    client = get_llm_client()
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL, messages=messages, max_tokens=1000, temperature=0.1,
        )
        answer = response.choices[0].message.content
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
        answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
        return answer or response.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "413" in err or "rate_limit_exceeded" in err or "tokens" in err.lower():
            if chunks:
                return call_llm_truncated(messages, chunks)
            return "⚠️ This question requires too much context for the free tier. Try breaking it into smaller questions."
        return f"⚠️ LLM error: {err}\n\nCheck your API key and provider config in config.py."

def call_llm_truncated(messages: list, chunks: list) -> str:
    client = get_llm_client()
    context_parts = []
    for i, chunk in enumerate(chunks[:3], 1):
        meta  = chunk["metadata"]
        label = f"[{i}] {meta.get('unit_name') or meta.get('category', 'Rule')} ({meta.get('army', '')})"
        context_parts.append(f"{label}\n{chunk['text'][:600]}")
    system_content = SYSTEM_PROMPT + "\n\nRULES CONTEXT:\n" + "\n\n---\n\n".join(context_parts)
    trimmed = [{"role": "system", "content": system_content}]
    trimmed.extend([m for m in messages if m["role"] != "system"][-4:])
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL, messages=trimmed, max_tokens=1000, temperature=0.1,
        )
        answer = response.choices[0].message.content
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
        answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
        answer = answer or response.choices[0].message.content
        return answer + "\n\n*Note: Response was generated with reduced context due to API limits.*"
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
        "leviathan_mode":        True,
        "refined_query":         None,
        "pending_clarification": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.title("⚖️ The Judge")
        st.caption("Warhammer 40K 10th Edition Rules")
        st.caption(f"Logged in as **{st.session_state.current_user}**")

        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            for key in ["messages", "last_chunks", "viewing_conv_id", "current_conv_id",
                        "refined_query", "pending_clarification"]:
                st.session_state[key] = [] if key in ("messages", "last_chunks") else None
            st.rerun()

        st.divider()

        _, factions     = build_faction_keyword_map()
        faction_options = ["All Factions"] + sorted(factions.values())
        selected = st.selectbox(
            "Faction Filter",
            options=faction_options,
            index=faction_options.index(st.session_state.selected_faction)
                  if st.session_state.selected_faction in faction_options else 0,
            help="Pre-filters retrieval to a specific faction for this session."
        )
        st.session_state.selected_faction = selected

        st.session_state.leviathan_mode = st.toggle(
            "Leviathan Matched Play",
            value=st.session_state.leviathan_mode,
            help="When on, Leviathan mission rules take precedence over Core Rules and are always included in retrieval."
        )

        st.divider()

        st.subheader("Past Conversations")
        archived = load_archived_conversations(st.session_state.current_user)
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
    user = st.session_state.current_user

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
    st.title("⚖️ The Judge")
    st.caption("Ask any Warhammer 40,000 10th Edition rules question.")

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
        active_input, leviathan_mode=st.session_state.leviathan_mode
    )
    if st.session_state.selected_faction != "All Factions" and auto_where is None:
        auto_where = {"army": st.session_state.selected_faction}

    # Retrieve extra candidates so dedup still fills TOP_K slots after
    # collapsing identical chunks. Ambiguity detection runs on raw chunks
    # so all unit variants are visible for clarification buttons.
    chunks_raw = retrieve(expanded_query, auto_where, n_results=config.TOP_K * 3)

    # Ambiguity check on raw chunks — only for fresh (non-refined) queries
    is_refined = (active_input != user_input)
    options    = None if is_refined else detect_ambiguity(chunks_raw, active_input)

    # Deduplicate and trim to TOP_K for LLM context
    chunks = deduplicate_chunks(chunks_raw)[:config.TOP_K]

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
            section_chunks = fetch_unit_sections(unit_name, army)
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
        upsert_conversation(st.session_state.messages, user)
        st.rerun()
        return

    # ── No ambiguity — call LLM ───────────────────────────────────────────────
    messages_for_llm = build_messages(
        st.session_state.messages, chunks, active_input,
        leviathan_mode=st.session_state.leviathan_mode
    )

    with st.chat_message("assistant"):
        with st.spinner("Adjudicating..."):
            answer = call_llm(messages_for_llm, chunks=chunks)
        st.markdown(answer)
        if chunks:
            render_source_expander(chunks)

    st.session_state.messages.append({"role": "user",      "content": active_input})
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_chunks = chunks
    upsert_conversation(st.session_state.messages, user)
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
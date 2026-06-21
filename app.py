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

def _light_stem(t: str) -> str:
    """Strip a common inflectional suffix so 'burning'/'burned'/'burns' all reduce to
    'burn'. Deliberately crude (no linguistic stemmer dependency) — used only to match
    a query token against the rules-corpus vocabulary for unit-signal rejection."""
    for suf in ("ing", "ed", "es", "s"):
        if len(t) - len(suf) >= 3 and t.endswith(suf):
            return t[: -len(suf)]
    return t

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

    # Mission-pack vocabulary: words that are MISSION language, not unit signals —
    # 'leviathan' (the pack name) sits only in the datasheet 'Leviathan Dreadnought',
    # 'burning' only in 'Burning Chariot', so without this they'd misfire a unit lookup
    # / unit slice on a pure mission question ("how does BURNING an objective score").
    # Any token in ≥1 mission-pack block (these blocks are far fewer than core) plus the
    # pack name itself is subtracted.
    mp_name  = config.get_edition(edition)["mission_pack"]["name"].lower()
    mp_vocab = set(re.findall(r"[a-z0-9]+", mp_name))
    mp_glob  = str((ROOT / "data" / "rule_blocks" / edition / f"{mp_name}_*.md"))
    for path in glob.glob(mp_glob):
        with open(path, encoding="utf-8") as f:
            mp_vocab |= set(re.findall(r"[a-z0-9]+", f.read().lower()))

    # Stem the MISSION-PACK vocab only, so a morphological variant in the query is still
    # recognised as mission language: the block says "burned", the query says "burning"
    # — both stem to "burn", so "burning" (→ datasheet "Burning Chariot") is rejected as
    # a unit signal. NOT applied to core_vocab: its ≥3-block threshold is tuned to keep
    # unit-type words like "terminator" (whose plural "terminators" sits in core
    # examples) AS unit signals — stemming core would wrongly drop them.
    mp_stems = {_light_stem(t) for t in mp_vocab}

    # Distinctive = long enough, not generic role vocab, not core-rules language, not
    # mission-pack language (literal or stemmed), not spread across many datasheets.
    tokens = {
        t for t, n in token_df.items()
        if len(t) >= 5 and t not in _UNIT_STOPWORDS
        and t not in core_vocab and t not in mp_vocab
        and _light_stem(t) not in mp_stems and n <= 40
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

# ── Unit-name resolution + sequential clarification (unit slice / disambiguation) ─
# detect_unit answers "is this a unit lookup?" (a bool, for routing). The functions
# below answer "WHICH datasheet(s)?" — needed to (a) source the unit's own chunks
# (retrieve_unit_slice) and (b) drive faction disambiguation BEFORE the heavy
# retrieval/rerank, deterministically from metadata rather than from whatever
# surfaced semantically (so a unit that doesn't embed near the query is still caught).

@st.cache_resource
def get_unit_name_resolver(edition: str):
    """Map a query to the specific datasheet name(s) it mentions. Returns
    (names, token_to_name):
      • names — datasheet names, LONGEST first, so substring matching prefers the
                most specific variant ('Land Raider Crusader' before 'Land Raider');
      • token_to_name — distinctive single tokens that resolve to exactly ONE
                datasheet ('snikrot'→'Boss Snikrot'). Tokens shared by several
                datasheets ('raider') are omitted — they need a full-name phrase or
                clarification, never a guess.
    Distinctiveness is reused from build_unit_index (stopwords + core-vocab stripped)."""
    import pandas as pd
    _, tokens = build_unit_index(edition)
    csv_path  = ROOT / config.get_edition(edition)["csv_dir"] / "Datasheets.csv"
    names = []
    if csv_path.exists():
        df = pd.read_csv(csv_path, sep="|", encoding="utf-8-sig", dtype=str)
        names = sorted({str(n).strip() for n in df["name"].dropna() if str(n).strip()},
                       key=len, reverse=True)
    tok2names = defaultdict(set)
    for nm in names:
        for t in set(re.findall(r"[a-z0-9]+", nm.lower())):
            if t in tokens:
                tok2names[t].add(nm)
    token_to_name = {t: next(iter(ns)) for t, ns in tok2names.items() if len(ns) == 1}
    return names, token_to_name

def resolve_named_units(query: str, edition: str) -> list[str]:
    """The specific datasheet name(s) a query mentions. Full-name substring match
    plus distinctive-single-token fallback; keeps only the most specific name when
    one matched name is a substring of another ('Land Raider' dropped when 'Land
    Raider Crusader' also matched)."""
    names, token_to_name = get_unit_name_resolver(edition)
    q = query.lower()
    found = {nm for nm in names if nm.lower() in q}
    for t in set(re.findall(r"[a-z0-9]+", q)) & token_to_name.keys():
        found.add(token_to_name[t])
    return sorted(n for n in found
                  if not any(n != m and n.lower() in m.lower() for m in found))

def find_unit_occurrences(query: str, edition: str) -> list[dict]:
    """Ordered occurrence SLOTS for the datasheet name(s) a query mentions, with
    positions and multiplicity preserved — unlike resolve_named_units, which returns a
    deduped set and loses the fact that the same chassis word can appear twice (the
    multi-occurrence case that this enables clarifying independently).

    Longest-match, left-to-right, consuming matched spans, so 'Land Raider' INSIDE
    'Land Raider Crusader' (or 'Chaos Land Raider') is not double-counted — the same
    substring-suppression intent as resolve_named_units, but applied per-occurrence
    instead of globally, so two genuinely separate mentions both survive.

    Returns [{id, ref, start, end}, ...] sorted by start; the same `ref` may appear in
    several slots. `id` is a stable per-query slot ordinal (keys the queue + buttons)."""
    names, token_to_name = get_unit_name_resolver(edition)
    q = query.lower()
    spans = []  # (start, end, ref)
    for nm in names:                                   # full-name occurrences
        low = nm.lower()
        start = q.find(low)
        while start != -1:
            spans.append((start, start + len(low), nm))
            start = q.find(low, start + 1)
    for t, nm in token_to_name.items():                # distinctive single tokens
        for m in re.finditer(rf"\b{re.escape(t)}\b", q):
            spans.append((m.start(), m.end(), nm))
    # Greedy: earliest start first, longest span at a tie; skip anything that overlaps
    # an already-claimed span (suppresses the shorter substring at the same position).
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    slots, consumed_end, sid = [], -1, 0
    for s, e, ref in spans:
        if s < consumed_end:
            continue
        slots.append({"id": sid, "ref": ref, "start": s, "end": e})
        consumed_end = e
        sid += 1
    return slots

def unit_armies(unit_name: str, edition: str) -> list[str]:
    """Distinct armies a datasheet name appears under — the faction-ambiguity axis."""
    collection = get_collection(edition)
    try:
        res = collection.get(where={"unit_name": unit_name}, include=["metadatas"])
    except Exception:
        return []
    return sorted({m.get("army") for m in res["metadatas"] if m.get("army")})

# ── Chassis disambiguation (faction-first → variant) ──────────────────────────
# A "chassis" is a datasheet name that is a substring of OTHER datasheet names
# ("Land Raider" ⊂ "Land Raider Crusader", "Venerable Land Raider", …). A bare
# chassis word in a query (resolve_named_units returns the base name) must fan out
# to the whole family so the user can pick faction, then variant — instead of being
# silently pinned to the lone datasheet literally named "Land Raider" (GK/SM only).

def is_chassis_base(name: str, all_names: list[str]) -> bool:
    """True if `name` is a proper substring of some OTHER datasheet name — i.e. it is
    a shared chassis with more specific variants, not a leaf datasheet."""
    low = name.lower()
    return any(o != name and low in o.lower() for o in all_names)

def _variant_signature(unit_name: str, army: str, edition: str) -> str:
    """Stable hash of a datasheet's rules text (army-scoped), so two differently
    NAMED variants with identical rules collapse to one button. Reuses content_key
    (which strips unit/faction/category headers) over the unit's own chunks."""
    collection = get_collection(edition)
    where = {"$and": [{"unit_name": unit_name}, {"army": army},
                      {"category": {"$in": list(UNIT_SLICE_CATEGORIES)}}]}
    try:
        res = collection.get(where=where, include=["documents"])
    except Exception:
        return unit_name  # degrade to name-only dedup
    keys = sorted(content_key({"text": d}) for d in res["documents"])
    return hashlib.md5("".join(keys).encode()).hexdigest() if keys else unit_name

@st.cache_resource
def chassis_family(ref: str, edition: str) -> dict:
    """{army: [variant datasheet names]} for the chassis a query reference names.

    For a chassis base ('Land Raider') the family is every datasheet whose name
    contains the base; for a leaf ('Land Raider Crusader', 'Abaddon …') it is just
    that one name. Within each army, variants whose rules are byte-identical are
    deduped (rules-signature) so a faction never shows two buttons for the same unit.
    """
    names, _ = get_unit_name_resolver(edition)
    low = ref.lower()
    family_names = ([n for n in names if low in n.lower()]
                    if is_chassis_base(ref, names) else [ref])
    by_army: dict = defaultdict(list)
    for nm in family_names:
        for army in unit_armies(nm, edition):
            by_army[army].append(nm)
    out = {}
    for army, variants in by_army.items():
        seen, deduped = {}, []
        for nm in sorted(set(variants)):
            sig = _variant_signature(nm, army, edition)
            if sig not in seen:
                seen[sig] = nm
                deduped.append(nm)
        out[army] = deduped
    return out

def _new_unit_state(ref: str, family: dict, pinned: str | None):
    """Per-reference clarification sub-state, or a finalized {ref,unit_name,army}
    resolution when no question is needed. Returns ("ask", unit_dict) |
    ("auto", resolution_dict) | ("skip", None)."""
    if pinned:
        if pinned not in family:
            return "skip", None          # pinned faction doesn't field this unit
        variants = family[pinned]
        if len(variants) <= 1:
            return "auto", {"ref": ref, "unit_name": variants[0], "army": pinned}
        return "ask", {"ref": ref, "family": {pinned: variants},
                       "stage": "variant", "army": pinned}
    armies = list(family)
    if len(armies) == 1:
        variants = family[armies[0]]
        if len(variants) <= 1:
            return "auto", {"ref": ref, "unit_name": variants[0], "army": armies[0]}
        return "ask", {"ref": ref, "family": family, "stage": "variant",
                       "army": armies[0]}
    return "ask", {"ref": ref, "family": family, "stage": "faction", "army": None}

def build_clarification_queue(query: str, edition: str,
                              selected_faction: str | None = None) -> dict | None:
    """Two-stage (faction → variant) disambiguation state for every chassis / multi-
    faction unit the query names. Runs BEFORE retrieval/rerank so the heavy work only
    happens once faction(s) and variant(s) are known. Returns None when nothing the
    query names needs disambiguating (single-faction leaf, no unit, …).

      {"query", "units": [{ref, family, stage, army}, ...],
       "resolved": [{ref, unit_name, army}, ...]}

    `units` are the pending prompts (in order); `resolved` accumulates the picks that
    needed no question (a faction that fields exactly one variant auto-resolves).
    """
    _, factions = build_faction_keyword_map(edition)
    pinned = None
    if selected_faction and selected_faction != "All Factions":
        pinned = selected_faction
    else:
        pinned = detect_faction(query, factions)

    names, _ = get_unit_name_resolver(edition)
    units, resolved = [], []
    # Iterate per OCCURRENCE (slot), not per unique name, so the same chassis mentioned
    # twice gets two independent prompts/resolutions. Each slot carries its id+span so
    # highlight targets the right word and the rewrite is offset-shift-immune.
    for slot in find_unit_occurrences(query, edition):
        ref = slot["ref"]
        # Only chassis bases or multi-faction leaves are ambiguous; a single-faction
        # leaf needs no prompt (retrieve_unit_slice derives its sole army).
        if not is_chassis_base(ref, names) and len(unit_armies(ref, edition)) <= 1:
            continue
        family = chassis_family(ref, edition)
        if not family:
            continue
        kind, payload = _new_unit_state(ref, family, pinned)
        slot_fields = {"slot_id": slot["id"], "start": slot["start"], "end": slot["end"]}
        if kind == "ask":
            units.append({**payload, **slot_fields})
        elif kind == "auto":
            resolved.append({**payload, **slot_fields})
    if not units and not resolved:
        return None
    return {"query": query, "units": units, "resolved": resolved}

def next_clarification(state: dict | None) -> tuple | None:
    """The next question to render, or None when no prompts remain.
      ("faction", ref, [army, ...])           — stage 1
      ("variant", ref, army, [unit_name, ...]) — stage 2
    """
    if not state or not state.get("units"):
        return None
    u = state["units"][0]
    if u["stage"] == "faction":
        return "faction", u["ref"], sorted(u["family"])
    return "variant", u["ref"], u["army"], list(u["family"][u["army"]])

def apply_clarification(state: dict, choice: str) -> dict:
    """Record a button click for the FIRST pending unit and advance (returns a NEW
    state). At the faction stage `choice` is an army; at the variant stage it is a
    datasheet name. A faction that fields exactly one variant resolves immediately."""
    units = [dict(u) for u in state["units"]]
    resolved = list(state["resolved"])
    u = units[0]
    # Carry the occurrence slot (id + span) onto the resolution so the inline rewrite
    # and unit slice can target the exact mention this pick was for.
    slot = {k: u[k] for k in ("slot_id", "start", "end") if k in u}
    if u["stage"] == "faction":
        variants = u["family"][choice]
        if len(variants) == 1:
            resolved.append({"ref": u["ref"], "unit_name": variants[0], "army": choice, **slot})
            units.pop(0)
        else:
            u["army"], u["stage"] = choice, "variant"
    else:  # variant stage
        resolved.append({"ref": u["ref"], "unit_name": choice, "army": u["army"], **slot})
        units.pop(0)
    return {**state, "units": units, "resolved": resolved}

def highlight_ref(query: str, ref: str, start: int | None = None,
                  end: int | None = None) -> str:
    """Mark the unit reference inside the query so the user sees WHICH word the
    clarification buttons are about. When the occurrence's span (start/end) is given,
    bold exactly THAT occurrence (so the second 'Land Raider' highlights on its own
    prompt); otherwise fall back to the first case-insensitive match of `ref`."""
    if start is not None and end is not None:
        return f"{query[:start]}**:blue[{query[start:end]}]**{query[end:]}"
    return re.sub(re.escape(ref), lambda m: f"**:blue[{m.group(0)}]**",
                  query, count=1, flags=re.IGNORECASE)

def apply_resolution_to_query(query: str, resolved: list) -> str:
    """Rewrite the query INLINE — replace each resolved chassis OCCURRENCE where it sits
    with the specific resolved datasheet + faction — rather than appending a trailing
    "specifically the …" (which leaves the generic word in place and over-weights the
    unit's own datasheet chunks at rerank).

    Offset-shift-immune: occurrences are keyed by their span (start/end) in the
    ORIGINAL string and the result is rebuilt in a single forward pass that only ever
    READS the original — so replacing one occurrence never invalidates a later one's
    span (the failure mode of count=1 replace-one-at-a-time). This is what makes the
    mirror case work: 'a Custodes Land Raider vs a Chaos Land Raider' rewrites BOTH
    mentions to their distinct (unit, army) pairs."""
    spanned = sorted((r for r in resolved if r.get("start") is not None
                      and r.get("end") is not None), key=lambda r: r["start"])
    if not spanned:                                    # legacy/no-span: name-based fallback
        out = query
        for r in resolved:
            out = re.sub(re.escape(r["ref"]), f'{r["unit_name"]} ({r["army"]})',
                         out, count=1, flags=re.IGNORECASE)
        return out
    out, prev = [], 0
    for r in spanned:
        out.append(query[prev:r["start"]])
        out.append(f'{r["unit_name"]} ({r["army"]})')
        prev = r["end"]
    out.append(query[prev:])
    return "".join(out)

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
    # Army/detachment rules are NOT scoped here — they reach context via the
    # name-gated retrieve_named_rules slice (folded into retrieve_rules_slice), which
    # mirrors the unit slice: a faction/detachment rule the query NAMES is reserved,
    # so it survives budget truncation without weakly-matched rules ballooning
    # unrelated questions (the cross-encoder saturates ~1.0 on off-topic rules, so a
    # name gate — not a rerank threshold — is the clean discriminator).
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
    coll = get_collection(edition)
    try:
        got = coll.get(
            where={"$or": [{"category": "Army_Rule"}, {"category": "Detachment_Rule"}]},
            include=["documents", "metadatas"],
        )
    except Exception:
        return []
    hits = []
    for doc, meta in zip(got.get("documents", []), got.get("metadatas", [])):
        lines = doc.splitlines()
        m_name   = _RULE_TITLE_RE.match(lines[0]) if lines else None
        name     = m_name.group(1).strip().lower() if m_name else ""
        m_detach = next((_RULE_DETACH_RE.search(l) for l in lines[:3]
                         if _RULE_DETACH_RE.search(l)), None)
        detach   = m_detach.group(1).strip().lower() if m_detach else ""
        if (len(name) >= 4 and name in q) or (len(detach) >= 5 and detach in q):
            # similarity 0.0 (not None) so boosted_score works pre-rerank — same
            # degraded-cosine convention the unit slice uses.
            hits.append({"text": doc, "metadata": meta, "similarity": 0.0})
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
            out.append({"text": doc, "metadata": meta, "similarity": 0.0, "unit_seed": True})
    return out

def authority_boost(meta: dict, edition: str, mission_pack_mode: bool) -> float:
    """Authority TIEBREAK (mission-pack > core > rest). Tiny by design: it only
    orders genuine ties without overpowering relevance. The old flat cosine-band
    boosts were retired — they leapfrogged more-relevant chunks in the compressed
    rerank band, and rules now surface as context by being *referenced*
    (seed_referenced_rules), not boosted. See spec/reranker.md §8e."""
    cat         = meta.get("category", "")
    mp_category = config.get_edition(edition)["mission_pack"]["category"]
    if mission_pack_mode and cat == mp_category:
        return 2 * config.AUTHORITY_TIEBREAK
    if cat == "Core_Rules":
        return config.AUTHORITY_TIEBREAK
    return 0.0

def boosted_score(chunk: dict, edition: str, mission_pack_mode: bool) -> float:
    """Relevance plus the authority tiebreak (mission-pack > core > rest).

    Relevance is the cross-encoder score (chunk['rerank'], 0..1) when the chunk was
    reranked; the bi-encoder cosine otherwise (e.g. a chunk that bypassed the
    reranker). The authority tiebreak stays deterministic — it encodes the
    mission-pack-overrides-core ordering, never delegated to a learned model.
    """
    relevance = chunk["rerank"] if "rerank" in chunk else chunk["similarity"]
    return relevance + authority_boost(chunk["metadata"], edition, mission_pack_mode)

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


def rerank_pools(query: str, edition: str, mission_pack_mode: bool, *pools: list) -> None:
    """Stamp chunk['rerank'] = sigmoid(cross-encoder logit) on every UNIQUE chunk
    across the given candidate pools, scoring each once (deduped by content_key).

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
    items  = list(unique.values())
    logits = model.predict([(query, c["text"]) for c in items])
    score_by_key = {k: _sigmoid(float(s)) for k, s in zip(unique.keys(), logits)}
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
        cand = {"text": payload["text"], "metadata": payload["metadata"],
                "similarity": 0.0, "dep_seed": True,
                "dep_parent_keys": sorted(dep_parents[d]),
                "dep_bridge": round(dep_bridge[d], 3)}
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
    qv = get_embedder().encode([query])[0]

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
    qv       = get_embedder().encode([query])[0]

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
    """Override each seeded dep's rerank score so it rides JUST BELOW the weakest
    parent that sourced it — the parent-cap, on the reranked parent score. The
    cross-encoder scores a seeded dep ~0 (it judges a *dependency*/referenced rule as
    irrelevant), so we replace that with a parent-derived score. Parents are matched
    by content_key (works for rule parents AND unit/ability parents). Mutates in
    place; call AFTER rerank_pools and BEFORE assemble_context. See §8d/§8e."""
    score_by_key = {content_key(c): boosted_score(c, edition, mission_pack_mode)
                    for c in chunks if not c.get("dep_seed")}
    deps = [c for c in chunks if c.get("dep_seed")]
    # strongest-bridge dep first so the EPS ladder keeps a stable, sensible order
    for i, dep in enumerate(sorted(deps, key=lambda c: c.get("dep_bridge", 0), reverse=True)):
        ps = [score_by_key[k] for k in dep.get("dep_parent_keys", []) if k in score_by_key]
        if not ps:
            continue
        eff = min(ps) - config.RULES_BOOST_DEP - i * config.DEP_SCORE_EPS
        # stamp rerank so boosted_score(dep) == eff (just below the weakest parent)
        dep["rerank"] = round(eff - authority_boost(dep["metadata"], edition, mission_pack_mode), 4)


def _reserve_unit_chunks(unit_chunks: list, reserved_keys: set, rank) -> list:
    """Per-unit reservation: group the named-unit slice by unit and keep each unit's
    best chunk (the query NAMING the unit is the relevance signal), plus its 2nd chunk
    unless that 2nd is legitimately irrelevant. Per-unit (not global) so one named unit
    can't sweep the slots from another in a multi-unit question.

    SELECTION SIGNAL = rerank + cosine. The cross-encoder SATURATES (~1.0) on every
    chunk of a named unit when the query names that unit prominently ("can my Venerable
    Land Raider charge" → Composition, Transport, Assault Ramp ALL ~0.9996), so rerank
    alone reserves arbitrary stat-block fluff and misses the answer-bearing ability
    (Assault Ramp, cosine 0.68). Adding the (propagated) cosine breaks that tie. It is a
    NO-OP when a unit never surfaced semantically (cosine 0 — e.g. Abaddon's datasheet
    for a "Devastating Wounds" question, where rerank 0.845 already discriminates), so
    the tuned rerank-only behavior is preserved.

    "Legitimately irrelevant 2nd" is judged RELATIVELY (within UNIT_SECOND_RATIO of the
    unit's own best) — BUT only when the best chunk's score is itself meaningful
    (≥ UNIT_SECOND_FLOOR). When the signal rates a unit's whole chunk set near-zero
    (a generic ability question — Snikrot's chunks 0.027/0.004), it cannot distinguish
    them, so the ratio would amplify pure noise into a spurious "6× worse" drop and lose
    a genuinely useful chunk (Snikrot's datasheet, which proves he HAS Infiltrators).
    Below the floor we keep both — same reasoning that sets the absolute gate to 0."""
    def sel(c):                                               # rerank + cosine
        return rank(c) + (c.get("similarity") or 0.0)
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
    # main pool onto its slice copy (the metadata fetch leaves slice chunks at 0.0), so
    # _reserve_unit_chunks can tell a unit's answer-bearing section from its stat-block
    # fluff even when the cross-encoder saturates on the named unit. No-op for sections
    # that never surfaced semantically (they stay 0.0).
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
    return reserved + rest


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
9. When a datasheet's weapon or ability names a keyword or rule (e.g. [DEVASTATING WOUNDS], Feel No Pain, Deadly Demise, Infiltrators) AND that rule's text is present in the context, cite and apply that provided rule explicitly. Do NOT call it 'implied', 'standard', or rule from memory when the actual rule chunk is in front of you.
"""

def mission_pack_context(edition: str) -> str:
    mp = config.get_edition(edition)["mission_pack"]["name"]
    return (f"This app is used for {mp} matched play games. When rules conflict "
            f"between Core Rules and {mp}, {mp} rules take precedence.\n\n")

# ── Token budgeting (Layer 2) ─────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Cheap ~chars/token proxy — avoids a tokenizer dependency on the hot path."""
    return len(text) // config.TOKEN_CHAR_RATIO


SEP        = "\n\n---\n\n"
SEP_TOKENS = len(SEP) // config.TOKEN_CHAR_RATIO + 1

def format_rules_context(chunks: list, token_budget: int) -> str:
    """
    Assemble the rules context from WHOLE chunks — a rule is never cut mid-text.
    Chunks arrive pre-ranked (reserved rules/units first, via assemble_context); each
    is added in full. token_budget is a SOFT target: the chunk that crosses it is still
    added whole (so an adjudication-critical rule is never reduced to a misleading
    header), and we stop after it. Rules chunks are ~300 tokens, so the total lands
    near the budget and tops out around budget + one chunk (~3k) in the worst case —
    an accepted overrun to guarantee no truncation. Lower-priority chunks past that
    are dropped whole, never sliced.
    """
    if not chunks:
        return "No relevant rules found for this query."
    parts, used = [], 0
    for i, chunk in enumerate(chunks, 1):
        meta  = chunk["metadata"]
        label = f"[{i}] {meta.get('unit_name') or meta.get('category', 'Rule')} ({meta.get('army', '')})"
        block = f"{label}\n{chunk['text']}"
        parts.append(block)
        used += estimate_tokens(block) + (SEP_TOKENS if len(parts) > 1 else 0)
        if used >= token_budget:      # included this chunk whole; stop before adding more
            break
    return SEP.join(parts)

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
        max_completion_tokens=config.MAX_OUTPUT_TOKENS, temperature=0.1,
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
            upsert_conversation(st.session_state.messages, user, edition)
            st.rerun()
            return
        elif clarify and clarify["resolved"]:
            # Everything the query named auto-resolved (e.g. a pinned faction fields
            # exactly one variant) — no question needed; pin the slice and proceed.
            resolution = clarify["resolved"]

    # ── Process query ─────────────────────────────────────────────────────────
    expanded_query, auto_where, _ = process_query(
        active_input, edition, mission_pack_mode=st.session_state.mission_pack_mode
    )
    if st.session_state.selected_faction != "All Factions" and auto_where is None:
        auto_where = {"army": st.session_state.selected_faction}

    # Retrieve a wide candidate pool for the reranker to sort (and so dedup still
    # fills TOP_K slots after collapsing identical chunks).
    chunks_raw = retrieve(expanded_query, auto_where, edition,
                          n_results=config.RERANK_CANDIDATES)

    # Guaranteed UNIT slice: metadata-sourced chunks for the datasheet(s) the query
    # names (army pinned by `resolution`), so a named unit reaches context even when
    # it doesn't embed near the query. Reranked with everything else; assemble_context
    # reserves the best per-unit chunks without forcing them to rank 1.
    unit_raw = retrieve_unit_slice(active_input, edition,
                                   st.session_state.mission_pack_mode, resolution)

    # Guaranteed rules slice: a second, category-scoped query for Core Rules
    # (and, only when the mission-pack toggle is on, mission-pack rules) so they
    # are represented even when the semantic match favors datasheets. When the
    # toggle is OFF, mission-pack chunks are never queried or surfaced.
    rules_raw = retrieve_rules_slice(
        expanded_query, edition,
        mission_pack_mode=st.session_state.mission_pack_mode,
        n_results=config.TOP_K_RULES * 2,
    )

    # P2: once clarification has resolved the named unit(s) to a faction set, scope
    # the broad candidate pools to those armies BEFORE the TOP_K cap, so a different
    # faction's same-named unit/rule (the Custodes-vs-Chaos Land Raider leak) is
    # dropped and the freed slots backfill with relevant same-faction/agnostic chunks.
    # No-op when nothing resolved. unit_raw is already resolution-scoped by construction.
    resolved_armies = {r["army"] for r in (resolution if isinstance(resolution, list) else [])
                       if r.get("army")}
    if resolved_armies:
        chunks_raw = scope_to_resolved_armies(chunks_raw, resolved_armies)
        rules_raw  = scope_to_resolved_armies(rules_raw,  resolved_armies)

    # Layer 3. Order: SEED the rules a surfaced chunk depends on into the pool — the
    # definitions a rule references (seed_definitions) and the core/mission-pack rules
    # a unit/ability references as context (seed_referenced_rules), both below the
    # bi-encoder candidacy ceiling — then RERANK the whole pool by joint (query,
    # passage) relevance, then cap each seeded dep just below its reranked parent
    # (rank_seeded_below_parents, since the cross-encoder rates a dependency ~0).
    # assemble_context then caps at TOP_K / the 2800-tok budget. See spec/reranker.md.
    mp_mode      = st.session_state.mission_pack_mode
    rerank_query = expanded_query if config.RERANK_USE_EXPANDED else active_input
    pool         = chunks_raw + rules_raw
    chunks_raw   = chunks_raw + seed_definitions(rerank_query, pool, edition, mp_mode) \
                             + seed_referenced_rules(rerank_query, pool, edition, mp_mode)
    rerank_pools(rerank_query, edition, mp_mode, chunks_raw, rules_raw, unit_raw)
    rank_seeded_below_parents(chunks_raw + rules_raw, edition, mp_mode)

    # Merge: reserve TOP_K_RULES slots for rules and up to UNIT_CHUNKS_PER_UNIT chunks
    # per named unit, fill toward the TOP_K target with the best datasheet/ability
    # matches; the 2800-token budget is the hard ceiling. The unit slice already carries
    # the unit's focused Datasheet_Section chunks (Transport, Keywords, …) — relevance-
    # ranked into the reserved slots — so no separate fetch_unit_sections injection is needed.
    chunks = assemble_context(
        chunks_raw, rules_raw, edition,
        mission_pack_mode=st.session_state.mission_pack_mode,
        unit_chunks=unit_raw,
    )


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
            # Show BOTH signals: cosine (semantic) AND the cross-encoder rerank. They
            # diverge in ways that explain the order — the reranker SATURATES (~1.0) on
            # any chunk of a named unit, so cosine is the real discriminator among a
            # unit's sections (Assault Ramp 0.68 vs stat-block fluff 0.0), while it
            # tanks (~0.0) on rules the cosine rates ~0.5. A seeded unit-slice chunk
            # carries cosine 0.0 (metadata fetch, never semantically scored).
            cos  = chunk.get("similarity")
            rer  = chunk.get("rerank")
            rer_s = f" · rerank `{round(rer, 3)}`" if rer is not None else ""
            tag   = " · _unit slice_" if chunk.get("unit_seed") else ""
            st.markdown(
                f"**[{i}]** {meta.get('unit_name') or meta.get('category', 'Rule')} "
                f"· {meta.get('army', '')} · {meta.get('category', '')} "
                f"· cosine `{cos}`{rer_s}{tag}"
            )
            st.code(chunk["text"][:600] + ("..." if len(chunk["text"]) > 600 else ""),
                    language="markdown")
            if i < len(chunks):
                st.divider()

# ── Entry point ───────────────────────────────────────────────────────────────

init_session()
render_sidebar()
render_chat()
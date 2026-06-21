"""
persistence.py — SQLite conversation store.
============================================
The conversation archive (create table + migrations, upsert, list, load), moved
out of app.py (Phase 5). Session-agnostic: `upsert_conversation` now TAKES and
RETURNS the conversation id instead of reading/writing st.session_state, so this
module has no Streamlit dependency and render_chat owns the session wiring.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

import config

ROOT = Path(__file__).resolve().parent


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


def upsert_conversation(messages: list, user: str, edition: str,
                        conv_id: int | None) -> int | None:
    """Insert a new conversation row (conv_id is None) or update the existing one.
    Returns the conversation id (the freshly-inserted rowid on insert, else conv_id),
    which the caller stores back into session state. No-op (returns conv_id) on empty."""
    if not messages:
        return conv_id
    first = next((m["content"] for m in messages if m["role"] == "user"), "Untitled")
    title = first[:60] + ("..." if len(first) > 60 else "")
    conn  = db_connect()
    if conv_id is None:
        cursor = conn.execute(
            "INSERT INTO conversations (user, title, messages, created, archived, edition) VALUES (?, ?, ?, ?, ?, ?)",
            (user, title, json.dumps(messages), datetime.now().isoformat(), datetime.now().isoformat(), edition)
        )
        conv_id = cursor.lastrowid
    else:
        conn.execute(
            "UPDATE conversations SET messages = ?, archived = ? WHERE id = ? AND user = ?",
            (json.dumps(messages), datetime.now().isoformat(), conv_id, user)
        )
    conn.commit()
    conn.close()
    return conv_id


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

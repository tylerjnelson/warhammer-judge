"""
ingest.py — Markdown Rule-Blocks → ChromaDB
============================================
Reads all .md files from data/rule_blocks/, extracts metadata from the
Markdown headers, embeds with sentence-transformers, and upserts into
ChromaDB.

Three passes per run:
  1. Full unit/stratagem/enhancement/rules blocks (one doc per file)
  2. Individual named abilities extracted from unit blocks
  3. Structural datasheet sections (Transport, Keywords, Unit Composition,
     Wargear Options, Damaged) extracted from unit blocks as focused chunks.
     These give transport capacity and keyword restrictions their own
     embeddings so they surface directly in semantic search rather than
     being buried in large truncated datasheet blocks.

Incremental: an ingest_manifest.json tracks content hashes per doc_id.
Documents whose content hasn't changed since the last run are skipped
entirely — no re-embedding, no upsert. Ability and section chunks track
their parent file hash so if a unit block changes, all its derived chunks
are also re-embedded.

Usage:
  python scripts/ingest.py               # incremental — only changed docs
  python scripts/ingest.py --reset       # wipe collection and rebuild
"""

import sys
import re
import json
import hashlib
import argparse
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT             = Path(__file__).resolve().parent.parent
BLOCKS_DIR       = ROOT / "data" / "rule_blocks"
CHROMA_DIR       = ROOT / "chroma_db"
INGEST_MANIFEST  = ROOT / "data" / "ingest_manifest.json"

# ── ChromaDB setup ────────────────────────────────────────────────────────────

COLLECTION_NAME = "warhammer_rules"

def get_collection(reset=False):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

# ── Ingest manifest ───────────────────────────────────────────────────────────

def load_ingest_manifest() -> dict:
    if INGEST_MANIFEST.exists():
        with open(INGEST_MANIFEST) as f:
            return json.load(f)
    return {}

def save_ingest_manifest(manifest: dict):
    with open(INGEST_MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)

def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# ── Metadata extraction ───────────────────────────────────────────────────────

HEADER_RE = re.compile(r'\*\*Faction:\*\*\s*([^|]+?)\s*\|.*\*\*Source:\*\*\s*(\S+)')
ERRATA_RE = re.compile(r'\*\(errata\)\*')

def extract_metadata(filepath, content):
    stem = filepath.stem

    if stem.startswith("unit_"):
        category = "Datasheet"
        doc_id   = stem[5:]
    elif stem.startswith("stratagem_"):
        category = "Stratagem"
        doc_id   = stem[10:]
    elif stem.startswith("enhancement_"):
        category = "Enhancement"
        doc_id   = stem[12:]
    elif stem.startswith("core_rules_"):
        category = "Core_Rules"
        doc_id   = stem[11:]
    elif stem.startswith("leviathan_"):
        category = "Leviathan"
        doc_id   = stem[10:]
    else:
        category = "Unknown"
        doc_id   = stem

    army      = ""
    source_id = ""
    for line in content.splitlines()[:6]:
        m = HEADER_RE.search(line)
        if m:
            army      = m.group(1).strip()
            source_id = m.group(2).strip()
            break

    unit_name  = ""
    first_line = content.splitlines()[0] if content else ""
    if first_line.startswith("# "):
        unit_name = first_line[2:].strip()
        for pfx in ("Stratagem: ", "Enhancement: "):
            if unit_name.startswith(pfx):
                unit_name = unit_name[len(pfx):]
                break

    priority = 2 if ERRATA_RE.search(content[:400]) else 1

    return {
        "doc_id":     f"{category.lower()}_{doc_id}",
        "army":       army,
        "faction_id": army,
        "category":   category,
        "unit_name":  unit_name,
        "source":     "Wahapedia",
        "priority":   priority,
        "source_id":  source_id,
    }

# ── Ability extraction (Pass 2) ───────────────────────────────────────────────

ABILITY_RE = re.compile(
    r'\*\*(?P<n>[^*()\n]+?)\*\*[^\n]*\n> (?P<desc>[^\n]+)',
    re.MULTILINE
)

def extract_abilities(content, base_meta):
    chunks    = []
    unit_name = base_meta.get("unit_name", "")
    army      = base_meta.get("army", "")
    base_id   = base_meta.get("doc_id", "")

    for i, m in enumerate(ABILITY_RE.finditer(content)):
        name = m.group("n").strip()
        desc = m.group("desc").strip()

        if name in ("(Unnamed)", "") or len(desc) < 20:
            continue

        ab_id  = f"ability_{base_id}_{i}"
        ab_doc = (
            f"# Ability: {name}\n"
            f"**Unit:** {unit_name}  |  **Faction:** {army}\n\n"
            f"{desc}"
        )
        ab_meta = {
            "army":       army,
            "faction_id": army,
            "category":   "Ability",
            "unit_name":  unit_name,
            "source":     "Wahapedia",
            "priority":   base_meta.get("priority", 1),
            "source_id":  base_meta.get("source_id", ""),
        }
        chunks.append((ab_id, ab_doc, ab_meta))

    return chunks

# ── Section extraction (Pass 3) ───────────────────────────────────────────────

# Structural sections to extract from unit datasheets as focused chunks.
# Each gets its own embedding so it surfaces directly in semantic search
# rather than being buried past the LLM truncation limit in a full datasheet.
SECTION_TYPES = [
    ("transport",    "Transport"),
    ("keywords",     "Keywords"),
    ("composition",  "Unit Composition"),
    ("options",      "Wargear Options"),
    ("damaged",      "Damaged"),
]

def extract_sections(content, base_meta):
    """
    Extract structural sections from a unit datasheet block.
    Returns list of (section_id, section_doc, section_meta) tuples.

    Each section is stored as category=Datasheet_Section with a
    section_type field for targeted filtering in app.py.
    """
    chunks    = []
    unit_name = base_meta.get("unit_name", "")
    army      = base_meta.get("army", "")
    base_id   = base_meta.get("doc_id", "")

    for section_type, heading in SECTION_TYPES:
        # Match from the heading to the next ## heading or end of document
        pattern = rf'## {re.escape(heading)}\n(.*?)(?=\n## |\Z)'
        match   = re.search(pattern, content, re.DOTALL)
        if not match:
            continue

        section_body = match.group(1).strip()
        if len(section_body) < 20:
            continue

        section_doc = (
            f"# {unit_name} — {heading}\n"
            f"**Unit:** {unit_name}  |  **Faction:** {army}\n\n"
            f"{section_body}"
        )
        section_id   = f"section_{section_type}_{base_id}"
        section_meta = {
            "army":         army,
            "faction_id":   army,
            "category":     "Datasheet_Section",
            "section_type": section_type,
            "unit_name":    unit_name,
            "source":       "Wahapedia",
            "priority":     base_meta.get("priority", 1),
            "source_id":    base_meta.get("source_id", ""),
        }
        chunks.append((section_id, section_doc, section_meta))

    return chunks

# ── Batch upsert ──────────────────────────────────────────────────────────────

BATCH_SIZE = 100

def upsert_batch(collection, ids, documents, metadatas):
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

# ── Main ingest ───────────────────────────────────────────────────────────────

def ingest_files(collection, md_files, ingest_manifest, reset=False):
    p1_upsert  = 0
    p1_skip    = 0
    p2_upsert  = 0
    p2_skip    = 0
    p3_upsert  = 0
    p3_skip    = 0

    # ── Pass 1: full rule blocks ──────────────────────────────────────────────
    print("  Pass 1: ingesting rule blocks...")

    batch_ids   = []
    batch_docs  = []
    batch_metas = []

    def flush_batch():
        if batch_ids:
            upsert_batch(collection, batch_ids, batch_docs, batch_metas)
            batch_ids.clear()
            batch_docs.clear()
            batch_metas.clear()

    for filepath in md_files:
        content   = filepath.read_text(encoding="utf-8")
        meta      = extract_metadata(filepath, content)
        doc_id    = meta["doc_id"]
        file_hash = content_hash(content)

        if not reset and ingest_manifest.get(doc_id) == file_hash:
            p1_skip += 1
            continue

        batch_ids.append(doc_id)
        batch_docs.append(content)
        batch_metas.append({k: v for k, v in meta.items() if k != "doc_id"})
        ingest_manifest[doc_id] = file_hash
        p1_upsert += 1

        if len(batch_ids) >= BATCH_SIZE:
            flush_batch()
            print(f"\r    Upserted: {p1_upsert} new/changed, {p1_skip} skipped",
                  end="", flush=True)

    flush_batch()
    print(f"\r    Upserted: {p1_upsert} new/changed, {p1_skip} skipped")

    # ── Passes 2 & 3: per-unit derived chunks ─────────────────────────────────
    # Both passes iterate the same unit files and share the parent hash check.
    print("  Pass 2: extracting and indexing abilities...")
    print("  Pass 3: extracting and indexing datasheet sections...")

    unit_files = [f for f in md_files if f.stem.startswith("unit_")]

    ab_ids   = []
    ab_docs  = []
    ab_metas = []

    sc_ids   = []
    sc_docs  = []
    sc_metas = []

    for filepath in unit_files:
        content   = filepath.read_text(encoding="utf-8")
        base_meta = extract_metadata(filepath, content)
        file_hash = content_hash(content)
        parent_id = base_meta["doc_id"]

        parent_changed = (
            reset or
            ingest_manifest.get(f"_parent_{parent_id}") != file_hash
        )

        # ── Pass 2: abilities ──
        for ab_id, ab_doc, ab_meta in extract_abilities(content, base_meta):
            ab_hash = content_hash(ab_doc)
            if not parent_changed and ingest_manifest.get(ab_id) == ab_hash:
                p2_skip += 1
                continue
            ab_ids.append(ab_id)
            ab_docs.append(ab_doc)
            ab_metas.append(ab_meta)
            ingest_manifest[ab_id] = ab_hash
            p2_upsert += 1

            if len(ab_ids) >= BATCH_SIZE:
                upsert_batch(collection, ab_ids, ab_docs, ab_metas)
                ab_ids, ab_docs, ab_metas = [], [], []
                print(f"\r    Abilities: {p2_upsert} new/changed, {p2_skip} skipped",
                      end="", flush=True)

        # ── Pass 3: structural sections ──
        for sc_id, sc_doc, sc_meta in extract_sections(content, base_meta):
            sc_hash = content_hash(sc_doc)
            if not parent_changed and ingest_manifest.get(sc_id) == sc_hash:
                p3_skip += 1
                continue
            sc_ids.append(sc_id)
            sc_docs.append(sc_doc)
            sc_metas.append(sc_meta)
            ingest_manifest[sc_id] = sc_hash
            p3_upsert += 1

            if len(sc_ids) >= BATCH_SIZE:
                upsert_batch(collection, sc_ids, sc_docs, sc_metas)
                sc_ids, sc_docs, sc_metas = [], [], []
                print(f"\r    Sections:  {p3_upsert} new/changed, {p3_skip} skipped",
                      end="", flush=True)

        ingest_manifest[f"_parent_{parent_id}"] = file_hash

    if ab_ids:
        upsert_batch(collection, ab_ids, ab_docs, ab_metas)
    if sc_ids:
        upsert_batch(collection, sc_ids, sc_docs, sc_metas)

    print(f"\r    Abilities: {p2_upsert} new/changed, {p2_skip} skipped")
    print(f"\r    Sections:  {p3_upsert} new/changed, {p3_skip} skipped")

    return p1_upsert, p1_skip, p2_upsert, p2_skip, p3_upsert, p3_skip

# ── Main ──────────────────────────────────────────────────────────────────────

def run(reset=False):
    md_files = sorted(BLOCKS_DIR.glob("*.md"))
    if not md_files:
        print("[ERROR] No .md files found in data/rule_blocks/. Run etl.py first.",
              file=sys.stderr)
        sys.exit(1)

    collection      = get_collection(reset=reset)
    ingest_manifest = {} if reset else load_ingest_manifest()
    existing        = collection.count()

    if reset:
        print(f"Collection reset. Ingesting {len(md_files)} rule blocks...")
    else:
        print(f"Collection has {existing} documents. "
              f"Checking {len(md_files)} rule blocks for changes...")

    p1_up, p1_sk, p2_up, p2_sk, p3_up, p3_sk = ingest_files(
        collection, md_files, ingest_manifest, reset=reset
    )

    save_ingest_manifest(ingest_manifest)

    final_count = collection.count()
    total_up    = p1_up + p2_up + p3_up
    total_sk    = p1_sk + p2_sk + p3_sk
    print(f"Ingest complete: {total_up} upserted, {total_sk} skipped. "
          f"Collection now has {final_count} documents.")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest rule-blocks into ChromaDB")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe the ChromaDB collection and rebuild from scratch"
    )
    args = parser.parse_args()
    run(reset=args.reset)
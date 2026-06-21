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
import logging
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config

CHROMA_DIR = ROOT / "chroma_db"   # shared across editions; collection differs

# Per-edition paths (blocks_dir / ingest_manifest / collection) are resolved
# inside run() from config.get_edition(edition).

# ── ChromaDB setup ────────────────────────────────────────────────────────────

def get_collection(reset=False, edition="10e"):
    collection_name = config.get_edition(edition)["collection"]
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    if reset:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

# ── Ingest manifest ───────────────────────────────────────────────────────────

def load_ingest_manifest(manifest_path) -> dict:
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {}

def save_ingest_manifest(manifest_path, manifest: dict):
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# ── Metadata extraction ───────────────────────────────────────────────────────

# Faction and Source are captured independently: unit blocks carry both on the
# header line, but Army_Rule/Detachment_Rule blocks carry **Faction:** with no
# **Source:** token. Requiring them together (the old combined regex) dropped the
# faction on rule chunks, leaving army=''. See spec/multi-unit-clarification-and-faction-scope.md (P3).
FACTION_RE = re.compile(r'\*\*Faction:\*\*\s*([^|]+?)\s*(?:\||$)')
SOURCE_RE  = re.compile(r'\*\*Source:\*\*\s*(\S+)')
ERRATA_RE = re.compile(r'\*\(errata\)\*')

def extract_metadata(filepath, content, edition_code="10e"):
    stem = filepath.stem
    mp   = config.get_edition(edition_code)["mission_pack"]

    if stem.startswith("unit_"):
        category = "Datasheet"
        doc_id   = stem[5:]
    elif stem.startswith("stratagem_"):
        category = "Stratagem"
        doc_id   = stem[10:]
    elif stem.startswith("enhancement_"):
        category = "Enhancement"
        doc_id   = stem[12:]
    elif stem.startswith("army_rule_"):
        category = "Army_Rule"
        doc_id   = stem[10:]
    elif stem.startswith("detachment_rule_"):
        category = "Detachment_Rule"
        doc_id   = stem[16:]
    elif stem.startswith("core_rules_"):
        category = "Core_Rules"
        doc_id   = stem[11:]
    elif stem.startswith(mp["prefix"] + "_"):
        category = mp["category"]
        doc_id   = stem[len(mp["prefix"]) + 1:]
    else:
        category = "Unknown"
        doc_id   = stem

    army      = ""
    source_id = ""
    for line in content.splitlines()[:6]:
        if not army:
            mf = FACTION_RE.search(line)
            if mf:
                army = mf.group(1).strip()
        if not source_id:
            ms = SOURCE_RE.search(line)
            if ms:
                source_id = ms.group(1).strip()
        if army and source_id:
            break

    unit_name  = ""
    first_line = content.splitlines()[0] if content else ""
    if first_line.startswith("# "):
        unit_name = first_line[2:].strip()
        for pfx in ("Stratagem: ", "Enhancement: ", "Army Rule: ", "Detachment Rule: "):
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
        "edition":    edition_code,
    }

# ── Rules-block chunking (Layer 2 Tracks A & C) ───────────────────────────────

STANDALONE_BOLD = re.compile(r'^\*\*([^*]+)\*\*\s*$')

def split_card_deck(content):
    """
    Track A: split a card-deck block into per-card (name, body) pairs at
    standalone-bold name lines (^**NAME**$). Returns [] unless there are >=3
    such lines — i.e. only genuine multi-card decks split; prose/inline-bold
    files (e.g. only_war) are left whole. Filename-agnostic, so 11e decks work.
    """
    lines = content.splitlines()
    idxs  = [i for i, l in enumerate(lines) if STANDALONE_BOLD.match(l.strip())]
    if len(idxs) < 3:
        return []
    cards = []
    for j, start in enumerate(idxs):
        end  = idxs[j + 1] if j + 1 < len(idxs) else len(lines)
        name = STANDALONE_BOLD.match(lines[start].strip()).group(1).strip()
        body = "\n".join(lines[start:end]).strip()
        if body:
            cards.append((name, body))
    return cards

def sequence_for(stem, edition_code):
    """Track C: (group, seq) if this rule-block stem is a curated sequence member."""
    for group, members in config.RULES_SEQUENCES.get(edition_code, {}).items():
        if stem in members:
            return group, members.index(stem) + 1
    return None, None

# Inline sub-rule lead: an ALL-CAPS rule name (1-4 caps words, >=4 chars) starting
# a line, followed by a sentence-case word — e.g. "DEEP STRIKE Some units ...".
# This is the delimiter Wahapedia's flattened styled name-spans leave behind; it
# is what actually carries structure in the few bundled core files (bold does
# not — 91/93 core files have none). See spec/retrieval.md (Layer 2 re-chunking).
RULE_LEAD = re.compile(r"^([A-Z][A-Z'’\-]{1,}(?: [A-Z][A-Z'’\-]+){0,3}) ([A-Z][a-z].*)$")

def split_subrules(content):
    """
    Split a rule block that bundles >=2 named sub-rules (each led by an ALL-CAPS
    name) into (parent_body, [(name, body), ...]). parent_body is everything
    before the first sub-rule — the file's main rule + intro, which KEEPS any
    Track C sequence metadata. Returns (None, []) for <2 leads so single-rule and
    prose files are left whole (mirrors split_card_deck's >=3 gate).
    """
    lines = content.splitlines()
    idxs  = [(i, m.group(1)) for i, l in enumerate(lines)
             if (m := RULE_LEAD.match(l.strip())) and len(m.group(1)) >= 4]
    if len(idxs) < 2:
        return None, []
    first  = idxs[0][0]
    parent = "\n".join(lines[:first]).strip()
    subs   = []
    for j, (start, name) in enumerate(idxs):
        end  = idxs[j + 1][0] if j + 1 < len(idxs) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        if body:
            subs.append((name, body))
    return parent, subs

def build_rules_chunks(filepath, content, base_meta, edition_code):
    """
    Expand a Core_Rules / mission-pack file into ingest chunks:
      • card decks -> one chunk per card (Track A),
      • otherwise  -> the whole section as one chunk.
    Adds a breadcrumb to every chunk and section_group/seq to curated-sequence
    members (Track C). Returns list of (chunk_id, doc, meta) — meta has no doc_id.
    """
    base_id   = base_meta["doc_id"]
    category  = base_meta["category"]
    source_id = base_meta.get("source_id", "")
    clean     = {k: v for k, v in base_meta.items() if k != "doc_id"}

    heading = content.splitlines()[0][2:].strip() if content.startswith("# ") else filepath.stem
    clean["breadcrumb"] = f"{category.replace('_', ' ')} > {heading}"

    group, seq = sequence_for(filepath.stem, edition_code)
    if group:
        clean["section_group"] = group
        clean["seq"]           = seq

    # Track A: per-card split for multi-card decks (>=3 standalone-bold names).
    cards = split_card_deck(content)
    if cards:
        out = []
        for i, (name, body) in enumerate(cards):
            meta = dict(clean)
            meta["breadcrumb"] = f"{clean['breadcrumb']} > {name}"
            meta["card_name"]  = name
            out.append((f"{base_id}_card{i}", body, meta))
        return out

    # Sub-rule split: files bundling >=2 ALL-CAPS-named sub-rules (e.g.
    # deployment_abilities → Deep Strike/Scouts/…; inflict_damage → Feel No Pain/
    # Deadly Demise). Each named rule gets its own focused embedding instead of
    # being averaged into — and bloating — the parent's vector.
    parent_body, subs = split_subrules(content)
    if not subs:
        return [(base_id, content, dict(clean))]

    out = []
    if parent_body:
        # Parent retains the main rule text AND any Track C section_group/seq.
        out.append((base_id, parent_body, dict(clean)))
    for i, (name, body) in enumerate(subs):
        meta = dict(clean)
        meta.pop("section_group", None)   # a sub-rule is not itself a sequence step
        meta.pop("seq", None)
        meta["breadcrumb"] = f"{clean['breadcrumb']} > {name.title()}"
        meta["rule_name"]  = name.title()
        sub_doc = (
            f"# {heading} — {name.title()}\n"
            f"**Category:** {category}  |  **Source:** {source_id}\n\n"
            f"{body}"
        )
        out.append((f"{base_id}_sub{i}", sub_doc, meta))
    return out

def expand_file_to_chunks(filepath, content, base_meta, edition_code):
    """Pass-1 chunks for a file: rules files may fan out (Track A); others are 1:1."""
    mp_category = config.get_edition(edition_code)["mission_pack"]["category"]
    if base_meta["category"] in ("Core_Rules", mp_category):
        return build_rules_chunks(filepath, content, base_meta, edition_code)
    clean = {k: v for k, v in base_meta.items() if k != "doc_id"}
    return [(base_meta["doc_id"], content, clean)]

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
            "edition":    base_meta.get("edition", "10e"),
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
            "edition":      base_meta.get("edition", "10e"),
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

def ingest_files(collection, md_files, ingest_manifest, reset=False, edition="10e"):
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
        base_meta = extract_metadata(filepath, content, edition)

        # Rules files may fan out into multiple chunks (Track A card decks);
        # every other file stays 1:1. Each chunk is hashed by its own doc so
        # incremental ingest tracks card chunks independently.
        for chunk_id, doc, meta in expand_file_to_chunks(filepath, content, base_meta, edition):
            chunk_hash = content_hash(doc)
            if not reset and ingest_manifest.get(chunk_id) == chunk_hash:
                p1_skip += 1
                continue

            batch_ids.append(chunk_id)
            batch_docs.append(doc)
            batch_metas.append(meta)
            ingest_manifest[chunk_id] = chunk_hash
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
        base_meta = extract_metadata(filepath, content, edition)
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

# ── Post-ingest verification ──────────────────────────────────────────────────

class _Tee:
    """Write to several streams at once — used to capture the audit report to
    both the console and a persisted log file in one pass."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def verify_after_ingest(edition="10e", recall=True, strict=False):
    """Audit the freshly-ingested corpus and persist a report for future audits.

    Runs the two harnesses that bracket corpus quality:
      • eval_completeness — every canonical rule's body is ingested AND retrievable
      • eval_fidelity     — chunks are verbatim-accurate to source AND fully cover it

    Both run for the core and Leviathan corpora. The full report is teed to a
    timestamped file under logs/ (and logs/last_ingest_audit.log) so a regression
    is diffable after the fact. Returns 0 on success, nonzero if strict and any
    gate fails. Audit failures never corrupt the ingest itself — the collection is
    already written by the time this runs.
    """
    tests_dir = ROOT / "tests" / "verify"
    sys.path.insert(0, str(tests_dir))
    try:
        import eval_completeness
        import eval_fidelity
    except Exception as e:                      # harness missing / import error
        print(f"  [verify] skipped — could not import audit harnesses: {e}")
        return 0

    # The completeness/fidelity ground truth is the cached core + Leviathan HTML,
    # which only ships for 10e. Other editions have no audit target — skip.
    if edition != "10e" or not (ROOT / "data/html_cache/10e/core_rules.html").exists():
        print("  [verify] skipped — no core/Leviathan source cache for this edition")
        return 0

    logs_dir = ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    logpath = logs_dir / f"ingest_audit_{ts}.log"

    rc = 0
    with open(logpath, "w", encoding="utf-8") as fh:
        tee     = _Tee(sys.__stdout__, fh)
        handler = logging.StreamHandler(tee)
        handler.setFormatter(logging.Formatter("%(message)s"))
        root    = logging.getLogger()
        prev_level = root.level
        root.setLevel(logging.INFO)
        root.addHandler(handler)
        old_stdout = sys.stdout
        sys.stdout = tee
        try:
            print("\n" + "#" * 72)
            print(f"# POST-INGEST AUDIT — edition {edition} · {ts}"
                  f"  (recall={'on' if recall else 'off'}, strict={strict})")
            print("#" * 72)
            for source in ("core", "leviathan"):
                rc |= eval_completeness.run(edition, verbose=False, do_recall=recall,
                                            strict=strict, source=source)
            results = [eval_fidelity.audit(source) for source in ("core", "leviathan")]

            print("\n" + "=" * 72)
            print("AUDIT SUMMARY")
            for r in results:
                print(f"  fidelity {r['source']:9}: "
                      f"accuracy_misses={r['accuracy_misses']}  "
                      f"review_gaps={r['review_gaps']}  "
                      f"coverage={r['coverage_pct']:.1f}%")
                if strict and not r["ok"]:
                    rc = 1
            print("=" * 72)
        finally:
            sys.stdout = old_stdout
            root.removeHandler(handler)
            root.setLevel(prev_level)

    # Refresh the stable "latest" pointer for quick lookup.
    latest = logs_dir / "last_ingest_audit.log"
    latest.write_text(logpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"  [verify] audit report written to {logpath.relative_to(ROOT)} "
          f"(and {latest.relative_to(ROOT)})")
    if strict and rc:
        print("  [verify] STRICT FAILURE — see REVIEW/MISSING lines above")
    return rc


# ── Collection reconciliation (orphan prune) ───────────────────────────────────

def derive_valid_ids(md_files, edition):
    """The exact set of chunk-ids the CURRENT corpus should produce.

    Mirrors ingest_files: pass-1 expansion for every file, plus the pass-2/3
    ability/section fan-out for unit_ files. Used to find vectors in the collection
    that no longer correspond to any current rule block.
    """
    valid_chunks  = set()
    valid_parents = set()
    for fp in md_files:
        content   = fp.read_text(encoding="utf-8")
        base_meta = extract_metadata(fp, content, edition)
        valid_parents.add(base_meta["doc_id"])
        for cid, _doc, _meta in expand_file_to_chunks(fp, content, base_meta, edition):
            valid_chunks.add(cid)
        if fp.stem.startswith("unit_"):
            for cid, _d, _m in extract_abilities(content, base_meta):
                valid_chunks.add(cid)
            for cid, _d, _m in extract_sections(content, base_meta):
                valid_chunks.add(cid)
    return valid_chunks, valid_parents


def reconcile_collection(collection, md_files, ingest_manifest, edition):
    """Delete embeddings (and manifest entries) that the current corpus no longer
    produces — deprecated/renumbered datasheets, removed rule sections, and
    content-shrink sub-chunks. This is the only thing that prunes the collection
    short of a full --reset; ingest is otherwise upsert-only.

    Safety floor: if the orphan set is implausibly large (>40% of the collection),
    something is wrong upstream (empty/incomplete corpus, wrong edition) — refuse
    to delete rather than gut the DB on a bad run.
    """
    valid_chunks, valid_parents = derive_valid_ids(md_files, edition)
    live = set(collection.get(include=[])["ids"])
    orphans = live - valid_chunks
    if not orphans:
        print("  Reconcile: 0 orphan chunks (collection matches corpus).")
        return 0
    if len(orphans) > 0.40 * max(len(live), 1):
        print(f"  [reconcile] ABORTED — {len(orphans)}/{len(live)} chunks would be "
              f"deleted (>40%); refusing in case the corpus is incomplete. "
              f"Run with --reset for an intentional full rebuild.", file=sys.stderr)
        return 0

    ids = list(orphans)
    for i in range(0, len(ids), BATCH_SIZE):
        collection.delete(ids=ids[i:i + BATCH_SIZE])

    # Prune stale manifest entries so it doesn't grow without bound either.
    for k in [k for k in ingest_manifest
              if k not in valid_chunks
              and not (k.startswith("_parent_") and k[len("_parent_"):] in valid_parents)]:
        ingest_manifest.pop(k, None)

    print(f"  Reconcile: deleted {len(orphans)} orphan chunk(s) from the collection.")
    return len(orphans)


# ── Main ──────────────────────────────────────────────────────────────────────

def run(reset=False, edition="10e", verify=True, verify_recall=True, strict_verify=False):
    ed            = config.get_edition(edition)
    blocks_dir    = ROOT / ed["blocks_dir"]
    manifest_path = ROOT / ed["ingest_manifest"]

    md_files = sorted(blocks_dir.glob("*.md"))
    if not md_files:
        print(f"[ERROR] No .md files found in {ed['blocks_dir']}. Run etl.py first.",
              file=sys.stderr)
        sys.exit(1)

    collection      = get_collection(reset=reset, edition=edition)
    ingest_manifest = {} if reset else load_ingest_manifest(manifest_path)
    existing        = collection.count()

    if reset:
        print(f"Collection reset. Ingesting {len(md_files)} rule blocks...")
    else:
        print(f"Collection has {existing} documents. "
              f"Checking {len(md_files)} rule blocks for changes...")

    p1_up, p1_sk, p2_up, p2_sk, p3_up, p3_sk = ingest_files(
        collection, md_files, ingest_manifest, reset=reset, edition=edition
    )

    # Prune embeddings the current corpus no longer produces. A fresh --reset build
    # is already in sync, so only reconcile on incremental runs.
    if not reset:
        reconcile_collection(collection, md_files, ingest_manifest, edition)

    save_ingest_manifest(manifest_path, ingest_manifest)

    final_count = collection.count()
    total_up    = p1_up + p2_up + p3_up
    total_sk    = p1_sk + p2_sk + p3_sk
    print(f"Ingest complete: {total_up} upserted, {total_sk} skipped. "
          f"Collection now has {final_count} documents.")

    # Post-ingest quality gate: completeness + fidelity audit (logged for audits).
    if verify:
        rc = verify_after_ingest(edition, recall=verify_recall, strict=strict_verify)
        if strict_verify and rc:
            sys.exit(rc)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest rule-blocks into ChromaDB")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe the ChromaDB collection and rebuild from scratch"
    )
    parser.add_argument(
        "--edition",
        default="10e",
        help="Edition code to ingest (default: 10e)"
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="skip the post-ingest completeness + fidelity audit"
    )
    parser.add_argument(
        "--verify-no-recall",
        action="store_true",
        help="run the audit but skip the slower retrieval (recall) checks"
    )
    parser.add_argument(
        "--strict-verify",
        action="store_true",
        help="exit nonzero if the post-ingest audit finds any gap (CI gate)"
    )
    args = parser.parse_args()
    run(reset=args.reset, edition=args.edition,
        verify=not args.no_verify,
        verify_recall=not args.verify_no_recall,
        strict_verify=args.strict_verify)
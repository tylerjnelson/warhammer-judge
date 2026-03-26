"""
scrape_rules.py — Scrape Core Rules and Leviathan rules from Wahapedia
=======================================================================
Fetches the Core Rules and Leviathan mission pack pages from Wahapedia,
splits them into per-section Markdown chunks, and writes them to
data/rule_blocks/ for ingestion into ChromaDB.

Handles both standard HTML (h2/h3/p/li) and Wahapedia's custom card
div classes (cgCardLCA, cgText, cgHeader, cgStep etc.) which contain
mission card rules, numbered battle steps, and secondary mission text.

The Leviathan page uses a Columns2 div containing the full game sequence
(numbered steps 1-14). Each h3 inside Columns2 becomes its own section
with all sibling content collected — this captures the full Fixed vs
Tactical Secondary Mission rules, the New Orders stratagem, etc.

Output files:
  core_rules_{slug}.md      — one file per Core Rules section
  leviathan_{slug}.md       — one file per Leviathan section

Usage:
  python scripts/scrape_rules.py             # scrape both pages
  python scripts/scrape_rules.py --core      # core rules only
  python scripts/scrape_rules.py --leviathan # leviathan only
  python scripts/scrape_rules.py --force     # rewrite all files
"""

import re
import sys
import json
import hashlib
import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).resolve().parent.parent
BLOCKS_DIR = ROOT / "data" / "rule_blocks"
MANIFEST   = BLOCKS_DIR / "manifest.json"

BLOCKS_DIR.mkdir(parents=True, exist_ok=True)

# ── Pages to scrape ───────────────────────────────────────────────────────────

PAGES = {
    "core_rules": {
        "url":      "https://wahapedia.ru/wh40k10ed/the-rules/core-rules/",
        "prefix":   "core_rules",
        "category": "Core_Rules",
        "source":   "Wahapedia_Core_Rules",
        "priority": 1,
    },
    "leviathan": {
        "url":      "https://wahapedia.ru/wh40k10ed/the-rules/leviathan/",
        "prefix":   "leviathan",
        "category": "Leviathan",
        "source":   "Wahapedia_Leviathan",
        "priority": 2,   # Leviathan rules override core rules
    },
}

# ── Nav/chrome selectors to remove before parsing ─────────────────────────────

REMOVE_SELECTORS = [
    "nav", "header", "footer", "script", "style",
    ".navBox", ".toc", "#toc",
    "[class*='settings']", "[class*='Settings']",
    "img",
]

# ── Text cleaning ─────────────────────────────────────────────────────────────

def clean_text(text):
    """Normalise whitespace and decode common unicode entities."""
    if not text:
        return ""
    text = (text
            .replace("\xa0", " ")
            .replace("\u2019", "'")
            .replace("\u2018", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2013", "-")
            .replace("\u2014", "--")
            .replace("\u2022", "-"))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:60].strip("_")

# ── Wahapedia custom div extraction ──────────────────────────────────────────

WAHAPEDIA_CARD_CLASSES = (
    "cgCard", "cgText", "cgStep", "abWrap", "abText",
    "frameLight", "frameDark", "redExample",
    "stratText", "stratLegend",
)

def is_wahapedia_card(element):
    if not hasattr(element, "get"):
        return False
    classes = element.get("class", [])
    return any(
        any(cls.startswith(prefix) for prefix in WAHAPEDIA_CARD_CLASSES)
        for cls in classes
    )

def extract_card_text(element):
    """
    Extract text from a Wahapedia custom card div, preserving structure.
    Handles cgCardLCA (mission cards), abWrap (ability boxes).
    """
    lines = []

    header = element.find(class_=re.compile(r"cgHeader|abName|stratName"))
    if header:
        lines.append(f"**{clean_text(header.get_text())}**")

    card_type = element.find(class_=re.compile(r"cgType|abType|stratType"))
    if card_type:
        type_text = clean_text(card_type.get_text())
        if type_text:
            lines.append(f"*{type_text}*")

    legend = element.find(class_=re.compile(r"stratLegend|ShowFluff|cgFluff"))
    if legend:
        legend_text = clean_text(legend.get_text())
        if legend_text and len(legend_text) > 10:
            lines.append(f"> {legend_text}")

    text_divs = element.find_all(class_=re.compile(r"cgText|abText|stratText|frameLight|frameDark"))
    for div in text_divs:
        text = clean_text(div.get_text(separator=" "))
        if text and len(text) > 15:
            lines.append(text)

    if not text_divs:
        already_captured = set()
        for el in [header, card_type, legend]:
            if el:
                already_captured.add(el)

        full_text = []
        for child in element.descendants:
            if isinstance(child, NavigableString):
                text = clean_text(str(child))
                if text and len(text) > 5:
                    parent_captured = any(
                        captured and captured in child.parents
                        for captured in already_captured
                    )
                    if not parent_captured:
                        full_text.append(text)

        combined = " ".join(full_text)
        if combined and len(combined) > 20:
            lines.append(combined)

    return "\n".join(lines)

# ── Columns2 step extractor ───────────────────────────────────────────────────

def extract_columns2_sections(soup, page_config):
    """
    Extract numbered game steps from Wahapedia's Columns2 div.

    The Leviathan page puts its 14-step game sequence inside a single
    <div class="Columns2">. Each step is delimited by an h3 heading —
    all sibling nodes between consecutive h3s belong to that step.

    This captures content that the main walker misses because it lives
    in loose text nodes, br-separated fragments, and inline elements
    rather than p/li tags.
    """
    sections  = []
    prefix    = page_config["prefix"]
    category  = page_config["category"]
    source    = page_config["source"]

    col2 = soup.find("div", class_="Columns2")
    if not col2:
        return sections

    current_heading = None
    current_lines   = []

    def flush(heading, lines):
        if not heading or not lines:
            return
        slug = slugify(heading)
        full_text = " ".join(lines)
        if len(full_text) < 80:
            return
        content = (
            f"# {heading}\n"
            f"**Category:** {category}  |  **Source:** {source}\n\n"
            + "\n".join(lines)
        )
        sections.append((f"{prefix}_{slug}.md", content))

    for node in col2.children:
        if not hasattr(node, 'name') or not node.name:
            # Bare text node between elements
            text = clean_text(str(node))
            if text and len(text) > 10 and current_heading:
                current_lines.append(text)
            continue

        if node.name == "h3":
            flush(current_heading, current_lines)
            current_heading = clean_text(node.get_text())
            current_lines   = []

        elif node.name == "div":
            classes = node.get("class", [])

            # Skip step number diamonds (redDiamond3) — just decorative
            if "redDiamond3" in classes:
                continue

            # Recursively get all text from any content div
            text = clean_text(node.get_text(separator=" "))
            if text and len(text) > 20 and current_heading:
                current_lines.append(text)

        elif node.name in ("ul", "ol"):
            for li in node.find_all("li", recursive=False):
                text = clean_text(li.get_text())
                if text and current_heading:
                    current_lines.append(f"- {text}")

        elif node.name in ("p", "span"):
            text = clean_text(node.get_text(separator=" "))
            if text and len(text) > 10 and current_heading:
                current_lines.append(text)

        # br and a tags — get their text if non-trivial
        elif node.name in ("a",):
            text = clean_text(node.get_text())
            if text and len(text) > 10 and current_heading:
                current_lines.append(text)

        # br tags carry no content — skip
        # Other tags: ignore

    flush(current_heading, current_lines)
    return sections

# ── Main section splitter ─────────────────────────────────────────────────────

SKIP_SECTIONS = {
    "books", "contents", "introduction", "hints and tips",
    "example battlefields", "mission map key", "mission generator",
    "card decks",
}

def split_into_sections(soup, page_config):
    """
    Walk the parsed HTML, grouping content under h2/h3 headings.
    Also extracts Wahapedia custom card div content and Columns2 steps.
    Returns list of (filename, markdown_content) tuples.
    """
    sections        = []
    current_heading = None
    current_lines   = []
    prefix          = page_config["prefix"]
    category        = page_config["category"]
    source          = page_config["source"]

    # ── Extract Columns2 numbered steps first ──
    # These contain the full game sequence (steps 1-14 for Leviathan)
    # and must be handled separately because their content is spread
    # across loose text nodes and br-separated fragments, not p/li tags.
    col2_sections = extract_columns2_sections(soup, page_config)
    sections.extend(col2_sections)

    # Build a set of all element IDs inside Columns2 so the main walk
    # skips them entirely — prevents double-processing.
    columns2_ids = set()
    col2 = soup.find("div", class_="Columns2")
    if col2:
        columns2_ids.add(id(col2))
        for el in col2.find_all():
            columns2_ids.add(id(el))

    # Track processed card elements to avoid duplicating card content
    processed_cards = set()

    def flush(heading, lines):
        if not heading or not lines:
            return
        slug = slugify(heading)
        if slug in SKIP_SECTIONS:
            return
        full_text = " ".join(lines)
        if len(full_text) < 80:
            return
        content = (
            f"# {heading}\n"
            f"**Category:** {category}  |  **Source:** {source}\n\n"
            + "\n".join(lines)
        )
        filename = f"{prefix}_{slug}.md"
        sections.append((filename, content))

    h1 = soup.find("h1")
    if not h1:
        return sections

    for element in h1.find_all_next():
        tag = element.name
        if tag is None:
            continue

        # Skip anything that lives inside Columns2 — handled above
        if id(element) in columns2_ids:
            continue

        # ── Section headings ──
        if tag in ("h2", "h3"):
            flush(current_heading, current_lines)
            current_heading = clean_text(element.get_text())
            current_lines   = []

        elif tag == "h4":
            text = clean_text(element.get_text())
            if text:
                current_lines.append(f"\n**{text}**")

        # ── Standard paragraph/list content ──
        elif tag == "p":
            if any(is_wahapedia_card(p) for p in element.parents):
                continue
            text = clean_text(element.get_text())
            if text and len(text) > 15:
                current_lines.append(text)

        elif tag in ("ul", "ol"):
            if any(is_wahapedia_card(p) for p in element.parents):
                continue
            for li in element.find_all("li", recursive=False):
                text = clean_text(li.get_text())
                if text:
                    current_lines.append(f"- {text}")

        elif tag == "table":
            if any(is_wahapedia_card(p) for p in element.parents):
                continue
            rows = []
            for row in element.find_all("tr"):
                cells = [clean_text(c.get_text()) for c in row.find_all(["td", "th"])]
                if any(c for c in cells):
                    rows.append(" | ".join(c for c in cells if c))
            if rows:
                current_lines.extend(rows)

        # ── Wahapedia custom card divs ──
        elif tag == "div":
            el_id = id(element)
            if el_id in processed_cards:
                continue

            classes = element.get("class", [])

            # Top-level card container (cgCardLCA, cgCardSM etc.)
            if any(cls.startswith("cgCard") for cls in classes):
                processed_cards.add(el_id)
                for child in element.find_all("div"):
                    processed_cards.add(id(child))

                card_text = extract_card_text(element)
                if card_text and len(card_text) > 30:
                    current_lines.append("")
                    current_lines.append(card_text)
                    current_lines.append("")

            # Ability/rule boxes (abWrap, frameLight, frameDark, redExample)
            elif any(cls.startswith(pfx)
                     for cls in classes
                     for pfx in ("abWrap", "frameLight", "frameDark", "redExample")):
                if any(id(p) in processed_cards for p in element.parents if hasattr(p, "get")):
                    continue
                processed_cards.add(el_id)
                box_text = clean_text(element.get_text(separator=" "))
                if box_text and len(box_text) > 30:
                    current_lines.append(box_text)

    flush(current_heading, current_lines)
    return sections

# ── Manifest helpers ──────────────────────────────────────────────────────────

def load_manifest():
    if MANIFEST.exists():
        with open(MANIFEST) as f:
            return json.load(f)
    return {}

def save_manifest(manifest):
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)

def content_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def write_if_changed(filepath, content, manifest, force=False):
    key   = filepath.name
    hash_ = content_hash(content)
    if not force and manifest.get(key) == hash_:
        return False
    filepath.write_text(content, encoding="utf-8")
    manifest[key] = hash_
    return True

# ── Main scraper ──────────────────────────────────────────────────────────────

def scrape_page(key, page_config, manifest, force=False):
    url = page_config["url"]
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}", file=sys.stderr)
        return 0, 0

    soup = BeautifulSoup(resp.content, "html.parser")

    for selector in REMOVE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    sections = split_into_sections(soup, page_config)

    written = 0
    skipped = 0
    for filename, content in sections:
        path = BLOCKS_DIR / filename
        if write_if_changed(path, content, manifest, force):
            written += 1
        else:
            skipped += 1

    return written, skipped

def run(pages=("core_rules", "leviathan"), force=False):
    manifest       = load_manifest()
    total_written  = 0
    total_skipped  = 0

    for key in pages:
        config = PAGES[key]
        print(f"Scraping {key} from {config['url']}...")
        written, skipped = scrape_page(key, config, manifest, force)
        print(f"  {key}: {written} written, {skipped} skipped")
        total_written += written
        total_skipped += skipped

    save_manifest(manifest)
    print(f"\nScrape complete: {total_written} written, {total_skipped} skipped (unchanged)")
    return total_written, total_skipped

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Wahapedia rules pages")
    parser.add_argument("--core",      action="store_true", help="Scrape core rules only")
    parser.add_argument("--leviathan", action="store_true", help="Scrape Leviathan only")
    parser.add_argument("--force",     action="store_true", help="Rewrite all files")
    args = parser.parse_args()

    if args.core:
        pages = ("core_rules",)
    elif args.leviathan:
        pages = ("leviathan",)
    else:
        pages = ("core_rules", "leviathan")

    run(pages=pages, force=args.force)
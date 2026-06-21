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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config

# Per-edition paths (blocks_dir / scrape_manifest) are resolved inside run()
# from config.get_edition(edition); nothing path-dependent lives at module scope.

# ── Pages to scrape ───────────────────────────────────────────────────────────

def build_pages(edition_code: str) -> dict:
    """Build the per-edition scrape targets (core rules + mission pack) from config."""
    ed = config.get_edition(edition_code)
    mp = ed["mission_pack"]
    return {
        "core_rules": {
            "url":      ed["core_rules_url"],
            "prefix":   "core_rules",
            "category": "Core_Rules",
            "source":   "Wahapedia_Core_Rules",
            "priority": 1,
        },
        "mission_pack": {
            "url":      mp["url"],
            "prefix":   mp["prefix"],
            "category": mp["category"],
            "source":   mp["source"],
            "priority": mp["priority"],   # mission-pack rules override core rules
        },
    }

# ── Nav/chrome selectors to remove before parsing ─────────────────────────────

REMOVE_SELECTORS = [
    "nav", "header", "footer", "script", "style",
    ".navBox", ".toc", "#toc",
    "[class*='settings']", "[class*='Settings']",
    "img",
    # Page chrome that otherwise gets vacuumed into the trailing section:
    "button", ".lfButton", "#btnDisableAds",   # "Disable Ads" controls
    ".tooltip_templates",                       # hidden hover-tooltip source — the
                                                # "X keyword is used in the following
                                                # datasheets" faction reference noise
    ".NavColumns3",                             # the page table-of-contents blob
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
    # Dice notation: after substitute_dice_images() turns <img d4.png> into "4",
    # the digit and its trailing "+" are separate nodes, so get_text(" ") yields
    # "4 +". Re-glue to "4+" (a digit followed only by whitespace then "+"). Safe
    # for rules prose \u2014 "+1"/"-1" modifiers are never preceded by a bare digit.
    text = re.sub(r"(\d)\s*\+", r"\1+", text)
    return text

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:60].strip("_")

# ── Dice-image → text ─────────────────────────────────────────────────────────

DICE_IMG = re.compile(r"^d([1-6])\.png$", re.I)

def substitute_dice_images(soup):
    """Replace Wahapedia dice-result images (d1.png … d6.png) with their digit.

    Wahapedia renders D6/D3 result values in stat tables (Wound roll, Pivot
    value, D3 conversion) as <img src=".../d{N}.png"> rather than text. The
    value is deterministically encoded in the filename, so we swap each such
    image for a NavigableString of its digit BEFORE REMOVE_SELECTORS strips all
    <img> tags. Without this, a "2+/3+/…" column collapses to a bare "+".
    Deterministic and exact — no LLM/vision (the pipeline model is text-only).
    Returns the number of images substituted.
    """
    n = 0
    for img in soup.find_all("img"):
        base = img.get("src", "").rsplit("/", 1)[-1]
        m = DICE_IMG.match(base)
        if m:
            img.replace_with(NavigableString(m.group(1)))
            n += 1
    return n

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

# ── Columns2 block extractor ──────────────────────────────────────────────────

# Walkthrough examples ("This model has a Move characteristic of 5"…", "A The
# Termagant unit is selected to fight…") are loose-text Columns2 blocks with no
# heading of their own. Un-handled they re-attach to the preceding rule (the old
# advance_moves.md pollution). They are not TOC rules, so we drop whole no-heading
# blocks that clearly read as an example. Conservative — these patterns never
# open a real rule body.
EXAMPLE_LEAD = re.compile(r"^(This|The same) (model|unit|VEHICLE|MONSTER)\b|^A The ")
EXAMPLE_PAT  = re.compile(
    r"has a [A-Z][a-z]+ characteristic of \d"
    r"|is selected to (fight|shoot|charge)"
    r"|has declared a charge"
    r"|begins the (Movement|Shooting|Charge|Fight) phase"
)

def looks_like_example(text):
    return bool(EXAMPLE_LEAD.match(text) or EXAMPLE_PAT.search(text[:400]))


def table_to_lines(element):
    """Row-format the *leaf* tables within (or equal to) `element`.

    Wahapedia wraps real tables in an outer layout <table>; the data lives in the
    innermost (leaf) table. We emit only leaves so a wrapper's rows aren't emitted
    2-3x. Dice values are already substituted in the DOM (substitute_dice_images),
    so "D6 RESULT REQUIRED" cells carry their N+ values.
    """
    if element.name == "table":
        leaves = [element] if not element.find("table") else \
                 [t for t in element.find_all("table") if not t.find("table")]
    else:
        leaves = [t for t in element.find_all("table") if not t.find("table")]
    lines = []
    for t in leaves:
        seen = set()
        for row in t.find_all("tr"):
            cells = [clean_text(c.get_text(separator=" ")) for c in row.find_all(["td", "th"])]
            line  = " | ".join(c for c in cells if c)
            if line and line not in seen:
                seen.add(line)
                lines.append(line)
    return lines


def extract_columns2_block(col2, page_config, seed_heading):
    """Parse ONE <div class="Columns2"> into per-rule sections.

    A block is a flat list of direct children mixing: inner h2/h3 rule headings
    (which delimit sub-sections), loose #text body prose interleaved with
    <br>/<a>/<span>, <ul>/<ol> lists, stat <table>s, and frame/BreakInsideAvoid
    summary boxes. The main split_into_sections walk drops the loose prose because
    Wahapedia doesn't wrap it in <p>; this parser reconstructs it.

    seed_heading titles any leading content before the first inner heading (and
    the whole block when it has none) — taken from the nearest preceding page
    heading by the caller.
    """
    sections = []
    prefix   = page_config["prefix"]
    category = page_config["category"]
    source   = page_config["source"]

    def flush(heading, lines):
        if not heading or not lines:
            return
        slug = slugify(heading)
        if is_skipped_slug(slug):
            return
        body = [l for l in lines if l and l.strip()]
        # 70-char floor (vs 80 in the main walk): drops decorative fragments but
        # keeps genuinely short self-titled steps — e.g. "Determine First Turn"
        # ("Each mission will tell you how to determine which player has the first
        # turn." is 76 chars), which would otherwise vanish from the sequence.
        if len(clean_text(" ".join(body))) < 70:
            return
        content = (
            f"# {heading}\n"
            f"**Category:** {category}  |  **Source:** {source}\n\n"
            + "\n".join(body)
        )
        sections.append((f"{prefix}_{slug}.md", content))

    current_heading = seed_heading
    current_lines   = []

    # Wahapedia lays a rule body out as a flat run of loose #text nodes interleaved
    # with inline keyword/term elements (<span class="kwb">AIRCRAFT</span>, <a>term
    # links</a>, emphasis). These are all one paragraph, so we accumulate the run in
    # prose_buf and emit it as a SINGLE line; appending each fragment straight to
    # current_lines (then "\n".join in flush) shattered the paragraph one keyword
    # per line. prose_buf is flushed at every real block boundary (heading, list,
    # table, card, self-titled box) so structure is preserved.
    prose_buf = []
    INLINE    = {"a", "span", "i", "b", "em", "strong", "sup", "sub"}

    def flush_prose():
        if prose_buf:
            joined = clean_text(" ".join(prose_buf))
            if joined:
                current_lines.append(joined)
            prose_buf.clear()

    for node in col2.children:
        if isinstance(node, NavigableString):
            text = clean_text(str(node))
            if text:
                prose_buf.append(text)
            continue
        name = node.name
        if not name:
            continue

        if name in ("h2", "h3"):
            flush_prose()
            flush(current_heading, current_lines)
            current_heading = clean_text(node.get_text(separator=" "))
            current_lines   = []
            continue
        if name == "br":
            continue

        classes = node.get("class", []) if hasattr(node, "get") else []
        if "redDiamond3" in classes:            # decorative step-number diamond
            continue

        # Inline keyword/term elements are part of the surrounding sentence —
        # coalesce them into the running paragraph rather than breaking the line.
        if name in INLINE:
            text = clean_text(node.get_text(separator=" "))
            if text:
                prose_buf.append(text)
            continue

        # Stat tables (Wound/Hit roll, Pivot value, D3) — row-format, don't flatten.
        # A wrapper div often holds BOTH prose and a table (the Dice intro + D3
        # table, the Pivots prose + pivot-value table); capture the non-table
        # prose first so it isn't dropped, then the table rows.
        if name == "table" or node.find("table"):
            flush_prose()
            if name != "table":
                prose = clean_text(" ".join(
                    str(s) for s in node.find_all(string=True)
                    if not s.find_parent("table")))
                if prose:
                    current_lines.append(prose)
            current_lines.extend(table_to_lines(node))
            continue
        if name in ("ul", "ol"):
            flush_prose()
            for li in node.find_all("li", recursive=False):
                text = clean_text(li.get_text(separator=" "))
                if text:
                    current_lines.append(f"- {text}")
            continue
        # Leviathan mission cards that sit inside a Columns2 (cgCard*)
        if any(str(c).startswith("cgCard") for c in classes):
            flush_prose()
            text = extract_card_text(node)
            if text:
                current_lines.append(text)
            continue

        # Self-titled box: a frame/BreakInsideAvoid box whose first element is its
        # own h2/h3 (e.g. the Devastating Wounds / Sustained Hits / Mortal Wounds
        # weapon-ability boxes nested inside a Columns2). The inner heading is NOT
        # a direct child of the Columns2, so it never delimits on its own — give
        # the box its own section instead of folding it into the parent rule.
        title_el = node.find(["h2", "h3"]) if hasattr(node, "find") else None
        if title_el:
            box_text = clean_text(node.get_text(separator=" "))
            title    = clean_text(title_el.get_text(" "))
            # Tolerate a leading step-number diamond: the mission-sequence boxes
            # read "1 Muster Armies Players muster…" while the inner h3 is just
            # "Muster Armies", so an exact startswith would miss and the whole
            # sequence would flatten into one section. Strip a leading "N " before
            # matching so each numbered step still gets its own section (slug from
            # the bare title, matching the per-step files the main walk used to
            # produce for the Columns3 Missions block).
            lead       = re.match(r"^\d+\s+", box_text)
            body_start = box_text[lead.end():] if lead else box_text
            if title and body_start.startswith(title) and len(body_start) - len(title) > 40:
                flush_prose()
                flush(current_heading, current_lines)
                body            = body_start[len(title):].strip()
                current_heading = title
                current_lines   = [body] if body else []
                continue

        # Default: block prose (p/div) and frame/BreakInsideAvoid summary boxes →
        # flattened text, each its own line. Flush the running inline paragraph
        # first so it isn't glued onto this block. An empty layout <div> carries no
        # text, so it must NOT flush — otherwise it would split a paragraph in two.
        text = clean_text(node.get_text(separator=" "))
        if text:
            flush_prose()
            current_lines.append(text)

    flush_prose()
    flush(current_heading, current_lines)
    return sections


# Wahapedia lays rule prose out in multi-column wrappers: Columns2 carries the
# bulk of the rules, Columns3 carries the army-construction sequence ("Muster Your
# Army": battle size, roster, faction, detachment, units, warlord — incl. the
# Enhancements/Epic-Hero/Battleline limits) and the datasheet-anatomy glossary
# (characteristic definitions). Both hold their bodies as the same loose
# #text/<br>/inline soup the main walk can't read, so the same block parser
# reconstructs both. extract_columns2_block is structure-agnostic — it just needs
# the list of column wrappers to drive.
COLUMN_BLOCK_CLASSES = ("Columns2", "Columns3")


def extract_all_column_blocks(soup, page_config):
    """Drive extract_columns2_block over EVERY Columns2 / Columns3 block.

    The core-rules page is ~52 Columns2 + 7 Columns3 blocks (Leviathan ~14
    Columns2); the original code parsed only the first Columns2. Each block's seed
    heading is the nearest preceding page heading (h1/h2/h3). No-heading blocks
    that read as walkthrough examples are dropped (Step 3). Same-slug output from
    a block and the main walk is reconciled by the merge-dedup pass downstream.
    """
    sections = []
    for cls in COLUMN_BLOCK_CLASSES:
        for col in soup.find_all("div", class_=cls):
            has_inner_heading = col.find(["h2", "h3"]) is not None
            if not has_inner_heading and looks_like_example(clean_text(col.get_text(separator=" "))):
                continue
            seed_el = col.find_previous(["h1", "h2", "h3"])
            seed    = clean_text(seed_el.get_text(separator=" ")) if seed_el else None
            sections.extend(extract_columns2_block(col, page_config, seed))
    return sections


def extract_loose_heading_sections(soup, page_config):
    """Capture rule prose that lives as loose text DIRECTLY under a heading,
    outside any Columns2 block.

    A handful of core-rules sections (Determining Visibility, Persisting Effects,
    Out-of-Phase Rules, the Transports intro …) keep their body as bare #text
    nodes interleaved with inline <a>/<span>/<i>, as direct children of the page's
    main content container — siblings of the headings and Columns2 blocks. The
    main walk iterates Tags only (find_all_next), so it never sees this loose
    text; the Columns2 pass doesn't cover it because it isn't inside a Columns2.

    We walk the content root's direct children, accumulate each contiguous run of
    loose text/inline under the current heading, and flush it. Columns2 blocks and
    classed block divs (frame boxes, cards, tables, lists) are handled elsewhere,
    so we flush-and-skip them here to avoid double-capture; the merge-dedup pass in
    split_into_sections folds any same-slug overlap.
    """
    prefix   = page_config["prefix"]
    category = page_config["category"]
    source   = page_config["source"]

    # Content root = the container holding the most h2/h3 as direct children.
    root, best = None, 0
    for div in soup.find_all("div"):
        n = len(div.find_all(["h2", "h3"], recursive=False))
        if n > best:
            best, root = n, div
    if root is None:
        return []

    sections = []
    inline   = {"a", "span", "i", "b", "em", "strong", "sup", "sub"}

    def flush(heading, lines):
        if not heading or not lines:
            return
        slug = slugify(heading)
        if is_skipped_slug(slug):
            return
        text = clean_text(" ".join(lines))
        if len(text) < 80:
            return
        content = (
            f"# {heading}\n"
            f"**Category:** {category}  |  **Source:** {source}\n\n"
            + text
        )
        sections.append((f"{prefix}_{slug}.md", content))

    current_heading = None
    current_lines   = []
    for node in root.children:
        if isinstance(node, NavigableString):
            t = clean_text(str(node))
            if t:
                current_lines.append(t)
            continue
        name = node.name
        if not name:
            continue
        if name in ("h2", "h3"):
            flush(current_heading, current_lines)
            current_heading = clean_text(node.get_text(separator=" "))
            current_lines   = []
        elif name in inline:
            t = clean_text(node.get_text(separator=" "))
            if t:
                current_lines.append(t)
        elif name == "br":
            continue
        else:
            # Block element (Columns2 / frame box / card / table / list) handled by
            # the other passes — flush the loose run before it, then skip it.
            flush(current_heading, current_lines)
            current_lines = []
    flush(current_heading, current_lines)
    return sections

# ── Main section splitter ─────────────────────────────────────────────────────

# Stored as SLUGS (matching slugify() output) — the previous space-separated form
# never matched, so these sections leaked through. Compared by prefix so mashed
# headings like "Hints and TipsObjective Markers..." (slug
# "hints_and_tipsobjective_markers...") are still caught.
SKIP_SECTIONS = {
    "books", "contents", "introduction", "hints_and_tips",
    "example_battlefields", "mission_map_key", "mission_generator",
    "card_decks", "only_war",
}

def is_skipped_slug(slug):
    """True if a section slug matches (or extends) any SKIP_SECTIONS slug."""
    return any(slug == s or slug.startswith(s) for s in SKIP_SECTIONS)

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

    # ── Extract every Columns2 / Columns3 block first ──
    # Each block holds its rule bodies as loose text nodes / br-separated
    # fragments / inline elements rather than p/li tags, so the main walk below
    # can't read them. extract_all_column_blocks parses all ~52 Columns2 + 7
    # Columns3 blocks (the page is built almost entirely from them); the main walk
    # then handles only content OUTSIDE any column block (standalone frame boxes,
    # cards, tables).
    col_sections = extract_all_column_blocks(soup, page_config)
    sections.extend(col_sections)

    # Loose rule prose that sits directly under a heading, outside any Columns2
    # (Determining Visibility, Persisting Effects, Out-of-Phase Rules, …).
    sections.extend(extract_loose_heading_sections(soup, page_config))

    # Build a set of all element IDs inside EVERY Columns2 / Columns3 so the main
    # walk skips them entirely — prevents double-processing.
    columns2_ids = set()
    for cls in COLUMN_BLOCK_CLASSES:
        for col in soup.find_all("div", class_=cls):
            columns2_ids.add(id(col))
            for el in col.find_all():
                columns2_ids.add(id(el))

    # Track processed card elements to avoid duplicating card content
    processed_cards = set()

    def flush(heading, lines):
        if not heading or not lines:
            return
        slug = slugify(heading)
        if is_skipped_slug(slug):
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
            # separator=" " so headings built from nested spans (e.g.
            # "Hints and Tips" + "Objective Markers...") don't mash into one token
            current_heading = clean_text(element.get_text(separator=" "))
            current_lines   = []

        elif tag == "h4":
            text = clean_text(element.get_text(separator=" "))
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
            # Wahapedia wraps every real table in an outer layout <table>; the
            # actual data lives in the innermost (leaf) table. Process leaves only
            # — walking a wrapper's find_all("tr") recurses into the nested table
            # and emits each row 2-3x (the "CAPTURE AND CONTROLProgressive Objective"
            # mashing). The leaf itself is reached separately in the walk.
            if element.find("table"):
                continue
            rows = []
            seen = set()
            for row in element.find_all("tr"):
                # separator=" " keeps adjacent cells from mashing together
                cells = [clean_text(c.get_text(separator=" ")) for c in row.find_all(["td", "th"])]
                line  = " | ".join(c for c in cells if c)
                if line and line not in seen:   # drop duplicate rows
                    seen.add(line)
                    rows.append(line)
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
                # Mark the whole box (incl. descendants) consumed: its text is
                # captured here via get_text, so the later walk must NOT re-process
                # inner headings/lists. Without this the box's own title heading
                # fires AFTER this flatten and opens an empty section that the NEXT
                # box then fills — the cross-rule off-by-one (Fall Back → Moving
                # Over Terrain, Advance → Desperate Escape, etc.). See spec.
                processed_cards.add(el_id)
                for child in element.find_all(True):
                    processed_cards.add(id(child))

                box_text = clean_text(element.get_text(separator=" "))
                if not (box_text and len(box_text) > 30):
                    pass
                else:
                    # Self-titled box? Wahapedia rule boxes lead with their own
                    # heading (h3, or h2.terrHeader2 for terrain). If so, the box
                    # IS its own section — flush the current one and retitle, so
                    # the rule body lands under its real name instead of bleeding
                    # onto whatever heading preceded the box.
                    title_el = element.find(["h2", "h3"])
                    title    = clean_text(title_el.get_text(" ")) if title_el else ""
                    if title and box_text.startswith(title):
                        flush(current_heading, current_lines)
                        body            = box_text[len(title):].strip()
                        current_heading = title
                        current_lines   = [body] if body else []
                    else:
                        current_lines.append(box_text)

            # Bare content prose (`BreakInsideAvoid`) that is NOT inside a frame
            # box and NOT the numbered first-Columns2 sequence. Wahapedia keeps
            # each rule's *detailed* prose here (the frame boxes are summary
            # panels); rules that have NO summary box — the Fight-phase activation
            # order, the numbered mission sequence, Measuring Distances, etc. —
            # otherwise vanish entirely. We capture the leaf prose block (NOT the
            # enclosing Columns2 wholesale, so its inner h3 sub-rules still split)
            # and, when self-titled, give it its own section; else it joins the
            # current heading. Dedup guards against the rules that ALSO have a
            # summary box, so we never double-ingest the same text.
            elif "BreakInsideAvoid" in classes:
                processed_cards.add(el_id)
                for child in element.find_all(True):
                    processed_cards.add(id(child))
                text = clean_text(element.get_text(separator=" "))
                if text and len(text) > 40 and text not in " ".join(current_lines):
                    title_el = element.find(["h2", "h3"])
                    title    = clean_text(title_el.get_text(" ")) if title_el else ""
                    if title and text.startswith(title) and len(text) - len(title) > 40:
                        flush(current_heading, current_lines)
                        body            = text[len(title):].strip()
                        current_heading = title
                        current_lines   = [body] if body else []
                    else:
                        current_lines.append(text)

    flush(current_heading, current_lines)

    # A rule can emit twice under the same slug — e.g. a summary frame box and a
    # bare detailed-prose block, or (for 5. Inflict Damage) the core rule in one
    # block and its Feel No Pain / Deadly Demise sub-abilities in another. MERGE
    # them: keep the longest as the base, then append any other version's body
    # that isn't already contained in it, so no unique rule text is dropped (a
    # plain longest-wins would have discarded the core Inflict Damage text).
    order  = list(dict.fromkeys(fn for fn, _ in sections))
    groups = {}
    for fn, content in sections:
        groups.setdefault(fn, []).append(content)
    merged = []
    for fn in order:
        versions = sorted(groups[fn], key=len, reverse=True)
        base     = versions[0]
        base_body_norm = re.sub(r"\s+", " ", base)
        for extra in versions[1:]:
            body = extra.split("\n\n", 1)[-1].strip()
            if body and re.sub(r"\s+", " ", body) not in base_body_norm:
                base += "\n" + body
                base_body_norm = re.sub(r"\s+", " ", base)
        merged.append((fn, base))
    return merged

# ── Manifest helpers ──────────────────────────────────────────────────────────

def load_manifest(manifest_path):
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {}

def save_manifest(manifest_path, manifest):
    with open(manifest_path, "w") as f:
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

def scrape_page(key, page_config, manifest, blocks_dir, force=False):
    url = page_config["url"]
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}", file=sys.stderr)
        return 0, 0, None

    soup = BeautifulSoup(resp.content, "html.parser")

    # Recover dice-result values from <img d{N}.png> BEFORE the img strip below.
    substitute_dice_images(soup)

    for selector in REMOVE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    sections = split_into_sections(soup, page_config)

    written  = 0
    skipped  = 0
    emitted  = set()   # filenames this page produced — drives the orphan sweep
    for filename, content in sections:
        emitted.add(filename)
        path = blocks_dir / filename
        if write_if_changed(path, content, manifest, force):
            written += 1
        else:
            skipped += 1

    return written, skipped, emitted

def run(pages=("core_rules", "mission_pack"), force=False, edition="10e"):
    ed            = config.get_edition(edition)
    blocks_dir    = ROOT / ed["blocks_dir"]
    manifest_path = ROOT / ed["scrape_manifest"]
    blocks_dir.mkdir(parents=True, exist_ok=True)

    all_pages      = build_pages(edition)
    manifest       = load_manifest(manifest_path)
    total_written  = 0
    total_skipped  = 0

    total_removed  = 0

    for key in pages:
        page_config = all_pages[key]
        print(f"Scraping {key} from {page_config['url']}...")
        written, skipped, emitted = scrape_page(key, page_config, manifest, blocks_dir, force)
        # Sweep orphaned sections for THIS page only — a heading the page no longer
        # carries leaves a stale {prefix}_{slug}.md behind. Skip the sweep when the
        # fetch failed (emitted is None) so a network blip can't wipe the corpus.
        removed = 0
        if emitted is not None:
            prefix = page_config["prefix"]
            for f in blocks_dir.glob(f"{prefix}_*.md"):
                if f.name not in emitted:
                    f.unlink()
                    manifest.pop(f.name, None)
                    removed += 1
        print(f"  {key}: {written} written, {skipped} skipped, {removed} swept")
        total_written += written
        total_skipped += skipped
        total_removed  += removed

    save_manifest(manifest_path, manifest)
    print(f"\nScrape complete: {total_written} written, {total_skipped} skipped (unchanged), "
          f"{total_removed} orphan blocks swept")
    return total_written, total_skipped

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Wahapedia rules pages")
    parser.add_argument("--core",         action="store_true", help="Scrape core rules only")
    parser.add_argument("--mission-pack", action="store_true",
                        help="Scrape the edition's mission pack only")
    # Hidden 10th-era alias for muscle memory; maps to the mission_pack target.
    parser.add_argument("--leviathan",    action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--force",        action="store_true", help="Rewrite all files")
    parser.add_argument("--edition",      default="10e", help="Edition code (default: 10e)")
    args = parser.parse_args()

    if args.core:
        pages = ("core_rules",)
    elif args.mission_pack or args.leviathan:
        pages = ("mission_pack",)
    else:
        pages = ("core_rules", "mission_pack")

    run(pages=pages, force=args.force, edition=args.edition)
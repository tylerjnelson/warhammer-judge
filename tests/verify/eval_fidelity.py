#!/usr/bin/env python3
"""
eval_fidelity.py — text-fidelity audit of the ingest corpus vs source HTML.
===========================================================================
`eval_completeness.py` answers "is each canonical rule's *opening sentence*
present and retrievable?" — its denominator is the Wahapedia TOC, so it is blind
to two failure modes:

  • ACCURACY  — a chunk could contain text the source never had (garbled inline
    spans, a mis-mapped dice image, two rules mashed across a boundary, an
    LLM-style hallucination). We assert every multi-word corpus *sentence* (and
    every reformatted table *cell* — where dice values live) appears verbatim,
    after normalisation, as a contiguous substring of the SOURCE text.

  • FULLNESS  — a rule's opening line can be ingested while the rest of its body
    is dropped (this is exactly how the Columns3 "Muster Your Army" army-build
    steps slipped through for months). We walk every SOURCE sentence and check
    it is present in the corpus, classifying each miss by the heading it sits
    under so intentional skips (intro, Hints & Tips, Example Battlefields, …)
    separate cleanly from genuine gaps that need REVIEW.

The source is put through the SAME transforms the scraper applies — dice-image
substitution, REMOVE_SELECTORS strip, clean_text — by importing scrape_rules, so
legitimate transforms never register as infidelity and the audit can't drift out
of sync with the scraper.

Run:
  python tests/verify/eval_fidelity.py                  # core + leviathan report
  python tests/verify/eval_fidelity.py --source core
  python tests/verify/eval_fidelity.py --strict         # exit nonzero on any REVIEW gap
                                                 # or any accuracy miss

Offline: reads cached HTML + the on-disk .md corpus. No network, no model.
"""

import argparse
import glob
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import scrape_rules as sr  # noqa: E402  (transforms + is_skipped_slug, kept in sync)
from bs4 import BeautifulSoup, NavigableString, Tag  # noqa: E402

log = logging.getLogger("fidelity")

# Per-source cached HTML + corpus glob. Mirrors eval_completeness's constants.
# Templated per edition; the cache holds the page the corpus was scraped from
# (data/html_cache/<edition>/<page key or mission-pack prefix>.html).
def sources_for(edition: str = "10e") -> dict:
    import config  # noqa: E402  (scripts/ is on sys.path; config sits beside it)
    ed = config.get_edition(edition)
    extras = ed.get("extra_core_pages", [])
    srcs = {
        "core": {
            "html":    f"data/html_cache/{edition}/core_rules.html",
            "glob":    f"data/rule_blocks/{edition}/core_rules_*.md",
            # extra core pages share the core_rules_ prefix; audit them separately
            "exclude": tuple(x["prefix"] + "_" for x in extras),
            "label":   "Wahapedia Core Rules",
        },
    }
    for x in extras:
        srcs[x["key"]] = {
            "html":  f"data/html_cache/{edition}/{x['key']}.html",
            "glob":  f"data/rule_blocks/{edition}/{x['prefix']}_*.md",
            "label": x["source"],
        }
    mp = ed["mission_pack"]
    srcs[mp["prefix"]] = {
        "html":  f"data/html_cache/{edition}/{mp['prefix']}.html",
        "glob":  f"data/rule_blocks/{edition}/{mp['prefix']}_*.md",
        "label": f"Wahapedia {mp['name']}",
        "drop_regions": mp.get("drop_regions", []),
    }
    return srcs

SOURCES = sources_for("10e")

HEAD = {"h1", "h2", "h3"}
ACC_MIN_WORDS = 8   # only assert accuracy on sentences distinctive enough to match
FULL_MIN_WORDS = 9  # ditto for source-side fullness sentences
SUBSTANCE_GRAM = 5  # a miss whose 5-gram is in corpus is a reworded duplicate


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def sentences(text: str):
    return re.split(r"(?<=[.!?])\s+", text)


# ── Source side (scraper-faithful) ────────────────────────────────────────────

def _clean_soup(html_path: str, drop_regions=()) -> BeautifulSoup:
    soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")
    sr.substitute_dice_images(soup)
    for selector in sr.REMOVE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()
    for start_id, end_id in drop_regions:      # page UI the scraper drops (not rules)
        sr.drop_page_region(soup, start_id, end_id)
    sr.strip_heading_numbers(soup)
    sr.badge_numbers_into_headings(soup)
    return soup


def source_full_text(soup: BeautifulSoup) -> str:
    return norm(sr.clean_text((soup.body or soup).get_text(" ")))


def source_sections(soup: BeautifulSoup) -> dict:
    """Map heading-slug -> cleaned body text, attributing each loose text node to
    the nearest preceding h1/h2/h3. Lets fullness misses be classified by section
    (intentional skip vs adjudicable rule). Leading preamble has slug ''."""
    buckets: dict = {}
    current = ""
    for node in (soup.body or soup).descendants:
        if isinstance(node, Tag):
            if node.name in HEAD:
                current = sr.slugify(sr.clean_text(node.get_text(" ")))
            continue
        if isinstance(node, NavigableString):
            parent = node.parent
            if parent is not None and parent.name in HEAD:
                continue  # the heading's own label, not body prose
            if str(node).strip():
                buckets.setdefault(current, []).append(str(node))
    return {slug: sr.clean_text(" ".join(parts)) for slug, parts in buckets.items()}


def section_is_skip(slug: str) -> bool:
    """A heading slug whose content is intentionally not ingested as a rule:
    the scraper's SKIP_SECTIONS, plus the leading preamble / page-title region."""
    if sr.is_skipped_slug(slug):
        return True
    if slug == "" or slug.startswith("warhammer_40_000") or slug.startswith("core_rules"):
        return True
    return False


def caps_lead(sentence: str) -> bool:
    """A navigation/section-divider blurb — leads with 2+ ALL-CAPS words
    (e.g. 'CORE CONCEPTS An introduction to the essential rules…')."""
    return sum(1 for w in sentence.split()[:6] if w.isupper() and len(w) > 1) >= 2


# Page scaffolding that survives REMOVE_SELECTORS as bare text but is not rule
# content: analytics/JS remnants and the interactive deck-selector widget labels.
NOISE_HINT = ("gtag", "noindex", "googletag", "maltsev", "function(",
              "press 'confirm'", "press confirm", "show gambit cards")


def is_noise(sentence: str) -> bool:
    low = sentence.lower()
    return "{" in low or any(h in low for h in NOISE_HINT)


# ALLOWLIST — normalised substrings of source sentences that legitimately are NOT
# ingested and never will be (worked-example fragments, tournament-companion
# lead-ins). Each keeps a genuine NEW gap from being masked while letting --strict
# pass on the known-irreducible residue. Add only after confirming the sentence is
# a non-rule; never to paper over a dropped rule.
ALLOW = (
    "as this model has a pivot value of 0",       # Pivot worked-example sentence
    "the remaining two termagants are too distant",  # Fast-dice worked example
    "these layouts were designed with a few key principles",  # terrain lead-in
    # Battle-round turn-alternation summary — a redundant styled `Corner14
    # float_center` callout; its substance ("the same player always takes the
    # first turn… each turn consists of phases…") is already in the ingested
    # core_rules_the_battle_round.md. Capturing all 74 Corner14 boxes would add
    # mostly-duplicate glossary panels, so this summary stays out by design.
    "once a player s turn has ended their opponent then starts",
    "once both players have completed a turn the battle round",
    # "Datasheet Name" anatomy label — 40-char description below the 80-char
    # ingest floor; the substantive datasheet-anatomy entries (profiles,
    # abilities, weapons, keywords, …) are all captured.
    "here you will find the name of the unit",
)


def is_allowed(normalised: str) -> bool:
    return any(a in normalised for a in ALLOW)


# ── Corpus side ───────────────────────────────────────────────────────────────

def _files(glob_pat, exclude=()):
    """Corpus files for a glob, minus any whose name starts with an excluded prefix."""
    return sorted(f for f in glob.glob(glob_pat) if not Path(f).name.startswith(tuple(exclude)))


def corpus_blob(glob_pat: str, exclude=()) -> str:
    out = []
    for f in _files(glob_pat, exclude):
        t = Path(f).read_text(encoding="utf-8")
        t = re.sub(r"^#.*$", "", t, flags=re.M)              # markdown titles
        t = re.sub(r"\*\*(Category|Source|Faction):.*$", "", t, flags=re.M)  # meta line
        out.append(t)
    return norm(" ".join(out))


def corpus_lines(glob_pat: str, exclude=()):
    """Yield (filename, prose_lines, table_rows) per corpus file, dropping chrome."""
    for f in _files(glob_pat, exclude):
        prose, rows = [], []
        for raw in Path(f).read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("**Category"):
                continue
            if " | " in line:
                rows.append(line)
            else:
                prose.append(line)
        yield Path(f).name, prose, rows


# ── Audits ────────────────────────────────────────────────────────────────────

# Structure the 11e mission-deck card renderer (scrape_rules.extract_ca7_card) adds
# around verbatim source text: list/OR/PLUS leads, a " — 2VP (UP TO 5VP)" tail,
# disposition matchups built from icon attributes, map-only deployment entries.
# Unwrapped before the verbatim check so the RULES text is still held to source.
_CARD_LEAD    = re.compile(r"^- (?:OR |PLUS )?")
_CARD_VP_TAIL = re.compile(r" — [+]?\d+VP.*$")
_CARD_MATCHUP = re.compile(r"^.+ \(you\) vs .+ \(opponent\): Primary Mission (.+)$")
_CARD_MAPONLY = re.compile(r"^(.+) \([a-z ]+: map image only\)$")
_CARD_META    = re.compile(r"^\*([^·*]+?)(?: · .*)?\*$")   # "*Primary Mission · Force Dispositions: …*"


def unwrap_rendered(line: str) -> str:
    line = _CARD_LEAD.sub("", line)
    for pat in (_CARD_MATCHUP, _CARD_MAPONLY, _CARD_META):
        m = pat.match(line)
        if m:
            return m.group(1)
    return _CARD_VP_TAIL.sub("", line)


def accuracy(src_full: str, glob_pat: str, exclude=()) -> dict:
    """Every multi-word corpus sentence + table cell must be verbatim in source."""
    s_ok = s_miss = 0
    cell_ok = cell_miss = 0
    miss_sent, miss_cell = [], []
    for fn, prose, rows in corpus_lines(glob_pat, exclude):
        for line in prose:
            for s in sentences(unwrap_rendered(line)):
                if len(s.split()) < ACC_MIN_WORDS:
                    continue
                if norm(s) in src_full:
                    s_ok += 1
                else:
                    s_miss += 1
                    miss_sent.append((fn, s))
        for row in rows:
            for cell in row.split(" | "):
                c = norm(cell)
                if len(c.split()) < 2:
                    continue
                if c in src_full:
                    cell_ok += 1
                else:
                    cell_miss += 1
                    miss_cell.append((fn, cell))
    return {
        "sent_ok": s_ok, "sent_miss": s_miss, "miss_sent": miss_sent,
        "cell_ok": cell_ok, "cell_miss": cell_miss, "miss_cell": miss_cell,
    }


def fullness(sections: dict, blob: str) -> dict:
    """Every source sentence should be in the corpus; classify the misses."""
    verbatim = reworded = skip = blurb = 0
    review = []
    for slug, text in sections.items():
        skip_section = section_is_skip(slug)
        for s in sentences(text):
            if len(s.split()) < FULL_MIN_WORDS:
                continue
            n = norm(s)
            if n in blob:
                verbatim += 1
                continue
            words = n.split()
            if any(" ".join(words[i:i + SUBSTANCE_GRAM]) in blob
                   for i in range(len(words) - SUBSTANCE_GRAM + 1)):
                reworded += 1
            elif skip_section or is_noise(s) or is_allowed(n):
                skip += 1
            elif caps_lead(s) or sr.looks_like_example(s):
                blurb += 1
            else:
                review.append((slug, s))
    return {
        "verbatim": verbatim, "reworded": reworded,
        "skip": skip, "blurb": blurb, "review": review,
    }


# ── Report ────────────────────────────────────────────────────────────────────

def audit(source: str, edition: str = "10e") -> dict:
    cfg  = sources_for(edition)[source]
    soup = _clean_soup(cfg["html"], cfg.get("drop_regions", ()))
    src_full = source_full_text(soup)
    secs = source_sections(soup)
    blob = corpus_blob(cfg["glob"], cfg.get("exclude", ()))

    acc = accuracy(src_full, cfg["glob"], cfg.get("exclude", ()))
    full = fullness(secs, blob)

    s_tot = acc["sent_ok"] + acc["sent_miss"]
    c_tot = acc["cell_ok"] + acc["cell_miss"]
    f_tot = full["verbatim"] + full["reworded"] + full["skip"] + full["blurb"] + len(full["review"])
    covered = full["verbatim"] + full["reworded"]

    log.info("")
    log.info("=" * 72)
    log.info("FIDELITY — %s %s (%s)", edition, source, cfg["label"])
    log.info("=" * 72)
    log.info("[ACCURACY] corpus text must be verbatim in source")
    log.info("    sentences : %d/%d verbatim   (%d not in source)",
             acc["sent_ok"], s_tot, acc["sent_miss"])
    log.info("    table cells: %d/%d verbatim   (%d not in source)",
             acc["cell_ok"], c_tot, acc["cell_miss"])
    for fn, s in acc["miss_sent"][:15]:
        log.warning("      ✗ ACC %s: %s", fn, s[:120])
    for fn, c in acc["miss_cell"][:15]:
        log.warning("      ✗ CELL %s: %s", fn, c[:120])

    log.info("[FULLNESS] source sentences present in corpus")
    log.info("    verbatim          : %d", full["verbatim"])
    log.info("    reworded (in corpus): %d", full["reworded"])
    log.info("    -> covered         : %d/%d (%.1f%%)",
             covered, f_tot, 100 * covered / max(f_tot, 1))
    log.info("    miss · skip section : %d   miss · section blurb: %d",
             full["skip"], full["blurb"])
    log.info("    REVIEW (adjudicable gap): %d", len(full["review"]))
    for slug, s in full["review"][:40]:
        log.warning("      ✗ REVIEW [%s] %s", slug or "(preamble)", s[:120])

    ok = acc["sent_miss"] == 0 and acc["cell_miss"] == 0 and not full["review"]
    log.info("RESULT %s: accuracy %s, %d REVIEW gap(s)",
             source, "OK" if (acc["sent_miss"] == 0 and acc["cell_miss"] == 0) else "FAIL",
             len(full["review"]))
    return {
        "source": source, "ok": ok,
        "accuracy_misses": acc["sent_miss"] + acc["cell_miss"],
        "review_gaps": len(full["review"]),
        "coverage_pct": 100 * covered / max(f_tot, 1),
        "detail": {"accuracy": acc, "fullness": full},
    }


def run(sources, strict: bool = False, edition: str = "10e") -> int:
    if not logging.getLogger().handlers and not log.handlers:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    rc = 0
    for source in sources:
        res = audit(source, edition)
        if strict and not res["ok"]:
            rc = 1
    return rc


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Text-fidelity audit (accuracy + fullness).")
    ap.add_argument("--source", default="all",
                    help="a source key of the edition (10e: core, leviathan; "
                         "11e: core, rules_appendix, chapter_approved) or 'all'")
    ap.add_argument("--strict", action="store_true",
                    help="exit nonzero on any accuracy miss or REVIEW gap")
    ap.add_argument("--edition", default="10e")
    args = ap.parse_args()
    srcs = list(sources_for(args.edition)) if args.source == "all" else [args.source]
    sys.exit(run(srcs, strict=args.strict, edition=args.edition))

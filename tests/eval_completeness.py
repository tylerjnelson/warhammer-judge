#!/usr/bin/env python3
"""
eval_completeness.py — corpus completeness + recall harness for The Judge.
==========================================================================
Where `eval_retrieval.py` asserts behaviour on a curated set of *known*
queries, this harness measures the two things that set has no denominator for:

  1. INGEST completeness — does every canonical 10e Core rule actually have its
     rule *body* present somewhere in the ingested corpus? (Catches the scraper
     silently dropping prose and keeping only summary boxes / example captions.)
  2. RECALL — for the rules that ARE ingested, does the real retrieval path
     (process_query → retrieve → rules slice → assemble) surface the rule's body
     when a user types the rule's name?

Ground truth is Wahapedia's own table of contents — the `.NavColumns3` sidebar
in the cached core-rules HTML (`data/html_cache/10e/core_rules.html`). That nav
lists every heading Wahapedia defines, so it is the canonical denominator. For
each TOC anchor we extract a *fingerprint*: the normalised opening sentence of
that rule's body, taken straight from the source HTML. A rule is INGESTED iff
its fingerprint appears in the corpus, and RECALLED iff a name query surfaces a
chunk containing it. Because the fingerprint comes from the source (not from our
own chunks), a miss is a real dropped-content / ranking bug, not a tautology.

Run:
  python tests/eval_completeness.py             # full report
  python tests/eval_completeness.py -v          # also list every PASS
  python tests/eval_completeness.py --strict     # exit nonzero if any rule missing
  python tests/eval_completeness.py --no-recall  # ingest check only (fast)

This is offline: it reads the cached HTML + on-disk .md corpus and drives app.py
assembly headless. No network, no Wahapedia fetch.
"""

import argparse
import glob
import logging
import re
import sys
import warnings
from pathlib import Path

logging.getLogger("streamlit").setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).resolve().parent))        # for eval_retrieval
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # for app / config

from eval_retrieval import final_context  # noqa: E402  (reuses the real assembly path)
import app     # noqa: E402
import config  # noqa: E402

HTML_CACHE = "data/html_cache/10e/core_rules.html"
CORPUS_GLOB = "data/rule_blocks/10e/core_rules_*.md"

# Leviathan (mission pack) has no .NavColumns3 TOC, so its ground-truth
# denominator is built from the page's own h2/h3 headings plus the mission-card
# (cgCardLCA) titles. See load_ground_truth_leviathan().
LEV_HTML = "data/html_cache/10e/leviathan.html"
LEV_CORPUS_GLOB = "data/rule_blocks/10e/leviathan_*.md"

# TOC entries that are navigation/section scaffolding, not adjudicable rules with
# their own body prose. ALL-CAPS phase headers (COMMAND PHASE, …) are detected
# automatically; this set is the remaining non-rule pointers.
META_SKIP = {"Books", "Introduction"}

# Fingerprint length: long enough to be distinctive, short enough to survive the
# inline-span splitting difference between source HTML text nodes and the
# space-joined .md text.
FP_LEN = 55


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def clean_query(name: str) -> str:
    """'2. Wound Roll' -> 'Wound Roll'; strip the leading 'N.' and smart quotes."""
    n = re.sub(r"^\s*\d+\.\s*", "", name)
    return n.replace("‘", "").replace("’", "").strip()


# ── Ground truth from the cached TOC ──────────────────────────────────────────

def load_ground_truth():
    """Return (rules, sections, meta_skipped).

    rules    : list of (name, fingerprint) for adjudicable rules.
    sections : list of all-caps phase-header names (reported, not asserted).
    """
    from bs4 import BeautifulSoup
    html = Path(HTML_CACHE).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.select(".NavColumns3")
    if not nav:
        sys.exit(f"FATAL: no .NavColumns3 TOC in {HTML_CACHE}")
    nav = nav[0]

    rules, sections, meta = [], [], []
    seen = set()
    for a in nav.find_all("a"):
        name = a.get_text(" ", strip=True)
        href = a.get("href", "")
        if not href.startswith("#"):
            continue
        anchor = href[1:]
        if anchor in seen:
            continue
        seen.add(anchor)

        if name in META_SKIP:
            meta.append(name)
            continue
        if name.isupper():
            sections.append(name)
            continue

        el = soup.find(id=anchor) or soup.find(attrs={"name": anchor})
        fp = None
        if el:
            nxt = el.find_next(string=lambda s: s and len(s.strip()) > 40)
            if nxt:
                fp = norm(nxt)[:FP_LEN]
        rules.append((name, fp))
    return rules, sections, meta


def load_ground_truth_leviathan():
    """Ground truth for the Leviathan mission pack (no .NavColumns3 TOC).

    Denominator = the page's own h2/h3 headings (the 14-step game sequence +
    tournament rules) plus every mission-card title (div.cgCardLCA → .cgHeader).
    Fingerprint each from the source HTML the same way as core: the normalised
    opening body sentence. Returns (rules, sections, meta) to match the core
    loader's shape; Leviathan headings are Title-Case (no ALL-CAPS phase headers),
    so `sections` stays empty.
    """
    from bs4 import BeautifulSoup
    html = Path(LEV_HTML).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    rules, meta, seen = [], [], set()

    # Heading-delimited rules (skip the Books/JS scaffolding heading).
    for h in soup.find_all(["h2", "h3"]):
        name = h.get_text(" ", strip=True)
        if not name or name in seen:
            continue
        if name in META_SKIP:
            meta.append(name)
            continue
        seen.add(name)
        nxt = h.find_next(string=lambda s: s and len(s.strip()) > 40
                          and "function" not in s and "{" not in s)
        fp = norm(nxt)[:FP_LEN] if nxt else None
        # Skip interactive deck-selector widgets — several h3s ("Selected Secondary
        # Missions", "… Secondary Mission Deck") are JS UI whose only "body" is the
        # button text "choose one gambit card and press confirm", not a rule.
        if fp and ("gambit card" in fp or "press confirm" in fp):
            meta.append(name)
            continue
        rules.append((name, fp))

    # Mission cards: title from .cgHeader, fingerprint from the card's own body.
    for card in soup.find_all("div", class_="cgCardLCA"):
        hdr = card.find(class_="cgHeader")
        if not hdr:
            continue
        name = hdr.get_text(" ", strip=True)
        if not name or name in seen:
            continue
        seen.add(name)
        body = card.find(class_="cgText")
        fp = norm(body.get_text(" ", strip=True))[:FP_LEN] if body else None
        rules.append((name, fp))

    return rules, [], meta


# ── Checks ────────────────────────────────────────────────────────────────────

def load_corpus_text(glob_pat: str = CORPUS_GLOB) -> str:
    return norm(" ".join(
        Path(f).read_text(encoding="utf-8") for f in glob.glob(glob_pat)
    ))


def recall_hit(name: str, fp: str, edition: str) -> bool:
    """Does a name query surface a chunk containing the rule body fingerprint?"""
    for mp_mode in (True, False):  # a rule is recalled if either toggle finds it
        chunks = final_context(clean_query(name), edition, mp_mode)
        blob = norm(" ".join(c["text"] for c in chunks))
        if fp and fp in blob:
            return True
    return False


# ── Report ────────────────────────────────────────────────────────────────────

def run(edition: str, verbose: bool, do_recall: bool, strict: bool,
        source: str = "core") -> int:
    if source == "leviathan":
        rules, sections, meta = load_ground_truth_leviathan()
        corpus = load_corpus_text(LEV_CORPUS_GLOB)
        gt_label = f"Wahapedia Leviathan headings + mission cards ({LEV_HTML})"
    else:
        rules, sections, meta = load_ground_truth()
        corpus = load_corpus_text(CORPUS_GLOB)
        gt_label = f"Wahapedia core-rules TOC ({HTML_CACHE})"

    print(f"\nCorpus completeness + recall — edition {edition} · source {source}")
    print(f"Ground truth: {gt_label}")
    print("=" * 72)
    print(f"TOC rules: {len(rules)} | section headers: {len(sections)} | "
          f"meta skipped: {len(meta)}")
    if sections:
        print(f"  (section headers, not asserted: {', '.join(sections)})")
    print("-" * 72)

    no_fp, ingested, missing = [], [], []
    for name, fp in rules:
        if not fp:
            no_fp.append(name)
        elif fp in corpus:
            ingested.append((name, fp))
        else:
            missing.append((name, fp))

    n_rules = len(rules)
    print(f"\n[1] INGEST COMPLETENESS — rule body present in corpus")
    print(f"    {len(ingested)}/{n_rules} ingested"
          + (f"  ·  {len(no_fp)} no-fingerprint" if no_fp else ""))
    if missing:
        print(f"\n    MISSING BODIES ({len(missing)}) — in source HTML, absent from corpus:")
        for name, fp in missing:
            print(f"      ✗ {name:42}  «{fp}…»")
    if no_fp:
        print(f"\n    NO FINGERPRINT ({len(no_fp)}) — couldn't extract opening prose:")
        for name in no_fp:
            print(f"      ? {name}")
    if verbose and ingested:
        print(f"\n    INGESTED ({len(ingested)}):")
        for name, _ in ingested:
            print(f"      ✓ {name}")

    recalled = []
    if do_recall and ingested:
        print(f"\n[2] RECALL@{config.TOP_K} — name query surfaces the ingested rule body")
        not_recalled = []
        for name, fp in ingested:
            if recall_hit(name, fp, edition):
                recalled.append(name)
            else:
                not_recalled.append(name)
        print(f"    {len(recalled)}/{len(ingested)} ingested rules retrievable by name")
        if not_recalled:
            print(f"\n    INGESTED BUT NOT RECALLED ({len(not_recalled)}) — ranking gap:")
            for name in not_recalled:
                print(f"      ✗ {name}")
        if verbose and recalled:
            print(f"\n    RECALLED ({len(recalled)}):")
            for name in recalled:
                print(f"      ✓ {name}")
    elif not do_recall:
        print(f"\n[2] RECALL — skipped (--no-recall)")

    print("\n" + "=" * 72)
    print(f"INGEST:  {len(ingested)}/{n_rules} rule bodies present"
          + (f"  ({len(missing)} missing, {len(no_fp)} unknown)" if (missing or no_fp) else ""))
    if do_recall and ingested:
        print(f"RECALL:  {len(recalled)}/{len(ingested)} ingested rules retrievable by name")
        e2e = len(recalled)
        print(f"END-TO-END: {e2e}/{n_rules} canonical rules both ingested AND retrievable "
              f"({100*e2e//n_rules}%)")
    print()

    if strict and (missing or (do_recall and ingested and len(recalled) < len(ingested))):
        return 1
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Corpus completeness + recall eval for The Judge.")
    ap.add_argument("--edition", default="10e")
    ap.add_argument("-v", "--verbose", action="store_true", help="list every PASS too")
    ap.add_argument("--no-recall", action="store_true", help="ingest check only (skip retrieval)")
    ap.add_argument("--strict", action="store_true", help="exit nonzero on any miss")
    ap.add_argument("--source", default="core", choices=["core", "leviathan"],
                    help="which corpus to measure (default: core)")
    args = ap.parse_args()
    sys.exit(run(args.edition, args.verbose, not args.no_recall, args.strict, args.source))

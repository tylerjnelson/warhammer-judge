"""
watcher.py — Wahapedia Change Detection + Pipeline Orchestration
================================================================
Runs daily via cron at 3AM:
  0 3 * * * cd /home/warhammer/app && /home/warhammer/venv/bin/python scripts/watcher.py >> logs/watcher.log 2>&1

Two independent change detection paths:
  1. HTML rules pages (Core Rules, Leviathan) — scraped unconditionally
     every day. The scraper's manifest detects actual content changes.
  2. Wahapedia CSV exports — checked via Last_update.csv hash. Only
     triggers the full ETL + download pipeline when CSVs have changed.

Ingest runs if either source has new content. If nothing changed
anywhere, the script exits after the scrape check with no further work.

Can also be run manually:
  python scripts/watcher.py --force    # force full sync regardless
"""

import sys
import re
import hashlib
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT        = Path(__file__).resolve().parent.parent
CSV_DIR     = ROOT / "data" / "raw_csv"
ARCHIVE_DIR = ROOT / "data" / "raw_csv_archive"
HASH_FILE   = ROOT / "data" / "last_synced_hash.txt"
LOG_DIR     = ROOT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Wahapedia CSV file list ───────────────────────────────────────────────────

BASE_URL = "https://wahapedia.ru/wh40k10ed"

CSV_FILES = [
    "Datasheets.csv",
    "Datasheets_models.csv",
    "Datasheets_wargear.csv",
    "Datasheets_abilities.csv",
    "Datasheets_options.csv",
    "Datasheets_unit_composition.csv",
    "Datasheets_models_cost.csv",
    "Datasheets_keywords.csv",
    "Abilities.csv",
    "Stratagems.csv",
    "Enhancements.csv",
    "Factions.csv",
    "Source.csv",
    "Last_update.csv",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def md5(content: bytes) -> str:
    return hashlib.md5(content).hexdigest()

def read_hash() -> str:
    if HASH_FILE.exists():
        return HASH_FILE.read_text().strip()
    return ""

def write_hash(hash_: str):
    HASH_FILE.write_text(hash_)

# ── Change detection ──────────────────────────────────────────────────────────

def fetch_remote_hash() -> tuple[str, bytes]:
    """Fetch Last_update.csv and return (md5_hash, raw_content)."""
    url = f"{BASE_URL}/Last_update.csv"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return md5(resp.content), resp.content
    except requests.RequestException as e:
        log(f"[ERROR] Failed to fetch Last_update.csv: {e}")
        sys.exit(1)

# ── Archive ───────────────────────────────────────────────────────────────────

def archive_current_csvs():
    """Copy current raw CSVs to archive dir before overwriting."""
    if not CSV_DIR.exists():
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for f in CSV_DIR.glob("*.csv"):
        shutil.copy2(f, ARCHIVE_DIR / f.name)
    log(f"Archived {len(list(CSV_DIR.glob('*.csv')))} CSVs to {ARCHIVE_DIR}")

# ── Download ──────────────────────────────────────────────────────────────────

def download_csvs():
    """Download all Wahapedia CSVs to data/raw_csv/."""
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    for filename in CSV_FILES:
        url = f"{BASE_URL}/{filename}"
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            (CSV_DIR / filename).write_bytes(resp.content)
        except requests.RequestException as e:
            log(f"[WARN] Failed to download {filename}: {e}")
            failed.append(filename)

    if failed:
        log(f"[WARN] {len(failed)} file(s) failed to download: {failed}")
    else:
        log(f"Downloaded {len(CSV_FILES)} CSVs successfully")

    return len(failed) == 0

# ── Pipeline steps ────────────────────────────────────────────────────────────

def run_scrape() -> bool:
    """
    Scrape Core Rules and Leviathan HTML pages.
    Returns True if any files were written (i.e. content changed).
    """
    log("Scraping rules pages...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "scrape_rules.py"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[ERROR] Scraper failed:\n{result.stderr}")
        sys.exit(1)

    # Parse written count from output: "Scrape complete: N written, M skipped"
    match = re.search(r"(\d+) written", result.stdout)
    written = int(match.group(1)) if match else 0
    return written > 0

def run_etl():
    log("Running ETL pipeline...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "etl.py"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[ERROR] ETL failed:\n{result.stderr}")
        sys.exit(1)

def run_ingest():
    log("Running ingest pipeline...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "ingest.py"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[ERROR] Ingest failed:\n{result.stderr}")
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────

def run(force=False):
    log("=" * 50)
    log("Watcher starting")

    # ── Step 1: Always scrape HTML rules pages ──
    # Last_update.csv has no awareness of HTML page changes.
    # The scraper's own manifest detects actual content changes cheaply.
    scrape_changed = run_scrape()

    # ── Step 2: Check Wahapedia CSV exports for changes ──
    new_hash, _  = fetch_remote_hash()
    local_hash   = read_hash()
    csv_changed  = force or (new_hash != local_hash)

    if force:
        log("--force flag set: running full sync")
    elif csv_changed:
        log("CSV change detected")
    else:
        log("No CSV changes detected")

    # ── Step 3: Exit early if nothing changed anywhere ──
    if not csv_changed and not scrape_changed:
        log("No changes detected anywhere. Exiting.")
        log("=" * 50)
        return

    # ── Step 4: If CSVs changed, run full download + ETL ──
    if csv_changed:
        archive_current_csvs()

        log("Downloading CSVs from Wahapedia...")
        success = download_csvs()
        if not success:
            log("[ERROR] Some CSVs failed to download. Aborting to preserve last good state.")
            log("=" * 50)
            sys.exit(1)

        run_etl()

    # ── Step 5: Re-embed everything that changed (CSV blocks + scraped files) ──
    run_ingest()

    # ── Step 6: Record new CSV hash only after successful sync ──
    if csv_changed:
        write_hash(new_hash)
        log(f"CSV hash updated to {new_hash[:8]}...")

    log("Sync complete.")
    log("=" * 50)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wahapedia change watcher")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip change detection and run full sync regardless"
    )
    args = parser.parse_args()
    run(force=args.force)
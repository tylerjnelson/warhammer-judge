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

ROOT    = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Per-edition locals (base_url / csv_dir / archive_dir / hash_file) are resolved
# inside run() from config.get_edition(code) for each active edition.

# ── Wahapedia CSV file list ───────────────────────────────────────────────────

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

def read_hash(hash_file) -> str:
    if hash_file.exists():
        return hash_file.read_text().strip()
    return ""

def write_hash(hash_file, hash_: str):
    hash_file.write_text(hash_)

# ── Change detection ──────────────────────────────────────────────────────────

def fetch_remote_hash(base_url, code) -> tuple[str, bytes]:
    """Fetch Last_update.csv and return (md5_hash, raw_content)."""
    url = f"{base_url}/Last_update.csv"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return md5(resp.content), resp.content
    except requests.RequestException as e:
        log(f"[{code}] [ERROR] Failed to fetch Last_update.csv: {e}")
        sys.exit(1)

# ── Archive ───────────────────────────────────────────────────────────────────

def archive_current_csvs(csv_dir, archive_dir, code):
    """Copy current raw CSVs to the edition archive dir before overwriting."""
    if not csv_dir.exists():
        return
    archive_dir.mkdir(parents=True, exist_ok=True)
    for f in csv_dir.glob("*.csv"):
        shutil.copy2(f, archive_dir / f.name)
    log(f"[{code}] Archived {len(list(csv_dir.glob('*.csv')))} CSVs to {archive_dir}")

# ── Download ──────────────────────────────────────────────────────────────────

def download_csvs(base_url, csv_dir, code):
    """Download all Wahapedia CSVs to the edition CSV dir."""
    csv_dir.mkdir(parents=True, exist_ok=True)
    failed = []
    for filename in CSV_FILES:
        url = f"{base_url}/{filename}"
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            (csv_dir / filename).write_bytes(resp.content)
        except requests.RequestException as e:
            log(f"[{code}] [WARN] Failed to download {filename}: {e}")
            failed.append(filename)

    if failed:
        log(f"[{code}] [WARN] {len(failed)} file(s) failed to download: {failed}")
    else:
        log(f"[{code}] Downloaded {len(CSV_FILES)} CSVs successfully")

    return len(failed) == 0

# ── Pipeline steps ────────────────────────────────────────────────────────────

def run_scrape(code) -> bool:
    """
    Scrape the edition's Core Rules and mission-pack HTML pages.
    Returns True if any files were written (i.e. content changed).
    """
    log(f"[{code}] Scraping rules pages...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "scrape_rules.py", "--edition", code],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[{code}] [ERROR] Scraper failed:\n{result.stderr}")
        sys.exit(1)

    # Parse written count from output: "Scrape complete: N written, M skipped"
    match = re.search(r"(\d+) written", result.stdout)
    written = int(match.group(1)) if match else 0
    return written > 0

def run_etl(code):
    log(f"[{code}] Running ETL pipeline...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "etl.py", "--edition", code],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[{code}] [ERROR] ETL failed:\n{result.stderr}")
        sys.exit(1)

def run_ingest(code):
    log(f"[{code}] Running ingest pipeline...")
    result = subprocess.run(
        [sys.executable, ROOT / "scripts" / "ingest.py", "--edition", code],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"[{code}] [ERROR] Ingest failed:\n{result.stderr}")
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────

def run(force=False):
    log("=" * 50)
    log("Watcher starting")

    # Service every active edition in turn. Inactive editions (e.g. 11e until
    # release) are absent from active_editions(), so the loop skips them with no
    # code change needed at launch — only the config flag flips.
    for code in config.active_editions():
        sync_edition(code, force=force)

    log("=" * 50)

def sync_edition(code, force=False):
    """Run the full change-detection + pipeline for a single edition."""
    ed          = config.get_edition(code)
    base_url    = ed["wahapedia_base"]
    csv_dir     = ROOT / ed["csv_dir"]
    archive_dir = ROOT / ed["csv_archive_dir"]
    hash_file   = ROOT / ed["hash_file"]

    log(f"[{code}] --- {ed['label']} ---")

    # ── Step 1: Always scrape HTML rules pages ──
    # Last_update.csv has no awareness of HTML page changes.
    # The scraper's own manifest detects actual content changes cheaply.
    scrape_changed = run_scrape(code)

    # ── Step 2: Check Wahapedia CSV exports for changes ──
    new_hash, _  = fetch_remote_hash(base_url, code)
    local_hash   = read_hash(hash_file)
    csv_changed  = force or (new_hash != local_hash)

    if force:
        log(f"[{code}] --force flag set: running full sync")
    elif csv_changed:
        log(f"[{code}] CSV change detected")
    else:
        log(f"[{code}] No CSV changes detected")

    # ── Step 3: Exit early if nothing changed anywhere ──
    if not csv_changed and not scrape_changed:
        log(f"[{code}] No changes detected anywhere. Skipping.")
        return

    # ── Step 4: If CSVs changed, run full download + ETL ──
    if csv_changed:
        archive_current_csvs(csv_dir, archive_dir, code)

        log(f"[{code}] Downloading CSVs from Wahapedia...")
        success = download_csvs(base_url, csv_dir, code)
        if not success:
            log(f"[{code}] [ERROR] Some CSVs failed to download. Aborting to preserve last good state.")
            sys.exit(1)

        run_etl(code)

    # ── Step 5: Re-embed everything that changed (CSV blocks + scraped files) ──
    run_ingest(code)

    # ── Step 6: Record new CSV hash only after successful sync ──
    if csv_changed:
        write_hash(hash_file, new_hash)
        log(f"[{code}] CSV hash updated to {new_hash[:8]}...")

    log(f"[{code}] Sync complete.")

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
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
import json
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
STATUS_FILE = LOG_DIR / "watcher_status.json"

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
    "Detachment_abilities.csv",
    "Detachments.csv",
    "Factions.csv",
    "Source.csv",
    "Last_update.csv",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

class SyncError(Exception):
    """A step failed for one edition. Raised instead of sys.exit so run() can record
    it and still service the remaining editions (a 10e network error must not skip 11e)."""

def log_stderr(code, step, result):
    """Always surface a child's stderr — warnings on a successful run used to be dropped."""
    if result.stderr.strip():
        log(f"[{code}] {step} stderr:\n{result.stderr.strip()}")

def write_status(code, ok, detail):
    """Record this run per edition in logs/watcher_status.json. last_success only moves
    on a clean run, so a stale value there is the signal that syncing has been failing."""
    try:
        status = json.loads(STATUS_FILE.read_text()) if STATUS_FILE.exists() else {}
    except (OSError, ValueError):
        status = {}
    now   = datetime.now().isoformat(timespec="seconds")
    entry = status.get(code, {})
    entry.update(last_run=now, last_result="ok" if ok else "error", detail=detail)
    if ok:
        entry["last_success"] = now
    status[code] = entry
    STATUS_FILE.write_text(json.dumps(status, indent=2) + "\n")

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
        raise SyncError(f"Failed to fetch Last_update.csv: {e}") from e

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

def run_scrape(code) -> tuple[bool, bool]:
    """
    Scrape the edition's Core Rules and mission-pack HTML pages.
    Returns (changed, fetch_failed): changed = any files written; fetch_failed = the
    scraper exited 2 (a page couldn't be fetched — HTML not refreshed this run).
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
    # Always surface stderr — fetch errors used to be printed there with exit 0,
    # so 60 nights of DNS failures logged as a harmless "0 written, 0 skipped".
    log_stderr(code, "scraper", result)
    if result.returncode == 2:
        # Fetch failure (network/HTTP): HTML pages are stale this run, but the CSV
        # path is independent, so warn and continue rather than abort.
        log(f"[{code}] [WARN] Scraper could not fetch one or more pages — HTML rules not refreshed this run")
    elif result.returncode != 0:
        raise SyncError(f"Scraper failed (exit {result.returncode})")

    # Parse written count from output: "Scrape complete: N written, M skipped"
    match = re.search(r"(\d+) written", result.stdout)
    written = int(match.group(1)) if match else 0
    return written > 0, result.returncode == 2

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
    log_stderr(code, "ETL", result)
    if result.returncode != 0:
        raise SyncError(f"ETL failed (exit {result.returncode})")

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
    log_stderr(code, "ingest", result)
    if result.returncode != 0:
        raise SyncError(f"Ingest failed (exit {result.returncode})")

# ── Main ──────────────────────────────────────────────────────────────────────

def run(force=False):
    log("=" * 50)
    log("Watcher starting")

    # Service every active edition in turn. Inactive editions (e.g. 11e until
    # release) are absent from active_editions(), so the loop skips them with no
    # code change needed at launch — only the config flag flips.
    failed = []
    for code in config.active_editions():
        try:
            detail = sync_edition(code, force=force)
            write_status(code, True, detail)
        except SyncError as e:
            log(f"[{code}] [ERROR] {e} — edition skipped, last good state preserved")
            write_status(code, False, str(e))
            failed.append(code)
        except Exception as e:                  # unexpected bug: record it, keep going
            log(f"[{code}] [ERROR] Unexpected {type(e).__name__}: {e}")
            write_status(code, False, f"unexpected {type(e).__name__}: {e}")
            failed.append(code)

    log(f"Watcher finished: {'FAILED for ' + ', '.join(failed) if failed else 'all editions OK'}")
    log("=" * 50)
    if failed:
        sys.exit(1)

def sync_edition(code, force=False):
    """Run the full change-detection + pipeline for a single edition. Returns a short
    outcome string for the status file; raises SyncError on any failed step."""
    ed          = config.get_edition(code)
    base_url    = ed["wahapedia_base"]
    csv_dir     = ROOT / ed["csv_dir"]
    archive_dir = ROOT / ed["csv_archive_dir"]
    hash_file   = ROOT / ed["hash_file"]

    log(f"[{code}] --- {ed['label']} ---")

    # ── Step 1: Always scrape HTML rules pages ──
    # Last_update.csv has no awareness of HTML page changes.
    # The scraper's own manifest detects actual content changes cheaply.
    scrape_changed, scrape_failed = run_scrape(code)

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
        if scrape_failed:
            raise SyncError("HTML rules page fetch failed (CSV check OK, no CSV changes)")
        return "no changes"

    # ── Step 4: If CSVs changed, run full download + ETL ──
    if csv_changed:
        archive_current_csvs(csv_dir, archive_dir, code)

        log(f"[{code}] Downloading CSVs from Wahapedia...")
        success = download_csvs(base_url, csv_dir, code)
        if not success:
            raise SyncError("Some CSVs failed to download; aborted to preserve last good state")

        run_etl(code)

    # ── Step 5: Re-embed everything that changed (CSV blocks + scraped files) ──
    run_ingest(code)

    # ── Step 6: Record new CSV hash only after successful sync ──
    if csv_changed:
        write_hash(hash_file, new_hash)
        log(f"[{code}] CSV hash updated to {new_hash[:8]}...")

    log(f"[{code}] Sync complete.")
    if scrape_failed:
        # CSV work above is done and kept; still record the edition as failed so a
        # broken rules-page fetch can't hide behind a healthy CSV sync.
        raise SyncError("HTML rules page fetch failed (CSV sync completed)")
    return "synced (" + ", ".join(
        [x for x, on in (("csv", csv_changed), ("html", scrape_changed)) if on]) + ")"

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
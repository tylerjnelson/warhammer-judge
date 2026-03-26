"""
etl.py — Wahapedia CSV → Markdown Rule-Block ETL Pipeline
==========================================================
Reads all Wahapedia CSV exports from data/raw_csv/, performs relational
joins, and writes self-contained Markdown chunks to data/rule_blocks/.

Output files:
  unit_{datasheet_id}.md        — full joined unit block
  stratagem_{id}.md             — individual stratagem chunk
  enhancement_{id}.md           — individual enhancement chunk

Incremental: on re-runs, only rewrites files whose content has changed.
A manifest file (data/rule_blocks/manifest.json) tracks content hashes.

Usage:
  python scripts/etl.py                  # run from /home/warhammer/app
  python scripts/etl.py --force          # ignore manifest, rewrite all
"""

import os
import sys
import re
import json
import hashlib
import argparse
from pathlib import Path

import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).resolve().parent.parent   # /home/warhammer/app
CSV_DIR    = ROOT / "data" / "raw_csv"
BLOCKS_DIR = ROOT / "data" / "rule_blocks"
MANIFEST   = BLOCKS_DIR / "manifest.json"

BLOCKS_DIR.mkdir(parents=True, exist_ok=True)

# ── CSV loading ───────────────────────────────────────────────────────────────

READ_OPTS = dict(sep="|", encoding="utf-8-sig", dtype=str)

def load_csvs():
    """Load all Wahapedia CSVs into a dict of DataFrames. Silent on success."""
    files = {
        "datasheets":   "Datasheets.csv",
        "models":       "Datasheets_models.csv",
        "wargear":      "Datasheets_wargear.csv",
        "abilities_ds": "Datasheets_abilities.csv",
        "options":      "Datasheets_options.csv",
        "composition":  "Datasheets_unit_composition.csv",
        "costs":        "Datasheets_models_cost.csv",
        "keywords":     "Datasheets_keywords.csv",
        "abilities":    "Abilities.csv",
        "stratagems":   "Stratagems.csv",
        "enhancements": "Enhancements.csv",
        "factions":     "Factions.csv",
        "source":       "Source.csv",
    }
    dfs = {}
    for key, filename in files.items():
        path = CSV_DIR / filename
        if not path.exists():
            print(f"[WARN] Missing CSV: {filename} — skipping", file=sys.stderr)
            dfs[key] = pd.DataFrame()
            continue
        df = pd.read_csv(path, **READ_OPTS)
        # Strip empty trailing column Wahapedia sometimes appends
        df = df.loc[:, ~df.columns.str.fullmatch(r"\s*")]
        # Strip whitespace from all string values
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        dfs[key] = df
    return dfs

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
    """Write content only if it differs from the last run. Returns True if written."""
    key   = filepath.name
    hash_ = content_hash(content)
    if not force and manifest.get(key) == hash_:
        return False
    filepath.write_text(content, encoding="utf-8")
    manifest[key] = hash_
    return True

# ── Text helpers ──────────────────────────────────────────────────────────────

def safe(val, fallback="—"):
    """Return val as a clean string, or fallback if null/empty."""
    if pd.isna(val) or str(val).strip() in ("", "nan", "None"):
        return fallback
    return str(val).strip()

def strip_html(text):
    """Strip HTML tags and normalise whitespace for clean LLM context."""
    if not text or text == "—":
        return text
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode common HTML entities
    text = (text
            .replace('&amp;',  '&')
            .replace('&lt;',   '<')
            .replace('&gt;',   '>')
            .replace('&nbsp;', ' ')
            .replace('&#39;',  "'")
            .replace('&quot;', '"'))
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ── Lookup helpers ────────────────────────────────────────────────────────────

def faction_name(faction_id, factions_df):
    if factions_df.empty:
        return faction_id
    row = factions_df[factions_df["id"] == faction_id]
    if row.empty:
        return faction_id
    return safe(row.iloc[0]["name"], faction_id)

def source_info(source_id, source_df):
    """Returns (date_str, is_errata) for a source_id."""
    if source_df.empty or pd.isna(source_id) or source_id == "—":
        return ("", False)
    row = source_df[source_df["id"] == source_id]
    if row.empty:
        return ("", False)
    r           = row.iloc[0]
    errata_date = safe(r.get("errata_date", ""), "")
    version     = safe(r.get("version", ""), "")
    date_str    = errata_date if errata_date not in ("", "—") else version
    is_errata   = errata_date not in ("", "—")
    return (date_str, is_errata)

# ── Unit block builder ────────────────────────────────────────────────────────

def build_unit_block(ds_row, dfs):
    """Joins all tables for one datasheet and returns a Markdown string."""
    ds_id      = safe(ds_row["id"])
    name       = safe(ds_row["name"])
    faction_id = safe(ds_row["faction_id"], "")
    role       = safe(ds_row.get("role", ""), "")
    loadout    = safe(ds_row.get("loadout", ""), "")
    transport  = safe(ds_row.get("transport", ""), "")
    ldr_head   = safe(ds_row.get("leader_head", ""), "")
    ldr_foot   = safe(ds_row.get("leader_footer", ""), "")
    dmg_w      = safe(ds_row.get("damaged_w", ""), "")
    dmg_desc   = safe(ds_row.get("damaged_description", ""), "")
    source_id  = safe(ds_row.get("source_id", ""), "")

    fname               = faction_name(faction_id, dfs["factions"])
    ver_date, is_errata = source_info(source_id, dfs["source"])

    lines = []

    # ── Header ──
    lines.append(f"# {name}")
    lines.append(f"**Faction:** {fname}  |  **Role:** {role}  |  **Source:** {source_id}")
    if ver_date:
        lines.append(
            f"**Version/Errata Date:** {ver_date}" + (" *(errata)*" if is_errata else "")
        )
    lines.append("")

    # ── Stat lines ──
    models_df   = dfs["models"]
    unit_models = (
        models_df[models_df["datasheet_id"] == ds_id].sort_values("line")
        if not models_df.empty else pd.DataFrame()
    )
    if not unit_models.empty:
        lines.append("## Stats")
        lines.append("| Model | M | T | Sv | Inv | W | Ld | OC | Base |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for _, m in unit_models.iterrows():
            inv      = safe(m["inv_sv"], "—")
            inv_desc = safe(m.get("inv_sv_descr", ""), "")
            if inv_desc and inv_desc != "—":
                inv = f"{inv} ({inv_desc})"
            base      = safe(m["base_size"], "—")
            base_desc = safe(m.get("base_size_descr", ""), "")
            if base_desc and base_desc != "—":
                base = f"{base} ({base_desc})"
            lines.append(
                f"| {safe(m['name'])} | {safe(m['M'])} | {safe(m['T'])} | "
                f"{safe(m['Sv'])} | {inv} | {safe(m['W'])} | "
                f"{safe(m['Ld'])} | {safe(m['OC'])} | {base} |"
            )
        lines.append("")

    # ── Unit composition ──
    comp_df   = dfs["composition"]
    unit_comp = (
        comp_df[comp_df["datasheet_id"] == ds_id].sort_values("line")
        if not comp_df.empty else pd.DataFrame()
    )
    if not unit_comp.empty:
        lines.append("## Unit Composition")
        for _, c in unit_comp.iterrows():
            lines.append(f"- {safe(c['description'])}")
        lines.append("")

    # ── Points costs ──
    costs_df   = dfs["costs"]
    unit_costs = (
        costs_df[costs_df["datasheet_id"] == ds_id].sort_values("line")
        if not costs_df.empty else pd.DataFrame()
    )
    if not unit_costs.empty:
        lines.append("## Points Costs")
        for _, c in unit_costs.iterrows():
            desc = safe(c["description"], "")
            cost = safe(c["cost"], "")
            if desc and cost:
                lines.append(f"- {desc}: **{cost} pts**")
            elif cost:
                lines.append(f"- {cost} pts")
        lines.append("")

    # ── Wargear / weapons ──
    wg_df   = dfs["wargear"]
    unit_wg = (
        wg_df[wg_df["datasheet_id"] == ds_id].sort_values(["line", "line_in_wargear"])
        if not wg_df.empty else pd.DataFrame()
    )
    if not unit_wg.empty:
        lines.append("## Wargear")
        lines.append("| Weapon | Range | Type | A | BS/WS | S | AP | D |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for _, w in unit_wg.iterrows():
            wname = safe(w["name"])
            desc  = safe(w.get("description", ""), "")
            dice  = safe(w.get("dice", ""), "")
            label = f"{dice}× {wname}" if dice and dice != "—" else wname
            lines.append(
                f"| {label} | {safe(w['range'])} | {safe(w['type'])} | "
                f"{safe(w['A'])} | {safe(w['BS_WS'])} | {safe(w['S'])} | "
                f"{safe(w['AP'])} | {safe(w['D'])} |"
            )
            if desc and desc != "—":
                lines.append(f"|   | *{desc}* | | | | | | |")
        lines.append("")

    # ── Wargear options ──
    opts_df   = dfs["options"]
    unit_opts = (
        opts_df[opts_df["datasheet_id"] == ds_id].sort_values("line")
        if not opts_df.empty else pd.DataFrame()
    )
    if not unit_opts.empty:
        lines.append("## Wargear Options")
        for _, o in unit_opts.iterrows():
            lines.append(f"- {safe(o['description'])}")
        lines.append("")

    # ── Abilities ──
    ab_ds_df = dfs["abilities_ds"]
    unit_ab  = (
        ab_ds_df[ab_ds_df["datasheet_id"] == ds_id].sort_values("line")
        if not ab_ds_df.empty else pd.DataFrame()
    )
    if not unit_ab.empty:
        ab_lookup = (
            dfs["abilities"].set_index("id")
            if not dfs["abilities"].empty else pd.DataFrame()
        )
        for ab_type in ["Datasheet", "Wargear", "Faction", "Core"]:
            typed = unit_ab[unit_ab["type"] == ab_type]
            if typed.empty:
                continue
            lines.append(f"## {ab_type} Abilities")
            for _, ab in typed.iterrows():
                ab_name = safe(ab["name"], "")
                ab_desc = safe(ab.get("description", ""), "")

                # Resolve empty descriptions via Abilities.csv lookup
                if (not ab_desc or ab_desc == "—") and not ab_lookup.empty:
                    ab_id = safe(ab.get("ability_id", ""), "")
                    if ab_id and ab_id != "—" and ab_id in ab_lookup.index:
                        val = ab_lookup.loc[ab_id, "description"]
                        ab_desc = safe(val.iloc[0] if hasattr(val, "iloc") else val, "")

                # Strip HTML from ability descriptions
                ab_desc = strip_html(ab_desc)

                # Suppress blank ability names
                if not ab_name or ab_name == "—":
                    ab_name = "(Unnamed)"

                param       = safe(ab.get("parameter", ""), "")
                model_scope = safe(ab.get("model", ""), "")

                header = f"**{ab_name}**"
                if model_scope and model_scope != "—":
                    header += f" *(applies to: {model_scope})*"
                if param and param != "—":
                    header += f" — {param}"

                lines.append(header)
                if ab_desc and ab_desc != "—":
                    lines.append(f"> {ab_desc}")
                lines.append("")

    # ── Leader rules ──
    if ldr_head and ldr_head != "—":
        lines.append("## Leader")
        lines.append(strip_html(ldr_head))
        if ldr_foot and ldr_foot != "—":
            lines.append("")
            lines.append(strip_html(ldr_foot))
        lines.append("")

    # ── Loadout / transport ──
    if loadout and loadout != "—":
        lines.append("## Loadout")
        lines.append(strip_html(loadout))
        lines.append("")
    if transport and transport != "—":
        lines.append("## Transport")
        lines.append(strip_html(transport))
        lines.append("")

    # ── Damaged threshold ──
    if dmg_w and dmg_w != "—":
        lines.append("## Damaged")
        lines.append(f"*Damaged threshold: {dmg_w} wounds remaining*")
        if dmg_desc and dmg_desc != "—":
            lines.append(f"> {strip_html(dmg_desc)}")
        lines.append("")

    # ── Keywords ──
    kw_df   = dfs["keywords"]
    unit_kw = (
        kw_df[kw_df["datasheet_id"] == ds_id]
        if not kw_df.empty else pd.DataFrame()
    )
    if not unit_kw.empty:
        faction_kws = [k for k in unit_kw[unit_kw["is_faction_keyword"].str.upper() == "TRUE"]["keyword"].tolist() if isinstance(k, str)]
        other_kws   = [k for k in unit_kw[unit_kw["is_faction_keyword"].str.upper() != "TRUE"]["keyword"].tolist() if isinstance(k, str)]
        lines.append("## Keywords")
        if faction_kws:
            lines.append(f"**Faction:** {', '.join(faction_kws)}")
        if other_kws:
            lines.append(f"**Other:** {', '.join(other_kws)}")
        lines.append("")

    return "\n".join(lines)

# ── Stratagem block builder ───────────────────────────────────────────────────

def build_stratagem_block(row, factions_df):
    faction_id  = safe(row["faction_id"], "")
    fname       = faction_name(faction_id, factions_df)
    name        = safe(row["name"])
    strat_type  = safe(row.get("type", ""), "")
    cp_cost     = safe(row.get("cp_cost", ""), "")
    turn        = safe(row.get("turn", ""), "")
    phase       = safe(row.get("phase", ""), "")
    detachment  = safe(row.get("detachment", ""), "")
    description = strip_html(safe(row.get("description", ""), ""))
    legend      = safe(row.get("legend", ""), "")

    lines = []
    lines.append(f"# Stratagem: {name}")
    lines.append(f"**Faction:** {fname}  |  **Type:** {strat_type}  |  **Cost:** {cp_cost} CP")
    if detachment and detachment != "—":
        lines.append(f"**Detachment:** {detachment}")
    if turn and turn != "—":
        when = turn + (f" — {phase}" if phase and phase != "—" else "")
        lines.append(f"**When:** {when}")
    if legend and legend != "—":
        lines.append(f"*{legend}*")
    lines.append("")
    if description and description != "—":
        lines.append(description)
    lines.append("")
    return "\n".join(lines)

# ── Enhancement block builder ─────────────────────────────────────────────────

def build_enhancement_block(row, factions_df):
    faction_id  = safe(row["faction_id"], "")
    fname       = faction_name(faction_id, factions_df)
    name        = safe(row["name"])
    cost        = safe(row.get("cost", ""), "")
    detachment  = safe(row.get("detachment", ""), "")
    description = strip_html(safe(row.get("description", ""), ""))
    legend      = safe(row.get("legend", ""), "")

    lines = []
    lines.append(f"# Enhancement: {name}")
    lines.append(f"**Faction:** {fname}  |  **Cost:** {cost} pts")
    if detachment and detachment != "—":
        lines.append(f"**Detachment:** {detachment}")
    if legend and legend != "—":
        lines.append(f"*{legend}*")
    lines.append("")
    if description and description != "—":
        lines.append(description)
    lines.append("")
    return "\n".join(lines)

# ── Schema validation ─────────────────────────────────────────────────────────

EXPECTED_COLUMNS = {
    "datasheets":   {"id", "name", "faction_id", "source_id"},
    "models":       {"datasheet_id", "line", "M", "T", "Sv", "W"},
    "wargear":      {"datasheet_id", "name", "range", "A", "S", "AP", "D"},
    "abilities_ds": {"datasheet_id", "ability_id", "name", "type"},
    "keywords":     {"datasheet_id", "keyword", "is_faction_keyword"},
    "stratagems":   {"faction_id", "name", "id", "cp_cost", "turn", "phase", "description"},
    "enhancements": {"faction_id", "id", "name", "description"},
    "factions":     {"id", "name"},
    "source":       {"id", "name", "errata_date"},
}

def validate_schema(dfs):
    """Check expected columns exist. Silent on success, prints errors to stderr."""
    ok = True
    for key, expected_cols in EXPECTED_COLUMNS.items():
        df = dfs.get(key, pd.DataFrame())
        if df.empty:
            continue
        missing = expected_cols - set(df.columns)
        if missing:
            print(f"[ERROR] {key}: missing columns: {missing}", file=sys.stderr)
            ok = False
    return ok

# ── Main ETL run ──────────────────────────────────────────────────────────────

def run(force=False):
    # 1. Load CSVs
    dfs = load_csvs()

    # 2. Validate schema — exit loudly on mismatch
    if not validate_schema(dfs):
        print("[FATAL] Schema validation failed. Aborting.", file=sys.stderr)
        sys.exit(1)

    # 3. Load manifest for incremental tracking
    manifest = {} if force else load_manifest()

    # 4. Generate blocks
    written = 0
    skipped = 0

    # ── Unit blocks ──
    for _, row in dfs["datasheets"].iterrows():
        # Skip virtual/composite datasheets — no standalone rules
        if safe(row.get("virtual", ""), "").upper() == "TRUE":
            skipped += 1
            continue
        ds_id   = safe(row["id"])
        content = build_unit_block(row, dfs)
        path    = BLOCKS_DIR / f"unit_{ds_id}.md"
        if write_if_changed(path, content, manifest, force):
            written += 1
        else:
            skipped += 1

    # ── Stratagem blocks ──
    for _, row in dfs["stratagems"].iterrows():
        strat_id = safe(row["id"])
        content  = build_stratagem_block(row, dfs["factions"])
        path     = BLOCKS_DIR / f"stratagem_{strat_id}.md"
        if write_if_changed(path, content, manifest, force):
            written += 1
        else:
            skipped += 1

    # ── Enhancement blocks ──
    for _, row in dfs["enhancements"].iterrows():
        enh_id  = safe(row["id"])
        content = build_enhancement_block(row, dfs["factions"])
        path    = BLOCKS_DIR / f"enhancement_{enh_id}.md"
        if write_if_changed(path, content, manifest, force):
            written += 1
        else:
            skipped += 1

    # 5. Save manifest
    save_manifest(manifest)

    print(f"ETL complete: {written} written, {skipped} skipped (unchanged or virtual)")
    return written, skipped

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wahapedia ETL pipeline")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rewrite all rule-blocks regardless of manifest (full rebuild)"
    )
    args = parser.parse_args()
    run(force=args.force)
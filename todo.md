# The Judge — Open Items / TODO

Single index of every deferred, follow-up, or "known residual" item still open across
`spec/` and the eval memories, with pointers back to the design-of-record. Anything not
listed here is either shipped or an intentional non-goal.

Legend: **P1** = has real product/operational impact · **P2** = quality/robustness ·
**P3** = cleanup / nice-to-have. Status as of 2026-07-30.

---

## 1. Dual-edition — 11th Edition launch (data-gated)

The single largest deferred block. All Stage-1 plumbing is built and live. **2026-07-30
recon: `wh40k11ed` is LIVE and serving real, evolving 11th data** — so this is now
buildable (core-rules + CSVs), not fully data-blocked. See recon findings below.

- **[P1] Ship 11th Edition (Stage 2).** Fill the `11e` `<FILL>` config values (URLs,
  mission-pack identity), validate the two transformation spots against real data, build
  the collection, flip `active` then later `default`.
  → `spec/dual-edition.md` §11 (the executable launch runbook), §12 (known risks)
  - **2026-10-10 RE-RECON (plan changed — supersedes the 2026-07-30 notes below):**
    - ✅ `wh40k11ed` `Last_update` now **2026-10-10** (actively maintained; newer than frozen 10e). Whole dataset now genuinely 11th: Stratagems/Enhancements/Detachments/Detachment_abilities ALL now differ from 10e (were identical in July).
    - ✅ Roster curated: **1,501 units (11e) vs 1,712 (10e)** — 167 dropped, 21 added. Built corpus-reconciliation orphan-sweep handles removals on `--reset`.
    - 🔴 **NEW required ETL fix — quantity-tiered points.** Headers still byte-identical (EXPECTED_COLUMNS safe), BUT `Datasheets_models_cost.csv` now encodes 11e tiered pricing as label rows (`desc="YOUR 1ST TO 2ND UNITS COST", cost=""` → `1 model|115` → `YOUR 3RD+ UNIT COSTS` → `1 model|130`). **2,369 label rows in 11e vs 0 in 10e; 423 multi-tier units.** `etl.py` points loop (`build_unit_block` ~L250-259, `if desc and cost / elif cost`) SILENTLY DROPS desc-with-empty-cost rows → multi-tier units render as contradictory bare `1 model: X/Y pts` with tier context lost. **Fix block builder before 11e ingest.** (Was previously assessed "no ETL change needed" — that is now wrong.)
    - 🟢 **Leviathan mission pack NOW LIVE for 11th — DECIDED 2026-10-10: INCLUDE it (reverses July core-rules-only deferral).** `wh40k11ed/the-rules/leviathan/` is distinct from 10e, 11th-tagged, full content: 132 `cgCard`+49 `cgCardLCA` (existing scraper classes), 48 Primary/228 Secondary mission mentions, 14-step sequence, NEW `Gambit Deck` card type (151×). Fill 11e `mission_pack.*` with Leviathan (name=Leviathan, url=.../the-rules/leviathan/), scrape `--mission-pack`, **validate the new Gambit-deck cards + frameDark on scrape.** (Contradicts spec §1 "Leviathan does not carry over.") `matched-play` slug still a 10e mirror — ignore.
    - ⚠️ HTML scraper core-rules work (§11.3) unchanged; page grew 637KB→773KB.
  - **2026-07-30 original recon (HISTORICAL — see re-recon above):** slug confirmed live; CSV data real 11th w/ unchanged schema; wargear/abilities/detachment divergence; concluded no ETL change (now superseded) and deferred mission decks as not-yet-published (now superseded).
- **[P2] 11e maintenance dependency:** if 11e introduces a *new faction-bearing category*
  that 10e lacks, add it to `FACTION_SCOPED_CATEGORIES` or the P2 cross-faction leak
  re-opens for that category.
  → `spec/multi-unit-clarification-and-faction-scope.md` (P2, "11th edition" subsection) · `spec/dual-edition.md` §12

## 2. LLM backend — resilience & the model swap

Roster (2026-10-12): **gpt-oss-120b = prod, qwen/qwen3.8-27b = automatic backup**
(`config.LLM_BACKUP_MODEL`); every other model retired. Failover, OTPM back-off and the
per-model `retry-after` wait shipped 2026-10-13 (`serving._call_llm`).

- **[P1] Watch gpt-oss-120b's 200K TPD under sustained load.** Billed reasoner; the daily
  budget (~65 questions/day) is the tight limit. When it runs out, requests now fail over
  to qwen (its own ~70/day bucket). Watch `journalctl -u thejudge` for `served by backup
  model` / `failing over` lines — frequent ones mean users are getting the 40/43 model.
  → `spec/free-llm-providers.md` §5a/§5
- **[P2] Adopt prompt v1 (rules 4/6 split "rule absent" vs "apply a stated rule").** A/B on
  qwen fixed its Q20/Q31 over-refusals 3/3 with guardrails intact (Q27/Q34/Q37/Q6). Needs a
  full 43-Q run on BOTH models before shipping — it also changes gpt-oss-120b's behaviour.
  Lifts the backup from 40/43 toward 42/43.
- **[P3] Reword eval Q12** to "how many VP do you score that turn": qwen reads "VP for
  destroying" as the kill alone (5) and treats the Tactical +1 as separate — defensible.
- **[P3] Re-evaluate system-prompt rule 10 (VP-stacking crutch).** Added for retired
  qwen3-32b; gpt-oss-120b resolves Q12 natively. A/B on Q11/Q12/Q19 present-vs-removed;
  harmless to leave. → `eval-followups` memory item 3
- **[P3] Eval-method hygiene:** use `collect_model_answers.py --no-cap` (mirrors prod) or
  `--tpm-room` for model runs — a fixed output cap truncates reasoning models and
  under-rates them. → `eval-followups` memory item 4

## 3. Retrieval quality

- **[P2] Layer 3 embedding-upgrade (DEFERRED).** Swap `all-MiniLM-L6-v2` →
  `bge-small-en-v1.5` / `e5-small-v2` to lift zero-keyword paraphrases over
  `SIMILARITY_THRESHOLD`. Two xfail `GAPS` cases track it (coherency 0.282, indirect-fire
  0.339); BM25 correctly doesn't fire on them. Requires a full re-index (free to adopt for
  11e since its data isn't built yet). Re-run `eval_retrieval.py` — GAPS should flip
  xfail→XPASS. → `spec/retrieval.md` Layer 3 "Embedding-upgrade half"
- **[P2] Mission-pack bleed / mission-relevance gating.** With the toggle ON, broadly-themed
  mission chunks (e.g. SWEEP AND CLEAR) still rank into generic rules questions. Harmless
  today (the LLM dismisses them) but the named next candidate: only surface mission-pack
  chunks for mission-themed queries. → `spec/retrieval.md` Layer 1b residual, Track B″/B′ residuals
- **[P2] Two core ranking gaps: Fight, Deployment Abilities.** Ingested but rank below
  `TOP_K` for a name lookup. Ranking, not corpus. → `spec/retrieval.md` status line · `spec/archive/scraper-rework.md` "Outcome"
- **[P3] Widen the referenced-rule seed vocabulary (`_USR_RULES`) for lone-operative /
  stealth.** The Painboy work added these to the *ability-boost* path
  (`_ABILITY_KEYWORD_SURFACES`), but the `seed_referenced_rules` seeding path still can't
  seed a USR that has no standalone rule chunk. → `spec/reranker.md` §9 step 5 · `eval-followups` memory item 1 (FIXED half)
- **[P3] BM25 cold-start (~22s on first query after boot).** Optionally persist/pickle the
  index keyed on collection count, or warm the cache at startup.
  → `spec/retrieval.md` Layer 3 lexical "Known cost"
- **[P3] Pin Pile-In@1 (compound-query) as a regression case in `eval_retrieval.py`** so the
  segment-maxpool win can't silently rot. Segmenter marker set is curated; a dependency
  parser (`advcl`) is the upgrade path if it proves brittle.
  → `spec/reranker.md` §11 "Watch-items / future"
- **[P3] Unit-query latency ~1.9–2.5s on large pools.** → `spec/reranker.md` §9 step 5

## 4. Config / eval-set overfit (the one structural debt the refactor left open)

- **[P2] Grow the eval set to de-risk knob overfit.** ~30 retrieval knobs are individually
  justified but collectively tuned against one ~30–43-question set, so the eval gate is the
  only safety net against a regression from nudging one. The refactor made the knobs legible
  (regrouped `config.py` + `assert_invariants`) but explicitly left the *data* problem open.
  → `spec/retrieval-pipeline-refresh.md` §6 · `spec/archive/retrieval-pipeline-audit.md` C14
- **[P3] Re-tuning the ~30 knobs** was deliberately out of scope of the structural refresh —
  a separate, later effort if the expanded eval set surfaces a better operating point.
  → `spec/retrieval-pipeline-refresh.md` §9

## 5. Corpus / ingest follow-ups

- **[P2] Datasheet→rule link tables (deferred).** Download + wire
  `Datasheets_detachment_abilities.csv`, `Datasheets_stratagems.csv`,
  `Datasheets_enhancements.csv`, `Datasheets_leader.csv` so unit blocks cross-link their
  legal detachment rules / stratagems / leader attachments and feed the dep-graph
  (`scripts/build_dep_graph.py`). → `spec/army-detachment-rules.md` §5
- **[P3] Raw-HTML-in-list-line ETL bug.** Some unit datasheet blocks carry raw markup in a
  list line (`…:<ul style="list-style-type:circle"><li>1 'ard case</li>…`) — an ETL
  list-rendering issue, distinct from the (fixed) keyword fragmentation.
  → `spec/archive/chunk-fragmentation.md` "Side note"
- **[P3] Confirm the choppy dense-keyword-prose residual is fully closed.** `scraper-rework`
  flagged army-build steps stored one-token-per-line; the later `chunk-fragmentation` fix
  (prose_buf coalescing) appears to resolve it — confirm and close, or re-open if the
  `split_subrules` regression risk it warned about still stands.
  → `spec/archive/scraper-rework.md` "Known residual" ↔ `spec/archive/chunk-fragmentation.md`

## 6. Test coverage / process

- **[P3] Manual live-render eyeball.** The live Streamlit path (chat answer, source-expander,
  clarification buttons, conversation save/load) is the one path no automated test fully
  covers; `test_app_boot.py` covers boot + clarification render only.
  → `spec/archive/retrieval-pipeline-refresh-implementation.md` "Final state"
- **[P3] Clarification UX nicety:** an "apply to all occurrences" shortcut on the first pick
  when the same chassis appears N times. → `spec/multi-unit-clarification-and-faction-scope.md` P1 "UX note"

---

## Spec-folder map (after the 2026-07-30 consolidation)

**`spec/` — active design-of-record (7 docs):**
- `dual-edition.md` — dual-edition plumbing (built) + 11th launch runbook (pending). *Consolidates the former architecture / 10th_edition / 11th_edition trio.*
- `retrieval.md` — retrieval-quality layers (routing, guaranteed slices, token budget, scraper Tracks A–D, hybrid lexical, deferred embedding upgrade).
- `reranker.md` — cross-encoder rerank + seeding + parent-cap; **§11 = clause-segmented max-pool** (formerly `segment-maxpool-rerank.md`).
- `retrieval-pipeline-refresh.md` — the module-architecture refactor design (typed `Chunk`, `retrieval.py` PIPELINE, caching). Implementation record is archived.
- `multi-unit-clarification-and-faction-scope.md` — occurrence-slot clarification, faction scoping, rule-chunk faction metadata.
- `army-detachment-rules.md` — CSV ingest of faction army rules + detachment rules.
- `free-llm-providers.md` — Groq rate-limit hardening (shipped) + deferred cross-provider pool.

**`spec/archive/` — historical build records (provenance only, all shipped):**
`retrieval-pipeline-audit.md`, `retrieval-pipeline-refresh-implementation.md`,
`scraper-rework.md`, `chunk-fragmentation.md`, `corpus-reconciliation.md`. See
`spec/archive/README.md`.

> `spec/new_questions.md` is referenced by two docs but was never committed; its Q1/Q2 were
> resolved into `army-detachment-rules.md` and the archived `chunk-fragmentation.md`.

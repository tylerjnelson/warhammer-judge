# Groq model accuracy — manual grading of The Judge's answers

> **⚠️ STATUS UPDATE (2026-07-21):** the model graded here as "(PROD)", **`qwen/qwen3-32b`**, has
> been **RETIRED — Groq closed it on the free tier and it is no longer callable.** Production is now
> **`openai/gpt-oss-120b`**, which is the co-best model in every grid below (43/43) and resolves Q12
> natively without the rule-10 crutch qwen3-32b needed. The qwen3-32b rows/grades below are kept as
> the historical measurement that justified promoting gpt-oss-120b; **qwen3-32b is not a selectable
> option anymore** — ignore any "current PROD"/rotation language that still names it. See
> `spec/free-llm-providers.md` (top banner) and `config.py`.

**Date:** 2026-06-24. **Method:** the 43-question `eval_quality.py` set was run through the
shipped retrieval pipeline (`retrieval.build_context`) **once per question**; the identical
system prompt + rules context + question was sent to every chat-capable Groq model
(`collect_model_answers.py`). Each answer was then **read and graded by hand** against the
rules in the provided context (not by substring match). Raw answers: `model_eval_results.json`
/ `model_eval_report.md`.

Grades: **✓** correct & complete · **~** right direction, material gap/imprecision ·
**✗** wrong / hallucinated / refused-with-context-present / empty / truncated-no-answer ·
**E** not collected (API error).

## Per-model summary (best → worst)

| Model | ✓ | ~ | ✗ | Collected | Fully-correct rate | Notes |
|---|---|---|---|---|---|---|
| **openai/gpt-oss-120b** | 43 | 0 | 0 | 43/43 | **100%** | Flawless. Only model to catch the Q12 Tactical-Missions +1 VP. Never truncated. |
| **qwen/qwen3-32b** (PROD) | 41 | 1 | 1 | 43/43 | **95%** | Only miss: Q11 (said 4VP not 5VP for Assassination/Tactical). Solid, fast, reliable. |
| **openai/gpt-oss-20b** | 40 | 1 | 2 | 43/43 | **93%** | Excellent quality; 2 losses were **2048-token truncation** (empty) on reasoning-heavy Qs. |
| **meta-llama/llama-4-scout-17b** | 37 | 2 | 4 | 43/43 | **86%** | Strong. Misses cluster on Feel-No-Pain-vs-mortal-wounds (Q6,Q21) + Q30 Assault Ramp. |
| **qwen/qwen3.6-27b** | 36 | 2 | 4 | 42/43 | **86%** | High quality *when it answers*; **4 answers lost to truncation** (Q3,9,16,32). Slow. |
| **llama-3.3-70b-versatile** | 10 | 1 | 1 | **12/43** | 83%* | *Partial sample only — daily token cap (TPD) exhausted after 12 Qs. Cannot be fully assessed. |
| **llama-3.1-8b-instant** | 26 | 5 | 12 | 43/43 | **60%** | Frequent hallucinations on rule interactions (see below). Fast but unreliable for adjudication. |
| **allam-2-7b** | 3 | 2 | 38 | 43/43 | **7%** | Unusable: refusals, empty outputs, raw context dumps, wrong faction (Drukhari for Orks). |

Excluded (not viable backends, verified this run):
- **groq/compound** — 413 *Request Entity Too Large* on our ~2800-tok RAG context.
- **groq/compound-mini** — internally routes to `llama-3.3-70b` (429 names that model); shares its bucket, adds nothing.
- **whisper-* / orpheus-* / *prompt-guard* / gpt-oss-safeguard** — audio / classifier models, not Q&A.

## Headline findings

1. **gpt-oss-120b beats the current production model (qwen3-32b).** It was the only model
   to score 43/43 *and* the only one to resolve the subtlest question (Q12: the Bring-It-Down
   Tactical-Missions +1 VP that every other model dropped). It also never truncated.
   → For spec `free-llm-providers.md` §5/§6, gpt-oss-120b is a strong primary or first
   rotation target, not just a fallback.

2. **The current PROD pick (qwen3-32b) is well-justified** — 95%, fast, zero truncation,
   only a single VP-value slip (Q11). Good default.

3. **Reasoning models pay a truncation tax.** qwen3.6-27b lost 4 answers and gpt-oss-20b
   lost 2 to hitting the 2048 `max_completion_tokens` cap while still inside `<think>` —
   they burned the whole budget reasoning and returned nothing. gpt-oss-120b did not.
   If qwen3.6-27b enters a rotation, it needs a higher output cap or a truncation-retry.

4. **llama-3.3-70b can't sustain eval-scale load on the free tier.** Its 100K **TPD (daily
   token)** cap exhausted after ~12 questions (`retry-after: 2085s`, per-minute buckets full).
   At ~4K tok/question it can't even finish one 43-Q pass/day. Fragile as a heavy backend —
   matches spec §5 caveat 2 (modest windows delay, don't remove, the wall).

5. **Small models hallucinate rule *interactions*.** llama-3.1-8b invented a "'surge' move"
   rule (Q1), said invulnerable saves work against Devastating Wounds (Q6, backwards), said
   you *can* Deep Strike 3" from the enemy (Q35, an illegal state), and missed Assault Ramp
   (Q30). llama-4-scout and llama-3.1-8b both botched **Feel No Pain vs mortal wounds**
   (Q6/Q21) — the exact "interacting rules" hard case spec §4 warns about.

## Suggested rotation order (by measured accuracy, best-first per spec §5)

1. `openai/gpt-oss-120b` (100%)
2. `qwen/qwen3-32b` (95%, current PROD)
3. `openai/gpt-oss-20b` (93%) — watch truncation
4. `meta-llama/llama-4-scout-17b` (86%)

Keep **out** of the quality tier: `llama-3.1-8b` (60%, hallucinations), `llama-3.3-70b`
(TPD too tight to rely on), `allam-2-7b` (7%), the `compound` models (won't take our context).

## Per-question grid

```
Q#  Suite            qwen3-32b qwen3.6 l3.3-70b l3.1-8b l4-scout oss-120b oss-20b allam
1   CORE                ✓         ✓        ✓        ✗        ✓        ✓        ✓       ✗
2   CORE                ✓         ✓        ✗        ✗        ✓        ✓        ✓       ✗
3   CORE                ✓         ✗trunc   ✓        ✗        ✓        ✓        ✓       ✗
4   CORE                ✓         ✓        ✓        ✓        ✓        ✓        ✓       ~
5   CORE                ✓         ✓        ✓        ✓        ✓        ✓        ✓       ✗empty
6   CORE                ✓         ✓        ✓        ✗        ✗        ✓        ✓       ✗
7   CORE                ✓         ✓        ✓        ✓        ✓        ✓        ✓       ✗
8   CORE                ✓         ✓        ✓        ✓        ✓        ✓        ✓       ✗empty
9   CORE                ✓         ✗trunc   ~        ~        ~        ✓        ✓       ✗
10  CORE                ✓         ✓        ✓        ✓        ✓        ✓        ✓       ✗
11  LEVIATHAN           ✗         ✓        E        ✓        ✓        ✓        ✓       ✓
12  LEVIATHAN           ~         ~        E        ✗        ~        ✓        ✓       ✗
13  LEVIATHAN           ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
14  LEVIATHAN           ✓         ✓        ✓        ✗        ✓        ✓        ✓       ✗
15  LEVIATHAN           ✓         ✓        E        ~        ✓        ✓        ✓       ✗
16  LEVIATHAN           ✓         ✗trunc   E        ✓        ✓        ✓        ✓       ✗
17  LEVIATHAN           ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
18  LEVIATHAN           ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
19  LEVIATHAN           ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
20  LEVIATHAN           ✓         ✓        E        ~        ✓        ✓        ~       ✗
21  UNITS               ✓         ✓        E        ✗        ✗        ✓        ✓       ✗
22  UNITS               ✓         ~trunc   E        ✗        ✗        ✓        ✓       ✗
23  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
24  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
25  UNITS               ✓         ✓        E        ✗        ✓        ✓        ✓       ✗
26  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
27  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
28  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ~
29  UNITS               ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
30  UNITS(multi-fac)    ✓         ✓        E        ✗        ✗        ✓        ✓       ✗
31  UNITS               ✓         ✓        E        ✗        ✓        ✓        ✓       ✗
32  UNITS               ✓         ✗trunc   E        ✓        ✓        ✓        ✗trunc  ✗
33  UNITS               ✓         ✓        E        ~        ✓        ✓        ✗trunc  ✗
34  ILLEGAL             ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
35  ILLEGAL             ✓         ✓        E        ✗        ✓        ✓        ✓       ✓
36  ILLEGAL             ✓         ✓        E        ✓        ✓        ✓        ✓       ✗empty
37  ILLEGAL             ✓         ✓        E        ✓        ✓        ✓        ✓       ✓
38  ILLEGAL             ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
39  ARMY_DETACH         ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
40  ARMY_DETACH         ✓         ✓        E        ✓        ✓        ✓        ✓       ✗
41  ARMY_DETACH         ✓         ✓        ✓        ✓        ✓        ✓        ✓       ✗
42  ARMY_DETACH         ✓         ✓        E        ~        ✓        ✓        ✓       ✗
43  ARMY_DETACH         ✓         E        E        ✓        ✓        ✓        ✓       ✗empty
```

Notable single-question discriminators:
- **Q12** (Bring It Down, Tactical +1 VP): only gpt-oss-120b & gpt-oss-20b got 6 VP; all
  others said 5 VP (dropped the achieved-bonus) or worse.
- **Q6 / Q21** (Feel No Pain vs Devastating-Wounds/Deadly-Demise mortal wounds): llama-3.1-8b
  and llama-4-scout claim FNP can't apply — backwards. The bigger models got it right.
- **Q30** (colloquial Land Raider + Assault Ramp): llama-3.1-8b & llama-4-scout got the
  formal version (Q29) right but the colloquial version wrong — a phrasing-robustness gap.

---

## 3072-cap rerun of the two truncating models (2026-06-26)

`MAX_OUTPUT_TOKENS` raised 2048→3072; the two models that truncated at 2048
(`qwen/qwen3.6-27b`, `openai/gpt-oss-20b`) were rerun (`model_eval_3072.json`, collected via
the daily-cap-aware `backfill_until_done.py`). Coverage: **both models 43/43** (qwen3.6's last
4 — Q16/Q21/Q25/Q29 — harvested off the rolling daily cap over ~2 days; Q21/Q25/Q29 match their
2048 ✓ grades).

**Rescued questions (truncated at 2048 → now finish at 3072) — all graded ✓:**

| Model | Q | comp_tok @3072 | Grade | Note |
|---|---|---|---|---|
| qwen3.6-27b | Q3 barricade charge | 2811 | ✓ | correct barricade ruling; rightly declines unsupported vertical part |
| qwen3.6-27b | Q9 Fights First order | 1992 | ✓ | two steps, non-active alternates — correct |
| qwen3.6-27b | Q16 ruins movement/visibility | 2878 | ✓ | LoS block, keyword move-through, can't end in wall; Leviathan doesn't override |
| qwen3.6-27b | Q22 An'ggrath FNP vs Deadly Demise MW | 2813 | ✓ | got the FNP-vs-mortal-wounds interaction RIGHT |
| qwen3.6-27b | Q32 Aegis Benefit of Cover | 2868 | ✓ | Reinforced Cover + BoC + Fortification, correct |
| gpt-oss-20b | Q32 Aegis Benefit of Cover | 1916 | ✓ | clean, fully cited |
| gpt-oss-20b | Q33 Obyron Ghostwalk Fights First | 982 | ✓ | correct both-sides resolution |

→ The truncated answers were never *wrong*, only cut off. Q3/Q22/Q32 genuinely needed
>2048 tokens (2811–2868), confirming legitimate 2048 truncation.

**New truncation REGRESSIONS introduced by 3072** (finished fine at 2048, now truncate):

| Model | Q | 2048 | 3072 |
|---|---|---|---|
| gpt-oss-20b | Q14 attacker/defender | ✓ | ✗ truncated (3072 tok) |
| qwen3.6-27b | Q27 Callidus Movement stat | ✓ | ✗ truncated (3072 tok) |

**Conclusion:** net truncations fell ~6→2 but not to zero, and 2 good answers broke — a higher
fixed cap only *moves* the cliff (reasoning length is variable and fills the budget). Robust fix
is a `finish_reason=="length"` retry, not a bigger number. See spec/free-llm-providers.md §5b.

---

## Production re-verification after the rule-10 prompt fix (2026-07-04)

**Goal:** confirm PROD (`qwen/qwen3-32b`) now answers ALL 43 correctly, since the 2026-06-24
baseline above graded it 95% (Q11 ✗, Q12 ~). Method: full 43-Q set re-run through the SHIPPED
pipeline with the **live rule-10 system prompt** (`collect_model_answers.py --models qwen/qwen3-32b
--out model_eval_verify`), hand-graded. New gate `grade_prod.py` does the mechanical first pass
(truncation/empty/refusal + the Q11=5VP / Q12=6VP checks); the read confirms it.

**Result: 43/43.** The two baseline misses are FIXED by rule 10:
- **Q11** → *"Assassination under Tactical Missions scores **5VP** … even if resurrected"* (was 4VP).
- **Q12** → reasons 2+1+1+1 = 5VP then *"+1VP achieve bonus, **totaling 6VP**"* (was 5VP / ~).

Nothing else regressed vs. the 2026-06-24 grid.

**Cap finding (drove config MAX_OUTPUT_TOKENS 3072→2048):** at the 3072 cap, **7/43 questions
413'd** (Q2,5,21,25,29,33,40) — real retrieved contexts run 2900-3300 input tok, and input+3072
exceeds the 6000 TPM admission wall, so in production those would hit `call_llm_reduced` and answer
on SHED context. All 7 fit at 2048 (max input ~3310; +2048 = 5358 < 6000); re-running them through
the real `serving.call_llm` at 2048 returned all 7 clean (reduced/cutoff/err all False) and correct.
qwen3-32b's longest completion across the whole run was **1383 tok**, so 2048 costs it nothing. The
3072 bump only ever helped the reasoning-heavy eval *alternates* (not prod) — it was pure downside
for the prod model. Cap set to 2048; prod restarted (`thejudge.service`) to load it.
(NOTE: the 2048 cap was itself later retired — production now sends NO output cap; see
spec/free-llm-providers.md §5d. This eval's `--tpm-room` mode caps per-model only for the
fan-out, see below.)

---

## Full 8-model re-grade, NO output cap (2026-07-06)

**Why:** re-run the whole 43-Q set across every chat-capable Groq model with the truncation
confound removed, to get each model's *true* answer quality. Method identical to the 2026-06-24
grade (shipped pipeline → `serving.build_messages` w/ the live rule-10 prompt → hand-graded),
except `collect_model_answers.py --tpm-room` sizes `max_completion_tokens` to each model's
measured TPM (6000→2560, 8000→4096, 12000/30000→8192) so no legit answer truncates while still
admitting. Data: `model_eval_uncapped.json`. Coverage assembled over 3 days (daily-cap harvest via
`backfill_until_done.py`).

**Coverage:** 7/8 models **43/43**; `allam-2-7b` 37/43 (its 6 gaps — Q5,21,29,36,39,40 — are
structural 413s: our ~3300-tok RAG context exceeds allam's context *window*, uncollectable). The
`--tpm-room` sizing worked: **zero truncation** except a single residual on gpt-oss-20b (Q20, whose
`<think>` still overran 4096).

### Per-model summary (best → worst)

| Model | Fully-correct | vs 2026-06-24 | Notes |
|---|---|---|---|
| **openai/gpt-oss-120b** | **43/43** | =100% | Still flawless. One of only TWO models to get Q12 (6VP) — the Tactical achieve-bonus every mid-tier model drops. |
| **qwen/qwen3-32b** (PROD) | **43/43** | ↑ from 95% | The rule-10 prompt (shipped since) fixes the old Q11/Q12 slips: Q11→5VP, Q12→6VP. Co-best, and it's what production runs. |
| **qwen/qwen3.6-27b** | **42/43** | ↑ from 86% | Only miss Q12 (5VP, drops Tactical +1). **The prior 4 truncation losses (Q3,9,16,32) are GONE** with no cap — its real quality was always top-tier. |
| **openai/gpt-oss-20b** | **41/43** | ↓ from 93%* | Miss Q12 (5VP); Q20 Gambits truncated-refusal (its 1 residual truncation). *Prior 93% was inflated by 2 truncations counting as losses; true quality ≈ this. |
| **llama-3.3-70b-versatile** | **~41/43** | (n/a — unassessable before) | Miss Q12 (5VP); otherwise solid on every interaction/illegal-state discriminator. Now fully assessable (3-day TPD harvest); a genuinely strong instruct backend on quality, still TPD-fragile operationally. |
| **meta-llama/llama-4-scout-17b** | **~39/43** | ≈86% | Repeats the exact prior weak spots: **Q22 Feel-No-Pain-vs-Deadly-Demise backwards** ("FNP is a saving throw, can't apply to mortal wounds" — wrong), **Q30 colloquial Assault Ramp** ("cannot charge" — wrong), + Q12. |
| **llama-3.1-8b-instant** | **~37/43** | ≈60% | **Q6 invuln-vs-Devastating-Wounds backwards**, Q22 FNP backwards, Q30, Q12; hallucination-prone on rule *interactions* as before. |
| **allam-2-7b** | **~3/37** | ≈7% | Unusable: refuses answerable Qs with context present (Q3, Q10), wrong VP, 6 structural 413s. Excluded from the quality tier. |

### Headline findings

1. **Removing the cap removed the confound, and the two "truncation-tax" reasoners jumped.**
   qwen3.6-27b (86%→42/43) and gpt-oss-20b lost answers in June *only* to the 2048 cap cutting them
   off mid-`<think>`; given room they answer correctly. The 2026-06-24 note "truncated answers were
   never wrong, just cut off" is now directly confirmed at full scale.

2. **gpt-oss-120b and prod qwen3-32b are the co-best at 43/43** — and they are the **only two models
   that resolve Q12** (Bring It Down, 20-wd Monster, Tactical = 6VP). Every other model — even with
   rule-10 in the prompt — drops the "extra 1VP if using Tactical Missions" achieve-bonus and says
   5VP. gpt-oss-120b gets it natively; qwen3-32b gets it via the rule-10 crutch. Q12 remains the
   single sharpest discriminator in the set.

3. **prod is validated at the top.** With rule-10 live, production qwen3-32b is 43/43 — tied with the
   strongest available model. No reason to switch prod on accuracy grounds; gpt-oss-120b remains the
   promote-if-ever candidate (it needs no prompt crutch and has higher TPM headroom).

4. **The bottom tier's errors are all rule-*interaction* failures, unchanged from June.** scout &
   llama-3.1-8b flip Feel-No-Pain-vs-mortal-wounds (Q6/Q21/Q22) and the colloquial Assault Ramp (Q30)
   — the exact "interacting rules" hard class. No-cap didn't help them; their misses are reasoning,
   not truncation.

5. **Q22 exposed a RETRIEVAL gap, not just a model gap.** The context retrieved the Painboy's
   *offensive* "Hold Still and Say 'Aargh!'" ability, not its Feel-No-Pain grant — so the Painboy's
   FNP was never in context. gpt-oss-20b actually graded BEST here by noticing the shown ability isn't
   FNP; the models that said "yes, FNP applies" imported an out-of-context fact (right rule, wrong
   grounding). Worth a retrieval follow-up (surface the Painboy FNP ability for that query).

### Method note
Easy questions (broad cross-model consensus) were confirmed by consensus + a mechanical sweep
(`grade_prod.py`: truncation/empty/refusal/VP checks); the discriminating/interaction/VP/illegal-state
questions were hand-read in full across all models. "REFUSED" is only a miss where the answer WAS in
context — Q20 (Gambits mechanics absent) and Q27 (Callidus Movement stat absent) are correct refusals.

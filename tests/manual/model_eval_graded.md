# Groq model accuracy — manual grading of The Judge's answers

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

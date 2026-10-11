"""
serving.py — prompt assembly, token budgeting, and the LLM call.
================================================================
The TPM-load-bearing half of the pipeline (spec/retrieval-pipeline-refresh.md §9):
the stable system prefix, history trim, the SOFT token budget, and the
reduced-context retry. Moved here verbatim from app.py — the 6K/min Groq ceiling
math is unchanged.

A leaf module: depends only on `config` (+ openai/streamlit for the cached client).
It reads chunks duck-typed via `chunk["metadata"]` / `chunk["text"]`, so it works on
the typed Chunk (via its mapping shim) without importing chunk_model.
"""
import re
import time

import streamlit as st
from openai import OpenAI, RateLimitError, APITimeoutError

import config
from applog import get_logger

log = get_logger(__name__)


# ── LLM client (cached) ───────────────────────────────────────────────────────

@st.cache_resource
def get_llm_client():
    # max_retries=0: the SDK's default retry silently masks 429s as multi-second hangs
    # and swallows the reset headers. We own the wait (call_llm) so we can read the
    # reset window and distinguish a transient TPM breach from the daily (TPD) cap.
    # timeout: production sends no max_completion_tokens (see config), so this wall-clock
    # ceiling is the runaway-<think> backstop — it bounds a pathological loop without
    # reserving any TPM at admission (which a token cap would). Legit answers finish well
    # under it; a timeout surfaces as an APITimeoutError handled in call_llm.
    return OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
        max_retries=0,
        timeout=config.LLM_REQUEST_TIMEOUT,
    )


# ── Prompt builder ────────────────────────────────────────────────────────────

def system_prompt(edition: str) -> str:
    ed = config.get_edition(edition)
    mp = ed["mission_pack"]["name"]
    return f"""You are 'The Judge,' an expert Warhammer 40,000 {ed['label']} rules adjudicator.

Rules:
1. Answer ONLY using the provided rules context below.
2. If the context contains a {mp} or errata entry, it OVERRIDES any base Core Rule.
3. Always cite the specific rule name and source in your answer.
4. If you cannot find a definitive answer, say: 'The provided rules do not clearly address this — I recommend checking the official GW FAQ.' Do NOT speculate.
5. Structure complex answers as: [Ruling] → [Rule Citation] → [Reasoning].
6. CRITICAL: Never infer or extrapolate rules that are not explicitly stated in the context. If an ability says 'Normal move', it means Normal move only — do not assume it also applies to Advance moves, Fall Back moves, or any other move type unless the rule explicitly says so.
7. If a rule citation appears to be cut off or incomplete, say so explicitly rather than ruling based on partial text.
8. If a question contains an illegal game state (e.g. a unit embarked in a transport it cannot legally embark in, based on transport capacity or keyword restrictions in the provided context), identify and state the illegal premise before ruling on any other aspect of the question.
9. When a datasheet's weapon or ability names a keyword or rule (e.g. [DEVASTATING WOUNDS], Feel No Pain, Deadly Demise, Infiltrators) AND that rule's text is present in the context, cite and apply that provided rule explicitly. Do NOT call it 'implied', 'standard', or rule from memory when the actual rule chunk is in front of you.
10. VP / mission-scoring rules often stack SEVERAL additive clauses: a base value, per-condition bonuses, AND a separate bonus for achieving the mission under the current mission type (e.g. 'if using Tactical Missions ... score an extra 1VP'). When a rule lists different values for different conditions (e.g. 'X if using Fixed Missions, Y if using Tactical Missions'), report the value for the condition the scenario actually specifies — do not default to the first number listed. To total the VP, list EVERY clause the scenario triggers and ADD them, then apply any maximum cap. Do not stop at the base or per-condition bonuses if a further 'extra VP' clause also applies.
"""

def mission_pack_context(edition: str) -> str:
    mp = config.get_edition(edition)["mission_pack"]["name"]
    return (f"This app is used for {mp} matched play games. When rules conflict "
            f"between Core Rules and {mp}, {mp} rules take precedence.\n\n")


# ── Token budgeting (Layer 2) ─────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Cheap ~chars/token proxy — avoids a tokenizer dependency on the hot path."""
    return len(text) // config.TOKEN_CHAR_RATIO


SEP        = "\n\n---\n\n"
SEP_TOKENS = len(SEP) // config.TOKEN_CHAR_RATIO + 1

def format_rules_context(chunks: list, token_budget: int) -> str:
    """
    Assemble the rules context from WHOLE chunks — a rule is never cut mid-text.
    Chunks arrive pre-ranked (reserved rules/units first, via assemble_context); each
    is added in full. token_budget is a SOFT target: the chunk that crosses it is still
    added whole (so an adjudication-critical rule is never reduced to a misleading
    header), and we stop after it. Rules chunks are ~300 tokens, so the total lands
    near the budget and tops out around budget + one chunk (~3k) in the worst case —
    an accepted overrun to guarantee no truncation. Lower-priority chunks past that
    are dropped whole, never sliced.
    """
    if not chunks:
        return "No relevant rules found for this query."
    parts, used = [], 0
    for i, chunk in enumerate(chunks, 1):
        meta  = chunk["metadata"]
        label = f"[{i}] {meta.get('unit_name') or meta.get('category', 'Rule')} ({meta.get('army', '')})"
        block = f"{label}\n{chunk['text']}"
        parts.append(block)
        used += estimate_tokens(block) + (SEP_TOKENS if len(parts) > 1 else 0)
        if used >= token_budget:      # included this chunk whole; stop before adding more
            break
    return SEP.join(parts)

def build_messages(conversation: list, chunks: list, user_query: str,
                   edition: str, mission_pack_mode: bool = True,
                   rules_budget: int | None = None,
                   history_messages: int | None = None) -> list:
    rules_budget     = config.RULES_CONTEXT_TOKEN_BUDGET if rules_budget is None else rules_budget
    history_messages = config.MAX_HISTORY_MESSAGES       if history_messages is None else history_messages

    # Stable, cacheable system prefix — instructions ONLY. Keeping the volatile
    # rules context OUT of this message lets Groq cache the prefix, so the Judge
    # instructions stop counting against TPM every call (spec/retrieval.md L2).
    mode_prefix    = mission_pack_context(edition) if mission_pack_mode else ""
    system_content = mode_prefix + system_prompt(edition)
    messages = [{"role": "system", "content": system_content}]

    # Prior turns are plain Q/A (rules context is never persisted to history),
    # but still a recurring per-call TPM cost — trim to the most recent few.
    for msg in conversation[-history_messages:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Volatile rules context rides in the final user message, budgeted.
    rules_context = format_rules_context(chunks, rules_budget)
    messages.append({
        "role": "user",
        "content": f"RULES CONTEXT (answer using ONLY this):\n{rules_context}\n\nQUESTION: {user_query}",
    })
    return messages


# ── LLM call ──────────────────────────────────────────────────────────────────

CUTOFF_NOTICE = "\n\n⚠️ *Response was cut off (model reached its context-length limit).*"

# Buffer added to a reported 429 reset before retrying, so clock skew / rounding can't
# make us retry a hair BEFORE the token bucket has actually refilled (→ another 429).
_RESET_MARGIN = 0.5

_DURATION_RE = re.compile(r'(\d+(?:\.\d+)?)(ms|h|m|s)')


def _complete(messages: list) -> tuple[str, str]:
    """Single Groq completion + reasoning-trace stripping. Returns
    (stripped_answer, finish_reason). Raises on API error.

    No max_completion_tokens: it is admission-reserved against the 6000/min TPM wall
    (so a cap 413s large-context questions), while omitting it reserves the input only.
    See config's 'Production sends NO completion cap' block. The runaway backstop is the
    client's wall-clock timeout (get_llm_client), not a token cap."""
    client   = get_llm_client()
    t0       = time.monotonic()
    response = client.chat.completions.create(
        model=config.LLM_MODEL, messages=messages, temperature=0.1,
    )
    choice = response.choices[0]
    usage  = getattr(response, "usage", None)
    # One line per API call: the token counts are the TPD-budget telemetry.
    log.info("llm call model=%s prompt_tok=%s completion_tok=%s total_tok=%s finish=%s %.2fs",
             config.LLM_MODEL, getattr(usage, "prompt_tokens", "?"),
             getattr(usage, "completion_tokens", "?"), getattr(usage, "total_tokens", "?"),
             choice.finish_reason, time.monotonic() - t0)
    raw    = choice.message.content or ""
    answer = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
    return (answer or raw), choice.finish_reason


def _complete_guarded(messages: list) -> str:
    """_complete + length guard. With no output cap, finish_reason=='length' can only mean
    the model exhausted its full ~40K context window mid-output — a rules answer never
    approaches this (longest ever seen: 1383 tok), so this branch is a near-unreachable
    backstop, not a routine path. If it ever fires, flag the stripped partial with an
    explicit cutoff notice so a severed answer can never masquerade as a complete ruling
    (system-prompt rule 7 asks the model to flag cutoffs, but it can't flag a cut that
    severs its own output). No re-roll: a context-window overflow would recur on identical
    input, so re-rolling can't help (unlike the retired output-cap case, where a smaller
    fresh draw could finish)."""
    answer, finish = _complete(messages)
    if finish == "length":
        log.warning("llm answer hit the context-window limit (finish=length); cutoff notice appended")
    return answer + CUTOFF_NOTICE if finish == "length" else answer


def _reset_seconds(err: RateLimitError) -> float | None:
    """Seconds to wait before the token bucket has refilled, read from the 429's headers
    — or None if unreadable. Returns the MAX of every reported reset signal
    (x-ratelimit-reset-tokens, retry-after), because they can disagree (measured
    reset-tokens=40.47s vs retry-after=21s) and waiting the smaller one would retry
    BEFORE the bucket refills → another 429. The caller waits this (plus a small margin)
    and uses its MAGNITUDE as the TPM-vs-TPD discriminator: ≤ RATE_LIMIT_MAX_WAIT (a
    per-minute window) is a TPM breach to wait out, larger is the daily cap → shed."""
    resp = getattr(err, "response", None)
    if resp is None:
        return None
    # reset-tokens is Go-duration ('7.66s', '2m59.56s'); retry-after is integer seconds.
    resets = [
        _parse_duration(resp.headers.get(name) or "")
        for name in ("x-ratelimit-reset-tokens", "retry-after")
    ]
    resets = [s for s in resets if s is not None]
    return max(resets) if resets else None


def _parse_duration(value: str) -> float | None:
    """Parse a Groq reset header into seconds. Handles a plain number ('5', retry-after)
    and Go-style durations ('7.66s', '2m59.56s', '88ms', '1h0m0s'). None if unparseable."""
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)                      # plain seconds (retry-after)
    except ValueError:
        pass
    mult = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0}
    parts = _DURATION_RE.findall(value)
    if not parts:
        return None
    return sum(float(num) * mult[unit] for num, unit in parts)


def call_llm(conversation: list, chunks: list, user_query: str, edition: str,
             mission_pack_mode: bool = True) -> str:
    """One user request → one answer. Logs a per-request summary (never the question
    text); the per-API-call token line and any failure path log separately."""
    t0 = time.monotonic()
    answer = _call_llm(conversation, chunks, user_query, edition, mission_pack_mode)
    log.info("request edition=%s chunks=%d mission_pack=%s %.2fs%s",
             edition, len(chunks), mission_pack_mode, time.monotonic() - t0,
             " [degraded]" if answer.startswith("⚠️") else "")
    return answer


def _call_llm(conversation: list, chunks: list, user_query: str, edition: str,
              mission_pack_mode: bool = True) -> str:
    messages = build_messages(conversation, chunks, user_query, edition, mission_pack_mode)
    try:
        return _complete_guarded(messages)
    except RateLimitError as e:
        wait = _reset_seconds(e)
        kind = ("unreadable" if wait is None
                else "TPM" if wait <= config.RATE_LIMIT_MAX_WAIT else "TPD/daily")
        log.warning("llm 429 rate-limited kind=%s reset=%ss", kind,
                    "?" if wait is None else f"{wait:.1f}")
        # Impl 3: 429 costs zero tokens, so on a transient TPM breach wait the server-
        # reported reset and retry FULL-context rather than shedding. A daily (TPD) reset
        # is too long to block a live user — fall through to context-shedding instead.
        return _retry_after_rate_limit(e, conversation, chunks, user_query, edition, mission_pack_mode)
    except APITimeoutError:
        # The wall-clock runaway backstop (LLM_REQUEST_TIMEOUT) fired — since production
        # sends no output cap, this is what bounds a pathological generation. A legit
        # answer finishes well under it, so a timeout means something went wrong; surface
        # it plainly rather than silently shedding.
        log.error("llm timeout after %ss (LLM_REQUEST_TIMEOUT)", config.LLM_REQUEST_TIMEOUT)
        return ("⚠️ The model took too long to respond and the request timed out. "
                "Please try again, or rephrase the question more narrowly.")
    except Exception as e:
        err = str(e)
        # 413 request-too-large is genuinely oversized context — waiting can't help, so
        # shed straight away (unlike a 429, which is transient and worth waiting out).
        if "413" in err or "tokens" in err.lower():
            log.warning("llm context too large (%s); shedding context", err[:200])
            if chunks:
                return call_llm_reduced(conversation, chunks, user_query, edition, mission_pack_mode)
            return "⚠️ This question requires too much context for the free tier. Try breaking it into smaller questions."
        log.error("llm error: %s", err[:500], exc_info=True)
        return f"⚠️ LLM error: {err}\n\nCheck your API key and provider config in config.py."

def _retry_after_rate_limit(err: RateLimitError, conversation: list, chunks: list,
                            user_query: str, edition: str, mission_pack_mode: bool) -> str:
    """Reset-aware 429 handling. If the reset window is bounded (≤ RATE_LIMIT_MAX_WAIT,
    i.e. a per-minute TPM breach), sleep it and retry the full request — a 429 costs no
    tokens, so this is cheap and preserves context/quality. A large reset (the daily TPD
    cap) or an unreadable header falls through to context-shedding — we never block a
    live user for hundreds of seconds."""
    for _ in range(config.RATE_LIMIT_RETRIES):
        wait = _reset_seconds(err)
        if wait is None or wait > config.RATE_LIMIT_MAX_WAIT:
            break                                # TPD / unreadable → don't block; shed below
        log.info("llm 429: waiting %.1fs then retrying full context", wait + _RESET_MARGIN)
        time.sleep(wait + _RESET_MARGIN)         # margin so we never retry before the refill
        try:
            messages = build_messages(conversation, chunks, user_query, edition, mission_pack_mode)
            return _complete_guarded(messages)
        except RateLimitError as retry_err:
            log.warning("llm 429 again on full-context retry")
            err = retry_err                      # bucket not clear yet; loop may retry again
    if chunks:
        log.warning("llm 429 not waitable; shedding to reduced context")
        return call_llm_reduced(conversation, chunks, user_query, edition, mission_pack_mode)
    log.error("llm 429 not waitable and no context to shed; returning rate-limit message")
    return "⚠️ The free-tier rate limit is exhausted (this may be the daily cap). Please try again shortly."

def call_llm_reduced(conversation: list, chunks: list, user_query: str, edition: str,
                     mission_pack_mode: bool = True) -> str:
    """Last-resort retry with a sharply reduced budget — shed context when a 429 can't be
    waited out (daily cap) or a 413 says the context is simply too large."""
    messages = build_messages(
        conversation, chunks[:3], user_query, edition, mission_pack_mode,
        rules_budget=config.RULES_CONTEXT_TOKEN_BUDGET // 3,
        history_messages=2,
    )
    try:
        answer = _complete_guarded(messages)
        log.warning("served a reduced-context answer")
        return answer + "\n\n*Note: Response was generated with reduced context due to API limits.*"
    except Exception as e:
        log.error("reduced-context retry also failed: %s", str(e)[:500], exc_info=True)
        return "⚠️ This question requires too much context for the free tier. Try breaking it into a smaller question."

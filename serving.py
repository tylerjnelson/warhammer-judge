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

import streamlit as st
from openai import OpenAI

import config


# ── LLM client (cached) ───────────────────────────────────────────────────────

@st.cache_resource
def get_llm_client():
    return OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
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

def _complete(messages: list) -> str:
    """Single Groq completion + reasoning-trace stripping. Raises on API error."""
    client   = get_llm_client()
    response = client.chat.completions.create(
        model=config.LLM_MODEL, messages=messages,
        max_completion_tokens=config.MAX_OUTPUT_TOKENS, temperature=0.1,
    )
    raw    = response.choices[0].message.content
    answer = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    answer = re.sub(r'<think>.*$',         '', answer, flags=re.DOTALL).strip()
    return answer or raw

def call_llm(conversation: list, chunks: list, user_query: str, edition: str,
             mission_pack_mode: bool = True) -> str:
    messages = build_messages(conversation, chunks, user_query, edition, mission_pack_mode)
    try:
        return _complete(messages)
    except Exception as e:
        err = str(e)
        if "413" in err or "rate_limit_exceeded" in err or "tokens" in err.lower():
            if chunks:
                return call_llm_reduced(conversation, chunks, user_query, edition, mission_pack_mode)
            return "⚠️ This question requires too much context for the free tier. Try breaking it into smaller questions."
        return f"⚠️ LLM error: {err}\n\nCheck your API key and provider config in config.py."

def call_llm_reduced(conversation: list, chunks: list, user_query: str, edition: str,
                     mission_pack_mode: bool = True) -> str:
    """Retry with a sharply reduced budget when the 6K/min TPM ceiling is hit."""
    messages = build_messages(
        conversation, chunks[:3], user_query, edition, mission_pack_mode,
        rules_budget=config.RULES_CONTEXT_TOKEN_BUDGET // 3,
        history_messages=2,
    )
    try:
        return _complete(messages) + "\n\n*Note: Response was generated with reduced context due to API limits.*"
    except Exception:
        return "⚠️ This question requires too much context for the free tier. Try breaking it into a smaller question."

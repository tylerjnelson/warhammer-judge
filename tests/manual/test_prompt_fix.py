#!/usr/bin/env python3
"""
test_prompt_fix.py — A/B a candidate system-prompt rule on qwen/qwen3-32b for the
conditional-value failures found in §5a (Q11/Q12: wrong Fixed-vs-Tactical branch +
dropped Tactical +1). Reuses the stored rules context per question (no pipeline rerun),
so the only variable is the system prompt. Includes regression controls.

Usage: python tests/manual/test_prompt_fix.py
"""
import json, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config, serving
from openai import OpenAI

EDITION = "10e"
FAILED   = [11, 12]          # the two qwen3-32b missed
CONTROLS = [13, 19, 39]      # branching/conditional Qs it already PASSED — must not regress

# Candidate new rule (appended as rule 10).
AUG = ("""10. When the provided rule lists DIFFERENT values for different conditions """
       """(e.g. 'score X if using Fixed Missions, Y if using Tactical Missions'), or grants """
       """an extra effect only 'if [a condition]' (a bonus, an additional VP, a cap), do NOT """
       """just report the first number you see. First identify which condition the question """
       """or scenario actually specifies, give the value for THAT condition, then apply every """
       """additional conditional clause it triggers (bonuses AND caps). Read the entire scoring """
       """entry before answering.\n""")


def build(system_extra, context, query, mp=True):
    sys_content = (serving.mission_pack_context(EDITION) if mp else "") + serving.system_prompt(EDITION)
    if system_extra:
        sys_content = sys_content.rstrip() + "\n" + system_extra
    user = f"RULES CONTEXT (answer using ONLY this):\n{context}\n\nQUESTION: {query}"
    return [{"role": "system", "content": sys_content},
            {"role": "user", "content": user}]


def ask(client, messages):
    r = client.chat.completions.create(model="qwen/qwen3-32b", messages=messages,
                                       max_completion_tokens=2048, temperature=0.1)
    raw = r.choices[0].message.content or ""
    a = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    a = re.sub(r'<think>.*$', '', a, flags=re.DOTALL).strip()
    return (a or raw)


def first_line(a):  # the [Ruling] line usually carries the VP number
    return ' '.join(a.split())[:280]


def main():
    data = {q['idx']: q for q in json.loads(Path('tests/manual/model_eval_results.json').read_text())['questions']}
    client = OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL)
    for idx in FAILED + CONTROLS:
        q = data[idx]
        tag = "FAILED" if idx in FAILED else "control"
        print("=" * 90)
        print(f"[Q{idx}] ({tag}) {q['query']}")
        for label, extra in (("BASE  ", ""), ("AUG+10", AUG)):
            ans = ask(client, build(extra, q['context'], q['query'], q['mp']))
            print(f"  {label}: {first_line(ans)}")
            time.sleep(2)
    print("\nExpected correct: Q11=5VP (Tactical), Q12=6VP (5 + Tactical +1), max 8VP.")
    print("Controls Q13/Q19/Q39 must keep their previously-correct rulings.")


if __name__ == "__main__":
    main()

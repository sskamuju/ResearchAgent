


import os
import json
from pathlib import Path


from core.models import Plan
from core.llm import client
from core.utils import load_prompt
from langsmith import traceable

PLANNER_PROMPT = load_prompt("prompts/planner.txt")

@traceable(name="PlannerAgent")
def make_plan(user_prompt: str) -> Plan:
    system_prompt = PLANNER_PROMPT
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User prompt: {user_prompt}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type" : "json_object"},
        temperature=0.2,
    )

    # Parse the JSON plan returned by the LLM
    content = response.choices[0].message.content
    try:
        plan_data = json.loads(content)
        return Plan(**plan_data)
    except Exception as e:
        print("[planner.py] Failed to parse plan:", e)
        print("Raw content:\n", content)
        raise


if __name__ == "__main__":
    plan = make_plan("What caused the 2008 financial crisis?")
    print(plan.model_dump_json(indent=2))


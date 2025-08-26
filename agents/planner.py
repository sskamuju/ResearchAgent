


import json
from datetime import datetime
from core.models import Plan
from core.llm import client
from core.utils import load_prompt
from langsmith import traceable

PLANNER_PROMPT = load_prompt("prompts/planner.txt")

@traceable(
    name="PlannerAgent",
    tags=["agent", "planner"],
    metadata={"description": "Generates a multi-step plan from user query"}
)
def make_plan(user_prompt: str) -> Plan:
    curr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user",
        "content": (
            f"User prompt: {user_prompt}\n"
            f"The current date and time is {curr}\n"
            "Prefer recent or up to date sources when possible"
            )
        }
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





import json
from pydantic import ValidationError
from core.models import Plan
from core.llm import client
from core.utils import load_prompt, log
from langsmith import traceable

PLANNER_PROMPT = load_prompt("prompts/planner.txt")

@traceable(
    name="PlannerAgent",
    tags=["agent", "planner"],
    metadata={"description": "Generates a multi-step plan from user query"}
)
def make_plan(user_prompt: str) -> Plan:
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": f"User prompt: {user_prompt}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type" : "json_object"},
        temperature=0.2,
    )

    content = response.choices[0].message.content
    
    try:
        plan_data = json.loads(response.choices[0].message.content)
        plan = Plan(**plan_data)
        return plan
    except json.JSONDecodeError as e:
        log("planner", f"Failed to parse JSON from LLM: {e}")
        raise RuntimeError("LLM did not return valid JSON.")
    except ValidationError as e:
        log("planner", f"Plan schema validation failed: {e}")
        raise RuntimeError("LLM output did not match expected plan schema.")
    except Exception as e:
        print("[planner.py] Failed to parse plan:", e)
        print("Raw content:\n", content)
        raise


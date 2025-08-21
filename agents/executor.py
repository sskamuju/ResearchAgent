


from agents.planner import make_plan
from core.models import Plan
from tools.tavily import tavily_search
from core.utils import log

# Tool function registry
TOOL_REGISTRY = {
    "tavily_search": tavily_search
}

def execute_plan(plan: Plan) -> dict:
    results = {}

    for step in plan.steps:
        log("executor", f"Executing {step.id} with tool '{step.tool}' and args {step.args}")

        tool_fn = TOOL_REGISTRY.get(step.tool)
        if not tool_fn:
            log("executor", f"Tool '{step.tool}' not recognized.")
            results[step.id] = {"error": f"Unknown tool: {step.tool}"}
            continue

        try:
            output = tool_fn(**step.args)
            results[step.id] = output
        except Exception as e:
            log("executor", f"Error executing {step.id}: {e}")
            results[step.id] = {"error": str(e)}

    return results

if __name__ == "__main__":
    user_query = "What caused the 2008 financial crisis?"
    plan = make_plan(user_query)
    print("[executor.py] Plan created:")
    print(plan.model_dump_json(indent=2))

    results = execute_plan(plan)
    print("\n[executor.py] Execution results:")
    for step_id, result in results.items():
        print(f"\nStep: {step_id}\nResult:\n{result}")


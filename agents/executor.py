


import argparse
from agents.planner import make_plan
from agents.synthesizer import synthesize_answer
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

def main():
    parser = argparse.ArgumentParser(description="Research Agent CLI")
    parser.add_argument(
        "--question",
        type=str,
        required=False,
        help="The research question to answer. If not provided, you'll be prompted interactively."
    )
    args = parser.parse_args()

    user_query = args.question or input("What would you like to learn about? ").strip()
    log("executor", f"Received user query: {user_query}")

    # Generate a plan
    plan = make_plan(user_query)
    print("\n[executor.py] Plan created:")
    print(plan.model_dump_json(indent=2))

    # Execute the plan
    results = execute_plan(plan)
    print("\n[executor.py] Execution results:")
    for step_id, result in results.items():
        print(f"\nStep: {step_id}\nResult:\n{result}")

    final_answer = synthesize_answer(user_query, results)
    print("\n[executor.py] Final synthesized answer:")
    print(final_answer)

if __name__ == "__main__":
    main()
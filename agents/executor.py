


import argparse
import os
from agents.planner import make_plan
from agents.synthesizer import synthesize_answer
from core.models import Plan
from tools.tavily import tavily_search
from core.utils import log

from langsmith import traceable, get_current_run_tree

# Tool function registry
TOOL_REGISTRY = {
    "tavily_search": tavily_search
}

@traceable(
    name="ExecutorAgent",
    run_type="chain",
    tags=["agent", "executor", "research"],
    metadata={"env": "local"}
)
def execute_plan(plan: Plan, user_query: str, langsmith_extra=None) -> dict:
    # Access current trace and append dynamic metadata/tags
    rt = get_current_run_tree()
    if rt:
        rt.metadata["user_query"] = user_query
        rt.tags.append("executing-plan")

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

    # Create plan and execute it with tagging and metadata passed as langsmith_extra
    plan = make_plan(user_query)

    results = execute_plan(
        plan,
        user_query,
        langsmith_extra={
            "tags": ["session-run"],
            "metadata": {
                "question_length": len(user_query),
                "output_file": "outputs/synthesis.md"
            }
        }
    )

    final_answer = synthesize_answer(user_query, results)

    output_dir = "outputs"
    output_path = os.path.join(output_dir, "synthesis.md")
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_answer)

if __name__ == "__main__":
    main()

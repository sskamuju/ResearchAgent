


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

def convert_to_citation_format(results: dict) -> list[dict]:
    """
    Converts raw execution results into a format usable by the synthesizer agent.
    Supports both dict and list outputs from tools.
    """
    formatted = []

    for step_id, result in results.items():
        if isinstance(result, dict) and "error" in result:
            continue  # Skip errored steps

        # Tavily and other tools might return a list of result dictionaries
        if isinstance(result, list):
            if not result:
                continue
            # Use only the first result for synthesis to keep things concise
            first = result[0]
            summary = first.get("content", first.get("title", "No summary available"))
            link = first.get("url", "No link provided")
        elif isinstance(result, dict):
            summary = result.get("summary") or result.get("text") or "No summary available"
            link = result.get("url") or result.get("link") or "No link provided"
        else:
            # Catch-all for weird outputs
            summary = str(result)
            link = "No link provided"

        formatted.append({
            "step_id": step_id,
            "summary": summary,
            "link": link
        })

    return formatted

@traceable(
    name="ExecutorAgent-plan",
    run_type="chain",
    tags=["agent", "executor", "research"],
    metadata={"env": "local"}
)
def execute_plan(plan: Plan, user_query: str, langsmith_extra=None) -> dict:
    rt = get_current_run_tree()
    if rt:
        rt.metadata["user_query"] = user_query
        rt.tags.append("executing-plan")

    results = {}

    for step in plan.steps:
        log("executor", f"Executing step '{step.query}' with tool '{step.tool}'")

        tool_fn = TOOL_REGISTRY.get(step.tool)
        if not tool_fn:
            log("executor", f"Tool '{step.tool}' not recognized.")
            results[step.id] = {"error": f"Unknown tool: {step.tool}"}
            continue

        try:
            output = tool_fn(step.query)
            results[step.id] = output
        except Exception as e:
            log("executor", f"Error executing {step.id}: {e}")
            results[step.id] = {"error": str(e)}

    return results

@traceable(
    name="ExecutorAgent-main",
    run_type="chain",
    tags=["agent", "executor", "research"],
    metadata={"env": "local"}
)
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

    formatted_results = convert_to_citation_format(results)
    final_answer = synthesize_answer(user_query, formatted_results)


    output_dir = "outputs"
    output_path = os.path.join(output_dir, "synthesis.md")
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_answer)

if __name__ == "__main__":
    main()

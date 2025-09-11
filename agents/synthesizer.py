


import json
from core.llm import client
from core.utils import load_prompt, log
from langsmith import traceable

SYNTHESIZER_PROMPT = load_prompt("prompts/synthesizer.txt")

def format_results_for_prompt(results: list[dict]) -> str:
    """
    Formats tool execution results into a markdown-friendly string for LLM prompting.

    Args:
        results (list[dict]): A list of dictionaries containing step_id, summary, and link keys.

    Returns:
        str: A newline-separated, markdown-formatted string for injection into the synthesis prompt.
    """
    
    formatted = ""

    for r in results:
        step_id = r.get("step_id", "N/A")
        summary = r.get("summary", "No summary provided")
        link = r.get("link", "No link available")
        formatted += f"[{step_id}] {summary} ({link})\n"
    return formatted

@traceable(
    name="SynthesizerAgent",
    run_type="chain",
    metadata={
        "description": "Synthesizes a structured markdown answer from tool outputs",
        "agent": "Synthesizer",
        "model": "gpt-4o"
    }
)
def synthesize_answer(user_question: str, results: list[dict]) -> str:
    """
    Synthesizes a structured, markdown-formatted answer using LLM completion.

    Combines the user's question and search results into a prompt, then sends it to the model
    to generate a high-quality, well-organized markdown response.

    Args:
        user_question (str): The original question posed by the user.
        results (list[dict]): List of dictionaries containing summaries and links for each tool step.

    Returns:
        str: A markdown-formatted response including key takeaways, structured outline, and references.
    """

    formatted_results = format_results_for_prompt(results)

    system_prompt = SYNTHESIZER_PROMPT.format(
        question=user_question,
        results=formatted_results
    )

    log("synthesizer", "Sending synthesis request to LLM")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


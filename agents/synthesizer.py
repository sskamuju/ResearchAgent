


import json
from core.llm import client
from core.utils import load_prompt, log
from langsmith import traceable

SYNTHESIZER_PROMPT = load_prompt("prompts/synthesizer.txt")

def format_results_for_prompt(results: list[dict]) -> str:
    """
    Takes a list of result dicts with step_id, summary, and link and
    formats them in a markdown-friendly way for injection into the prompt.
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
    tags=["agent", "synthesizer"],
    metadata={"description": "Synthesizes final answer from tool results"}
)
def synthesize_answer(user_question: str, results: list[dict]) -> str:
    """
    Synthesizes an answer to the user_question using the formatted list of search results.
    Each result must contain: step_id, summary, and link.
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





import json
from core.llm import client
from core.utils import load_prompt, log

SYNTHESIZER_PROMPT = load_prompt("prompts/synthesizer.txt")

def synthesize_answer(user_question: str, results: dict) -> str:
    formatted_results = json.dumps(results, indent=2)

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

if __name__ == "__main__":
    # Minimal CLI test
    dummy_results = {"step1": "Banks failed", "step2": "Housing collapsed"}
    answer = synthesize_answer("What caused the 2008 financial crisis?", dummy_results)
    print("\nSynthesized Answer:\n", answer)

# ResearchAgent

ResearchAgent is a headless Python research agent that automates research tasks using LLMs and external APIs. It is modular, extensible, and runs as a backend service or script—ideal for automation, data gathering, and intelligent workflow execution.

## Features

- **Headless operation:** No UI, runs as a backend service or CLI.
- **LLM-powered planning:** Uses OpenAI models to generate structured research plans.
- **Tool integration:** Supports external APIs (e.g., Tavily) for web search and data gathering.
- **Extensible architecture:** Easily add new tools, models, or workflows.
- **LangSmith integrated:** End-to-end observability of each query, including tool usage and synthesized answers.

## Project Structure

```
ResearchAgent/
├── agents/
│   ├── planner.py        # Generates research plans using LLMs
│   ├── executor.py       # Executes plan steps, manages tool registry, logging, and output
│   └── synthesizer.py    # Synthesizes final answer from tool results
├── core/
│   ├── llm.py            # OpenAI client setup
│   ├── models.py         # Pydantic models for plans and steps
│   └── utils.py          # Utility functions (e.g., logging, prompt loading)
├── tools/
│   └── tavily.py         # Tavily web search tool wrapper
├── prompts/
│   ├── planner.txt       # Prompt for planning agent
│   ├── executor.txt      # (Optional) Prompt for executor agent
│   └── synthesizer.txt   # Prompt for synthesizing agent
├── outputs/
│   └── synthesis.md      # Final answer written here on each run
├── .env.example          # Environment variable template
├── Dockerfile            # Containerization support
├── requirements.txt      # Python dependencies
├── run.py                # CLI entry point for running the agent
└── README.md             # Project documentation
```
## Docker Quickstart
docker build -t research-agent .
docker run --rm -it --env-file .env research-agent --question "Who are the most influential R&B singers of the 2010s?"
docker run --rm -it --env-file .env research-agent

## Core Workflow

1. **Planner Agent (`agents/planner.py`):**  
	Generates a step-by-step research plan using GPT-4o and a curated system prompt.

2. **Executor Agent (`agents/executor.py`):**  
	Executes each step in the plan using registered tools (e.g., web search), logs results, and handles errors.

3. **Synthesizer Agent (`agents/synthesizer.py`):**  
	Summarizes and compiles all tool results into a coherent final answer using an LLM and a synthesis prompt.

4. **LangSmith Logging:**  
	Each step is traced with tags and metadata for observability and evaluation.

## Usage

### Environment Setup

1. Install dependencies:
	```sh
	pip install -r requirements.txt
	```

2. Copy `.env.example` to `.env` and fill in your API keys:
	- `OPENAI_API_KEY`
	- `TAVILY_API_KEY`
	- (Optional) `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT` for LangSmith

### Running the Agent

```sh
python run.py --question "What caused the 2008 financial crisis?"
```
or simply:
```sh
python run.py
```
and enter your question interactively.

The final answer will be written to `outputs/synthesis.md`.

### Docker Usage

```sh
docker build -t research-agent .
docker run --rm -it --env-file .env research-agent --question "Your research question here"
```

## Extending the Agent

- Add new tools in `tools/` and register them in `agents/executor.py`.
- Modify prompts in `prompts/` to change agent behavior.
- Add new models or workflows as needed.

## Observability

- All major agent actions are traced and tagged using LangSmith for easy debugging and evaluation.
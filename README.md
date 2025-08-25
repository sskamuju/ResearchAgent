# ResearchAgent

ResearchAgent is a headless Python research agent designed to automate research tasks using LLMs and external APIs. It is modular, extensible, and runs without a user interface, making it ideal for backend automation, data gathering, and intelligent workflow execution.

## Features
- **Headless operation**: No UI, runs as a backend service or script.
- **LLM-powered planning**: Uses OpenAI models to generate structured research plans.
- **Tool integration**: Supports external APIs (e.g., Tavily) for web search and data gathering.
- **Extensible architecture**: Easily add new tools, models, or workflows.

## Project Structure

```
ResearchAgent/
├── agents/
│   ├── planner.py      # Generates research plans using LLMs
│   └── executor.py     # (To be implemented) Executes plan steps
├── core/
│   ├── llm.py          # OpenAI client setup
│   ├── models.py       # Pydantic models for plans and steps
│   └── utils.py        # Utility functions (e.g., prompt loading)
├── tools/
│   └── tavily.py       # Tavily web search integration
├── prompts/
│   └── planner.txt     # System prompt for the planner agent
├── cli.py              # Example CLI entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Containerization support
└── README              # Project documentation
```

## 🐳 Quickstart with Docker

To build and run the research agent using Docker:

```bash
# 1. Build the image
docker build -t research-agent .

# 2. Run with a CLI prompt
docker run --rm -it --env-file .env research-agent --question "Who are the most influential R&B singers of the 2010s?"

# Or to run interactively
docker run --rm -it --env-file .env research-agent

## Core Components

- **Planner Agent**: Generates a step-by-step research plan using an LLM and a custom prompt.
- **Executor Agent**: (Planned) Executes each step in the plan, calling tools or APIs as needed.
- **Tools**: Integrate with external APIs (e.g., Tavily for web search).
- **Models**: Pydantic schemas for plans and steps ensure structured data flow.

## Example Usage

```
$ python -m agents.planner
{
  "steps": [
	 {
		"id": "1",
		"tool": "tavily_search",
		"args": {"query": "2008 financial crisis causes"},
		"rationale": "Gather background information from the web."
	 },
	 ...
  ]
}
```

## Extending the Agent

- Add new tools in the `tools/` directory and register them in the executor.
- Update prompts in `prompts/` to change agent behavior.
- Add new models or workflows as needed.

## License

MIT License

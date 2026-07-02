# langsmith-lab

A hands-on lab project for learning LangSmith: tracing, manual instrumentation,
feedback logging, and evaluation of an LLM application.

## What this project does

A small question-answering service built with FastAPI and LangGraph, powered by
Groq (llama-3.3-70b-versatile). Every request is traced in LangSmith. The agent
uses a calculator tool for arithmetic, producing multi-step traces. The project
also demonstrates feedback logging via the API and offline evaluation with
heuristic and LLM-as-judge evaluators.

## Stack

- Python 3.13, Poetry
- FastAPI + Uvicorn
- LangGraph + langchain-groq
- LangSmith (tracing, feedback, evaluation)
- pytest

## Setup

1. Clone the repo and install dependencies:

       poetry install

2. Create a `.env` file in the project root:

       LANGSMITH_TRACING=true
       LANGSMITH_API_KEY=your_key
       LANGSMITH_PROJECT=langsmith-lab
       GROQ_API_KEY=your_key

3. Run the API:

       poetry run uvicorn app.main:app --reload

## Project structure

    app/
    ├── config.py            # Settings from .env; export_langsmith_env() for tracing
    ├── main.py              # FastAPI app (lifespan pattern) + /health
    ├── constants/           # Prompts, model config, eval data, messages, tags
    ├── routers/
    │   └── qa.py            # /qa/ask and /qa/feedback endpoints
    ├── schemas/
    │   └── qa.py            # Request/response models
    └── services/
        ├── agent_service.py      # LangGraph ReAct agent + calculator tool
        ├── preprocess_service.py # Traced question cleaning/validation
        ├── feedback_service.py   # Writes user feedback to LangSmith
        └── evaluators.py         # Heuristic and LLM-judge evaluators
    scripts/                 # Runnable demos and setup (see Scripts section)
    tests/                   # Offline pytest suite (see Testing section)

## Testing

The test suite runs fully offline — no Groq or LangSmith calls — so it is free,
fast, and deterministic.

    poetry run pytest -v

How the isolation works:

- LangSmith tracing is disabled in `tests/conftest.py` by setting
  `LANGSMITH_TRACING=false` before any app module is imported.
- The real `AgentService` (which builds a live LLM client) is never constructed
  in tests. FastAPI's dependency-injection override swaps in a `FakeAgentService`
  that returns a canned answer, via `app.dependency_overrides`.

This means the API contract — response shape, run_id generation, input
validation — is verified without depending on external services.

## Scripts

All scripts are run from the project root with `poetry run python scripts/<name>.py`
and require a populated `.env`.

- `check_tracing.py` — Verifies LangSmith connectivity and lists visible projects.
  Useful for diagnosing tracing/auth issues.
- `demo_agent.py` — Runs a single question through the traced pipeline. The quickest
  way to produce a trace in the LangSmith UI.
- `create_dataset.py` — Creates the evaluation dataset in LangSmith (idempotent;
  skips if it already exists).
- `run_evaluation.py` — Runs the agent against the dataset with heuristic and
  LLM-as-judge evaluators, producing a scored experiment.
- `push_prompt.py` — Pushes the agent system prompt to the LangSmith Prompt Hub.
- `demo_hub_prompt.py` — Pulls the prompt back from the Hub to demonstrate runtime
  decoupling.

## Evaluation

The project evaluates answer quality with two evaluators (`app/services/evaluators.py`):

- `correctness` — a heuristic checking whether the expected numeric value appears in
  the answer. Fast and deterministic, but brittle to phrasing (e.g. commas or written
  numbers).
- `relevance` — an LLM-as-judge scoring relevance and correctness against a reference
  answer, returning a score plus reasoning.

Run `create_dataset.py` once, then `run_evaluation.py` to produce a scored experiment
viewable in LangSmith's Datasets & Testing section. Comparing experiments across prompt
or model changes is the core regression-testing workflow.
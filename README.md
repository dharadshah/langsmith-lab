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
    ├── config.py        # Settings loaded from .env via pydantic-settings
    ├── constants/       # Prompts, model names, tags — no literals in logic files
    ├── routers/         # FastAPI routers
    ├── schemas/         # Pydantic request/response models
    └── services/        # Agent and LangSmith integration logic
    tests/               # pytest suite

## Status

Work in progress — built step by step as a learning exercise.
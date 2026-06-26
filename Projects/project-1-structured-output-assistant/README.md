# Project 1: Structured Output Assistant

This project implements a **Messy Feature Request to Engineering-Ready Requirements Assistant**.

It takes vague stakeholder input and returns a validated JSON requirements document. The goal is not to build a general chatbot. The goal is to prove that we can control model output with clear instructions, a typed schema, validation, one repair loop, and explicit clarification or refusal behavior.

## Why This Scenario

From the recommended Project 1 options, the **requirements summarizer** has the strongest engineering signal:

- It naturally needs structured output.
- It exposes incomplete-input behavior.
- It maps cleanly to product and system design interviews.
- It is easy to test with golden prompts.
- It can grow later into RAG, workflow orchestration, MCP, or a hiring-grade capstone.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| Clear system and developer instructions | `prompts.py` separates system behavior from developer constraints. |
| Schema-driven output | `schemas.py` defines strict Pydantic contracts. |
| Validation plus retry or repair loop | LangGraph routes invalid output to one repair node, then validates again. |
| Explicit refusal or clarification path | `precheck_input` handles unsafe and incomplete requests before generation. |
| At least 10 golden test prompts | `data/golden_prompts.json` contains the initial test set. |

## Architecture

```text
raw user request
    |
    v
precheck_input
    |-- unsafe request ----------> finalize(refused)
    |-- incomplete request ------> finalize(needs_clarification)
    |
    v
generate_output
    |
    v
validate_output
    |-- valid -------------------> finalize(valid document)
    |-- invalid and retry left --> repair_output --> validate_output
    |-- invalid after retry -----> finalize(schema_error)
```

## What This Recalls From The Modules

- **Module 1: Mental models** - an LLM is not the product by itself. The product is the full system around it: instructions, schema, validation, routing, and failure handling.
- **Module 3: Prompting and structured generation** - JSON instructions alone are not enough. We use a Pydantic schema and reject invalid output before it reaches downstream code.
- **Module 10/12 preview: agent and graph thinking** - even a small assistant benefits from explicit control flow. LangGraph makes the retry and clarification paths visible instead of hidden in a while loop.
- **Engineering interview habit** - every generated answer should have a status, confidence, missing information, and a reasoned failure path.

## Folder Layout

```text
Projects/project-1-structured-output-assistant/
  data/
    golden_prompts.json
  docs/
    failure_log.md
    prompt_versions.md
  src/structured_output_assistant/
    cli.py
    llm.py
    prompts.py
    schemas.py
    validation.py
    workflow/
      graph.py
      nodes.py
      state.py
  tests/
    test_golden_prompts.py
    test_schema_validation.py
```

## Run Locally

```bash
cd Projects/project-1-structured-output-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run with the deterministic local model:

```bash
requirements-assistant --input "We need admins to approve vendor onboarding requests, keep an audit trail, and notify requesters when the status changes."
```

Run with OpenAI through LangChain:

```bash
export OPENAI_API_KEY="..."
requirements-assistant --provider openai --model gpt-4o-mini --input "..."
```

## Tests

```bash
cd Projects/project-1-structured-output-assistant
pytest
```

The tests use the deterministic local model so they do not require a live API key.

## Why Not Use ADK Here

ADK and OpenAI Agents SDK are important later in the track, but Project 1 is about **structured generation discipline**, not full agent runtime comparison. For this first project, the right stack is:

- Python for implementation.
- Pydantic for schema contracts.
- LangGraph for explicit control flow.
- LangChain as an optional model-call adapter.

We should introduce ADK when the project objective asks for runtime comparison or production agent deployment patterns.

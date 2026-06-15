# Trend-Aware Video Agent

This is a learning-first project for building a video editing agent in very small steps.

The long-term product idea is:

> Upload a long video, find strong short-form clips, edit them in different styles, score their viral potential, and explain why each version may perform well.

Step 01 is intentionally only a skeleton. It gives us named places for the system parts before we add real video processing, LLM calls, RAG, MCP, or agent-to-agent communication.

## Current Skeleton

```text
src/trend_video_agent/
  main.py              FastAPI app entrypoint
  schemas.py           API request/response contracts
  config.py            App settings
  workflow/            LangGraph-shaped workflow state and nodes
  agents/              Specialist agent stubs
  tools/               Video/trend tool stubs
  rag/                 Vector memory placeholder
  mcp/                 MCP server placeholder
  a2a/                 Agent-to-agent message placeholder
tests/
  test_skeleton_contract.py
docs/
  STEP_01_SKELETON.md
```

## Run Later

We are not installing dependencies in Step 01. When we are ready to run the API, use:

```bash
cd App
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn trend_video_agent.main:app --reload
```

## First API Shape

- `GET /health` checks that the app is alive.
- `POST /projects` creates a learning project record from basic metadata.
- `POST /workflows/dry-run` returns the planned agent stages without processing a real video.

# GenAI Interview-Ready Pack

This folder turns the GenAI learning system into interview preparation material.

The main canon teaches the concepts. The projects prove implementation. This pack helps you convert both into clear interview answers, system-design discussions, debugging stories, and production judgment.

## Folder Map

| File | Use it for |
|---|---|
| [TOP_CONCEPTS.md](./TOP_CONCEPTS.md) | The highest-yield concepts to touch in GenAI interviews, with traps and talk tracks. |
| [INTERVIEW_QUESTIONS.md](./INTERVIEW_QUESTIONS.md) | Common conceptual, system-design, debugging, and project deep-dive questions. |
| [PRODUCTION_SCENARIOS.md](./PRODUCTION_SCENARIOS.md) | Realistic incidents and production situations, with first inspection points and mitigations. |
| [ANSWER_FRAMEWORKS.md](./ANSWER_FRAMEWORKS.md) | Reusable structures for answering design, debugging, tradeoff, and project questions. |
| [PORTFOLIO_STORIES.md](./PORTFOLIO_STORIES.md) | How to turn each project in this repo into interview evidence. |
| [QUICK_REVIEW_CARDS.md](./QUICK_REVIEW_CARDS.md) | Fast recall cards for last-mile review. |

## How To Use This Pack

Use the main learning track for depth. Use this folder when you need interview readiness.

### 7-Day Prep Loop

| Day | Focus | Output |
|---|---|---|
| 1 | Read [TOP_CONCEPTS.md](./TOP_CONCEPTS.md) | Mark weak concepts. |
| 2 | Drill conceptual questions | Answer 15 aloud from [INTERVIEW_QUESTIONS.md](./INTERVIEW_QUESTIONS.md). |
| 3 | Drill RAG, vector search, eval, and safety designs | Whiteboard 2 designs using [ANSWER_FRAMEWORKS.md](./ANSWER_FRAMEWORKS.md). |
| 4 | Drill production scenarios | Diagnose 10 cases from [PRODUCTION_SCENARIOS.md](./PRODUCTION_SCENARIOS.md). |
| 5 | Practice project stories | Use [PORTFOLIO_STORIES.md](./PORTFOLIO_STORIES.md) to build 3 crisp stories. |
| 6 | Mock interview | One system design, one debugging case, one project deep dive. |
| 7 | Quick review | Use [QUICK_REVIEW_CARDS.md](./QUICK_REVIEW_CARDS.md). |

### Daily 45-Minute Maintenance Loop

| Time | Drill |
|---:|---|
| 10m | Recite 5 top concepts without notes. |
| 15m | Answer 3 interview questions aloud. |
| 15m | Diagnose 1 production scenario. |
| 5m | Record one weak answer and improve it. |

## Interview Readiness Definition

You are interview-ready when you can do all of the following without bluffing:

- Explain a GenAI system as layers: model, prompt, retrieval, tools, orchestration, eval, safety, observability, cost.
- Design a RAG system with ingestion, chunking, retrieval, reranking, citations, permissions, and evals.
- Separate retrieval failures from generation failures using traces and metrics.
- Explain when an agent is justified and when a deterministic workflow is better.
- Add safety controls for prompt injection, data exfiltration, unsafe tools, and unauthorized retrieval.
- Budget token cost, latency, model routing, retries, caching, and fallbacks.
- Defend framework choices across LangChain, LangGraph, MCP, LlamaIndex, ADK, and OpenAI Agents SDK.
- Walk through one project using problem, architecture, tradeoffs, failures, metrics, and next improvements.

## The Core Interview Identity

The target answer style is:

> I design GenAI systems as debuggable production systems, not chatbot demos. I separate retrieval, generation, tools, orchestration, safety, evaluation, and cost so failures can be measured and fixed by layer.

Everything in this folder trains that identity.


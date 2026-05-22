# GenAI 10-12 Hour Weekly Execution Plan

This file operationalizes the roadmap in [GENAI_MASTERY_CANON.md](./GENAI_MASTERY_CANON.md).

It is built for a realistic pace of 10 to 12 hours per week and is optimized for the hiring-ready track first. The goal is not perfect completion of every concept. The goal is visible skill, repeated shipping, and steady progression toward a strong GenAI systems profile.

## Linked Documents

- [GenAI Document Index](./GENAI_DOC_INDEX.md)
- [GenAI Mastery Canon](./GENAI_MASTERY_CANON.md)
- [GenAI Mini-Project Specifications](./GENAI_MINI_PROJECT_SPECS.md)

## Core Rules

- Ship imperfect systems. Learn through failure, not completeness.
- Every week must produce one visible output: notes, metrics, a design, a benchmark, or a working slice.
- Every build checkpoint must include a failure log.
- If you get stuck for more than 90 minutes, write down the blocker, classify it by layer, and move on.
- Track cost, latency, and evaluation from early builds onward.
- Data quality is not a side topic. Treat it as a primary system variable in every retrieval-heavy build.

## Weekly Time Budget Template

Use this structure unless a build week needs more implementation time.

- 4h core learning
- 2h reading and note synthesis
- 3h hands-on lab or implementation
- 1h weekly loops from the canon
- 1h review, reflection, and next-week prep

## What This Plan Covers

- Weeks 1-40: hiring-ready track with one packaged capstone slice
- Weeks 41-52: optional extension toward the broader mastery canon

## Linked References

- Core execution order in the canon: [Module 1](./GENAI_MASTERY_CANON.md#module-1-genai-landscape-and-mental-models), [Module 3](./GENAI_MASTERY_CANON.md#module-3-prompting-and-structured-generation), [Module 4](./GENAI_MASTERY_CANON.md#module-4-embeddings-and-semantic-representations), [Module 5](./GENAI_MASTERY_CANON.md#module-5-vector-search-and-vector-datastores), [Module 6](./GENAI_MASTERY_CANON.md#module-6-rag-foundations), [Module 8](./GENAI_MASTERY_CANON.md#module-8-evaluation-observability-and-experimentation), [Module 20](./GENAI_MASTERY_CANON.md#module-20-cost-engineering-and-product-tradeoffs-for-genai), [Module 7](./GENAI_MASTERY_CANON.md#module-7-advanced-retrieval-engineering), [Module 9](./GENAI_MASTERY_CANON.md#module-9-safety-guardrails-and-reliability), [Module 10](./GENAI_MASTERY_CANON.md#module-10-agent-fundamentals), [Module 11](./GENAI_MASTERY_CANON.md#module-11-langchain-core), [Module 12](./GENAI_MASTERY_CANON.md#module-12-langgraph-mastery), [Module 13](./GENAI_MASTERY_CANON.md#module-13-model-context-protocol-mcp), [Module 21](./GENAI_MASTERY_CANON.md#module-21-genai-debugging-playbook), [Module 2](./GENAI_MASTERY_CANON.md#module-2-transformer-and-modern-llm-internals), [Module 19](./GENAI_MASTERY_CANON.md#module-19-capstones-and-mastery-loops), and [Module 22](./GENAI_MASTERY_CANON.md#module-22-portfolio-packaging-and-hiring-signal-design)
- Build checkpoints and projects: [Project 1](./GENAI_MINI_PROJECT_SPECS.md#project-1-structured-output-assistant), [Project 2](./GENAI_MINI_PROJECT_SPECS.md#project-2-semantic-search-lab), [Project 3](./GENAI_MINI_PROJECT_SPECS.md#project-3-baseline-rag-assistant-with-citations), [Project 4](./GENAI_MINI_PROJECT_SPECS.md#project-4-advanced-rag-with-reranking-and-guardrails), [Project 5](./GENAI_MINI_PROJECT_SPECS.md#project-5-langgraph-workflow-agent), [Project 6](./GENAI_MINI_PROJECT_SPECS.md#project-6-mcp-enabled-workflow-with-cost-and-latency-budget), [Project 7](./GENAI_MINI_PROJECT_SPECS.md#project-7-data-heavy-assistant-and-framework-selection-memo), [Project 8](./GENAI_MINI_PROJECT_SPECS.md#project-8-long-lived-multimodal-or-human-in-the-loop-system), [Project 9](./GENAI_MINI_PROJECT_SPECS.md#project-9-optimization-or-debugging-case-study), and [Project 10](./GENAI_MINI_PROJECT_SPECS.md#project-10-hiring-grade-capstone-asset-pack)

## Weeks 1-40: Hiring-Ready Track

| Week | Focus | Hours | Primary Output |
|---|---|---:|---|
| 1 | Module 1: taxonomy, vocabulary, anatomy of GenAI systems | 11h | One-page system layer map and glossary |
| 2 | Module 1: failure modes plus Module 3: prompt design patterns | 11h | Failure taxonomy notes and prompt pattern cheat sheet |
| 3 | Module 3: structured outputs, validation, prompt debugging | 12h | Validated structured-output assistant plan |
| 4 | [Build Checkpoint 1](./GENAI_MINI_PROJECT_SPECS.md#project-1-structured-output-assistant) | 10h | Shipped [Project 1](./GENAI_MINI_PROJECT_SPECS.md#project-1-structured-output-assistant) plus short failure log |
| 5 | Module 4: embeddings, vector geometry, similarity metrics | 11h | Embedding model comparison notes |
| 6 | Module 4: embedding pipelines plus Module 5: ANN basics | 11h | Chunk representation strategy and ANN notes |
| 7 | Module 5: vector store ecosystem, filters, hybrid retrieval | 12h | Vector datastore tradeoff memo |
| 8 | [Build Checkpoint 2](./GENAI_MINI_PROJECT_SPECS.md#project-2-semantic-search-lab) | 10h | Shipped [Project 2](./GENAI_MINI_PROJECT_SPECS.md#project-2-semantic-search-lab) plus retrieval benchmark summary |
| 9 | Module 6: ingestion, parsing, chunking, metadata design | 11h | Corpus preparation and chunking policy |
| 10 | Module 6: retrieval flow, citations, context packing | 11h | Baseline RAG architecture sketch |
| 11 | Module 6: grounded generation plus Module 8: metrics | 12h | Initial eval rubric for RAG |
| 12 | Module 8: golden sets, LLM-as-judge, tracing, observability | 11h | Small eval dataset and trace checklist |
| 13 | [Build Checkpoint 3](./GENAI_MINI_PROJECT_SPECS.md#project-3-baseline-rag-assistant-with-citations) | 10h | Shipped [Project 3](./GENAI_MINI_PROJECT_SPECS.md#project-3-baseline-rag-assistant-with-citations) with citations and initial eval suite |
| 14 | Module 20: token economics, request cost, latency decomposition | 11h | Cost and latency budget worksheet |
| 15 | Module 20: ROI/product tradeoffs plus Module 7: hierarchical retrieval | 11h | Product decision memo: when GenAI is justified |
| 16 | Module 7: query rewriting, multi-query retrieval, reranking | 12h | Retrieval improvement experiment plan |
| 17 | Module 7: advanced RAG patterns plus Module 9: safety basics | 12h | Baseline-vs-advanced RAG change list |
| 18 | Module 9: tool security, retrieval security, reliability design | 11h | Guardrails and approval policy draft |
| 19 | [Build Checkpoint 4](./GENAI_MINI_PROJECT_SPECS.md#project-4-advanced-rag-with-reranking-and-guardrails) | 10h | Shipped [Project 4](./GENAI_MINI_PROJECT_SPECS.md#project-4-advanced-rag-with-reranking-and-guardrails) plus failure analysis report |
| 20 | Module 10: what agents are, planning styles, tool use | 11h | Agent suitability rubric |
| 21 | Module 10: memory, failure handling plus Module 11: LangChain core | 11h | Agent control-flow notes and LangChain abstraction map |
| 22 | Module 11: LangChain retrieval, tools, production use | 12h | Minimal LangChain-powered workflow skeleton |
| 23 | Module 12: LangGraph state design and graph mental models | 11h | State schema and node/edge diagram |
| 24 | Module 12: durable execution, interrupts, approvals | 12h | Approval and recovery design for a workflow |
| 25 | Module 12: production graph patterns and trace review | 11h | LangGraph workflow test plan |
| 26 | [Build Checkpoint 5](./GENAI_MINI_PROJECT_SPECS.md#project-5-langgraph-workflow-agent) | 10h | Shipped [Project 5](./GENAI_MINI_PROJECT_SPECS.md#project-5-langgraph-workflow-agent) with traces and one approval step |
| 27 | Module 13: MCP protocol, tools, resources, capabilities | 11h | MCP client/server concept notes |
| 28 | Module 13: enterprise MCP usage, auth, policy, audit | 11h | MCP capability design memo |
| 29 | Module 21: failure taxonomy, layer-based triage, reproducibility | 12h | GenAI debugging checklist |
| 30 | [Build Checkpoint 6](./GENAI_MINI_PROJECT_SPECS.md#project-6-mcp-enabled-workflow-with-cost-and-latency-budget) | 10h | Shipped [Project 6](./GENAI_MINI_PROJECT_SPECS.md#project-6-mcp-enabled-workflow-with-cost-and-latency-budget) with cost budget and debug memo |
| 31 | Module 2: tokens, context, segmentation, token budgeting | 11h | Context budget worksheet |
| 32 | Module 2: transformer mechanics, KV cache, batching | 12h | Transformer intuition notes for engineers |
| 33 | Module 2: alignment, tool use, reasoning behavior plus capstone scoping | 11h | Capstone scope, success metrics, and constraints |
| 34 | Module 19 slice: capstone architecture, data plan, eval targets | 10h | Architecture diagram and evaluation plan |
| 35 | Module 19 slice: capstone implementation week 1 | 12h | Working capstone backbone |
| 36 | Module 19 slice: capstone implementation week 2 | 12h | Retrieval or workflow path completed |
| 37 | Module 19 slice: eval, debugging, safety, and cost optimization | 11h | Failure analysis and improvement log |
| 38 | Module 22: architecture storytelling, README, demo narrative | 11h | Architecture diagram and project README |
| 39 | Module 22: tradeoff memo, failure writeup, hiring-facing assets | 11h | Tradeoff justification and case-study summary |
| 40 | Final hiring-ready consolidation | 10h | Interview walkthrough, resume bullets, and next-phase plan |

## Weeks 41-52: Optional Mastery Extension

| Week | Focus | Hours | Primary Output |
|---|---|---:|---|
| 41 | Module 14: LlamaIndex ingestion, indexing, nodes | 11h | Data-heavy system ingestion notes |
| 42 | Module 14: retrievers, query engines, workflows | 11h | Document assistant design using a data-centric stack |
| 43 | Module 15: ADK and OpenAI Agents SDK concepts | 11h | Runtime comparison notes |
| 44 | [Build Checkpoint 7](./GENAI_MINI_PROJECT_SPECS.md#project-7-data-heavy-assistant-and-framework-selection-memo) | 10h | Shipped [Project 7](./GENAI_MINI_PROJECT_SPECS.md#project-7-data-heavy-assistant-and-framework-selection-memo) plus framework-selection memo |
| 45 | Module 16: multi-agent coordination and approval logic | 11h | Multi-agent suitability memo |
| 46 | Module 16: long-lived memory and execution | 11h | Memory design policy |
| 47 | Module 17: multimodal, voice, visual grounding | 12h | Multimodal system scope and evaluation rubric |
| 48 | [Build Checkpoint 8](./GENAI_MINI_PROJECT_SPECS.md#project-8-long-lived-multimodal-or-human-in-the-loop-system) | 10h | Shipped [Project 8](./GENAI_MINI_PROJECT_SPECS.md#project-8-long-lived-multimodal-or-human-in-the-loop-system) with operational boundaries |
| 49 | Module 18: prompt ceiling, DSPy, optimization logic | 11h | Optimization decision memo |
| 50 | Module 18: fine-tuning, distillation, adaptation | 11h | Model adaptation comparison notes |
| 51 | [Build Checkpoint 9](./GENAI_MINI_PROJECT_SPECS.md#project-9-optimization-or-debugging-case-study) | 10h | Shipped [Project 9](./GENAI_MINI_PROJECT_SPECS.md#project-9-optimization-or-debugging-case-study) with before-vs-after metrics |
| 52 | [Full capstone expansion plus portfolio hardening](./GENAI_MINI_PROJECT_SPECS.md#project-10-hiring-grade-capstone-asset-pack) | 12h | Upgraded capstone and final [Project 10 asset pack](./GENAI_MINI_PROJECT_SPECS.md#project-10-hiring-grade-capstone-asset-pack) |

## Monthly Review Ritual

Run this at the end of Weeks 4, 8, 13, 19, 26, 30, 40, 44, 48, and 52.

- Review what you shipped.
- List the top 3 recurring failure modes.
- Record one cost or latency mistake you made.
- Record one retrieval or evaluation lesson you would now teach someone else.
- Decide whether the next month needs more theory, more building, or more debugging.

## Design Interview Layer To Run In Parallel

Starting from Week 13, spend 30 to 45 minutes every other week on one design prompt.

Suggested prompts:

- Design an internal document assistant with citations and permission-aware retrieval.
- Design a voice-based assistant with low-latency responses and safe tool use.
- Design a long-running workflow agent that needs human approval for risky actions.
- Design a multimodal document analysis system for contracts or reports.

For each prompt, answer five things:

- Why GenAI is justified or not justified
- Data and retrieval strategy
- Evaluation and failure handling
- Cost and latency tradeoffs
- Why this orchestration choice is appropriate

## What Success Looks Like By Week 40

By the end of Week 40, you should be able to:

- Build and evaluate at least three meaningful GenAI systems
- Explain retrieval, orchestration, evaluation, safety, cost, and debugging as separate layers
- Show one hiring-grade capstone slice with architecture, failure analysis, and tradeoff evidence
- Defend your design choices in an interview without relying on framework slogans

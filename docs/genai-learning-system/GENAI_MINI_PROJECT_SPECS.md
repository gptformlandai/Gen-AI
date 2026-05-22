# GenAI Mini-Project Specifications

This file turns the build checkpoints from [GENAI_MASTERY_CANON.md](./GENAI_MASTERY_CANON.md) into concrete project specs.

These are not toy demos. Each project is designed to prove one layer of GenAI systems maturity.

## Linked Documents

- [GenAI Document Index](./GENAI_DOC_INDEX.md)
- [GenAI Mastery Canon](./GENAI_MASTERY_CANON.md)
- [GenAI 10-12 Hour Weekly Execution Plan](./GENAI_10_12H_WEEKLY_EXECUTION_PLAN.md)

## Universal Rules For Every Project

- Ship a working slice before polishing.
- Keep a short failure log with at least 5 real issues.
- Add one simple evaluation or benchmark, even if it is imperfect.
- Record one cost or latency observation once cost becomes relevant.
- Write one short tradeoff note: why this architecture and not the obvious alternative.

## Project 1: Structured Output Assistant

**Unlocked after:** [Module 1](./GENAI_MASTERY_CANON.md#module-1-genai-landscape-and-mental-models) and [Module 3](./GENAI_MASTERY_CANON.md#module-3-prompting-and-structured-generation)  
**Time box:** 1 week  
**Core layer proven:** prompt and schema discipline

### Objective

Build an assistant that converts messy user requests into reliable structured output instead of free-form text.

### Recommended use cases

- Task planner
- Meeting brief generator
- Requirements summarizer
- Study-plan generator

### Required capabilities

- Clear system and developer instructions
- Schema-driven output such as JSON or typed fields
- Validation plus one retry or repair loop
- Explicit refusal or clarification path when input is incomplete
- At least 10 golden test prompts

### Deliverables

- Working assistant
- Output schema
- Prompt versions with notes on what changed
- Short failure log
- 1-page reflection on common prompt failures

### Success criteria

- At least 90% schema-valid responses on the golden set
- Clear handling of incomplete input
- No silent failure when required fields are missing

### What it proves

You can move beyond “chatbot prompting” into controlled generation.

---

## Project 2: Semantic Search Lab

**Unlocked after:** [Module 4](./GENAI_MASTERY_CANON.md#module-4-embeddings-and-semantic-representations) and [Module 5](./GENAI_MASTERY_CANON.md#module-5-vector-search-and-vector-datastores)  
**Time box:** 1 week  
**Core layer proven:** embeddings and retrieval fundamentals

### Objective

Build a semantic search system over a small but non-trivial corpus and compare exact retrieval against approximate retrieval behavior.

### Recommended corpus size

- 300 to 2,000 documents or chunks

### Required capabilities

- Document ingestion and chunking
- Embedding pipeline with one chosen model
- Exact similarity baseline or brute-force baseline
- One ANN-backed retrieval option
- Metadata filters
- At least 10 labeled search queries

### Deliverables

- Search interface or CLI
- Retrieval comparison table
- Recall or hit-rate notes on the labeled queries
- Vector store tradeoff memo

### Success criteria

- Explain why certain queries fail
- Show exact-vs-ANN differences
- Demonstrate at least one metadata filtering use case

### What it proves

You understand vector retrieval as a system, not a magic box.

---

## Project 3: Baseline RAG Assistant With Citations

**Unlocked after:** [Module 6](./GENAI_MASTERY_CANON.md#module-6-rag-foundations) and [Module 8](./GENAI_MASTERY_CANON.md#module-8-evaluation-observability-and-experimentation)  
**Time box:** 1 week  
**Core layer proven:** baseline RAG plus first evaluation discipline

### Objective

Build a grounded assistant that answers questions using retrieved context and returns citations.

### Required capabilities

- Ingestion and chunking strategy
- Vector retrieval over your corpus
- Prompting that separates evidence from final answer
- Citation output with source traceability
- Small evaluation set with at least 20 to 25 questions
- One basic trace or logging mechanism

### Deliverables

- Working RAG assistant
- Evaluation sheet with pass or fail outcomes
- Citation examples
- Failure categories such as missed retrieval, wrong grounding, weak answer synthesis

### Success criteria

- Answer uses evidence instead of unsupported claims
- Refuses when evidence is insufficient
- Evaluation set reveals real failure patterns

### What it proves

You can build a practical RAG baseline and evaluate it honestly.

---

## Project 4: Advanced RAG With Reranking And Guardrails

**Unlocked after:** [Module 7](./GENAI_MASTERY_CANON.md#module-7-advanced-retrieval-engineering) and [Module 9](./GENAI_MASTERY_CANON.md#module-9-safety-guardrails-and-reliability)  
**Time box:** 1 week  
**Core layer proven:** retrieval engineering plus safety and reliability thinking

### Objective

Upgrade the baseline RAG system with better retrieval quality, safer behavior, and clearer failure handling.

### Required capabilities

- Query rewriting or multi-query retrieval
- Reranking layer
- Guardrails or approval logic for risky requests
- Failure analysis comparing baseline vs advanced system
- Permission-aware or safety-aware refusal behavior

### Deliverables

- Side-by-side baseline vs advanced comparison
- Before-vs-after retrieval or answer quality notes
- Short safety policy
- Failure analysis report

### Success criteria

- Clear quality improvement over Project 3 on a comparable eval set
- At least one safety or guardrail scenario handled correctly
- Tradeoff note on extra cost vs improved quality

### What it proves

You can improve a retrieval system using engineering methods, not just prompt changes.

---

## Project 5: LangGraph Workflow Agent

**Unlocked after:** [Module 10](./GENAI_MASTERY_CANON.md#module-10-agent-fundamentals) and [Module 12](./GENAI_MASTERY_CANON.md#module-12-langgraph-mastery)  
**Time box:** 1 week  
**Core layer proven:** explicit orchestration and stateful workflow design

### Objective

Build a tool-using workflow agent with explicit graph state, retries, and one human approval point.

### Recommended use cases

- Research assistant
- Workflow triage agent
- Multi-step document reviewer
- Task-routing assistant

### Required capabilities

- Explicit state schema
- At least 3 nodes in a graph with conditional routing
- One retry or recovery branch
- One human approval or interrupt step
- Trace capture or state inspection output

### Deliverables

- Graph diagram
- Working workflow
- State transition notes
- Failure cases involving loops, retries, or bad tool outputs

### Success criteria

- Workflow behavior is explainable node by node
- Human approval is meaningful, not decorative
- Failure handling is visible in the graph

### What it proves

You can move from agent hype to controlled orchestration.

---

## Project 6: MCP-Enabled Workflow With Cost And Latency Budget

**Unlocked after:** [Module 13](./GENAI_MASTERY_CANON.md#module-13-model-context-protocol-mcp) and [Module 20](./GENAI_MASTERY_CANON.md#module-20-cost-engineering-and-product-tradeoffs-for-genai)  
**Time box:** 1 week  
**Core layer proven:** standards-based tool integration plus cost-aware system design

### Objective

Build a workflow that consumes one or more MCP-exposed capabilities and attach a cost and latency budget to the end-to-end run.

### Required capabilities

- At least one MCP tool or resource
- One workflow that meaningfully uses the MCP capability
- Approval or policy boundary for a risky action
- Token, latency, or request-budget estimate
- Debug memo describing one expensive or slow path

### Deliverables

- MCP capability description
- Workflow demo
- Cost and latency budget sheet
- One debugging note on performance or failure handling

### Success criteria

- MCP is used for a real capability, not only for novelty
- Budget assumptions are explicit
- Dangerous actions are gated or reviewed

### What it proves

You understand interoperability, not just SDK-specific tool use.

---

## Project 7: Data-Heavy Assistant And Framework Selection Memo

**Unlocked after:** [Module 14](./GENAI_MASTERY_CANON.md#module-14-llamaindex-and-data-centric-genai-systems) and [Module 15](./GENAI_MASTERY_CANON.md#module-15-adk-and-openai-agents-sdk)  
**Time box:** 1 week  
**Core layer proven:** data-centric system design plus runtime comparison maturity

### Objective

Build a document-heavy or data-heavy assistant and justify your framework/runtime choices in writing.

### Recommended use cases

- Contract assistant
- Research memo assistant
- Knowledge-base assistant with complex documents
- Extraction and summarization pipeline

### Required capabilities

- Document ingestion and structure-aware parsing
- Retrieval or workflow path suited to data-heavy work
- Written comparison of at least two frameworks or runtimes
- Evaluation plan for document-heavy failure modes

### Deliverables

- Working assistant or pipeline
- Framework-selection memo
- Example difficult documents and how your system handles them
- Evaluation notes for structure-heavy data

### Success criteria

- Framework choice is justified with tradeoffs
- You can explain why this is data-heavy rather than generic chat
- Difficult document structure is handled intentionally

### What it proves

You can choose frameworks with engineering judgment.

---

## Project 8: Long-Lived Multimodal Or Human-In-The-Loop System

**Unlocked after:** [Module 16](./GENAI_MASTERY_CANON.md#module-16-multi-agent-human-in-the-loop-and-long-lived-systems) and [Module 17](./GENAI_MASTERY_CANON.md#module-17-multimodal-voice-and-realtime-genai)  
**Time box:** 1 week  
**Core layer proven:** operational boundaries for advanced agent systems

### Objective

Build a system that is either multimodal, long-lived, or human-in-the-loop with explicit operational boundaries.

### Recommended use cases

- Voice assistant with approval before action
- Visual document reviewer
- Human-reviewed research workflow
- Long-running incident assistant

### Required capabilities

- One non-text modality or one clear human-review boundary
- Long-lived state or resumable workflow behavior
- Failure-mode list for latency, ambiguity, and unsafe actions
- Evaluation rubric suited to the chosen modality

### Deliverables

- System demo or workflow run-through
- Operational boundary definition
- Evaluation rubric
- Failure log focused on modality or long-horizon behavior

### Success criteria

- The system has clear constraints and escalation rules
- Multimodal or human-review behavior is not superficial
- Latency and safety expectations are stated explicitly

### What it proves

You can design more than a single-turn text assistant.

---

## Project 9: Optimization Or Debugging Case Study

**Unlocked after:** [Module 18](./GENAI_MASTERY_CANON.md#module-18-dspy-fine-tuning-distillation-and-optimization) and [Module 21](./GENAI_MASTERY_CANON.md#module-21-genai-debugging-playbook)  
**Time box:** 1 week  
**Core layer proven:** senior-style diagnosis and measurable improvement

### Objective

Take one earlier project that is meaningfully flawed, diagnose it by layer, and improve it with measurable before-vs-after results.

### Required capabilities

- Clear failure hypothesis
- Layer-based diagnosis: retrieval, prompt, model, tool, or orchestration
- One targeted intervention such as reranking, prompt restructure, model switch, context compression, or control-flow repair
- Before-vs-after evaluation or performance comparison

### Deliverables

- Incident-style writeup
- Root-cause analysis
- Metrics table before and after
- Remediation note and remaining risks

### Success criteria

- Diagnosis is evidence-based, not guessed
- Improvement is measurable
- Remaining limitations are stated clearly

### What it proves

You can debug GenAI systems like an engineer, not just tweak them until they look better.

---

## Project 10: Hiring-Grade Capstone Asset Pack

**Unlocked after:** [Module 19](./GENAI_MASTERY_CANON.md#module-19-capstones-and-mastery-loops) and [Module 22](./GENAI_MASTERY_CANON.md#module-22-portfolio-packaging-and-hiring-signal-design)  
**Time box:** 1 week  
**Core layer proven:** ability to present serious work as hiring evidence

### Objective

Take your best capstone and package it so a recruiter, hiring manager, or senior engineer can understand its value quickly.

### Required capabilities

- Architecture diagram
- Failure analysis document
- Tradeoff justification memo
- Evaluation summary
- README that explains the problem, system, and results
- Interview walkthrough outline

### Deliverables

- One polished case-study package
- 3 to 5 resume bullets grounded in measurable outcomes
- 3-minute demo narrative
- FAQ for likely interview questions

### Success criteria

- A reviewer can understand the project without a live explanation
- Tradeoffs and failures are visible, not hidden
- The project reads like engineering evidence, not portfolio theater

### What it proves

You can turn execution into hiring signal.

---

## If You Only Build Three Projects

If time gets tight, prioritize these three:

- Project 3: Baseline RAG Assistant With Citations
- Project 4: Advanced RAG With Reranking And Guardrails
- Project 5 or Project 6: LangGraph Workflow Agent or MCP-Enabled Workflow

That combination gives you the strongest near-term hiring story: retrieval, evaluation, orchestration, and modern tooling discipline.

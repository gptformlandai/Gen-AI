# Portfolio Stories And Project Evidence

This file helps you turn the repo into interview evidence. The goal is to answer like an engineer who built and debugged systems, not someone who only studied concepts.

## The Strongest Portfolio Narrative

> I built a GenAI systems learning track with runnable projects that move from structured output to semantic search, RAG, advanced retrieval, orchestration, MCP, HITL workflows, debugging, and capstone packaging. The strongest thread is RAG reliability engineering: measure failures by layer, improve retrieval and guardrails, and package the results with metrics and tradeoffs.

## Project Evidence Map

| Project | What it proves | Best interview use |
|---|---|---|
| Project 1: Structured Output Assistant | Schema discipline, validation, repair loop, clarification/refusal. | Prompting and structured generation question. |
| Project 2: Semantic Search Lab | Embeddings, exact vs ANN retrieval, metadata filters, retrieval evaluation. | Vector search and embedding question. |
| Project 3: Baseline RAG Assistant | Grounded answers, citations, refusal, traces, evals. | Baseline RAG design question. |
| Project 4: Advanced RAG | Query rewriting, reranking, guardrails, before/after comparison. | Advanced retrieval and safety question. |
| Project 5: LangGraph Workflow Agent | Explicit state, conditional routing, retries, human approval. | Agent vs workflow or LangGraph question. |
| Project 6: MCP Workflow | Tools/resources boundary, policy gate, cost/latency budget. | MCP and production tool integration question. |
| Project 7: Contract Data Assistant | Structure-aware parsing, data-heavy retrieval, framework selection. | LlamaIndex/data-centric design question. |
| Project 8: HITL Incident Assistant | Long-lived state, resumability, approval boundaries, event log. | HITL and production incident workflow question. |
| Project 9: RAG Debugging Case Study | Root cause analysis, layer diagnosis, measurable improvement. | Debugging and senior ownership question. |
| Project 10: Capstone Pack | Architecture storytelling, metrics, tradeoffs, resume bullets. | Project deep-dive and portfolio question. |
| ADK Enterprise Ops Lab | End-to-end enterprise agent reference with RAG, MCP, memory, eval, observability, guardrails. | Advanced runtime and enterprise-readiness question. |
| App: Trend-Aware Video Agent | Skeleton for multimodal/video agent path. | Future roadmap and product imagination question. |

## Story 1: RAG Reliability Engineering

**Use when asked:** "Tell me about your strongest GenAI project."

**Problem:** Support and operations assistants need answers grounded in trusted knowledge with citations and safe refusals.

**Architecture:** Baseline RAG over a deterministic corpus, then advanced RAG with query rewriting, reranking, role-aware guardrails, citations, and evaluation.

**Tradeoffs:** Reranking improves top-rank evidence but adds latency and complexity. Guardrails reduce unsafe answers but require role and policy modeling. Deterministic evals are debuggable but less realistic than messy production traffic.

**Failure:** The baseline missed incident-triage and analytics-export queries and answered some restricted requests.

**Fix:** Added query rewriting, reranking, and permission-aware refusal.

**Metric:** Project 4 reports improvement from 76% to 100% on its deterministic evaluation set.

**Honest limitation:** The corpus is small and deterministic, so the next step is a harder holdout set with noisy documents, adversarial queries, and real embeddings.

## Story 2: Layer-Based Debugging

**Use when asked:** "How do you debug GenAI failures?"

**Problem:** A flawed RAG baseline had weak answers.

**Diagnosis:** Instead of changing the prompt randomly, Project 9 checked whether the expected evidence was retrieved, ranked first, and used by the answer synthesizer.

**Root cause:** The answer layer worked when the right evidence reached it. The failure was retrieval ranking: distractor documents ranked above expected evidence.

**Fix:** Added a targeted reranking layer with title, tag, synonym, and phrase features.

**Metric:** Project 9 reports pass rate and top-1 accuracy improvement from 58.33% to 100% on its test set.

**Interview line:** I treat bad answers as symptoms. I first isolate the failing layer, then make one targeted change and measure before versus after.

## Story 3: Controlled Agentic Workflow

**Use when asked:** "When would you use LangGraph?"

**Problem:** Operational requests need classification, policy lookup, retries, approval, execution, and finalization.

**Architecture:** Project 5 uses explicit workflow state and graph nodes for receive, classify, policy lookup, recovery, draft plan, approval, execute, and finalize.

**Tradeoffs:** A graph is less open-ended than an unconstrained agent, but it is easier to test, trace, pause, resume, and secure.

**Failure handling:** Policy lookup can retry and then use conservative fallback. High-risk requests stop at a human approval boundary.

**Interview line:** I use LangGraph when the workflow needs durable state, conditional routing, recovery, or approval. I do not use an agent loop just because the product sounds AI-heavy.

## Story 4: MCP And Cost-Aware Tool Integration

**Use when asked:** "What is MCP and why does it matter?"

**Problem:** Tool access should be standardized, policy-gated, and measurable.

**Architecture:** Project 6 exposes a change-management policy resource and tools for risk assessment, ticket creation, and stakeholder notification through a local MCP-style gateway.

**Tradeoffs:** A local deterministic gateway is not the same as a remote MCP server, but it makes the protocol boundary and budget accounting easy to test.

**Production concern:** Risky production changes require approval before ticket creation. Each boundary call contributes to cost and latency estimates.

**Interview line:** MCP is useful because it standardizes tool and context boundaries, but enterprise use still needs auth, versioning, audit, and approval.

## Story 5: Long-Lived HITL Incident Assistant

**Use when asked:** "How do you design safe long-running agents?"

**Problem:** Incident workflows require safe diagnostics, human approval for risky remediation, persisted state, and resumability.

**Architecture:** Project 8 triages incident reports, plans safe and unsafe actions, executes safe diagnostics, persists state, waits for approval, resumes, and records an event log.

**Tradeoffs:** Approval slows automation but controls blast radius. Persistence adds complexity but prevents losing state between triage and action.

**Interview line:** Human approval should bind to a specific action and state, not a vague conversation.

## Story 6: Data-Heavy Contract Assistant

**Use when asked:** "When is a data-centric framework useful?"

**Problem:** Contracts are not generic text. Meaning lives in clauses, sections, tables, obligations, parties, and exceptions.

**Architecture:** Project 7 parses contract markdown into typed sections, clauses, tables, metadata, and obligations. Retrieval runs over structured elements rather than raw text only.

**Tradeoffs:** Structure-aware parsing is more work than simple chunking, but it improves reliability for legal or document-heavy questions.

**Interview line:** Document AI often fails because structure is lost before retrieval starts.

## Story 7: ADK Enterprise Ops Lab

**Use when asked:** "Have you thought about enterprise agent runtimes?"

**Problem:** Production-like agent systems need more than a single agent: tools, RAG, MCP, memory, sessions, artifacts, callbacks, evals, guardrails, and deployment notes.

**Architecture:** The ADK lab simulates an enterprise operations intelligence agent with root and specialist agents, local runbook RAG, MCP operations tools, session state, memory, artifacts, workflows, callbacks, evals, and observability docs.

**Tradeoffs:** It is still local and deterministic, but it gives a reference architecture for enterprise concerns.

**Interview line:** Runtime choice matters less than whether the system has explicit state, tool governance, evals, safety, and operational traces.

## How To Answer "What Would You Improve?"

Use this exact order:

1. Add harder evals with noisy, adversarial, and held-out data.
2. Add real LLM and real embedding provider paths.
3. Add CI eval gates and regression thresholds.
4. Add OpenTelemetry or LangSmith-style tracing dashboards.
5. Add auth, tenant isolation, and adversarial security tests.
6. Deploy one full-stack capstone with Docker and a model gateway path.

## Resume Bullet Patterns

Use this shape:

```text
Built <system> that <outcome>, using <technical layers>, measured by <metric>, with <production discipline>.
```

Examples:

- Built a deterministic RAG reliability capstone with query rewriting, reranking, citations, role-aware guardrails, and before/after evaluation, improving project pass rate from 76% to 100% on a controlled eval set.
- Built a LangGraph-style operational workflow with explicit state, retries, fallback recovery, human approval, and traceable state transitions for high-risk actions.
- Built an MCP-enabled change-management workflow with resource/tool boundaries, policy gating, cost/latency budget tracking, and structured workflow traces.
- Built a RAG debugging case study that isolated retrieval ranking as the root cause and improved top-1 retrieval accuracy from 58.33% to 100% on the project eval set.

## Project Deep-Dive Checklist

Before an interview, prepare these for your best project:

| Question | Your answer should include |
|---|---|
| What problem did you solve? | User, pain, risk, why GenAI was justified. |
| What did you build? | Architecture layers and data flow. |
| What tradeoffs did you make? | At least 2 rejected alternatives. |
| What failed? | Real failure mode, not "nothing failed." |
| How did you debug it? | Trace, metric, hypothesis, targeted fix. |
| How did you measure success? | Before/after metric or eval result. |
| What would you productionize next? | Real data, auth, CI, observability, deployment. |


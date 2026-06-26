# Quick Review Cards

Use these for fast recall before interviews. Cover the answer, then say it aloud in your own words.

## Core Cards

| Prompt | Recall answer |
|---|---|
| What is the permanent GenAI system mental model? | Model, prompt, retrieval, tools, orchestration, memory, eval, safety, observability, and cost are separate layers. |
| First thing to inspect for bad RAG answer? | Retrieved evidence and trace, before prompt tweaking. |
| Embeddings prove what? | Similarity candidates, not truth or authorization. |
| RAG solves what? | Fresh, private, cited, permissioned knowledge grounding. |
| RAG does not solve what by itself? | Correctness, permissions, freshness, citation faithfulness, or safe tool use. |
| Good eval separates what? | Retrieval quality from generation quality. |
| Main retrieval metrics? | Recall@k, hit rate, MRR, NDCG. |
| Main generation metrics? | Faithfulness, groundedness, citation accuracy, schema validity, refusal correctness. |
| Agent vs workflow? | Agent chooses actions under uncertainty; workflow follows explicit state transitions. |
| When is LangGraph useful? | Stateful workflows, retries, conditional routing, checkpoints, interrupts, approvals. |
| What is MCP? | A protocol boundary for tools, resources, and prompts between clients and servers. |
| First safety principle? | Do not rely on prompts alone. Enforce controls outside the model. |

## RAG Cards

| Prompt | Recall answer |
|---|---|
| Why chunking matters? | It controls what can be found and what evidence reaches the model. |
| Fixed chunking weakness? | Can split sections, tables, and clauses badly. |
| Parent-child retrieval? | Match small chunks, return larger parent context. |
| Hybrid retrieval? | Combines dense semantic and sparse lexical signals. |
| Reranking purpose? | Improve candidate ordering after first-stage retrieval. |
| Query rewriting purpose? | Recover intent and synonym mismatch. |
| Context packing risk? | Correct evidence can be dropped or buried. |
| Citation risk? | Citation may be attached but not actually support the claim. |
| Refusal condition? | Evidence insufficient, unauthorized, unsafe, or ambiguous. |
| Freshness risk? | Old source ranks above newer policy unless metadata and filters handle it. |

## Agent And Tool Cards

| Prompt | Recall answer |
|---|---|
| Tool schema must define what? | Inputs, outputs, errors, side effects, auth, risk, timeout. |
| Unsafe tool mitigation? | Approval gate, allowlist, argument validation, idempotency, audit. |
| Agent loop failure? | Repeated calls, dead ends, hidden state, unsafe action, bad handoff. |
| First debug step for agent loop? | Inspect trajectory and state diff per step. |
| Human approval should bind to what? | Specific action, state version, actor, timestamp, and idempotency key. |
| Durable workflow needs what? | Persisted state, checkpointing, replay/recovery rules, audit trail. |
| MCP tool vs resource? | Tool performs operation; resource exposes context/data. |
| Tool output security? | Treat tool output as untrusted input. |

## Safety Cards

| Prompt | Recall answer |
|---|---|
| Direct prompt injection? | Malicious instruction from user input. |
| Indirect prompt injection? | Malicious instruction from retrieved docs, websites, emails, or tool output. |
| Permission-aware retrieval? | Filter or constrain retrieval using authenticated user/tenant/role context. |
| Data exfiltration risk? | Model or tool reveals restricted data through answer or action. |
| Cache security risk? | Response served across tenant, role, source version, or freshness boundary. |
| PII logging risk? | Production traces become unsafe datasets. |
| Defense in depth layers? | Input checks, retrieval filters, tool constraints, output checks, approvals, audit. |

## Cost And Latency Cards

| Prompt | Recall answer |
|---|---|
| Cost per request vs cost per successful task? | Successful task includes retries, failures, escalation, and user completion. |
| Token cost drivers? | Prompt size, retrieved context, tool output, output length, retries. |
| Latency drivers? | Retrieval, reranking, tool calls, model TTFT, decode, TTS for voice. |
| Gateway benefits? | Routing, fallback, quotas, logging, caching, provider abstraction. |
| Cache tradeoff? | Lower cost/latency vs staleness and false hits. |
| Semantic cache key must include? | Tenant, role, prompt/model/source versions, safety policy, locale when relevant. |
| Retry danger? | Multiplies latency/cost and can duplicate side effects. |

## Debugging Cards

| Prompt | Recall answer |
|---|---|
| Bad answer classification layers? | Retrieval, prompt, model, tool, orchestration, safety, eval, infra. |
| Retrieval migrated, quality drops? | Check chunking, embeddings, metric, index params, filters, source count. |
| Judge passes bad answer? | Check rubric, calibration, same-model bias, human agreement, deterministic checks. |
| User complains but eval passes? | Eval coverage gap; add production failures to regression set. |
| Agent unsafe action? | Missing tool governance, risk tier, approval, idempotency, auth. |
| Cost spike? | Inspect token counts, retries, model mix, cache hit rate, top-k, output length. |
| Latency spike? | Break down p95 by retrieval, reranking, tools, model, streaming. |

## One-Line Interview Answers

| Question | One-line answer |
|---|---|
| Why not always use an agent? | Deterministic workflows are safer, cheaper, and easier to test when the steps are known. |
| Why not always use fine-tuning? | It is expensive to maintain and does not solve fresh, private, or permissioned knowledge as cleanly as RAG. |
| Why not always increase top-k? | It can improve recall but adds latency, cost, and noise. |
| Why not trust citations? | Citation formatting can be correct while the cited span does not support the claim. |
| Why not rely on system prompts for security? | Prompts are guidance; security boundaries need enforceable controls. |
| Why use eval gates? | GenAI changes can regress quality or safety silently, so promotion needs measurable checks. |

## Last-Minute Whiteboard Flow

```text
User
  -> Auth / Risk Context
  -> Router
  -> Retrieval or Tool Planning
  -> Permission Filter
  -> Rerank / Validate
  -> Context Packing or Tool Execution
  -> Model Generation
  -> Guardrail / Citation Check
  -> Response
  -> Trace + Eval + Feedback
```

## Last-Minute Self-Test

Answer these aloud:

1. Design permission-aware RAG for internal policies.
2. Debug a wrong answer with a citation.
3. Explain agent vs workflow vs copilot.
4. Explain MCP in one minute.
5. Explain how you would reduce GenAI cost by 40%.
6. Explain how prompt injection can arrive through retrieval.
7. Walk through Project 9 as a debugging story.
8. Name the first metric you would inspect for retrieval quality.
9. Explain why a 100% eval score on a small corpus is not enough.
10. Describe what you would add before production deployment.


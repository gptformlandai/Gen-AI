# Top GenAI Interview Concepts

Use this file as the high-yield concept map. In interviews, you do not need to recite everything. You need to show that you understand the system layer, the tradeoff, the failure mode, and the production consequence.

## How To Answer Any Concept

Use this shape:

1. Define it in one sentence.
2. Explain why it exists.
3. Say where it fits in the system.
4. Name the main tradeoff.
5. Name one production failure mode.
6. Mention how you would measure or debug it.

Example:

> RAG grounds model output in retrieved evidence. It exists because model memory is not enough for private, fresh, or permissioned knowledge. The tradeoff is added retrieval complexity, latency, and citation quality work. If answers are wrong, I first inspect retrieved chunks before tuning the prompt.

## Concept Priority Map

| Priority | Concept | Why interviewers care |
|---|---|---|
| P0 | RAG, retrieval, evaluation, safety, cost | These are the highest-signal GenAI application engineering topics. |
| P0 | Agents vs workflows, tool use, LangGraph, MCP | These separate controlled systems from agent hype. |
| P1 | Embeddings, vector DBs, hybrid retrieval, reranking | Needed for serious search and knowledge systems. |
| P1 | Observability, tracing, debugging, production incidents | Shows senior engineering maturity. |
| P2 | LLM internals, inference, serving, caching, gateways | Important for scale and staff-level depth. |
| P2 | Multimodal, voice, fine-tuning, DSPy, data flywheel | Useful for breadth and advanced follow-ups. |

## 1. GenAI System Anatomy

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you see beyond the model? | Explain model, prompt, retrieval, tool, memory, orchestration, eval, safety, observability, cost. | Talking as if the LLM alone is the system. |

**Talk track:** A production GenAI app is a system around a model. The model generates, but retrieval grounds, tools act, orchestration controls, evals measure, guardrails constrain, and traces explain failures.

**Production failure:** User gets a polished but wrong answer. First inspect retrieval candidates, prompt context, tool outputs, and trace spans before blaming the model.

**Repo evidence:** Module 1, Projects 1-6, ADK enterprise ops lab.

## 2. Prompting And Structured Output

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you control output reliably? | Use schema, validation, retry, repair, refusal, and prompt versioning. | Trusting "return JSON" without validation. |

**Talk track:** Prompting is not just wording. For production, I treat prompt outputs as untrusted data. I validate them with schemas and route invalid outputs through repair or refusal paths.

**Production failure:** Downstream code crashes because a field is missing. First inspect raw model output, validation errors, schema version, and retry behavior.

**Repo evidence:** Project 1 structured output assistant.

## 3. LLM Internals And Inference Basics

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Do you understand model behavior enough to reason about limits? | Explain tokens, context, attention, KV cache, prefill vs decode, batching. | Overexplaining transformer math while missing serving implications. |

**Talk track:** For application design, the key internals are tokenization, context limits, attention behavior, and inference phases. Long prompts affect prefill and KV cache. Long outputs affect decode, latency, and concurrency.

**Production failure:** Latency rises sharply after adding long retrieved context. First inspect prompt token count, output token count, time to first token, inter-token latency, and context packing.

**Repo evidence:** Module 2, Pro Module P1.

## 4. Embeddings

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Do you understand semantic search as approximation? | Embeddings produce candidate similarity, not truth. | Saying "closest vector equals correct answer." |

**Talk track:** Embeddings map text or other objects into vector space so related items are near each other. They are useful for candidate retrieval, clustering, and memory, but they do not prove correctness, freshness, permissions, or exact numeric constraints.

**Production failure:** Search returns semantically related but wrong policy. First inspect query, top-k chunks, metadata filters, source version, and hard negatives.

**Repo evidence:** Module 4, Project 2.

## 5. Vector Search And Vector Datastores

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you choose retrieval infrastructure? | Compare exact vs ANN, HNSW, metadata filters, pgvector, Qdrant, Chroma, managed options. | Picking a vector DB by popularity. |

**Talk track:** Vector stores solve similarity retrieval plus indexing, filtering, storage, and operational concerns. Exact search is simple but expensive at scale. ANN improves latency but trades recall. Metadata filters and tenancy boundaries are often as important as vector distance.

**Production failure:** Relevant docs disappear after adding filters. First inspect filter predicates, tenant/permission metadata, candidate counts before and after filtering, and recall@k.

**Repo evidence:** Module 5, Project 2.

## 6. RAG Foundations

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you build grounded assistants? | Cover ingestion, parsing, chunking, metadata, retrieval, context packing, citations, refusal. | Reducing RAG to "vector DB plus prompt." |

**Talk track:** RAG works when the system retrieves the right evidence, packs it clearly, instructs the model to answer only from evidence, cites sources, and refuses when support is insufficient.

**Production failure:** Answer has citation but citation does not support claim. First inspect citation span, retrieved chunk text, answer sentence alignment, and faithfulness metric.

**Repo evidence:** Module 6, Project 3.

## 7. Advanced Retrieval

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you improve retrieval with engineering methods? | Discuss query rewriting, multi-query, hybrid search, reranking, parent-child retrieval, GraphRAG. | Only increasing top-k or switching models. |

**Talk track:** Advanced retrieval improves candidate quality before generation. Query rewriting helps lexical mismatch. Hybrid search combines dense and sparse signals. Reranking improves top result quality. Parent-child retrieval balances small matching chunks with larger readable context.

**Production failure:** Correct document is in top 10 but not used. First inspect rank position, context packing, reranking scores, and whether the right chunk was dropped.

**Repo evidence:** Module 7, Project 4, Project 9.

## 8. Evaluation And Observability

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you measure GenAI systems? | Separate retrieval metrics, generation metrics, task success, latency, cost, safety. | Reporting only user thumbs-up or demo examples. |

**Talk track:** I measure retrieval and generation separately. Retrieval uses recall@k, MRR, NDCG, hit rate. Generation uses groundedness, faithfulness, citation accuracy, task success, refusal correctness. Traces connect failures to system layers.

**Production failure:** Overall pass rate drops. First slice by query type, source, tenant, model version, prompt version, retrieval config, and guardrail decision.

**Repo evidence:** Module 8, Projects 3, 4, 9, ADK evals.

## 9. Safety, Guardrails, And Reliability

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you design safe GenAI behavior? | Layered controls: input checks, retrieval permissions, tool allowlists, output checks, approvals, audit logs. | Believing a system prompt prevents all attacks. |

**Talk track:** Prompt injection and unsafe actions need defense in depth. I constrain what data can be retrieved, what tools can be called, what arguments are allowed, and which actions require approval. I log decisions for audit.

**Production failure:** Assistant leaks restricted information. First inspect auth context, retrieval filters, source permissions, trace logs, and whether the answer included unauthorized chunks.

**Repo evidence:** Module 9, Project 4, Project 8, ADK guardrails.

## 10. Agents And Tool Use

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Do you know when agents are justified? | Distinguish assistant, chain, workflow, and agent. Prefer deterministic workflow when possible. | Calling every multi-step system an agent. |

**Talk track:** Agents are useful when the system must choose actions under uncertainty. If the steps are known, a deterministic workflow is safer, cheaper, and easier to test. Tool use needs schemas, idempotency, timeouts, retries, and permission checks.

**Production failure:** Agent loops or repeats tool calls. First inspect trajectory trace, stop conditions, tool errors, state updates, and max-step policy.

**Repo evidence:** Module 10, Project 5, ADK lab.

## 11. LangGraph And Explicit Orchestration

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you control long-running flows? | Use state, nodes, edges, conditional routing, checkpoints, interrupts, recovery. | Hiding control flow inside one giant prompt. |

**Talk track:** LangGraph is useful when I need explicit state transitions, human approval, retries, recovery, and traceable workflows. The graph makes the system debuggable and testable.

**Production failure:** Workflow resumes incorrectly after approval. First inspect persisted state, checkpoint ID, pending action list, approval decision, and replay trace.

**Repo evidence:** Module 12, Project 5.

## 12. MCP

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Do you understand tool interoperability? | Explain clients, servers, tools, resources, prompts, auth, policy, audit. | Describing MCP as just another function-call wrapper. |

**Talk track:** MCP standardizes how assistants and agents access tools and context. Tools perform actions, resources expose read-only context, and prompts can standardize reusable instructions. Enterprise use requires auth, least privilege, audit, and approval boundaries.

**Production failure:** MCP tool outage blocks workflow. First inspect server health, transport errors, timeout policy, fallback path, and whether the workflow can degrade safely.

**Repo evidence:** Module 13, Project 6, ADK MCP docs.

## 13. Memory, HITL, And Long-Lived Systems

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you design beyond single-turn chat? | Discuss session state, durable state, semantic memory, approvals, resumability, forgetting. | Treating memory as unlimited chat history. |

**Talk track:** Long-lived systems need explicit state and memory policy. Session state handles the current task. Durable memory stores reusable facts or outcomes. Human review is needed for irreversible, risky, or ambiguous actions.

**Production failure:** Assistant acts on stale memory. First inspect memory source, timestamp, confidence, ownership, retention policy, and whether fresh retrieval should override memory.

**Repo evidence:** Module 16, Project 8, ADK memory.

## 14. Multimodal, Voice, And Realtime

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you reason about non-text systems? | Discuss OCR vs VLM, visual grounding, STT/TTS, streaming, turn-taking, latency. | Treating multimodal as text prompt plus image. |

**Talk track:** Multimodal systems need grounding at the right unit: page, block, region, frame, timestamp, or transcript segment. Voice systems add turn-taking, interruption, streaming, and low-latency tool decisions.

**Production failure:** Voice assistant feels slow. First inspect STT latency, model time to first token, tool-call latency, TTS start time, and turn-taking policy.

**Repo evidence:** Module 17, App video-agent skeleton.

## 15. Cost And Latency Engineering

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you make systems affordable and fast enough? | Budget by layer: retrieval, reranking, tools, prompt tokens, output tokens, retries, cache. | Optimizing only model price. |

**Talk track:** Cost per successful task matters more than cost per call. I decompose latency and cost by layer, then choose smaller models, caching, routing, compression, streaming, or deterministic logic where appropriate.

**Production failure:** Cost doubles after launch. First inspect token growth, retry rate, top-k, reranker calls, output length, model routing, cache hit rate, and failed task rate.

**Repo evidence:** Module 20, Project 6, Pro Module P4.

## 16. Caching And Model Gateway

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you reduce cost safely? | Explain exact cache, semantic cache, prompt cache, routing, fallback, rate limits, quotas. | Caching all LLM outputs without correctness policy. |

**Talk track:** A model gateway centralizes model access, routing, fallback, quota, logging, and cost control. Caching reduces latency and cost, but every cache needs correctness, staleness, tenant isolation, and invalidation rules.

**Production failure:** User receives stale cached answer. First inspect cache key, semantic threshold, source freshness, tenant scope, TTL, and invalidation path.

**Repo evidence:** Pro Module P4.

## 17. LLMOps And Deployment Lifecycle

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you ship GenAI changes safely? | Version prompts, models, datasets, evals, configs. Use gates, canaries, rollback. | Editing prompts directly in production. |

**Talk track:** Prompt and model changes should move through the same release discipline as code: versioning, offline evals, staging, canary or shadow traffic, monitoring, and rollback triggers.

**Production failure:** New prompt hurts answer quality. First compare prompt version, eval diff, failure slices, online traces, and canary metrics. Roll back if thresholds are breached.

**Repo evidence:** Pro Module P2, ADK CI eval gate doc.

## 18. Security And Responsible AI

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you survive enterprise review? | OWASP LLM risks, tenant isolation, secret handling, data retention, audit, red-team evals. | Saying "we will moderate input" and stopping there. |

**Talk track:** Security for GenAI includes prompt injection, data exfiltration, insecure tool use, sensitive information disclosure, supply-chain risk, and output handling vulnerabilities. Controls must be enforceable outside the prompt.

**Production failure:** Retrieved malicious document instructs model to reveal secrets. First inspect retrieval source trust, content sanitization, instruction hierarchy, tool permissions, and output policy.

**Repo evidence:** Pro Module P3, Module 9.

## 19. Data Flywheel

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can the system improve after launch? | Capture traces, feedback, failures, labels, hard negatives, eval updates, privacy controls. | Logging everything without consent or privacy design. |

**Talk track:** The strongest GenAI systems turn production failures into regression fixtures. The flywheel captures safe signals, labels failures, grows eval coverage, and then justifies retrieval fixes, prompt changes, distillation, or fine-tuning.

**Production failure:** Quality degrades on new query types. First inspect drift, unlabeled failure clusters, eval coverage gaps, source changes, and whether captured failures were added to regression tests.

**Repo evidence:** Pro Module P5, Module 8, Project 9.

## 20. Debugging GenAI Systems

| Interviewer is testing | Strong answer signal | Common trap |
|---|---|---|
| Can you debug by layer? | Classify failures as retrieval, prompt, model, tool, orchestration, safety, eval, infra. | Randomly tweaking prompts. |

**Talk track:** I debug GenAI systems by isolating the failing layer. I reproduce the case, inspect trace data, compare expected vs actual evidence, check prompt and tool calls, then make one targeted intervention and measure before vs after.

**Production failure:** Pass rate drops after index migration. First inspect source-to-chunk mapping, embedding model version, index version, filter behavior, recall@k, and top failing query slices.

**Repo evidence:** Module 21, Project 9, Project 10.


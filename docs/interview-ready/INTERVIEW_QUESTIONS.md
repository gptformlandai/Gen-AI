# GenAI Interview Questions

Use this as a question bank. For each answer, aim for structure, tradeoffs, and failure handling. A strong answer usually sounds calm and layered, not encyclopedic.

## Conceptual Questions

### 1. What is the difference between a chatbot, a copilot, a workflow, and an agent?

**Strong answer outline:**

- A chatbot is conversational and may not act.
- A copilot assists a user inside a task or product workflow.
- A workflow follows explicit steps and is usually deterministic.
- An agent chooses tools or next actions under uncertainty.
- In production, I prefer the simplest control structure that solves the problem.

**Trap:** Calling everything an agent.

### 2. What is RAG, and why does it exist?

**Strong answer outline:**

- RAG retrieves external evidence and uses it to ground generation.
- It solves private knowledge, freshness, permissions, and citation needs.
- It does not guarantee correctness by itself.
- Good RAG needs ingestion, chunking, metadata, retrieval, reranking, context packing, citations, refusal, and evals.

**Trap:** Saying RAG is just a vector database.

### 3. How do embeddings work in retrieval systems?

**Strong answer outline:**

- Embeddings convert text or objects into vectors.
- Similar meaning tends to produce nearby vectors.
- They are useful for candidate retrieval, not final truth.
- They struggle with exact constraints, numbers, negation, freshness, and permissions.
- Evaluate with labeled queries and retrieval metrics.

**Trap:** Treating vector similarity as correctness.

### 4. How would you choose an embedding model?

**Strong answer outline:**

- Start with task and corpus: language, domain, query style, document length, latency, cost.
- Build a small labeled retrieval set.
- Compare recall@k, MRR, NDCG, latency, cost, and dimension/storage impact.
- Check slice performance for domain jargon and hard negatives.
- Plan re-embedding and rollback.

**Trap:** Choosing by benchmark leaderboard alone.

### 5. What is the difference between dense, sparse, hybrid, and reranked retrieval?

**Strong answer outline:**

- Dense retrieval uses embeddings for semantic similarity.
- Sparse retrieval uses lexical term matching, often BM25-style.
- Hybrid combines semantic and lexical strengths.
- Reranking reorders candidates with richer features or a stronger model.
- Use hybrid and reranking when exact terms, domain jargon, or top-rank quality matter.

**Trap:** Assuming dense retrieval replaces lexical search.

### 6. What makes chunking hard?

**Strong answer outline:**

- Chunks must be small enough to match but large enough to answer.
- Structure matters: headings, sections, tables, permissions, timestamps.
- Bad chunks cause missed retrieval or unsupported answers.
- Parent-child retrieval can match small chunks and return larger context.
- Evaluate chunking with retrieval metrics and failure review.

**Trap:** Using one fixed chunk size everywhere.

### 7. How do you evaluate a RAG system?

**Strong answer outline:**

- Evaluate retrieval and generation separately.
- Retrieval: recall@k, hit rate, MRR, NDCG.
- Generation: faithfulness, groundedness, citation accuracy, refusal correctness, task success.
- Add latency, cost, safety, and permission metrics.
- Use traces to map failures to layers.

**Trap:** Only evaluating final answer polish.

### 8. What is LLM-as-judge, and what are its risks?

**Strong answer outline:**

- An LLM judge scores outputs for correctness, faithfulness, style, or preference.
- Useful for scaling qualitative evaluation.
- Risks include judge bias, self-grading bias, prompt sensitivity, inconsistent criteria, and missing source evidence.
- Use rubrics, calibration sets, deterministic checks where possible, and human spot checks.

**Trap:** Treating judge scores as ground truth.

### 9. What is prompt injection?

**Strong answer outline:**

- Prompt injection is an attempt to override instructions or manipulate model behavior.
- Direct injection comes from user input.
- Indirect injection comes from retrieved docs, websites, emails, or tool outputs.
- Defense must include permissions, tool constraints, content isolation, output checks, and audit logs.

**Trap:** Saying "the system prompt says ignore bad instructions."

### 10. How do you decide whether to fine-tune, use RAG, or improve prompting?

**Strong answer outline:**

- Prompting first for instruction and formatting failures.
- Retrieval fixes knowledge, freshness, citations, and private data.
- Fine-tuning helps repeated behavior, style, extraction, classification, or domain adaptation when enough data exists.
- Do not fine-tune to memorize volatile knowledge.
- Make the decision from error analysis and ROI.

**Trap:** Fine-tuning before measuring the failure layer.

## System Design Questions

### 11. Design an internal policy assistant with citations and permission-aware retrieval.

**Strong answer outline:**

1. Clarify users, data sources, permissions, freshness, latency, and risk.
2. Ingest policies with source, owner, version, effective date, tenant, and permission metadata.
3. Chunk by section and clause; preserve hierarchy.
4. Use hybrid retrieval plus metadata filters.
5. Rerank top candidates and pack context with source IDs.
6. Generate answers with citations and refusal when evidence is insufficient.
7. Evaluate retrieval recall, citation faithfulness, refusal correctness, latency, and permission leakage.
8. Add tracing, audit logs, prompt/version tracking, and feedback loop.

**Tradeoffs to mention:** Recall vs latency, freshness vs re-indexing cost, citation strictness vs answer usefulness, semantic search vs permission filters.

### 12. Design a customer support RAG assistant for a SaaS product.

**Strong answer outline:**

- Sources: docs, runbooks, known issues, tickets, changelogs.
- Retrieval: hybrid search, product/version filters, freshness boost.
- Generation: grounded answer, steps, citations, escalation path.
- Safety: no account-specific actions without auth, no unsupported claims.
- Observability: query trace, retrieved chunks, answer, feedback, ticket deflection.
- Evals: common questions, incident-specific queries, stale-doc cases, ambiguous queries.

**Tradeoffs to mention:** Answer speed vs completeness, top-k vs cost, docs freshness vs ingestion load.

### 13. Design a long-running incident response agent.

**Strong answer outline:**

- Use explicit workflow state, not free-form chat memory.
- Nodes: triage, gather evidence, retrieve runbooks, call tools, plan remediation, approval gate, execute, report.
- Human approval for production-changing actions.
- Tool calls need schemas, timeouts, retries, idempotency, audit.
- Persist state for resumability.
- Evaluate trajectory correctness, safety gates, latency, and final report quality.

**Tradeoffs to mention:** Autonomy vs safety, speed vs approval latency, deterministic workflow vs agent flexibility.

### 14. Design a model gateway for multiple LLM providers.

**Strong answer outline:**

- Gateway gives one internal API for model access.
- Handles routing, fallback, retries, rate limits, quotas, logging, caching, auth, and cost attribution.
- Routing can depend on task type, latency, cost, quality, tenant, and availability.
- Add exact and semantic cache with safety rules.
- Track success rate, latency, cost, cache hit rate, fallback rate, and provider errors.

**Tradeoffs to mention:** Gateway complexity vs control, caching savings vs stale answers, fallback quality differences.

### 15. Design a prompt/model CI/CD pipeline.

**Strong answer outline:**

- Version prompts, model config, retrieval config, eval set, and datasets together.
- Run lint/schema checks, offline evals, safety tests, retrieval regressions, and cost/latency checks.
- Deploy with canary or shadow traffic.
- Monitor quality, latency, cost, safety, fallback, and refusal metrics.
- Roll back automatically on threshold breach.

**Tradeoffs to mention:** Eval coverage vs release speed, canary risk vs confidence, online metrics lag.

### 16. Design a multimodal document understanding assistant.

**Strong answer outline:**

- Ingest PDFs/images with OCR, layout extraction, tables, figures, and page coordinates.
- Store text chunks plus layout metadata and visual references.
- Retrieve by document, page, section, table, or region.
- Use VLM only where text/OCR is insufficient.
- Cite page and region, not just document.
- Evaluate table extraction, visual grounding, citation accuracy, and refusal.

**Tradeoffs to mention:** OCR pipeline vs VLM cost, page-level context vs block-level precision, latency vs visual reasoning quality.

### 17. Design a semantic cache for GenAI responses.

**Strong answer outline:**

- Exact cache for deterministic repeated prompts.
- Semantic cache for near-duplicate requests with embeddings and threshold.
- Cache key must include tenant, user role, model version, prompt version, retrieval/source versions, safety policy, and locale where relevant.
- Never cache unsafe, personalized, or permission-sensitive responses without strict scope.
- Measure hit rate, savings, stale rate, false-hit rate, and latency improvement.

**Tradeoffs to mention:** Savings vs correctness, semantic threshold vs false hits, invalidation complexity.

### 18. Design an evaluation dashboard for GenAI systems.

**Strong answer outline:**

- Offline: retrieval metrics, generation metrics, safety checks, cost/latency.
- Online: task success, user feedback, escalation, refusal rate, cache hit rate, fallback rate.
- Slice by query type, user role, tenant, source, model version, prompt version, language, and risk tier.
- Include trace drill-down from metric regression to request-level evidence.

**Tradeoffs to mention:** Metric completeness vs dashboard noise, user feedback bias, judge reliability.

## Debugging Questions

### 19. The assistant gives a wrong answer with a citation. What do you inspect first?

**Strong answer outline:**

- Inspect retrieved chunks and cited span.
- Check whether citation supports the answer sentence.
- Check if the correct source was retrieved but dropped.
- Check prompt instructions for evidence use.
- Classify as retrieval miss, context packing issue, synthesis hallucination, or citation mapping bug.

### 20. Retrieval quality dropped after re-indexing. What happened?

**Strong answer outline:**

- Compare old and new chunk IDs, chunking version, embedding model, index config, metadata filters, and source count.
- Run canary queries against both indexes.
- Inspect recall@k, MRR, and failing slices.
- Check deletes, backfills, malformed metadata, and dimension mismatch.

### 21. Cost doubled after adding an agent workflow. What do you inspect?

**Strong answer outline:**

- Token count by step.
- Tool-call count.
- Retry and loop rate.
- Model routing.
- Retrieved context size.
- Output length.
- Cache hit rate.
- Failed-task rate.

### 22. A tool-using agent performed an unsafe action. What controls were missing?

**Strong answer outline:**

- Tool allowlist and argument validation.
- Risk classification.
- Human approval gate.
- Idempotency and side-effect control.
- Auth and least privilege.
- Audit logs.
- Dry-run or confirmation path.

### 23. LLM-as-judge says quality is high, but users complain. What do you do?

**Strong answer outline:**

- Check judge rubric and calibration set.
- Compare judge score with human labels.
- Slice user complaints by task type.
- Add hard cases and negative examples.
- Use deterministic checks for facts, citations, schemas, and refusals.

### 24. The assistant leaks restricted content. Where is the likely bug?

**Strong answer outline:**

- Auth context not propagated.
- Metadata permissions missing or incorrect.
- Retrieval filters applied after ranking instead of before where required.
- Cached response not scoped by tenant/user role.
- Tool returned data outside least privilege.
- Output guardrail failed to detect leakage.

## Project Deep-Dive Questions

### 25. Walk me through your strongest GenAI project.

**Strong answer shape:**

- Problem: what user pain or operational risk existed?
- System: what layers did you build?
- Tradeoffs: what choices did you make and reject?
- Evaluation: how did you measure quality?
- Failures: what broke and how did you debug it?
- Production next step: what would you harden?

### 26. What was the hardest failure you diagnosed?

**Strong answer shape:**

- Symptom.
- Hypothesis.
- Trace or metric evidence.
- Root cause.
- Targeted fix.
- Before/after metric.
- Remaining risk.

### 27. Why did you use LangGraph instead of a simple agent loop?

**Strong answer shape:**

- The workflow needed visible state, retries, recovery, and approval.
- A graph makes transitions explicit and testable.
- Human approval and resumability are cleaner with durable state.
- Simple agent loops are flexible but harder to constrain and debug.

### 28. Why did you simulate some components instead of using real APIs?

**Strong answer shape:**

- The early projects isolate mechanism: retrieval, validation, routing, eval, safety.
- Determinism makes tests and debugging reliable.
- Production versions should replace simulated embeddings, local stores, and synthetic corpora with real services.
- I know the limitation and have a clear hardening path.

### 29. What would you improve next in this repo?

**Strong answer shape:**

- Add harder holdout eval sets.
- Add real LLM and real embedding integrations.
- Add CI eval gates.
- Add adversarial security tests.
- Add one deployed full-stack capstone.
- Add production observability with traces and dashboards.

## Rapid-Fire Traps

| Question | Strong short answer |
|---|---|
| Is RAG always better than fine-tuning? | No. RAG is better for fresh/private/source-grounded knowledge. Fine-tuning is better for repeated behavior or adaptation when data justifies it. |
| Can a system prompt stop prompt injection? | No. It helps, but production defense needs permissions, tool constraints, retrieval isolation, output checks, and audit. |
| Does high recall guarantee good answers? | No. The generator may ignore evidence, context packing may drop it, or citations may be wrong. |
| Should agents call tools freely? | No. Tools need schemas, allowlists, auth, rate limits, risk tiers, and approval gates. |
| Is a vector database enough for RAG? | No. You still need ingestion, chunking, metadata, retrieval tuning, context packing, citations, evals, and safety. |
| What is the first debugging step for a bad RAG answer? | Inspect retrieved evidence and trace the answer back to the supporting chunks. |


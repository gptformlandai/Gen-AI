# Interview Answer Frameworks

This file gives reusable structures for answering GenAI interviews. Use these to stay crisp when the question is broad, ambiguous, or stressful.

## 1. The 60-Second Concept Answer

Use this when asked "Explain X."

```text
Definition:
  X is ...

Why it exists:
  It solves ...

Where it fits:
  In the system, it sits between ...

Tradeoff:
  It improves ..., but costs ...

Failure mode:
  It breaks when ...

How I debug it:
  I first inspect ...
```

Example:

```text
Reranking reorders retrieved candidates using a stronger scoring signal after first-stage retrieval. It exists because vector similarity alone often returns semantically related distractors above the right evidence. It sits between retrieval and context packing. It improves top-rank quality but adds latency and cost. It breaks when the reranker is poorly calibrated or receives too many irrelevant candidates. I first inspect rank movement, score distribution, and whether expected evidence is promoted.
```

## 2. GenAI System Design Flow

Use this for broad prompts like "Design an internal document assistant."

```text
1. Clarify requirements
   users, data, freshness, permissions, latency, cost, risk

2. Decide if GenAI is justified
   deterministic logic vs search vs RAG vs agent/workflow

3. Data layer
   source inventory, ingestion, parsing, chunking, metadata, freshness

4. Retrieval layer
   dense/sparse/hybrid, filters, reranking, context packing

5. Generation layer
   prompt, schema, citations, refusals, model routing

6. Tool/orchestration layer
   workflow state, tool schemas, retries, approvals, idempotency

7. Safety layer
   permissions, prompt injection defense, output policy, audit

8. Evaluation layer
   retrieval metrics, generation metrics, safety, cost, latency

9. Observability and operations
   traces, logs, dashboards, alerts, CI eval gates, rollback

10. Tradeoffs and next steps
   cost vs quality, latency vs recall, autonomy vs safety
```

## 3. RAG Design Checklist

| Layer | Decisions to mention |
|---|---|
| Sources | What data, owners, formats, freshness, permissions. |
| Parsing | PDF/HTML/docs/tables, structure preservation, metadata extraction. |
| Chunking | Fixed, semantic, recursive, section-aware, parent-child. |
| Embeddings | Model choice, dimensions, multilingual/domain fit, migration plan. |
| Retrieval | Dense, sparse, hybrid, metadata filters, top-k. |
| Reranking | Cross-encoder, LLM reranker, heuristic, fusion, cost budget. |
| Context packing | Ordering, dedupe, quote spans, source IDs, conflict handling. |
| Generation | Evidence-only answer, citations, refusal, schema. |
| Evaluation | Recall@k, MRR, groundedness, citation accuracy, refusal correctness. |
| Safety | Permission-aware retrieval, injection defense, PII, audit. |

## 4. Debugging Framework

Use this whenever the interviewer gives a failure.

```text
1. Reproduce
   Capture exact query, user role, time, source versions, model/prompt versions.

2. Classify symptom
   Wrong answer, no answer, unsafe answer, slow answer, expensive answer, bad tool action.

3. Inspect trace by layer
   input -> routing -> retrieval -> context -> prompt -> model -> tools -> output -> guardrails

4. Compare expected vs actual
   expected evidence, expected action, expected refusal, expected latency/cost.

5. Isolate root cause
   retrieval, prompt, model, tool, orchestration, safety, eval, infra.

6. Apply one targeted fix
   rerank, filter, rewrite, prompt constraint, schema validation, retry policy, approval gate.

7. Measure before vs after
   metric, trace, eval case, regression test.
```

## 5. Production Incident Answer

Use this shape:

```text
Immediate mitigation:
  Reduce blast radius first.

Diagnosis:
  Inspect traces and metrics by layer.

Root cause:
  State the most likely failing layer and evidence.

Permanent fix:
  Add code/config/data change.

Regression guard:
  Add eval or test so it does not recur.
```

Example:

```text
If a RAG assistant leaks restricted content, I first disable or restrict the affected retrieval path, then inspect auth context, metadata filters, cache scope, cited chunks, and tool responses. The likely root cause is permission filtering or cache scoping, not the model itself. The permanent fix is permission-aware retrieval before ranking, cache keys that include tenant and role, and regression tests for cross-tenant leakage.
```

## 6. Tradeoff Language

Use tradeoff pairs instead of one-sided claims.

| Decision | Gain | Cost |
|---|---|---|
| Increase top-k | Higher recall | More tokens, latency, noise. |
| Add reranker | Better top-rank quality | More latency and cost. |
| Use larger model | Better reasoning and synthesis | Higher cost and latency. |
| Use smaller model | Lower cost and faster response | Lower quality on complex tasks. |
| Add semantic cache | Lower cost and latency | Staleness and false-hit risk. |
| Use agent loop | Flexibility | Harder to test and constrain. |
| Use deterministic graph | Control and debuggability | Less open-ended autonomy. |
| Fine-tune | Better repeated behavior | Data, maintenance, rollback, safety risk. |
| RAG | Fresh/private/cited knowledge | Retrieval and eval complexity. |

## 7. Clarifying Questions

Ask 3 to 5 before designing.

| Area | Question |
|---|---|
| User | Who uses this and what decisions will they make from the output? |
| Data | What sources, formats, freshness, and ownership do we have? |
| Risk | What happens if the system is wrong or unsafe? |
| Permissions | Are answers user-specific, tenant-specific, or role-specific? |
| Latency | Is this interactive, batch, realtime, or human-reviewed? |
| Scale | How many docs, users, requests, tenants, and updates? |
| Evaluation | What does success mean and do we have labels? |
| Cost | Is the constraint cost per request, cost per successful task, or infra budget? |

## 8. Metrics To Mention

| Layer | Metrics |
|---|---|
| Retrieval | Recall@k, hit rate, MRR, NDCG, filter pass rate, freshness. |
| Generation | Faithfulness, groundedness, citation accuracy, schema validity, refusal correctness. |
| Tools | Tool success rate, timeout rate, retry rate, unsafe-action block rate. |
| Agents | Trajectory success, loop rate, handoff count, approval correctness. |
| Safety | Prompt-injection pass rate, leakage rate, policy violation rate, PII exposure. |
| Cost | Cost/request, cost/session, cost/successful task, token count by layer. |
| Latency | p50/p95 total latency, TTFT, retrieval latency, rerank latency, tool latency. |
| Reliability | Error rate, fallback rate, cache hit rate, stale-cache rate, rollback count. |

## 9. Approximate Numbers Worth Remembering

These are not universal constants. Use them as reasoning anchors and always say they depend on workload and provider.

| Topic | Useful range |
|---|---|
| Interactive chat latency | Users usually feel friction after a few seconds without streaming. |
| Voice turn-taking | Sub-second partial response feels much more natural than multi-second silence. |
| RAG top-k | Common first-stage retrieval may fetch 10-100 candidates, then rerank and pack fewer. |
| Final context chunks | Often 3-10 high-quality chunks beat stuffing dozens of noisy chunks. |
| Eval set starter size | 20-50 cases can reveal obvious failures; 100+ is better for serious regression. |
| Canary rollout | Start with a small traffic slice, monitor quality/safety/cost, then expand. |
| Cache TTL | Depends on source freshness; policy or price data needs stricter invalidation. |
| Retry count | Keep low for interactive paths; retries can multiply cost and latency quickly. |

## 10. Strong Phrases

Use these when they are true:

- "I would separate retrieval quality from generation quality."
- "I would inspect the trace before changing the prompt."
- "I would treat retrieved documents and tool outputs as untrusted input."
- "I would make the approval boundary explicit in the workflow state."
- "I would measure cost per successful task, not just cost per request."
- "I would prefer deterministic control flow unless the task truly needs agentic choice."
- "I would version prompts, models, retrieval config, and eval sets together."
- "I would add the production failure back into the regression set."

## 11. Weak Phrases To Avoid

Avoid these because they sound hand-wavy:

- "The LLM will understand the context."
- "We can just use a vector database."
- "The prompt will tell it not to hallucinate."
- "We can fine-tune it later."
- "An agent can handle that."
- "We can use feedback to improve it" without saying what feedback, how labeled, and how evaluated.

## 12. Whiteboard Skeletons

### RAG Assistant

```text
Sources -> Ingestion -> Parsing -> Chunking + Metadata -> Embeddings
      -> Vector/Hybrid Index -> Retrieval -> Reranking -> Context Packing
      -> Grounded Generation -> Citations/Refusal -> Eval + Trace
```

### Tool-Using Workflow

```text
User Request -> Risk Classifier -> State Graph
      -> Tool Selection -> Tool Validation -> Approval Gate
      -> Execution -> Audit Log -> Final Report -> Evaluation
```

### Model Gateway

```text
Client -> Gateway Auth/Policy -> Cache -> Router
      -> Provider A/B/C -> Fallback -> Logging/Cost/Trace -> Response
```

### Data Flywheel

```text
Production Traces -> Privacy Filter -> Failure Triage -> Labels
      -> Eval Set Growth -> Experiment -> Deployment Gate -> Monitoring
```


# Production Scenarios And Incident Drills

Use this file to practice senior-style diagnosis. The goal is not to guess the fix immediately. The goal is to isolate the failing layer, inspect the right evidence, apply a targeted mitigation, and prevent recurrence.

## Scenario Format

For any incident, answer:

1. What changed?
2. What layer is likely failing?
3. What trace or metric do we inspect first?
4. What is the immediate mitigation?
5. What regression test prevents this from recurring?

## Scenario 1: RAG Answer Is Wrong But Has A Citation

| Field | Notes |
|---|---|
| Symptom | User receives a confident answer with a citation, but the cited text does not support the claim. |
| Likely causes | Wrong chunk retrieved, correct chunk dropped, answer synthesis hallucinated, citation mapper attached nearest source instead of true source. |
| First inspection | Open the request trace and compare answer sentences to cited source spans. |
| Immediate mitigation | Tighten grounded-answer prompt, require sentence-level citation support, lower confidence or refuse when support is weak. |
| Prevention | Add citation faithfulness eval cases and fail CI when unsupported citations pass. |

**Interview line:** I do not start by rewriting the whole prompt. I first verify whether the cited evidence actually supports the answer.

## Scenario 2: Correct Document Retrieved But Answer Still Wrong

| Field | Notes |
|---|---|
| Symptom | The expected document appears in top-k retrieval, but the final answer misses the key fact. |
| Likely causes | Relevant chunk ranked too low, context packing dropped it, prompt overemphasized earlier evidence, model ignored a table or clause. |
| First inspection | Compare top-k, reranked list, final packed context, and answer. |
| Immediate mitigation | Improve reranking, context ordering, quote extraction, or answer constraints. |
| Prevention | Add eval case that checks both retrieval presence and answer inclusion. |

**Interview line:** Retrieval success at top-k is not enough. I check whether the evidence actually reached the model in a usable position.

## Scenario 3: Permission Leak In Internal Assistant

| Field | Notes |
|---|---|
| Symptom | Employee receives answer based on admin-only or tenant-private content. |
| Likely causes | Missing metadata, auth context not propagated, filters applied too late, cache key missing role or tenant, tool returned unrestricted data. |
| First inspection | Inspect user identity, retrieval filters, source metadata, cache hit status, and cited chunks. |
| Immediate mitigation | Disable affected cache/retrieval path, enforce permission filter before ranking, block risky roles. |
| Prevention | Add permission-leak tests and cache-scope tests. |

**Interview line:** Permission-aware retrieval is architecture, not prompt wording.

## Scenario 4: Indirect Prompt Injection From Retrieved Document

| Field | Notes |
|---|---|
| Symptom | Assistant follows instructions inside a retrieved document, such as revealing secrets or ignoring policy. |
| Likely causes | Retrieved content not isolated as data, tool permissions too broad, output policy absent, source trust not modeled. |
| First inspection | Inspect retrieved document text, prompt structure, tool-call trace, and policy decision. |
| Immediate mitigation | Treat retrieved text as untrusted data, disable risky tools for affected flow, add output blocking for secret disclosure. |
| Prevention | Add adversarial docs to retrieval evals. |

**Interview line:** The model cannot reliably distinguish trusted developer instructions from malicious content unless the system architecture enforces that boundary.

## Scenario 5: Latency Regression After Adding Reranking

| Field | Notes |
|---|---|
| Symptom | p95 response latency jumps after advanced retrieval launch. |
| Likely causes | Reranking too many candidates, LLM reranker on critical path, slow vector query, no timeout, serial retrieval calls. |
| First inspection | Trace latency by retrieval, reranking, context packing, generation, and tools. |
| Immediate mitigation | Reduce candidate count, use cheaper reranker, parallelize retrieval, add timeout and fallback. |
| Prevention | Add latency budget tests and p95 dashboards by component. |

**Interview line:** I do not remove reranking blindly. I measure whether the quality gain justifies the p95 cost and tune the candidate path.

## Scenario 6: Cost Spike After Launch

| Field | Notes |
|---|---|
| Symptom | Daily LLM spend doubles without matching traffic growth. |
| Likely causes | Longer prompts, larger retrieved contexts, retry loop, model routing bug, lower cache hit rate, longer outputs, failed tasks repeating. |
| First inspection | Cost per request, cost per successful task, token count by layer, retry rate, model mix, cache hit rate. |
| Immediate mitigation | Cap output tokens, reduce context size, route low-risk calls to cheaper model, pause broken retry path. |
| Prevention | Add budget alerts and cost regression checks. |

**Interview line:** I look at cost per successful task, not just cost per model call.

## Scenario 7: Agent Loops And Repeats Tool Calls

| Field | Notes |
|---|---|
| Symptom | Agent repeatedly calls the same tool or cycles through similar actions. |
| Likely causes | Missing stop condition, state not updated, ambiguous tool result, planner cannot observe progress, no max-step policy. |
| First inspection | Agent trajectory, state diff after each tool call, tool result schema, max-step and retry config. |
| Immediate mitigation | Add max steps, loop detection, explicit state updates, and deterministic route checks. |
| Prevention | Add trajectory evals for loop and recovery cases. |

**Interview line:** This is usually a control-flow bug, not a reason to make the prompt longer.

## Scenario 8: Human Approval Workflow Resumes Incorrectly

| Field | Notes |
|---|---|
| Symptom | Workflow executes wrong action after approval or loses pending action state. |
| Likely causes | Bad checkpoint, action ID mismatch, stale state, non-idempotent tool call, approval applied to wrong incident. |
| First inspection | Persisted state, checkpoint ID, pending action list, approval event, tool idempotency key. |
| Immediate mitigation | Stop execution, require manual review, restore previous checkpoint, add action ID validation. |
| Prevention | Add resumability tests and approval-state regression cases. |

**Interview line:** Human approval must bind to a specific action, version, and state, not a vague conversation.

## Scenario 9: Stale Knowledge In RAG

| Field | Notes |
|---|---|
| Symptom | Assistant answers from outdated policy even though newer policy exists. |
| Likely causes | Ingestion lag, stale embeddings, missing effective dates, ranking favors old high-similarity text, cache not invalidated. |
| First inspection | Source version, ingestion timestamp, index version, chunk metadata, cache entry, freshness filter. |
| Immediate mitigation | Disable stale source, force re-index, add freshness boost or effective-date filtering. |
| Prevention | Add freshness SLO and stale-policy eval cases. |

**Interview line:** Freshness is a retrieval and data-pipeline concern, not just a model knowledge issue.

## Scenario 10: Vector Search Recall Drops After Migration

| Field | Notes |
|---|---|
| Symptom | Known queries no longer retrieve expected documents after moving vector DB or embedding model. |
| Likely causes | Different embedding model, dimension mismatch, metric mismatch, HNSW parameter change, metadata bug, chunking change. |
| First inspection | Compare old/new index versions on canary queries and inspect recall@k and MRR. |
| Immediate mitigation | Roll back index routing or use dual-read while investigating. |
| Prevention | Add index migration checklist and shadow evaluation. |

**Interview line:** Re-embedding and index migration need versioned datasets, canary queries, and rollback.

## Scenario 11: Cache Returns Wrong Answer

| Field | Notes |
|---|---|
| Symptom | User receives answer intended for another context or stale source version. |
| Likely causes | Cache key missing tenant, role, prompt version, model version, source version, or locale; semantic threshold too loose. |
| First inspection | Cache key, cache metadata, hit reason, semantic similarity score, source version, user scope. |
| Immediate mitigation | Disable semantic cache for affected route, tighten threshold, flush risky entries. |
| Prevention | Add cache-scope and stale-answer tests. |

**Interview line:** Semantic caching is useful only when correctness boundaries are explicit.

## Scenario 12: Model Provider Rate Limits Or Outage

| Field | Notes |
|---|---|
| Symptom | Requests fail or queue during provider degradation. |
| Likely causes | No gateway fallback, no rate-limit backoff, no queue backpressure, single provider dependency. |
| First inspection | Provider error rate, retry storm, queue depth, timeout count, fallback route. |
| Immediate mitigation | Enable fallback model, throttle low-priority traffic, return degraded response with user-visible status. |
| Prevention | Add model gateway routing, circuit breaker, and provider failover tests. |

**Interview line:** A GenAI service still needs normal distributed-systems resilience: timeouts, retries, circuit breakers, and graceful degradation.

## Scenario 13: Long Context Makes Quality Worse

| Field | Notes |
|---|---|
| Symptom | Adding more retrieved chunks reduces answer quality. |
| Likely causes | Context dilution, conflicting evidence, poor ordering, lost-in-the-middle behavior, irrelevant chunks. |
| First inspection | Packed context, rank order, relevance scores, conflict markers, prompt token count. |
| Immediate mitigation | Improve reranking, compress context, group by source, quote only relevant spans, reduce top-k. |
| Prevention | Add context-packing evals and answer-support checks. |

**Interview line:** More context is not always better. The question is whether the right evidence is visible and unambiguous.

## Scenario 14: LLM Judge Passes Bad Answers

| Field | Notes |
|---|---|
| Symptom | Automated eval reports high quality, but manual review finds hallucinations. |
| Likely causes | Weak rubric, same-model bias, judge prompt too permissive, no source-grounding requirement, missing negative examples. |
| First inspection | Judge prompt, sampled graded outputs, calibration cases, human disagreement rate. |
| Immediate mitigation | Tighten rubric, add human-reviewed calibration set, use deterministic checks for citations and exact facts. |
| Prevention | Track judge agreement and add known-bad examples. |

**Interview line:** LLM-as-judge is a tool, not an oracle.

## Scenario 15: Tool Output Poisoning

| Field | Notes |
|---|---|
| Symptom | A tool returns unexpected text that causes the model to take wrong action. |
| Likely causes | Tool output treated as instruction, schema too loose, no output validation, untrusted third-party API response. |
| First inspection | Raw tool output, schema validation, prompt placement, action decision trace. |
| Immediate mitigation | Validate and sanitize tool output, isolate it as data, restrict downstream tool calls. |
| Prevention | Add malformed tool-output tests. |

**Interview line:** Tool outputs are also untrusted inputs.

## Scenario 16: Memory Drift

| Field | Notes |
|---|---|
| Symptom | Assistant uses old or incorrect user/project memory. |
| Likely causes | Memory has no TTL, confidence, owner, source, or forgetting policy; summary memory lost important nuance. |
| First inspection | Memory record, source event, timestamp, update path, retrieval score, conflict with fresh data. |
| Immediate mitigation | Disable stale memory, require fresh retrieval for critical facts, add memory confidence display. |
| Prevention | Add memory lifecycle and deletion tests. |

**Interview line:** Memory should be governed data, not hidden chat residue.

## Scenario 17: Voice Assistant Feels Slow

| Field | Notes |
|---|---|
| Symptom | User experiences awkward pauses in realtime voice interaction. |
| Likely causes | Slow STT, delayed model first token, blocking tool call, late TTS start, no streaming, poor turn-taking. |
| First inspection | Latency breakdown: capture, STT, model TTFT, tool, TTS, playback. |
| Immediate mitigation | Stream partials, avoid unnecessary tools, prefetch context, use faster model, shorten response. |
| Prevention | Add p50/p95 voice latency dashboard by stage. |

**Interview line:** Voice quality is about turn-taking and latency budget, not just final answer quality.

## Scenario 18: Visual Document Assistant Misses Table Data

| Field | Notes |
|---|---|
| Symptom | Assistant answers correctly from prose but misses table values or layout-specific facts. |
| Likely causes | OCR flattened table, chunking lost row/column relation, retrieval indexed text without layout metadata. |
| First inspection | Parsed document representation, table extraction, page coordinates, retrieved block. |
| Immediate mitigation | Use table-aware parsing, store structured table rows, cite page/table/row. |
| Prevention | Add table-specific eval cases. |

**Interview line:** Document AI often fails at structure, not vocabulary.

## Scenario 19: Canary Prompt Release Regresses Quality

| Field | Notes |
|---|---|
| Symptom | New prompt version performs worse for a subset of users. |
| Likely causes | Changed instruction priority, worse context formatting, stricter refusal behavior, regression on edge cases. |
| First inspection | Prompt diff, canary eval slices, refusal rate, task success, user feedback, trace samples. |
| Immediate mitigation | Roll back canary, keep traces, compare failing cases to offline eval coverage. |
| Prevention | Add failing canary cases to regression suite. |

**Interview line:** Prompt changes need release discipline just like code changes.

## Scenario 20: Data Capture Creates Privacy Risk

| Field | Notes |
|---|---|
| Symptom | Traces or eval datasets contain PII, secrets, or customer-sensitive data. |
| Likely causes | Logging raw prompts/context, no redaction, no retention policy, no consent boundary, eval set copied from production. |
| First inspection | Trace fields, storage location, retention policy, redaction pipeline, access logs. |
| Immediate mitigation | Stop unsafe logging, rotate exposed secrets, redact/delete affected records, restrict access. |
| Prevention | Add privacy-safe logging contract and redacted eval generation. |

**Interview line:** Data flywheels only help if the captured data is safe to keep and reuse.

## Scenario 21: MCP Server Returns Unexpected Capability Schema

| Field | Notes |
|---|---|
| Symptom | Agent fails after MCP server changes a tool schema or resource payload. |
| Likely causes | No capability versioning, loose client validation, missing compatibility tests. |
| First inspection | MCP capability list, tool schema diff, client validation errors, failing request trace. |
| Immediate mitigation | Pin capability version or route to compatibility adapter. |
| Prevention | Add contract tests for MCP tools and resources. |

**Interview line:** MCP standardizes the boundary, but you still need contract versioning and validation.

## Scenario 22: Production Tool Runs Twice

| Field | Notes |
|---|---|
| Symptom | A mutating action such as ticket creation, rollback, or notification executes twice. |
| Likely causes | Retry without idempotency key, timeout ambiguity, workflow replay, duplicate approval event. |
| First inspection | Tool call trace, idempotency key, retry logs, external system records. |
| Immediate mitigation | Disable retries for unsafe action or add idempotency key and reconciliation. |
| Prevention | Add side-effect control tests. |

**Interview line:** Retrying LLM workflows is easy; retrying side effects safely is engineering.

## Scenario 23: Retrieval Works In English But Fails In Spanish

| Field | Notes |
|---|---|
| Symptom | Multilingual users receive weak answers or refusals. |
| Likely causes | Embedding model weak cross-lingual alignment, documents only in English, query rewrite not multilingual, eval lacks language slices. |
| First inspection | Query language, embedding model capability, top-k docs, translation path, language-specific metrics. |
| Immediate mitigation | Translate query, use multilingual embeddings, add language-specific evals. |
| Prevention | Track metrics by language and locale. |

**Interview line:** Average retrieval quality can hide language-specific failure.

## Scenario 24: Evaluation Passes But Production Fails On Ambiguous Queries

| Field | Notes |
|---|---|
| Symptom | Eval set looks good, but users ask vague or underspecified questions that produce wrong answers. |
| Likely causes | Golden set too clean, no ambiguity labels, missing clarification path, overly eager answering. |
| First inspection | Production failure samples, query ambiguity, clarification/refusal rate, eval coverage. |
| Immediate mitigation | Add clarification route for low-confidence or under-specified questions. |
| Prevention | Add ambiguous and incomplete-query fixtures. |

**Interview line:** Production users do not write evaluation queries.

## Scenario 25: Fine-Tuned Model Regresses On Safety

| Field | Notes |
|---|---|
| Symptom | Fine-tuned model improves task accuracy but becomes less safe or more overconfident. |
| Likely causes | Training data lacks refusal cases, overfits desired output style, safety eval not part of release gate. |
| First inspection | Safety eval, refusal correctness, confidence calibration, training data slices. |
| Immediate mitigation | Roll back model, add safety data, adjust deployment gate. |
| Prevention | Require quality, safety, cost, and latency gates before promotion. |

**Interview line:** Model adaptation needs rollback and safety evals, not just task accuracy.

## Scenario 26: Graph Workflow Has Too Many Specialist Agents

| Field | Notes |
|---|---|
| Symptom | Multi-agent system is slower, harder to debug, and no better than one workflow. |
| Likely causes | Agents added for roles instead of real decision boundaries, duplicated context, unclear ownership, no trajectory evals. |
| First inspection | Trajectory trace, handoff count, token use, error locations, task success by path. |
| Immediate mitigation | Collapse unnecessary agents into deterministic nodes or functions. |
| Prevention | Require a justification for every agent boundary. |

**Interview line:** Multi-agent design is not automatically more advanced. It is only justified when the coordination boundary adds value.


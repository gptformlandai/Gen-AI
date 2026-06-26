# Pro Module P4 - Caching And Model Gateway Architecture

> **Module time:** 22h
> **Why this module matters:** Caching and a gateway layer are frequently 30-60% cost reduction and a major reliability upgrade in real systems, yet most learners never build them. This is high-leverage, interview-relevant infrastructure.

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic P4.1** | **Caching strategies for GenAI (8h)** | |
| P4.1.a | Exact-match response caching and cache key design | Done |
| P4.1.b | Semantic caching with embeddings and similarity thresholds | Done |
| P4.1.c | Provider prompt caching and prefix reuse | Done |
| P4.1.d | Cache invalidation, staleness, and correctness risks | Done |
| **Topic P4.2** | **Model gateway and routing layer (8h)** | |
| P4.2.a | Why a gateway (LiteLLM-style) exists: one interface, many providers | Done |
| P4.2.b | Model routing, fallback tiers, and dynamic quality/cost tiers | Done |
| P4.2.c | Rate-limit handling, quotas, retries, and request hedging | Done |
| P4.2.d | Multi-provider and multi-region failover for resilience | Done |
| **Topic P4.3** | **Cost and reliability engineering (6h)** | |
| P4.3.a | FinOps for GenAI: cost per request, per session, per successful task | Done |
| P4.3.b | Budget enforcement, throttling, and graceful degradation | Done |
| P4.3.c | Observability for caches and gateways: hit rate, savings, fallbacks | Done |
| **Module checkpoint** | Caching and model gateway architecture synthesis | Done |

**Covered so far:**
- P4.1.a - Exact-match response caching and cache key design: response cache mental model, deterministic-cache eligibility, cache key dimensions, tenant and permission boundaries, prompt/model/policy/version hashing, normalization risks, cache value schema, TTLs, negative caching, safety exclusions, Python key builder, lab, active recall, and interview-ready answer.
- P4.1.b - Semantic caching with embeddings and similarity thresholds: semantic cache architecture, query embedding, vector lookup, similarity threshold tuning, false-hit vs miss tradeoff, context-aware matching, permission-aware namespaces, answer reuse risks, reranker/LLM judge verification, offline evaluation, lab, active recall, and interview-ready design.
- P4.1.c - Provider prompt caching and prefix reuse: difference between response cache and provider KV/prefix cache, stable-prefix prompt design, tool/schema ordering, volatile-content placement, prompt cache keys, cached-token metrics, long-context economics, failure modes, lab, active recall, and interview-ready explanation.
- P4.1.d - Cache invalidation, staleness, and correctness risks: correctness classes, stale answers, permission drift, source updates, model and prompt version changes, policy updates, event-driven invalidation, versioned namespaces, stale-if-error, bypass controls, cache incident handling, active recall, and interview-ready correctness answer.
- P4.2.a - Why a gateway exists: unified provider interface, centralized routing, auth, quotas, spend tracking, logging, retry/fallback policy, provider abstraction limits, governance, deployment topology, lab, active recall, and interview-ready gateway justification.
- P4.2.b - Model routing, fallback tiers, and dynamic quality/cost tiers: task classification, tiered model policy, confidence-based escalation, budget-aware routing, context-length routing, safety-aware routing, fallback rules, downgrade risks, routing table design, lab, active recall, and interview-ready routing answer.
- P4.2.c - Rate-limit handling, quotas, retries, and request hedging: provider limits, tenant quotas, token buckets, backoff, retry budgets, idempotency, circuit breakers, hedged requests, cancellation, overload shedding, active recall, and interview-ready reliability answer.
- P4.2.d - Multi-provider and multi-region failover for resilience: failure-domain mental model, active-active vs active-passive, regional routing, provider capability parity, data residency, consistency of prompts/tools/evals, failover drills, active recall, and interview-ready failover answer.
- P4.3.a - FinOps for GenAI: cost per request, per session, per successful task: unit economics, direct and indirect cost components, cache-adjusted cost, gateway-attributed spend, success-adjusted cost, cohort analysis, worksheet, active recall, and interview-ready FinOps answer.
- P4.3.b - Budget enforcement, throttling, and graceful degradation: hard vs soft budgets, admission control, tier downgrade, retrieval compression, output caps, async fallback, user messaging, product policy, active recall, and interview-ready budget answer.
- P4.3.c - Observability for caches and gateways: hit rate, savings, fallbacks: cache and gateway metrics, logs, traces, dashboards, SLOs, alerting, cache correctness sampling, fallback reason tracking, cost reports, active recall, and interview-ready observability answer.
- Module checkpoint - Caching and model gateway architecture synthesis: semantic cache design, correctness vs savings tradeoff, gateway routing and failover design, cost/reliability impact quantification, workload worksheet, active recall, and senior-level architecture defense.

---

## Topic P4.1: Caching Strategies for GenAI

> **Topic time:** 8h
> Focus: Reducing model calls, input-token processing, latency, and provider dependency while preserving correctness, safety, tenant boundaries, and product trust.

Caching in GenAI is not one thing.

There are at least three different caches:

```text
exact response cache:
  same request -> reuse same final answer

semantic cache:
  similar request -> maybe reuse a previous answer

provider prompt cache:
  same prompt prefix -> provider reuses internal prefill/KV work
```

They look related because all reduce cost or latency.

But their correctness rules are different.

The central idea:

> In GenAI, a cache is not only a performance optimization. It is a product decision about when an answer is allowed to be reused.

That sentence is the whole module in miniature.

---

## Subtopic P4.1.a: Exact-Match Response Caching and Cache Key Design

> **Subtopic time:** 2h
> Outcome: You should be able to design a response cache key that avoids cross-user leakage, stale policy behavior, model-version confusion, and nondeterministic-answer surprises.

### Add to Knowledge Base

Exact-match response caching stores a completed model response and returns it when a future request is exactly equivalent.

The simplest form:

```text
request hash -> model response
```

But that is too simple for production.

The real form:

```text
cache_key = hash(
  tenant_id,
  user_permission_scope,
  task_type,
  normalized_input,
  retrieved_context_ids_and_versions,
  model_alias,
  model_version,
  prompt_template_version,
  tool_schema_version,
  safety_policy_version,
  generation_parameters,
  locale,
  output_format
)
```

The intuition:

> A cache key is a promise that every variable affecting the correct answer has been represented.

If one important variable is missing, the cache can become a silent correctness bug.

---

### 1. What Exact-Match Caching Is

Exact-match caching means:

```text
same effective request
same effective context
same effective policy
same effective model behavior
reuse answer
```

Good candidates:

```text
FAQ answers
static documentation Q&A
classification on stable text
summaries of immutable documents
tool-free deterministic transformations
high-volume repeated product questions
```

Bad candidates:

```text
account-specific answers
fresh financial/medical/legal claims
answers using fast-changing data
high-temperature creative generation
private or sensitive outputs without strict namespace isolation
tool calls with side effects
```

Exact cache hits are highly reliable when the cache key is complete.

They are dangerous when the cache key pretends two different situations are the same.

---

### 2. The Cache Eligibility Question

Before designing the key, ask:

```text
Is this response reusable at all?
```

A response is cacheable only if:

1. The output is not user-secret or session-secret unless the cache is scoped to that user/session.
2. The answer does not depend on data that changes faster than the TTL.
3. The request does not trigger side effects.
4. The model settings make reuse acceptable.
5. The product can tolerate a repeated answer.
6. The answer is policy-compliant under the current policy version.

For example:

```text
"Summarize this public product manual section" -> usually cacheable
"Should I approve this loan?" -> usually not globally cacheable
"What is my current deductible?" -> only cacheable per user, with short TTL or event invalidation
"Send this email" -> do not cache the action result as authorization
```

---

### 3. Cache Key Dimensions

A production key should include the dimensions that affect answer correctness.

| Dimension | Why It Matters |
|---|---|
| `tenant_id` | prevents cross-tenant leakage |
| `user_id` or permission scope | prevents user A seeing user B's answer |
| `input_hash` | identifies the user's effective request |
| `prompt_version` | prompt changes can change answer semantics |
| `model_alias` and model version | different models can answer differently |
| `generation_params` | temperature, max tokens, reasoning settings, seed if available |
| `retrieval_snapshot` | same question with different evidence is not same request |
| `tool_schema_version` | available tools affect reasoning and output |
| `policy_version` | safety and citation rules affect valid output |
| `locale` and timezone | answer formatting and date interpretation |
| `output_schema_version` | output shape affects parseability |

The tricky one is retrieval.

For RAG, the user's text is not enough.

The answer depends on:

```text
which documents were retrieved
which chunks were selected
which chunk versions were used
which permissions were applied
which reranker ordering was used
```

So a RAG cache key often includes:

```text
retrieval_fingerprint = hash([
  (doc_id, chunk_id, content_version, acl_version, rank_position)
])
```

If the source changes, the retrieval fingerprint changes.

---

### 4. Normalization: Useful but Dangerous

Normalization improves hit rate.

Examples:

```text
trim whitespace
collapse repeated spaces
lowercase non-case-sensitive fields
canonicalize JSON
sort dictionary keys
remove request IDs from model prompt
move timestamps to metadata instead of prompt text
```

But normalization can break meaning.

These are not always the same:

```text
"polish this" vs "Polish this"
"US" vs "us"
"May 2026" vs "may 2026"
"resume" vs "resume"
```

The rule:

> Normalize syntax, not meaning, unless you have a test proving the meaning is unchanged for your task.

For exact cache keys, aggressive semantic normalization belongs in semantic caching, not exact caching.

---

### 5. Cache Value Schema

Do not store only the text answer.

Store a response envelope:

```json
{
  "answer": "The policy allows cancellation within 30 days.",
  "model": "premium-reasoning-v1",
  "model_version": "2026-06-01",
  "prompt_version": "rag_answer_v17",
  "policy_version": "safety_2026_05",
  "retrieval_fingerprint": "sha256:...",
  "citations": [
    {"doc_id": "refund_policy", "chunk_id": "c12", "version": "42"}
  ],
  "created_at": "2026-06-26T10:00:00Z",
  "expires_at": "2026-06-26T11:00:00Z",
  "cache_scope": "tenant:user",
  "quality_flags": {
    "grounded": true,
    "schema_valid": true
  }
}
```

This supports:

```text
audit
debugging
invalidation
staleness checks
replay
cost accounting
```

---

### 6. TTL Mental Model

TTL should follow the data, not the cache engineer's optimism.

| Data Type | Typical TTL Direction |
|---|---|
| Immutable public docs | long TTL or version-based invalidation |
| Product documentation | medium TTL plus source-version invalidation |
| Pricing, policy, availability | short TTL or event-driven invalidation |
| User account data | very short TTL, per-user scope, event invalidation |
| Safety refusals | short TTL, because policies and context can change |
| Tool failure results | very short TTL, if cached at all |

Interview-grade phrase:

> I would prefer versioned invalidation for content correctness and TTL as a backstop, not the primary guarantee.

---

### 7. Exact Cache Control Flow

```text
1. Receive request.
2. Authenticate user and derive tenant/permission scope.
3. Decide whether task is cache-eligible.
4. Normalize safe request fields.
5. Build cache key from all correctness dimensions.
6. Look up cache.
7. If hit, validate TTL, policy version, ACL version, and output schema.
8. Return cached response with cache metadata.
9. If miss, call retrieval/tools/model.
10. Validate output.
11. Store response if eligible.
12. Emit cache hit/miss, token savings, latency, and correctness sampling metadata.
```

Notice the important order:

```text
auth first
cache lookup second
```

You do not want an unauthenticated request probing cache keys.

---

### 8. Code Sample: Cache Key Builder

```python
import hashlib
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CacheRequest:
    tenant_id: str
    permission_scope_hash: str
    task_type: str
    normalized_user_input: str
    model_alias: str
    model_version: str
    prompt_version: str
    policy_version: str
    retrieval_fingerprint: str
    output_schema_version: str
    generation_params: dict[str, Any]


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def build_response_cache_key(req: CacheRequest) -> str:
    payload = {
        "tenant": req.tenant_id,
        "perm": req.permission_scope_hash,
        "task": req.task_type,
        "input": req.normalized_user_input,
        "model_alias": req.model_alias,
        "model_version": req.model_version,
        "prompt_version": req.prompt_version,
        "policy_version": req.policy_version,
        "retrieval": req.retrieval_fingerprint,
        "schema": req.output_schema_version,
        "params": req.generation_params,
    }
    digest = hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()
    return f"llm_response:v1:{digest}"
```

The point is not the exact code.

The point is that the cache key is explicit.

---

### 9. Mini Program: Exact Cache Savings Estimate

```python
def estimate_exact_cache_savings(requests: int, hit_rate: float, uncached_cost: float, cached_cost: float = 0.0):
    hits = requests * hit_rate
    misses = requests - hits
    baseline = requests * uncached_cost
    actual = misses * uncached_cost + hits * cached_cost
    savings = baseline - actual
    return {
        "baseline_cost": baseline,
        "actual_cost": actual,
        "savings": savings,
        "savings_pct": savings / baseline if baseline else 0,
    }


if __name__ == "__main__":
    result = estimate_exact_cache_savings(
        requests=1_000_000,
        hit_rate=0.35,
        uncached_cost=0.012,
        cached_cost=0.0002,
    )
    for key, value in result.items():
        print(key, round(value, 4))
```

If one million requests cost 1.2 cents each and 35% can be safely cached, even a simple cache can move real budget.

But the word "safely" is doing the serious work.

---

### 10. Practical Interview Question

> You are building a customer-support RAG assistant. How would you design exact-match response caching?

### Strong Answer

I would start by deciding which routes are cache-eligible. Public documentation answers and static policy explanations are good candidates. Account-specific answers, side-effecting actions, and volatile data are not globally cacheable.

The cache key would include tenant, permission scope, normalized user request, model and prompt versions, generation settings, safety policy version, output schema version, and a retrieval fingerprint based on doc IDs, chunk IDs, content versions, ACL versions, and rank order. I would authenticate before cache lookup and keep cache namespaces tenant-aware.

For invalidation, I would use source-version changes and prompt/model/policy version changes as primary invalidation, with TTL as a backstop. I would log hit rate, avoided tokens, latency savings, stale-hit rate, and sampled correctness failures. If the cache ever returns an answer whose citations or permissions are no longer valid, that is a correctness incident, not just a cache miss bug.

### Active Recall

1. Why is user input alone not enough for a RAG cache key?
2. Which version fields should be included in a response cache key?
3. Why should authentication happen before cache lookup?
4. What is the difference between TTL invalidation and versioned invalidation?
5. Which tasks should never be globally response-cached?

Final takeaway:

> Exact-match caching is simple only when the request's correctness boundary is simple. In production, the cache key is a security and correctness contract.

---

## Subtopic P4.1.b: Semantic Caching With Embeddings and Similarity Thresholds

> **Subtopic time:** 2h
> Outcome: You should be able to design a semantic cache, tune its threshold using eval data, and explain when its savings are not worth its correctness risk.

### Add to Knowledge Base

Semantic caching reuses an answer when a new request is semantically similar to a previous request.

Exact cache:

```text
"How do I reset my password?" == "How do I reset my password?"
```

Semantic cache:

```text
"How do I reset my password?"
similar to
"I forgot my password, how can I change it?"
```

The intuition:

> Semantic caching trades exact equality for meaning-based reuse.

That trade is powerful.

It is also risky.

Because "similar" is not the same as "answer-equivalent."

---

### 1. Semantic Cache Architecture

Basic flow:

```text
1. Receive request.
2. Decide if route is semantic-cache eligible.
3. Embed the user request, or a canonicalized query representation.
4. Search a vector index of cached requests.
5. Retrieve nearest cached entries.
6. Check similarity threshold.
7. Apply tenant, permission, policy, and context filters.
8. Optionally run a verifier.
9. Return cached answer or fall through to normal model call.
10. Store new request/answer if eligible.
```

The cache entry stores:

```text
query text
query embedding
answer
citations
tenant and permission scope
source versions
prompt/model/policy versions
created_at / expires_at
quality flags
```

Semantic cache is usually a two-stage system:

```text
vector search -> candidate answers
verification -> safe reuse decision
```

The verifier can be:

```text
strict metadata checks
retrieval fingerprint comparison
cross-encoder/reranker
small LLM equivalence judge
rule-based task constraints
```

---

### 2. Similarity Is Not Equivalence

These look similar:

```text
"Can I cancel my subscription?"
"Can my admin cancel my subscription?"
```

But the answer may differ.

These look similar:

```text
"What is the refund policy for monthly plans?"
"What is the refund policy for annual plans?"
```

But the key entity changed.

These look similar:

```text
"Summarize this complaint."
"Summarize this complaint and identify legal exposure."
```

But the risk tier changed.

Semantic caches fail when they confuse:

```text
topic similarity
with
answer equivalence
```

The correct question is:

```text
Would the same answer be acceptable for both requests?
```

Not:

```text
Are these requests close in embedding space?
```

---

### 3. Threshold Tuning

A higher threshold means:

```text
fewer hits
lower false-hit risk
less savings
```

A lower threshold means:

```text
more hits
higher false-hit risk
more savings
```

The threshold should be selected using labeled examples.

Create an eval set:

```text
query_a
query_b
same_answer_allowed: true/false
risk_level: low/medium/high
domain: billing/security/legal/support
```

Then measure:

```text
semantic_cache_precision = correct_cache_hits / all_cache_hits
semantic_cache_recall = correct_cache_hits / all_reusable_pairs
false_hit_rate = incorrect_cache_hits / all_cache_hits
savings_per_false_hit = dollars_saved / correctness_incidents
```

For high-risk domains, optimize precision.

For low-risk FAQ domains, you may accept lower precision if the answer includes conservative framing.

---

### 4. Semantic Cache Safety Gates

Before accepting a semantic hit, check:

```text
same tenant
compatible permission scope
same task type
same output schema
same safety policy version
same major prompt version
same model family or approved equivalent
fresh enough source data
no side effects
no personalized answer unless scoped to the same user/session
similarity above route-specific threshold
```

Then consider a second-stage equivalence check:

```text
Question A: How do I reset my password?
Question B: I forgot my password. How can I get back in?
Cached answer: Use the password reset link...

Verifier decision:
  equivalent: true
  risk: low
  reason: both ask for self-service password reset flow
```

The verifier costs money.

But it can still be cheaper than a full premium model call.

---

### 5. Where Semantic Cache Works Best

Strong fit:

```text
FAQ assistants
public support questions
developer documentation Q&A
policy explanations with stable sources
low-risk summarization templates
classification with stable labels
```

Weak fit:

```text
personalized account answers
financial/legal/medical decisions
questions involving current state
multi-turn conversations with hidden context
agentic workflows with tools
answers requiring exact citations from fresh retrieval
```

Semantic cache is most useful when many users ask the same intent in many different phrasings.

It is least useful when small wording differences change the answer.

---

### 6. Multi-Turn and Context Risk

This request:

```text
"What about the second option?"
```

cannot be semantically cached from the current turn alone.

It depends on conversation history.

A context-aware semantic cache might embed:

```text
conversation summary
latest user query
selected entities
task type
retrieved evidence
```

But that increases complexity.

For many systems, a safer rule is:

```text
Only semantic-cache standalone queries.
Bypass semantic cache for context-dependent follow-ups.
```

That rule sacrifices hit rate to protect correctness.

Good architecture often does that.

---

### 7. Code Sample: Semantic Cache Decision

```python
from dataclasses import dataclass


@dataclass
class Candidate:
    cache_key: str
    similarity: float
    tenant_id: str
    permission_scope_hash: str
    task_type: str
    policy_version: str
    source_fresh: bool
    answer: str


def can_use_semantic_hit(
    candidate: Candidate,
    tenant_id: str,
    permission_scope_hash: str,
    task_type: str,
    policy_version: str,
    threshold: float,
) -> bool:
    if candidate.similarity < threshold:
        return False
    if candidate.tenant_id != tenant_id:
        return False
    if candidate.permission_scope_hash != permission_scope_hash:
        return False
    if candidate.task_type != task_type:
        return False
    if candidate.policy_version != policy_version:
        return False
    if not candidate.source_fresh:
        return False
    return True
```

This function is intentionally boring.

Semantic cache correctness comes from boring gates.

---

### 8. Mini Program: Threshold Tradeoff

```python
examples = [
    {"similarity": 0.94, "same_answer": True},
    {"similarity": 0.91, "same_answer": True},
    {"similarity": 0.88, "same_answer": False},
    {"similarity": 0.86, "same_answer": True},
    {"similarity": 0.81, "same_answer": False},
]


def evaluate_threshold(threshold: float):
    hits = [e for e in examples if e["similarity"] >= threshold]
    if not hits:
        return {"threshold": threshold, "hit_rate": 0, "precision": None}
    correct = sum(1 for e in hits if e["same_answer"])
    return {
        "threshold": threshold,
        "hit_rate": len(hits) / len(examples),
        "precision": correct / len(hits),
    }


for threshold in [0.95, 0.9, 0.85, 0.8]:
    print(evaluate_threshold(threshold))
```

The lesson:

```text
Hit rate alone can make a semantic cache look amazing.
Precision tells you whether it is safe.
```

---

### 9. Practical Interview Question

> You want to add semantic caching to a documentation assistant. How do you avoid incorrect answers?

### Strong Answer

I would only enable semantic caching for low-risk, standalone documentation questions first. The cache would be tenant-aware and policy-versioned. Each cached entry would store the original query embedding, answer, citations, source versions, prompt/model versions, and permission scope.

At runtime I would embed the new query, retrieve nearest cached questions, apply a conservative similarity threshold, then run deterministic gates: same tenant, compatible permission scope, same task type, fresh source versions, same output schema, and current policy version. For ambiguous or high-value hits, I would add a verifier that decides whether the cached answer is answer-equivalent for the new request.

I would tune thresholds on a labeled eval set and report semantic-cache precision, false-hit rate, hit rate, latency savings, and cost savings. If false hits affect user trust or compliance, I would tighten the threshold or disable semantic caching for that route. The goal is not maximum hit rate. The goal is acceptable reuse.

### Active Recall

1. Why is semantic similarity not the same as answer equivalence?
2. What metric matters more than hit rate for high-risk semantic caching?
3. Which metadata gates should run before accepting a semantic hit?
4. Why are multi-turn follow-ups risky for semantic caches?
5. When would you use a verifier after vector lookup?

Final takeaway:

> Semantic caching saves money by betting that two requests can share one answer. The engineering job is to make that bet explicit, measured, and reversible.

---

## Subtopic P4.1.c: Provider Prompt Caching and Prefix Reuse

> **Subtopic time:** 2h
> Outcome: You should be able to explain provider-side prompt caching as prefix/KV reuse, design prompts for cache locality, and distinguish it from response caching.

### Add to Knowledge Base

Provider prompt caching is different from response caching.

Response caching:

```text
skip the model call
return a stored final answer
```

Prompt caching:

```text
still call the model
reuse provider-side work for repeated prompt prefixes
reduce prefill cost and time-to-first-token
```

The mental model:

> Response caching reuses answers. Prompt caching reuses the model's internal work for the shared prefix.

This matters because prompt caching can be safe even when response caching is not.

Example:

```text
large stable system prompt
large stable tool schema list
large stable policy instructions
large stable document prefix
small changing user query at the end
```

The final answer still changes per request.

But the repeated prefix can be reused.

---

### 1. Why Prefix Reuse Matters

LLM inference has a prefill phase.

During prefill, the model processes prompt tokens and builds internal attention state.

If many requests share the same long prefix, provider or serving-engine prompt caching can avoid recomputing that shared prefix.

This improves:

```text
time to first token
input-token cost when provider discounts cached tokens
GPU prefill throughput
long-context responsiveness
agent loop efficiency
```

Common repeated prefixes:

```text
system instructions
developer instructions
tool definitions
JSON schemas
safety policies
few-shot examples
large static context blocks
conversation history that is appended rather than rewritten
```

The best prefix cache optimization is often prompt layout, not infrastructure.

---

### 2. Prompt Layout for Cache Hits

Place stable content first:

```text
1. system instructions
2. durable policy
3. stable tool definitions
4. stable output schema
5. stable examples
6. retrieved/static context that repeats
7. volatile user input
8. volatile timestamps, request IDs, random values, current turn data
```

Avoid placing volatile content early:

```text
timestamp
request ID
user name
session-specific small field
random nonce
dynamic tool subset
dynamic schema ordering
```

One changed token early in the prefix can reduce reuse.

So this is bad:

```text
Request time: 2026-06-26T10:01:11Z
You are a support assistant...
Tools: ...
User asks: ...
```

This is better:

```text
You are a support assistant...
Tools: ...
Schema: ...
User asks: ...

metadata:
  request_time: 2026-06-26T10:01:11Z
```

The timestamp is still available to the application.

It does not poison the prefix.

---

### 3. Tool and Schema Stability

Tool definitions are often large.

They are also often stable.

That makes them good prompt-cache material.

But teams accidentally break caching by:

```text
reordering tools per request
changing schema key order
injecting dynamic descriptions
removing tools from the array on each turn
changing enum order
changing examples
```

Better:

```text
keep full tool list stable
keep schema canonicalized
use separate allowlist/tool_choice metadata to limit tools per request
version tool schemas intentionally
```

The gateway can help here by canonicalizing tool schemas and prompt templates before they reach providers.

---

### 4. Provider Details Change

Provider-side prompt caching rules vary.

Some providers expose:

```text
cached token counters
prompt cache keys
cache-control markers
minimum cacheable prefix lengths
provider-specific TTLs
discounted cached-token pricing
```

Some self-hosted engines expose:

```text
prefix caching
KV-cache reuse
engine-local cache behavior
request routing for cache locality
```

Before making a cost commitment, verify:

```text
which models support caching
minimum prefix length
cache granularity
TTL
discount
metrics
routing controls
data isolation guarantees
```

The stable principle:

> Prompt caching rewards stable, repeated prefixes and punishes unnecessary early-token churn.

---

### 5. Prompt Caching vs Semantic Caching

| Dimension | Provider Prompt Cache | Semantic Cache |
|---|---|---|
| Reuses | internal prefix computation | final answer |
| Match type | exact prefix | embedding similarity |
| Model call still happens | yes | usually no |
| Correctness risk | lower | higher |
| Main savings | prefill latency/input cost | full generation cost |
| Best for | long stable prompts | repeated intents |
| Dangerous when | prefix includes secrets or volatile data | similar questions need different answers |

Prompt caching is usually safer.

Semantic caching is usually more aggressive.

You often use both:

```text
semantic cache hit:
  skip model call

semantic cache miss:
  call model with stable prompt layout
  benefit from provider prompt caching
```

---

### 6. Prefix Reuse in Agent Loops

Agent systems often send repeated context:

```text
system prompt
tool definitions
policy
workspace context
conversation state
trace instructions
```

If the agent rewrites earlier messages every turn, prefix reuse suffers.

Better:

```text
append new messages
do not mutate old prefix
summarize only at controlled boundaries
keep tool arrays stable
move diagnostics to metadata
route related requests with stable cache keys if provider supports it
```

This connects directly to P1:

```text
less repeated prefill
lower TTFT
better GPU utilization
lower input-token cost
```

---

### 7. Code Sample: Canonical Tool Ordering

```python
def canonicalize_tools(tools: list[dict]) -> list[dict]:
    return sorted(tools, key=lambda tool: tool["name"])


def build_messages(system_prompt: str, tools: list[dict], user_input: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        "tools": canonicalize_tools(tools),
        "metadata": {
            "cache_strategy": "stable-prefix-v1"
        },
    }
```

This is not a full client.

It demonstrates the habit:

```text
stable ordering
stable prefix
volatile values moved away from prefix
```

---

### 8. Practical Interview Question

> Your agent sends a 15,000-token prompt every turn. Costs and TTFT are high. How would provider prompt caching help?

### Strong Answer

I would distinguish prompt caching from response caching. We are not trying to reuse the final answer. We are trying to reuse the provider or serving engine's computation for repeated prompt prefixes. That mostly helps prefill, so I would expect lower time to first token and lower input-token cost where the provider discounts cached tokens.

I would restructure the prompt so stable content comes first: system instructions, policy, tool definitions, output schemas, and durable examples. Volatile content like request IDs, timestamps, user input, and dynamic state should move later or into metadata. I would keep tool and schema ordering stable and avoid rewriting previous conversation turns unless compaction is intentionally triggered.

Then I would measure cached-token counts, TTFT, cost per request, and cache hit rate by route. If a provider supports a prompt cache key or routing hint, I would use it carefully to improve locality for related traffic while avoiding hot-key overload or cross-tenant leakage.

### Active Recall

1. Why is provider prompt caching safer than response caching?
2. Which part of inference does prompt caching mainly reduce?
3. Why do timestamps near the top of a prompt hurt cache hits?
4. How do tool schema changes affect prefix reuse?
5. What metrics prove prompt caching is working?

Final takeaway:

> Provider prompt caching is a prompt-architecture optimization: put stable tokens first, keep them stable, and measure cached-token reuse.

---

## Subtopic P4.1.d: Cache Invalidation, Staleness, and Correctness Risks

> **Subtopic time:** 2h
> Outcome: You should be able to explain why cache invalidation is harder for GenAI than normal web caching and design practical controls for stale, unsafe, or unauthorized answers.

### Add to Knowledge Base

Caching is only useful if the answer is still valid.

In GenAI, validity depends on more than source data.

It can depend on:

```text
source content
source permissions
retrieval index
prompt version
model version
tool schema
safety policy
output schema
tenant membership
user role
current date
business process state
```

The central mental model:

> A GenAI cache entry expires when any assumption behind the answer expires.

TTL handles time.

Versioning handles meaning.

Authorization handles access.

All three matter.

---

### 1. Correctness Classes

Not every answer needs the same cache strictness.

| Class | Example | Cache Strategy |
|---|---|---|
| Immutable factual | old public API docs version | versioned long TTL |
| Slowly changing | product docs | content-version invalidation plus TTL |
| Operational state | order status | short TTL or no response cache |
| Permissioned state | HR policy by employee region | tenant/user scope plus ACL version |
| High consequence | medical/legal/financial recommendation | avoid semantic cache, strict retrieval freshness |
| Side-effecting | refund, email, deployment | never cache authorization or action result as permission |

The mistake is treating all LLM answers like web pages.

They are not.

Some are closer to decisions.

---

### 2. Staleness Failure Modes

Stale content:

```text
policy changed but assistant returns old policy
```

Stale permission:

```text
user lost access but cached answer still reveals content
```

Stale safety policy:

```text
new safety rule deployed but old cached answer bypasses it
```

Stale model behavior:

```text
model upgrade fixes hallucination but cache continues serving old bad answer
```

Stale retrieval index:

```text
document deleted but cached citation still points to it
```

Stale output schema:

```text
downstream parser expects v3 but cache returns v2
```

Each stale class needs a different invalidation signal.

---

### 3. Invalidation Patterns

Versioned namespace:

```text
cache:v1:prompt17:policy9:modelA:...
```

When a major version changes, old keys naturally stop matching.

Event-driven invalidation:

```text
document_updated -> evict entries citing doc_id
acl_changed -> evict entries under affected permission scope
policy_changed -> bump policy namespace
model_changed -> bump model namespace
```

TTL backstop:

```text
even if events fail, entries age out
```

Stale-while-revalidate:

```text
serve cached answer for low-risk route
refresh in background
```

Stale-if-error:

```text
if provider is down, serve recently cached low-risk answer with stale label
```

Bypass:

```text
force fresh response for high-risk query, audit investigation, user escalation, or admin testing
```

---

### 4. Do Not Cache These Blindly

Avoid global response caching for:

```text
identity-specific answers
authorization decisions
compliance decisions
medical/legal/financial recommendations
moderation decisions under changing policy
tool outputs with side effects
answers containing secrets
answers from untrusted retrieved data without validation
```

Also be careful with negative caching:

```text
"No policy found"
"User has no access"
"No matching document"
```

Negative answers can become stale quickly after a document is added or permission changes.

---

### 5. Cache Incident Handling

A cache correctness incident should answer:

```text
Which cache key served the response?
Which user/tenant received it?
Which source versions were assumed?
Which prompt/model/policy versions were assumed?
Was the entry stale by TTL, version, ACL, or policy?
How many users received it?
Can we purge all related keys?
Can we replay impacted requests?
Which guardrail failed?
```

That means cache observability is part of cache correctness.

No trace, no confident incident response.

---

### 6. Practical Interview Question

> A cached assistant answer gave users an old refund policy after the policy changed. How would you prevent this?

### Strong Answer

I would treat it as a cache invalidation and versioning failure. Refund policy answers should include a retrieval fingerprint with document IDs and content versions, and the cache key should include prompt, model, and policy versions. When the refund policy document changes, the ingestion pipeline should emit an event that invalidates cache entries citing that document or bumps a source namespace.

TTL should be a backstop, not the main correctness mechanism. For policy content I would use moderate TTLs, event-driven invalidation, and citation freshness checks before serving a cached answer. I would also log cache key, source version, user, tenant, and response ID so an incident review can identify impacted users and purge related entries.

### Active Recall

1. What assumptions can invalidate a GenAI cache entry?
2. Why is TTL not enough for source correctness?
3. What is stale permission risk?
4. What is negative caching and why can it be dangerous?
5. What fields do you need to debug a cache incident?

Final takeaway:

> Cache invalidation in GenAI is not only about freshness. It is about preserving the assumptions that made an answer safe, authorized, and correct.

---

## Topic P4.2: Model Gateway and Routing Layer

> **Topic time:** 8h
> Focus: Designing a central control plane for model access, routing, fallbacks, quotas, provider resilience, spend tracking, and policy enforcement.

Without a gateway, every application team learns provider behavior the hard way.

They each implement:

```text
auth
retries
fallbacks
rate limits
spend tracking
logging
model aliases
provider-specific request mapping
guardrails
cache integration
```

That creates inconsistent behavior and expensive mistakes.

A model gateway centralizes these concerns.

The central idea:

> A model gateway turns model access from scattered SDK calls into governed infrastructure.

---

## Subtopic P4.2.a: Why a Gateway (LiteLLM-Style) Exists - One Interface, Many Providers

> **Subtopic time:** 2h
> Outcome: You should be able to justify a gateway as an operating layer, not merely a wrapper around APIs.

### Add to Knowledge Base

A model gateway sits between applications and model providers.

```text
applications
    |
    v
model gateway
    |
    +--> provider A
    +--> provider B
    +--> self-hosted model
    +--> regional deployment
```

It provides a common interface and central policy.

Common responsibilities:

```text
provider abstraction
model aliases
routing
fallbacks
load balancing
auth and virtual keys
quotas and budgets
rate-limit handling
retries and timeouts
caching
logging and tracing
cost attribution
guardrails
request/response normalization
```

The simplest explanation:

> A gateway is the API management layer for LLM usage.

---

### 1. Why Direct SDK Calls Break Down

Direct SDK calls are fine for prototypes.

They break down when:

```text
multiple apps call multiple providers
teams need consistent retry policy
finance needs spend by tenant/team/feature
security needs central key management
providers have different rate limits
providers have different error formats
models need fast rollback
traffic needs fallback across regions
cache should be shared across apps
```

Without a gateway, every service becomes its own mini platform.

That causes:

```text
duplicated code
inconsistent safety behavior
untracked cost
hard provider migration
fragile fallback behavior
slow incident response
```

---

### 2. What a Gateway Should Not Hide

A gateway should abstract mechanics.

It should not pretend all models are identical.

Models differ by:

```text
context window
tool calling behavior
structured output reliability
latency
cost
safety behavior
language support
reasoning depth
modality support
regional availability
data-retention terms
```

So the gateway should expose capabilities:

```text
model_alias: support-fast
capabilities:
  tool_calling: true
  json_schema: strong
  max_context_tokens: 128000
  pii_region: us
  cost_tier: low
  quality_tier: medium
```

Good gateway design:

```text
abstracts provider plumbing
preserves capability differences
```

Bad gateway design:

```text
pretends every model is a drop-in replacement
```

---

### 3. Gateway Policy Surface

The gateway is where you can enforce:

```text
which teams can use which model tiers
which routes can use expensive models
which tenants require regional isolation
which requests are cache-eligible
which fallbacks are allowed
which safety checks are mandatory
which users hit hard budget limits
which app owns each dollar of spend
```

This is why gateways matter in enterprise systems.

They are not just latency optimizers.

They are governance infrastructure.

---

### 4. Gateway Request Flow

```text
1. App sends model request to gateway.
2. Gateway authenticates app/user/team key.
3. Gateway checks budget, quota, route policy, and model access.
4. Gateway canonicalizes request.
5. Gateway checks exact/semantic cache if enabled.
6. Gateway selects model/deployment/provider/region.
7. Gateway applies timeout and retry policy.
8. Gateway sends request to provider.
9. Gateway normalizes response and usage.
10. Gateway applies response validation/guardrails if configured.
11. Gateway stores cache entry if eligible.
12. Gateway emits trace, cost, latency, hit/miss, fallback, and error metrics.
```

This flow makes the gateway a control plane and data plane.

---

### 5. Code Sample: Gateway Routing Table

```yaml
routes:
  support_fast:
    allowed_teams: ["support", "growth"]
    default_model: "small-fast"
    fallback_models: ["small-fast-region2", "medium-safe"]
    max_input_tokens: 24000
    max_output_tokens: 800
    cache:
      exact: true
      semantic: true
      semantic_threshold: 0.92
    budget:
      monthly_usd: 5000

  legal_review:
    allowed_teams: ["legal-ai"]
    default_model: "premium-reasoning"
    fallback_models: ["premium-reasoning-region2"]
    cache:
      exact: false
      semantic: false
      prompt_prefix: true
    approvals:
      required_for_external_send: true
```

Gateway config is product policy in executable form.

---

### 6. Practical Interview Question

> Why would you add a model gateway instead of letting services call model providers directly?

### Strong Answer

I would add a gateway once more than one service, team, provider, or model tier is involved. Direct SDK calls are faster to start, but they scatter critical policy: retries, timeouts, fallbacks, quotas, budgets, logging, provider credentials, cache behavior, and model access.

The gateway gives us one interface for applications and one place to enforce routing, cost controls, safety requirements, and observability. It can map logical model aliases to providers or self-hosted deployments, handle rate limits and retries consistently, and fail over across providers or regions. It also gives finance and platform teams spend attribution by tenant, team, route, and task.

I would avoid pretending all models are equivalent. The gateway should expose capability metadata and only use fallbacks that are compatible with the task's context length, tool-calling needs, safety requirements, region constraints, and quality bar.

### Active Recall

1. What problems appear when every app calls providers directly?
2. Which policies belong in a model gateway?
3. Why should a gateway not hide model capability differences?
4. How does a gateway help cost attribution?
5. When is a gateway overkill?

Final takeaway:

> A model gateway is the shared operating layer for LLM access: one interface, centralized policy, measured cost, and controlled resilience.

---

## Subtopic P4.2.b: Model Routing, Fallback Tiers, and Dynamic Quality/Cost Tiers

> **Subtopic time:** 2h
> Outcome: You should be able to route requests by task risk, required capability, budget, latency, context length, and confidence instead of hardcoding one model everywhere.

### Add to Knowledge Base

Model routing decides which model should handle a request.

The naive strategy:

```text
send everything to the best model
```

This is simple.

It is also often too expensive and too slow.

Another naive strategy:

```text
send everything to the cheapest model
```

This is cheap.

It can destroy quality and trust.

The production strategy:

```text
route by task, risk, capability, latency, budget, and confidence
```

The central mental model:

> Model routing is product triage: spend expensive intelligence only where it changes the outcome.

---

### 1. Routing Signals

Common routing signals:

```text
task type
risk tier
input length
required output schema
tool-calling requirement
modality
language
tenant SLA
user plan
latency budget
monthly budget remaining
retrieval confidence
answer confidence
safety classification
provider health
region/data residency
```

Example:

```text
simple FAQ -> small fast model
ambiguous policy question -> medium model plus retrieval
legal-risk answer -> premium reasoning model, no semantic cache
long document analysis -> long-context model
tool action -> model with strong tool-calling plus approval gate
```

---

### 2. Static Tiers

You can define tiers:

```text
tier_0_deterministic:
  rules, templates, SQL, search, cache

tier_1_fast:
  cheap low-latency model

tier_2_balanced:
  reliable general model

tier_3_premium:
  high-reasoning or high-context model

tier_4_human:
  escalation for high-risk or low-confidence cases
```

The best first routing question:

```text
Can deterministic logic or cache answer this?
```

Do not route to a model if you do not need a model.

---

### 3. Dynamic Escalation

Dynamic routing uses runtime signals.

Example:

```text
1. Try exact cache.
2. Try deterministic retrieval answer for known FAQ.
3. Use fast model.
4. If confidence low or citation missing, escalate to stronger model.
5. If risk high, require human approval.
```

Confidence can come from:

```text
retrieval score
reranker score
schema validation
groundedness check
self-check
tool result status
policy classifier
user feedback
```

Important:

```text
self-reported model confidence alone is weak
```

Use observable signals whenever possible.

---

### 4. Fallback Is Not Always Downgrade

Fallback can mean:

```text
same model in another region
same model through another provider
same quality tier different vendor
smaller model with degraded answer mode
larger model for context-window overflow
human escalation
async job instead of synchronous response
```

Bad fallback:

```text
premium legal answer fails
silently route to cheap model
return confident legal advice
```

Better fallback:

```text
premium legal answer fails
try same quality tier in backup region
if unavailable, return graceful message or escalate
```

Fallback policy must preserve:

```text
safety tier
quality tier
context capability
tool capability
data residency
structured output reliability
```

---

### 5. Routing Decision Table

| Request Type | First Choice | Fallback | Cache Policy |
|---|---|---|---|
| Public FAQ | exact/semantic cache, small model | medium model | semantic allowed |
| Account-specific support | medium model with permissioned retrieval | medium backup region | per-user exact only |
| Legal risk | premium model | premium backup or human | prompt cache only |
| Bulk summarization | batch/flex/self-hosted | cheaper async tier | exact by document version |
| Tool action | strong tool model plus approval | same capability model | no action authorization cache |
| Long context | long-context model | context compression plus premium model | prompt cache helpful |

---

### 6. Code Sample: Routing Function

```python
def choose_model(route):
    if route["cache_hit"]:
        return "cache"
    if route["risk"] == "high":
        return "premium-reasoning"
    if route["requires_tools"]:
        return "tool-strong-balanced"
    if route["input_tokens"] > 100_000:
        return "long-context"
    if route["budget_remaining_pct"] < 10:
        return "small-fast"
    if route["retrieval_confidence"] < 0.55:
        return "premium-reasoning"
    return "balanced"
```

Real gateways need more nuance.

But this captures the principle:

```text
route by constraints
not brand preference
```

---

### 7. Practical Interview Question

> How would you route model calls for a SaaS support assistant with free and enterprise users?

### Strong Answer

I would define logical tiers rather than hardcoding provider names. Free-tier public FAQ traffic would first use exact or semantic cache, then a small fast model. Enterprise account-specific traffic would use permission-aware retrieval and a balanced model, with per-tenant quotas and no cross-tenant cache. High-risk billing, contract, or legal questions would route to a premium reasoning model or human escalation.

Routing would consider task type, tenant plan, risk tier, input length, tool requirements, budget remaining, latency SLA, retrieval confidence, and provider health. Fallbacks would preserve required capabilities. If the premium model fails for a legal route, I would not silently downgrade to a cheap model unless the product changes the response mode to "unable to complete, escalating."

I would measure cost per successful task by route, fallback rate, cache savings, model escalation rate, quality metrics, and user satisfaction. The goal is to spend more only when it improves task success or risk posture.

### Active Recall

1. What routing signals matter besides cost?
2. Why is fallback not always a downgrade?
3. When should routing escalate to a stronger model?
4. How does user plan affect routing?
5. Why should model aliases be logical rather than provider-specific?

Final takeaway:

> Routing is where product priorities become runtime decisions: quality, cost, latency, risk, and resilience all meet at the gateway.

---

## Subtopic P4.2.c: Rate-Limit Handling, Quotas, Retries, and Request Hedging

> **Subtopic time:** 2h
> Outcome: You should be able to design overload behavior that protects providers, tenants, budgets, and users without creating retry storms or duplicate side effects.

### Add to Knowledge Base

LLM systems fail under load in distinctive ways:

```text
provider rate limits
tokens-per-minute limits
requests-per-minute limits
long-tail latency
context-window errors
gateway saturation
tool timeouts
retry storms
budget exhaustion
```

The gateway should control this centrally.

The central mental model:

> Rate limits and retries are not error handling. They are traffic shaping.

Without traffic shaping, a busy LLM system can punish itself:

```text
429 -> retry immediately -> more 429s -> more retries -> provider outage for your app
```

---

### 1. Rate Limits vs Quotas

Rate limit:

```text
how fast can you spend?
```

Quota:

```text
how much can you spend over a window?
```

Examples:

```text
rate limit: 500 requests per minute
token limit: 2 million tokens per minute
quota: $10,000 per month
quota: 1 million premium-model tokens per day
```

Production systems need both.

Rate limits protect availability.

Quotas protect budgets and fairness.

---

### 2. Token Buckets

A common implementation:

```text
bucket has capacity
tokens refill at a fixed rate
each request consumes request tokens and estimated model tokens
if insufficient tokens, delay, downgrade, or reject
```

For LLMs, you often need two buckets:

```text
requests per minute
tokens per minute
```

And multiple scopes:

```text
provider
deployment
model alias
tenant
team
user
route
```

The gateway is the natural place to enforce this.

---

### 3. Retry Policy

Retries are useful for transient failures:

```text
429 rate limit
500 provider error
connection reset
timeout before model accepted request
```

Retries are dangerous for:

```text
side-effecting tool calls
non-idempotent operations
very long requests
provider overload
policy refusals
invalid input
context window exceeded without compression/fallback
```

Good retry policy includes:

```text
bounded retry count
exponential backoff with jitter
retry budget per request and per tenant
idempotency keys
error-type-specific handling
global circuit breaker
deadline awareness
```

If the user's end-to-end timeout is 8 seconds, a retry at second 7 may be pointless.

Retries should respect the remaining deadline.

---

### 4. Request Hedging

Hedging sends a duplicate request when the first request is unusually slow.

Example:

```text
send to provider A
after 2 seconds with no first token, send to provider B
return first successful response
cancel the loser if possible
```

Hedging improves tail latency.

It increases cost.

It can double provider load if used carelessly.

Use hedging only for:

```text
high-priority requests
latency-sensitive routes
idempotent generation
providers with independent failure domains
requests where duplicate cost is acceptable
```

Do not hedge:

```text
tool calls with side effects
already overloaded provider pools
low-value background tasks
long expensive generations
```

Hedging should have a budget.

---

### 5. Circuit Breakers and Cooldowns

If a provider or region starts failing:

```text
open circuit
stop sending traffic temporarily
route to fallback
probe with small health checks
close circuit when healthy
```

Circuit breakers prevent repeated failed calls from wasting latency and money.

Track:

```text
error rate
timeout rate
429 rate
TTFT p95
provider status
fallback success
```

The gateway should cool down unhealthy deployments.

---

### 6. Code Sample: Retry Budget Skeleton

```python
import random
import time


def should_retry(error_type: str) -> bool:
    return error_type in {"rate_limit", "timeout", "server_error"}


def call_with_retries(call_provider, deadline_seconds: float, max_attempts: int = 3):
    started = time.monotonic()
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        remaining = deadline_seconds - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError("request deadline exceeded")

        try:
            return call_provider(timeout=remaining)
        except Exception as exc:
            error_type = getattr(exc, "error_type", "unknown")
            if not should_retry(error_type) or attempt == max_attempts:
                raise

            sleep = min(0.25 * (2 ** (attempt - 1)) + random.random() * 0.1, remaining)
            time.sleep(sleep)
```

The key detail:

```text
remaining deadline controls retries
```

Retries that ignore deadlines create bad user experiences.

---

### 7. Practical Interview Question

> Your model provider starts returning rate-limit errors during a traffic spike. What should the gateway do?

### Strong Answer

The gateway should avoid turning rate limits into a retry storm. It should enforce provider, model, tenant, and route-level request/token buckets. On 429s, it should apply bounded retries with exponential backoff and jitter only if the request still has deadline budget. It should also respect retry-after signals if available.

If a deployment exceeds an error threshold, the gateway should cool it down with a circuit breaker and route compatible traffic to another deployment, provider, or region. For lower-priority traffic, it can queue, downgrade model tier, reduce max output tokens, serve cache, or return a graceful degradation response.

I would track 429 rate, retry attempts, retry success rate, queue time, fallback rate, dropped requests, p95 latency, and cost amplification from retries. The goal is to protect user-facing priority traffic without making the provider failure worse.

### Active Recall

1. What is the difference between a rate limit and a quota?
2. Why can retries make a provider incident worse?
3. What is request hedging and when is it justified?
4. Why do LLM gateways need token-per-minute limits, not just request limits?
5. What does a circuit breaker protect?

Final takeaway:

> Gateway reliability is mostly disciplined traffic control: limit, queue, retry carefully, hedge rarely, and fail over only when capability and safety still hold.

---

## Subtopic P4.2.d: Multi-Provider and Multi-Region Failover for Resilience

> **Subtopic time:** 2h
> Outcome: You should be able to design failover that improves availability without breaking capability, safety, data residency, or answer quality.

### Add to Knowledge Base

Failover means routing traffic away from a failing dependency.

For GenAI, dependencies include:

```text
model provider
specific model
regional endpoint
gateway cluster
vector database
reranker
tool service
embedding provider
```

The central mental model:

> Failover is useful only if the backup can safely satisfy the same contract.

If the backup cannot meet the contract, failover becomes silent degradation.

---

### 1. Failure Domains

Design around failure domains:

```text
single model deployment
provider region
entire provider
gateway cluster
cloud region
network path
identity provider
cache backend
```

A real resilience plan avoids single-provider assumptions.

But multi-provider systems add complexity:

```text
different APIs
different tokenizer behavior
different context windows
different safety filters
different tool-calling formats
different output schema reliability
different latency and price
different data-processing terms
```

A gateway absorbs some of this, but not all of it.

---

### 2. Active-Active vs Active-Passive

Active-active:

```text
traffic regularly flows to multiple providers/regions
```

Pros:

```text
warm paths
known backup behavior
continuous health signal
less failover surprise
```

Cons:

```text
more cost
more consistency work
more evaluation surface
```

Active-passive:

```text
primary handles traffic, backup waits
```

Pros:

```text
simpler normal operation
lower steady-state cost
```

Cons:

```text
cold backup risk
untested failure path
capacity may not be ready
model behavior drift unnoticed
```

For critical systems, active-active or regular failover drills are usually better.

---

### 3. Capability-Compatible Failover

Before allowing fallback, verify:

```text
context window >= required context
tool calling supported
structured output supported
latency SLA plausible
data residency allowed
safety policy compatible
cost allowed
quality acceptable on evals
language/modality supported
```

Example:

```text
route: enterprise_contract_review
primary: premium-reasoning-us
allowed fallback: premium-reasoning-us-backup
not allowed fallback: small-chat-global
```

For some routes, graceful failure is better than unsafe fallback.

---

### 4. Data Residency and Compliance

Multi-region failover can break compliance.

Example:

```text
EU tenant data routed to US model endpoint during outage
```

That may be unacceptable even if the answer is good.

The gateway must encode:

```text
tenant region
allowed processing regions
provider data terms
logging region
cache region
trace region
```

Failover policy must respect:

```text
data residency
retention
privacy constraints
contractual provider allowlist
```

Resilience is not allowed to bypass governance.

---

### 5. Failover Drills

Do not wait for an outage to test failover.

Practice:

```text
disable primary provider in staging
simulate 429s
simulate slow TTFT
simulate malformed provider output
simulate regional outage
simulate cache backend outage
simulate fallback model schema drift
```

Measure:

```text
time to detect
time to fail over
fallback success rate
quality delta
cost delta
latency delta
manual intervention required
customer-visible errors
```

This is where P2 deployment discipline meets P4 runtime infrastructure.

---

### 6. Practical Interview Question

> How would you design multi-provider failover for a production RAG assistant?

### Strong Answer

I would define logical model aliases and allowed fallback sets per route. For each route, the fallback must preserve required capabilities: context length, tool calling, structured output, safety behavior, region, data terms, and quality threshold on evals. Public FAQ traffic can fall back to a cheaper compatible provider. Legal or regulated traffic may only fail over to a same-tier model in an approved region or else degrade gracefully.

The gateway would track provider health, 429s, timeout rates, TTFT, output validation failures, and fallback success. It would use circuit breakers and cooldowns to avoid repeatedly calling unhealthy deployments. I would keep backups warm through active-active traffic slices or scheduled drills.

I would also test failover with replay evals because a provider fallback is not only an availability change. It is a model behavior change. If the backup model cannot maintain answer quality or safety, the right behavior is controlled degradation rather than silent fallback.

### Active Recall

1. What makes a fallback capability-compatible?
2. Why can multi-region failover violate compliance?
3. What is the difference between active-active and active-passive failover?
4. Why should failover be tested with evals?
5. When is graceful failure better than fallback?

Final takeaway:

> Multi-provider resilience is not "try another model." It is contract-preserving failover across capability, safety, cost, region, and quality.

---

## Topic P4.3: Cost and Reliability Engineering

> **Topic time:** 6h
> Focus: Measuring whether caching and gateways actually improve the workload, using cost, latency, success, availability, and correctness metrics.

Caching and gateways are infrastructure investments.

They need proof.

The proof is not:

```text
we added Redis
we added fallbacks
we support three providers
```

The proof is:

```text
cost per successful task fell
p95 latency improved
availability improved
quality did not regress
cache correctness stayed within tolerance
operational visibility improved
```

The central idea:

> Caching and gateway architecture are successful only when they improve measured product economics and reliability without damaging correctness.

---

## Subtopic P4.3.a: FinOps for GenAI - Cost per Request, per Session, per Successful Task

> **Subtopic time:** 2h
> Outcome: You should be able to quantify GenAI cost using product-relevant units, not only provider token prices.

### Add to Knowledge Base

Cost per request is useful.

But it is not enough.

For product decisions, measure:

```text
cost per request
cost per session
cost per successful task
cost per retained customer
cost per dollar of revenue protected or created
```

The central mental model:

> Token cost is an ingredient. Unit economics decide whether the system is worth running.

---

### 1. Cost Components

Direct model costs:

```text
input tokens
cached input tokens
output tokens
reasoning tokens
embedding tokens
reranking calls
image/audio tokens if multimodal
```

Infrastructure costs:

```text
gateway compute
cache storage
vector database
observability traces
queues
self-hosted GPU time
network egress
```

Operational costs:

```text
human review
incident response
evaluation runs
red-team runs
engineering maintenance
provider support contracts
```

Hidden costs:

```text
retries
fallback duplicates
request hedging
long context bloat
tool output explosion
failed sessions
low-quality answers requiring repeat attempts
```

---

### 2. Cost per Successful Task

Request cost can fall while business cost rises.

Example:

```text
cheap model cost per request: $0.002
success rate: 40%
expected cost per successful task: $0.002 / 0.40 = $0.005

better model cost per request: $0.004
success rate: 90%
expected cost per successful task: $0.004 / 0.90 = $0.0044
```

The "expensive" model is cheaper per success.

This is why gateways should log outcome metrics, not only token metrics.

---

### 3. Cache-Adjusted Cost

Baseline:

```text
cost_without_cache = requests * average_uncached_cost
```

Actual:

```text
cost_with_cache =
  exact_hits * exact_hit_cost
  + semantic_hits * semantic_hit_cost
  + prompt_cache_hits * discounted_prefill_cost
  + misses * full_model_cost
  + verifier_cost
  + cache_infra_cost
```

Savings:

```text
savings = cost_without_cache - cost_with_cache
```

But include correctness:

```text
net_value = savings - cost_of_cache_errors - operating_cost
```

Semantic cache with a high false-hit rate can produce negative net value.

---

### 4. Gateway-Attributed Spend

Every request should carry:

```text
tenant_id
team_id
user_plan
route
feature
model_alias
actual_provider
actual_model
cache_status
fallback_reason
prompt_tokens
cached_tokens
output_tokens
estimated_cost
task_success
```

This lets you answer:

```text
Which route burns the most money?
Which tenant is causing spikes?
Which model tier has the best cost per success?
Which cache saves the most?
Which fallback path is expensive?
Which product feature is not economically viable?
```

Without attribution, GenAI spend feels mysterious.

With attribution, it becomes engineering.

---

### 5. Practical Interview Question

> How would you prove that caching plus a gateway reduced cost?

### Strong Answer

I would define a baseline period before the rollout and compare route-level metrics after rollout. I would measure cost per request, cost per session, and cost per successful task, not just aggregate token spend. The gateway would attribute spend by tenant, feature, route, model alias, actual provider, cache status, and fallback reason.

For caching, I would separate exact hit rate, semantic hit rate, provider cached-token rate, avoided input tokens, avoided output tokens, verifier cost, cache infrastructure cost, and sampled cache correctness failures. For the gateway, I would measure model tier distribution, fallback rate, retry amplification, hedging cost, and provider price differences.

The final report would show gross savings, net savings, latency impact, quality impact, and reliability impact. If cost fell but successful task rate also fell, I would not call it a win.

### Active Recall

1. Why is cost per request not enough?
2. How can a more expensive model be cheaper per successful task?
3. What costs does caching add?
4. Which request fields are needed for spend attribution?
5. What is retry amplification?

Final takeaway:

> GenAI FinOps is not token counting alone. It is route-level unit economics tied to task success.

---

## Subtopic P4.3.b: Budget Enforcement, Throttling, and Graceful Degradation

> **Subtopic time:** 2h
> Outcome: You should be able to design budget controls that protect the business while keeping the product useful under spend pressure or provider overload.

### Add to Knowledge Base

Budgets are product guardrails.

They answer:

```text
How much are we willing to spend?
For whom?
For which tasks?
At what quality level?
Before we slow down, downgrade, or stop?
```

The central mental model:

> Budget enforcement is admission control for money.

Without it, a bug, attack, or runaway agent can turn into a finance incident.

---

### 1. Budget Scopes

Budgets can apply to:

```text
organization
tenant
team
user
API key
route
feature
model tier
provider
environment
```

Examples:

```text
free users get $0.05/day
enterprise tenant gets $5,000/month
support assistant gets $300/day
premium reasoning model capped at 10% of traffic
staging environment capped tightly
```

Budgets should be close to product value.

Do not only set one global budget.

---

### 2. Soft vs Hard Limits

Soft limit:

```text
warn, alert, downgrade, require approval
```

Hard limit:

```text
block, throttle, or require manual override
```

Good budget behavior is staged:

```text
70% used -> notify owner
85% used -> downgrade non-critical routes
95% used -> disable premium routes or require approval
100% used -> hard stop except emergency allowlist
```

This avoids surprise outages.

---

### 3. Graceful Degradation Options

When budget or capacity is constrained:

```text
serve exact cache
serve semantic cache for low-risk routes
use provider prompt caching
reduce top-k retrieval
skip reranking for low-risk routes
compress retrieved context
reduce max output tokens
switch to cheaper model
ask clarifying question
queue for async processing
return extractive answer only
disable non-essential tools
route to human for high-risk cases
```

Graceful degradation should be route-aware.

Do not degrade a legal review the same way you degrade a casual FAQ.

---

### 4. User-Facing Behavior

Bad:

```text
silent quality drop
random failures
confident incomplete answer
```

Better:

```text
"I can answer from the available documentation, but advanced analysis is temporarily unavailable."
"This request is queued for deeper review."
"I can provide a shorter answer now or run a full analysis later."
```

For internal tools, transparent degradation is usually better than pretending nothing changed.

For consumer products, keep messaging simple but honest.

---

### 5. Code Sample: Budget Decision

```python
def budget_action(usage_pct: float, risk: str) -> str:
    if usage_pct < 0.70:
        return "normal"
    if usage_pct < 0.85:
        return "alert_only"
    if usage_pct < 0.95:
        if risk == "low":
            return "downgrade_model"
        return "normal_with_alert"
    if usage_pct < 1.00:
        if risk == "high":
            return "require_approval"
        return "cache_or_degrade"
    if risk == "high":
        return "human_escalation"
    return "block_or_async_queue"
```

The point:

```text
budget policy depends on risk
```

---

### 6. Practical Interview Question

> Your GenAI feature is about to exceed its monthly budget. What should happen automatically?

### Strong Answer

I would use staged budget enforcement. At 70% spend, notify the service owner. At 85%, start degrading low-risk routes: prefer cache, reduce max output tokens, route simple tasks to cheaper models, and defer batch work. At 95%, require approval for premium model routes and disable non-essential high-cost features. At 100%, hard-stop low-priority traffic while preserving emergency or contractual routes if explicitly allowed.

The policy should be route-aware. High-risk legal or financial routes should not silently downgrade to a weaker model. They should either use an approved fallback, queue, or escalate. Low-risk FAQ traffic can use semantic cache or cheaper models.

I would expose budget status in dashboards and logs so product and finance can see cost per request, per session, and per successful task. Budget enforcement should reduce spend without creating hidden quality regressions.

### Active Recall

1. What is the difference between soft and hard budget limits?
2. Why is silent model downgrade dangerous?
3. Name five graceful degradation options.
4. Which scopes should budgets apply to?
5. Why should high-risk routes degrade differently from low-risk routes?

Final takeaway:

> Budget enforcement is not just blocking requests. It is controlled product degradation under financial constraints.

---

## Subtopic P4.3.c: Observability for Caches and Gateways - Hit Rate, Savings, Fallbacks

> **Subtopic time:** 2h
> Outcome: You should be able to define the metrics, traces, logs, dashboards, and alerts that prove cache and gateway behavior is correct, economical, and reliable.

### Add to Knowledge Base

If you cannot observe the cache and gateway, you cannot trust them.

The central mental model:

> A model gateway without observability is just a hidden place for cost, latency, and quality bugs to accumulate.

You need visibility into:

```text
who called what
which model was selected
why it was selected
whether cache was used
whether fallback happened
what it cost
how long it took
whether the task succeeded
whether quality or safety regressed
```

---

### 1. Cache Metrics

Exact cache:

```text
hit rate
miss rate
hit rate by route
hit rate by tenant
TTL expiry rate
manual bypass rate
eviction count
stale-hit incidents
cache lookup latency
cache storage size
```

Semantic cache:

```text
semantic hit rate
average similarity score
threshold rejection rate
verifier pass/fail rate
false-hit rate from sampling
precision by route
cache correctness incident rate
```

Provider prompt cache:

```text
cached input tokens
cached-token ratio
TTFT for cached vs uncached
input-token cost savings
prefix churn rate
tool/schema version churn
```

Cost:

```text
gross avoided spend
net savings after infra/verifier cost
savings by route
savings by tenant
cost of cache errors
```

---

### 2. Gateway Metrics

Routing:

```text
requests by model alias
requests by actual provider/model
model tier distribution
routing reason
escalation rate
downgrade rate
```

Reliability:

```text
provider error rate
rate-limit error rate
timeout rate
retry count
retry success rate
fallback rate
fallback success rate
circuit breaker state
hedged request count
```

Latency:

```text
gateway overhead
queue time
provider latency
time to first token
inter-token latency
end-to-end latency
p50/p95/p99 by route
```

Cost:

```text
cost per request
cost per session
cost per successful task
spend by tenant/team/feature
retry amplification cost
fallback cost delta
hedging cost delta
```

Quality:

```text
task success rate
schema validation failure
groundedness failure
user correction rate
thumbs up/down
escalation to human
post-fallback quality delta
```

---

### 3. Trace Fields

Each model request trace should include:

```text
request_id
session_id
tenant_id
team_id
route
risk_tier
model_alias_requested
model_selected
provider_selected
region_selected
routing_reason
cache_status
cache_key_hash
semantic_similarity
prompt_cache_cached_tokens
fallback_reason
retry_count
input_tokens
output_tokens
estimated_cost
latency_breakdown
policy_version
prompt_version
retrieval_fingerprint
quality_flags
```

Sensitive content should be redacted or sampled according to policy.

Do not log secrets just to debug a cache.

---

### 4. Alerts

Useful alerts:

```text
semantic cache false-hit rate above threshold
exact cache stale-hit incident
provider 429 rate spike
fallback rate spike
fallback quality drop
cost per successful task spike
premium model usage spike
prompt cache hit rate collapse
gateway p95 latency spike
retry amplification spike
budget threshold crossed
cache backend unavailable
```

Bad alerts:

```text
total token count changed
```

without route context.

Good alerts tie symptoms to action.

---

### 5. Practical Interview Question

> What dashboard would you build for a model gateway with caching?

### Strong Answer

I would build a route-level dashboard. The top row would show request volume, p95 latency, error rate, fallback rate, cost per successful task, and task success rate. Then I would separate cache metrics: exact hit rate, semantic hit rate, semantic precision from sampling, provider cached-token ratio, avoided spend, and cache lookup latency.

For the gateway, I would show model alias to actual provider mapping, routing reasons, tier distribution, retry rate, 429 rate, circuit breaker state, fallback success, and provider health. I would also show budget usage by tenant/team/feature and cost spikes by route.

Every graph should be filterable by tenant, route, model alias, provider, region, and risk tier. The point is to answer operational questions quickly: why did cost rise, why did latency rise, why did fallbacks increase, and did quality change?

### Active Recall

1. What is the difference between semantic cache hit rate and semantic cache precision?
2. Which metrics prove provider prompt caching is working?
3. Why should gateway traces include routing reason?
4. What is retry amplification cost?
5. Which alerts indicate cache correctness risk?

Final takeaway:

> Cache and gateway observability must connect infrastructure behavior to product outcomes: cost, latency, reliability, quality, and correctness.

---

## Module P4 Checkpoint: Caching and Model Gateway Architecture Synthesis

> **Checkpoint focus:** Design a semantic cache, justify a model gateway, explain routing/failover behavior, and quantify the cost and reliability impact of caching plus gateway on a workload.

By the end of Pro Module P4, you should be able to:

1. Design a semantic cache and explain its correctness vs savings tradeoff.
2. Justify a model gateway and describe its routing and failover behavior.
3. Quantify the cost and reliability impact of caching plus gateway on a workload.

---

### 1. The Big Picture

Caching and gateways solve different but connected problems.

Caching asks:

```text
Can we avoid or reduce model work?
```

Gateway architecture asks:

```text
Can we control model access centrally and route traffic intelligently?
```

Together:

```text
cache first
route second
fallback third
observe always
```

The mature architecture:

```text
client/app
  -> model gateway
  -> auth/quota/budget policy
  -> exact cache
  -> semantic cache for eligible routes
  -> route to model/provider/region
  -> provider prompt cache benefits from stable prefix
  -> validate response
  -> store cache if eligible
  -> log trace/cost/quality/fallback
```

The core checkpoint sentence:

> Caching reduces unnecessary model work; the gateway decides which model work should happen, where it should happen, and under what budget, safety, and reliability constraints.

---

### 2. Semantic Cache Design

A strong semantic cache design includes:

```text
route eligibility
tenant-aware namespace
permission-aware filters
query embedding
vector index
similarity threshold
metadata gates
optional verifier
source freshness checks
prompt/model/policy version checks
TTL and event invalidation
observability and sampled correctness evals
kill switch
```

Example flow:

```text
1. User asks support question.
2. Gateway authenticates user and identifies tenant/permission scope.
3. Route policy allows semantic cache only for public support docs.
4. Query is embedded.
5. Vector cache retrieves nearest previous requests.
6. Candidate must pass threshold >= 0.92.
7. Candidate must match tenant, permission scope, task type, source version, prompt version, and policy version.
8. Optional verifier checks answer equivalence.
9. If accepted, cached answer is returned with trace metadata.
10. If rejected, normal retrieval/model pipeline runs.
```

Correctness vs savings:

```text
lower threshold -> more savings, more false-hit risk
higher threshold -> less savings, lower false-hit risk
verifier -> higher cost, better precision
route restriction -> lower hit rate, safer behavior
```

Senior-level answer:

```text
I would optimize semantic-cache precision, not hit rate, for any user-trust-sensitive route.
```

---

### 3. Gateway Justification

Use a gateway when:

```text
multiple apps call models
multiple providers or deployments exist
spend attribution matters
rate limits matter
fallbacks matter
security needs central key management
model changes need fast rollback
cache should be shared
governance needs route-level policy
```

Gateway responsibilities:

```text
auth
model access control
logical model aliases
routing
fallbacks
load balancing
rate limits
quotas
budgets
retries
timeouts
circuit breakers
caching
request/response normalization
observability
cost attribution
```

Strong phrasing:

> The gateway is not just a provider adapter. It is the policy and reliability layer for model access.

---

### 4. Routing and Failover Behavior

Routing should consider:

```text
task type
risk tier
required capabilities
context length
latency budget
tenant plan
budget remaining
retrieval confidence
provider health
region and data residency
```

Fallback should preserve:

```text
quality tier
safety tier
tool capability
schema capability
context window
region constraints
data policy
```

Bad fallback:

```text
premium legal route -> cheap chat model -> confident answer
```

Good fallback:

```text
premium legal route -> same-tier approved backup -> if unavailable, human escalation or graceful failure
```

---

### 5. Quantifying Impact

Start with workload assumptions:

```text
monthly requests: 2,000,000
average uncached model cost: $0.010
exact cache hit rate: 20%
semantic cache hit rate: 15%
semantic verifier cost: $0.001 per semantic candidate
provider prompt cache input savings on misses: 15%
gateway/cache infra cost: $1,500/month
```

Baseline:

```text
2,000,000 * $0.010 = $20,000/month
```

Exact hits:

```text
400,000 requests skip model
savings = 400,000 * $0.010 = $4,000
```

Semantic hits:

```text
300,000 requests skip model
gross savings = 300,000 * $0.010 = $3,000
verifier cost = 300,000 * $0.001 = $300
net semantic savings = $2,700
```

Prompt cache savings on remaining misses:

```text
remaining misses = 1,300,000
average model cost saved = 15% * $0.010 = $0.0015
savings = 1,300,000 * $0.0015 = $1,950
```

Total:

```text
gross savings = $4,000 + $2,700 + $1,950 = $8,650
infra cost = $1,500
net savings = $7,150/month
baseline cost = $20,000
net reduction = 35.75%
```

Then add reliability:

```text
provider outage without gateway:
  2% monthly request failure during incidents

with gateway failover:
  0.5% monthly request failure

availability impact:
  1.5 percentage point fewer failed requests
  30,000 more requests completed per 2,000,000 monthly requests
```

But validate quality:

```text
semantic false-hit rate
post-fallback quality delta
schema validation failures
user complaint rate
groundedness
```

Cost savings are not a win if correctness collapses.

---

### 6. Architecture Review Scenario

Product:

```text
enterprise support assistant
2M requests/month
RAG over public docs and tenant-specific docs
free and enterprise users
latency target: p95 under 5 seconds
budget target: reduce model spend by 40%
availability target: 99.9%
```

Design:

```text
1. Gateway is the only model access path.
2. Gateway enforces auth, tenant, model access, budgets, and quotas.
3. Exact cache handles public docs and immutable source-versioned summaries.
4. Semantic cache handles low-risk public FAQ intents with high threshold and verifier.
5. Account-specific routes use per-user exact cache only, short TTL, no semantic cache.
6. High-risk routes use premium model or human escalation, prompt cache only.
7. Stable prompt prefix maximizes provider prompt caching.
8. Routing chooses model by task, risk, context, SLA, and budget.
9. Fallback preserves capability and region constraints.
10. Observability tracks hit rate, precision, cached tokens, cost per success, latency, fallbacks, and quality.
```

Tradeoff:

```text
more infra complexity
more testing surface
better cost control
better resilience
better governance
faster provider migration
```

---

### 7. Interview-Ready Answer

> Design a caching and model gateway architecture for a high-traffic GenAI assistant.

I would put a model gateway between applications and providers so model access is centrally governed. The gateway would handle auth, tenant policy, model aliases, routing, rate limits, quotas, budgets, retries, fallbacks, caching, request normalization, logging, and spend attribution.

For caching, I would use three layers. First, exact-match response caching for deterministic, low-risk, source-versioned answers. The key would include tenant, permission scope, normalized input, prompt/model/policy versions, output schema, generation parameters, and retrieval fingerprint. Second, semantic caching for low-risk standalone questions where similar wording can safely reuse the same answer. That cache would use embeddings, a conservative threshold, metadata gates, source freshness checks, and possibly a verifier. Third, provider prompt caching through stable prompt prefixes: instructions, tools, schemas, and durable context first; volatile user data later or in metadata.

For routing, I would use logical tiers: cache/deterministic, small-fast, balanced, premium-reasoning, and human escalation. The gateway would route by task type, risk, context length, latency SLA, tenant plan, budget remaining, retrieval confidence, and provider health. Fallbacks must preserve capability, region, safety, and quality; I would not silently downgrade high-risk routes.

I would quantify impact with baseline vs post-rollout cost per request, session, and successful task. I would report exact hit rate, semantic precision, cached-token ratio, avoided tokens, net savings after infra and verifier cost, p95 latency, fallback rate, provider error rate, and post-fallback quality. The success condition is not maximum hit rate. It is lower cost and higher reliability without measurable correctness or safety regression.

---

### 8. Active Recall

1. What is the difference between exact response caching, semantic caching, and provider prompt caching?
2. Why does a RAG cache key need a retrieval fingerprint?
3. Why is semantic cache precision more important than hit rate for high-risk routes?
4. What belongs in a model gateway besides provider abstraction?
5. What signals should drive model routing?
6. Why is fallback not always allowed?
7. How do retries create cost and reliability risk?
8. What metrics prove caching actually saves money?
9. What metrics prove gateway failover actually improves reliability?
10. When should the right answer be graceful degradation instead of cheaper fallback?

---

### 9. Final Checkpoint Summary

- One-line summary: Caching reduces repeated model work; the model gateway centralizes policy, routing, resilience, and cost control.
- Three keywords: cache correctness, routing policy, cost per success.
- One interview trap: bragging about hit rate without measuring false hits, stale answers, or quality after fallback.
- One memory trick: exact cache reuses answers, semantic cache reuses "similar" answers, prompt cache reuses prefix computation, gateway decides who gets which model path.

Final takeaway:

> P4 is where GenAI stops being individual model calls and becomes shared production infrastructure: cache what is safe, route what remains, fail over without breaking the contract, and measure the economics honestly.

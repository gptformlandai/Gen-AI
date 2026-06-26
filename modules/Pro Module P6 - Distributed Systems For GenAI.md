# Pro Module P6 - Distributed Systems For GenAI

> **Module time:** 20h
> **Why this module matters:** The core canon deliberately excluded general infra to stay focused. At the pro tier that exclusion must be lifted, because every scaling, latency, and reliability decision in GenAI is ultimately a distributed-systems decision.

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic P6.1** | **Concurrency, queues, and backpressure (7h)** | |
| P6.1.a | Async request handling and streaming at scale | Done |
| P6.1.b | Queues, worker pools, and backpressure for spiky LLM traffic | Done |
| P6.1.c | Timeouts, retries, idempotency, and the thundering-herd problem | Done |
| **Topic P6.2** | **Scaling, state, and storage (7h)** | |
| P6.2.a | Horizontal scaling, load balancing, and stateless service design | Done |
| P6.2.b | Where state lives: sessions, memory stores, and vector DB scaling | Done |
| P6.2.c | Consistency, partitioning, and multitenancy at the data layer | Done |
| **Topic P6.3** | **Reliability and observability at scale (6h)** | |
| P6.3.a | SLOs, error budgets, and circuit breakers for GenAI services | Done |
| P6.3.b | Distributed tracing (OpenTelemetry-style) across the GenAI stack | Done |
| P6.3.c | Capacity, failure injection, and chaos basics for LLM systems | Done |
| **Module checkpoint** | Distributed systems for GenAI synthesis | Done |

**Covered so far:**
- P6.1.a - Async request handling and streaming at scale: async mental model, event loops, non-blocking provider calls, streaming response lifecycle, client disconnects, cancellation, flow control, long-lived connections, backpressure at stream boundaries, code sample, active recall, and interview-ready answer.
- P6.1.b - Queues, worker pools, and backpressure for spiky LLM traffic: burst absorption, admission control, priority queues, worker pools, queue depth, queue age, concurrency limits, overload modes, async jobs, fairness, dead-letter queues, active recall, and interview-ready traffic-spike design.
- P6.1.c - Timeouts, retries, idempotency, and the thundering-herd problem: deadline propagation, retry budgets, exponential backoff with jitter, idempotency keys, duplicate suppression, retry storms, cache stampedes, provider cooldowns, active recall, and interview-ready failure handling.
- P6.2.a - Horizontal scaling, load balancing, and stateless service design: stateless API tier, load balancers, sticky vs non-sticky routing, gateway scaling, streaming connection pressure, autoscaling signals, graceful shutdown, active recall, and interview-ready scaling answer.
- P6.2.b - Where state lives: sessions, memory stores, and vector DB scaling: state taxonomy, conversation state, short-term memory, long-term memory, checkpoints, tool state, cache state, vector index scaling, hot partitions, sharding, replication, active recall, and interview-ready state placement answer.
- P6.2.c - Consistency, partitioning, and multitenancy at the data layer: consistency levels, read-your-writes, eventual consistency, tenant isolation, partitioning keys, noisy neighbors, ACL-aware retrieval, per-tenant indexes, shared indexes, active recall, and interview-ready data design.
- P6.3.a - SLOs, error budgets, and circuit breakers for GenAI services: SLI/SLO definitions, quality-aware reliability, latency and cost SLOs, error budget policy, burn rate, circuit breaker states, fallback behavior, active recall, and interview-ready SLO answer.
- P6.3.b - Distributed tracing across the GenAI stack: trace propagation, spans for gateway/retrieval/reranking/tools/model/streaming, token and cost attributes, redaction, sampling, trace-to-eval conversion, active recall, and interview-ready tracing answer.
- P6.3.c - Capacity, failure injection, and chaos basics for LLM systems: capacity modeling, traffic shape, concurrency, token throughput, queueing, failure injection, chaos drills, game days, rollback, active recall, and interview-ready resilience answer.
- Module checkpoint - Distributed systems for GenAI synthesis: backpressure and queues under spikes, stateless vs stateful boundaries, state placement, SLO and circuit-breaker design, production endpoint scenario, active recall, and senior-level distributed systems defense.

---

## Topic P6.1: Concurrency, Queues, and Backpressure

> **Topic time:** 7h
> Focus: Keeping GenAI services stable when requests are slow, streaming, expensive, bursty, and dependent on external model providers or GPU capacity.

Traditional web requests are often short.

GenAI requests are often:

```text
long-running
token-streaming
provider-dependent
GPU-dependent
tool-dependent
costly
stateful from the user's point of view
```

That changes the reliability problem.

The central idea:

> A GenAI service is not just serving HTTP responses. It is scheduling scarce model, retrieval, tool, network, and budget capacity under uncertainty.

If you do not control concurrency, queues, timeouts, and retries, the system can collapse exactly when users need it most.

---

## Subtopic P6.1.a: Async Request Handling and Streaming at Scale

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain how async request handling and streaming improve scalability and user experience, and where they introduce new failure modes.

### Add to Knowledge Base

Async request handling means a service can wait on slow I/O without blocking a worker thread.

Streaming means the service sends partial output as it arrives instead of waiting for the full model response.

The mental model:

> Async keeps the server from wasting workers while waiting. Streaming keeps the user from staring at silence.

But streaming does not make model inference free.

It changes:

```text
perceived latency
connection lifetime
memory usage
cancellation behavior
backpressure needs
load balancer behavior
observability shape
```

---

### 1. Why Async Matters for GenAI

A GenAI endpoint may wait on:

```text
embedding call
vector DB search
reranker call
model provider call
tool API call
streamed token output
moderation check
trace write
```

If each waiting request occupies a blocking thread, concurrency becomes expensive.

Async lets one process handle many waiting requests by yielding while I/O is in progress.

This is useful when the bottleneck is:

```text
network I/O
provider latency
database I/O
streaming token waits
```

It is not magic when the bottleneck is:

```text
CPU-bound tokenization
local GPU inference
synchronous blocking libraries
large JSON serialization
```

Async only helps if the code actually yields.

---

### 2. Streaming Lifecycle

Streaming flow:

```text
1. Client opens request.
2. API authenticates and validates.
3. Gateway/retrieval/tool work runs.
4. Model call starts.
5. First token or event arrives.
6. Server forwards chunks to client.
7. Client renders partial response.
8. Server tracks usage, latency, and final status.
9. Stream completes, errors, or is cancelled.
```

Important streaming metrics:

```text
time to first byte
time to first token
inter-token latency
stream duration
tokens streamed
client disconnect rate
stream error rate
server cancellation latency
```

Streaming improves user experience especially when:

```text
answers are long
model decode is slow
tools run before generation
users can start reading before completion
```

---

### 3. Streaming Failure Modes

Streaming introduces new problems:

```text
client disconnects but provider keeps generating
server continues paying for abandoned output
load balancer times out idle stream
proxy buffers stream and ruins token-by-token output
too many open streams consume memory
slow client causes send buffer buildup
partial answer is shown before safety validation
trace logs record incomplete output as success
retry duplicates a partially completed answer
```

Production streaming needs:

```text
disconnect detection
cancellation propagation
heartbeat events
flow control
per-stream memory limits
finalization hooks
partial-output safety strategy
```

---

### 4. Safety and Streaming

Streaming creates a safety tradeoff.

If you stream every token immediately:

```text
lowest perceived latency
harder to block unsafe late output
```

If you buffer and validate:

```text
safer
higher latency
less "live" feel
```

Common compromise:

```text
pre-check input
stream low-risk routes directly
buffer high-risk routes or sentences
run output classifiers on chunks
stop stream on policy breach
route high-risk tasks to non-streaming review
```

The correct design depends on risk tier.

---

### 5. Backpressure at the Stream Boundary

A model may generate faster than the client can receive.

That creates buffers:

```text
provider buffer
server buffer
network buffer
client buffer
```

If buffers grow without limit, memory rises.

If the client is slow, the server should:

```text
pause reading from upstream if possible
drop low-priority stream
cancel after timeout
limit per-stream buffer size
```

This is backpressure:

```text
the slow downstream component forces upstream components to slow or stop
```

Without it, slow clients can become a system-wide memory problem.

---

### 6. Code Sample: Async Streaming Skeleton

```python
import asyncio


class ClientDisconnected(Exception):
    pass


async def model_stream(prompt: str):
    for token in ["Hello", ",", " world", "."]:
        await asyncio.sleep(0.1)
        yield token


async def send_to_client(token: str):
    await asyncio.sleep(0.01)
    print(token, end="", flush=True)


async def stream_response(prompt: str, client_connected):
    try:
        async for token in model_stream(prompt):
            if not client_connected():
                raise ClientDisconnected()
            await send_to_client(token)
    except ClientDisconnected:
        # In production, propagate cancellation to provider if supported.
        print("\nstream cancelled by client")
        raise
    finally:
        # Record final stream status: complete, error, or cancelled.
        print("\nstream finalized")
```

The important part is not the toy model.

The important part is that streaming has a lifecycle.

---

### 7. Practical Interview Question

> Your GenAI endpoint streams responses and traffic grows 10x. What scaling issues do you expect?

### Strong Answer

I would expect long-lived connections to become a major resource. Streaming improves perceived latency, but each open stream consumes connection slots, memory, load balancer state, and trace state. I would track time to first token, stream duration, open streams, client disconnects, cancellation latency, and per-stream buffer size.

The service should use async I/O so waiting on provider tokens does not block worker threads. It also needs cancellation propagation so if the client disconnects, the upstream provider or inference request is cancelled when possible. Load balancers and proxies must be configured not to buffer streams or kill healthy long-running responses too early.

Finally, I would apply route-specific safety. Low-risk routes can stream directly. High-risk routes may need chunk buffering, output checks, or non-streaming review. Streaming is a UX improvement, but at scale it is also a connection-management and backpressure problem.

### Active Recall

1. What does async request handling actually save?
2. Why does streaming improve perceived latency but not eliminate compute cost?
3. What happens if a client disconnect is not propagated upstream?
4. Why can proxy buffering ruin streaming?
5. What streaming metrics would you put on a dashboard?

Final takeaway:

> Async and streaming make GenAI feel responsive, but production streaming must manage open connections, cancellation, buffers, safety, and observability.

---

## Subtopic P6.1.b: Queues, Worker Pools, and Backpressure for Spiky LLM Traffic

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain how queues and worker pools absorb bursts, where they do not create capacity, and how backpressure protects the system under overload.

### Add to Knowledge Base

Queues let you decouple request arrival from request processing.

The mental model:

> A queue is a shock absorber, not an engine.

It can absorb a burst.

It cannot create infinite model capacity.

If work arrives faster than the system can process it, queue depth grows.

At some point, you must:

```text
scale workers
slow intake
downgrade work
drop work
reject work
ask the user to wait
```

That is backpressure.

---

### 1. Where Queues Fit in GenAI

Queues are useful for:

```text
batch document ingestion
embedding jobs
long summarization jobs
offline eval runs
fine-tuning data processing
non-interactive report generation
human review workflows
tool-heavy agent tasks
retryable provider calls
```

Queues are less useful for:

```text
interactive chat requiring immediate response
low-latency streaming
high-risk actions requiring synchronous approval
requests that expire quickly
```

For interactive routes, queueing must be bounded and visible to the user.

---

### 2. Queue Metrics

Important metrics:

```text
queue depth
oldest message age
enqueue rate
dequeue rate
processing time
worker utilization
retry count
dead-letter count
priority mix
drop/reject count
```

Queue depth alone is not enough.

A queue of 1,000 tiny jobs may be fine.

A queue of 1,000 30-minute jobs is a crisis.

Oldest message age is often the more user-relevant metric.

---

### 3. Worker Pools

Worker pools process queued jobs.

Workers should have:

```text
bounded concurrency
per-provider limits
per-tenant fairness
deadline awareness
retry policy
idempotency
resource reservations
graceful shutdown
dead-letter behavior
```

A worker pool without concurrency limits can stampede a provider.

A worker pool without fairness can let one tenant starve everyone else.

---

### 4. Backpressure Strategies

When the system is overloaded:

```text
reject low-priority requests quickly
return 429 with retry-after
queue only if the job can still finish before deadline
degrade model tier
serve cache
reduce max output tokens
switch to async job mode
pause ingestion
apply per-tenant limits
increase workers only if downstream capacity exists
```

Bad overload behavior:

```text
accept everything
queue forever
retry aggressively
time out at the edge after wasting backend work
```

Good overload behavior:

```text
admit only work you can finish
preserve high-priority traffic
fail fast for work you cannot serve
```

---

### 5. Priority and Fairness

GenAI workloads often mix:

```text
interactive user requests
background evals
embedding backfills
batch reports
premium tenant traffic
free-tier traffic
internal test traffic
```

If all share one queue, background work can harm user traffic.

Use:

```text
priority queues
separate worker pools
weighted fair scheduling
tenant-level limits
deadline-aware scheduling
```

Rule:

> Background work should yield to interactive user work unless the business explicitly says otherwise.

---

### 6. Dead-Letter Queues

Some jobs fail repeatedly.

Do not retry forever.

Move them to a dead-letter queue with:

```text
job ID
failure reason
attempt count
last error
trace ID
tenant
input reference
privacy classification
```

Dead-letter queues are not trash.

They are failure evidence.

They feed debugging and eval creation.

---

### 7. Code Sample: Admission Control

```python
def admit_request(queue_age_seconds: float, route: str, user_plan: str) -> str:
    if route == "interactive_chat" and queue_age_seconds > 3:
        if user_plan == "enterprise":
            return "serve_with_priority"
        return "degrade_or_retry_after"

    if route == "background_embedding" and queue_age_seconds > 60:
        return "pause_ingestion"

    if queue_age_seconds > 300:
        return "reject_fast"

    return "admit"
```

The key idea:

```text
admission depends on queue age, route, and priority
```

---

### 8. Practical Interview Question

> A product launch causes a 20x spike in LLM traffic. How do queues and backpressure help?

### Strong Answer

I would first separate traffic classes. Interactive user requests, background embeddings, evals, and batch jobs should not all compete in one FIFO queue. The gateway should apply admission control based on route, tenant, priority, queue age, provider health, and remaining deadline.

Queues can absorb short bursts, but they do not create model capacity. I would track queue depth, oldest message age, worker utilization, provider rate-limit errors, retry count, and task deadlines. If the queue age grows beyond what users can tolerate, the system should apply backpressure: serve cache, downgrade low-risk routes, reduce output length, pause background jobs, return retry-after, or reject low-priority work quickly.

Worker pools should have bounded concurrency and per-provider limits so they do not stampede the model provider. The goal is to keep high-priority work healthy instead of accepting all work and failing slowly.

### Active Recall

1. Why is a queue a shock absorber, not an engine?
2. Why is oldest message age often more useful than queue depth?
3. What traffic classes should be separated?
4. What is a dead-letter queue for?
5. What does "admit only work you can finish" mean?

Final takeaway:

> Queues protect GenAI systems from bursts only when paired with bounded workers, priorities, deadlines, and backpressure.

---

## Subtopic P6.1.c: Timeouts, Retries, Idempotency, and the Thundering-Herd Problem

> **Subtopic time:** 2h
> Outcome: You should be able to design retry and timeout behavior that improves resilience without duplicating work, multiplying cost, or causing a self-inflicted outage.

### Add to Knowledge Base

Distributed systems fail partially.

GenAI systems fail expensively.

The mental model:

> A retry is not free. In GenAI, a retry can duplicate tokens, tools, actions, and cost.

Timeouts and retries are necessary.

But careless retries create:

```text
retry storms
duplicate tool actions
provider overload
cache stampedes
thundering-herd recovery
cost explosions
```

---

### 1. Deadline Propagation

Every request should have an end-to-end deadline.

Example:

```text
user-facing SLA: 8 seconds
```

Budget:

```text
auth: 100ms
retrieval: 600ms
rerank: 800ms
model: 5s
post-processing: 500ms
buffer: 1s
```

If retrieval already used 4 seconds, the model call should know it has less time.

Do not let each layer use its own full timeout.

Bad:

```text
gateway timeout 8s
retrieval timeout 8s
model timeout 8s
tool timeout 8s
```

This can turn an 8-second user request into a 30-second backend mess.

Good:

```text
one deadline propagated through all layers
```

---

### 2. Retry Budgets

Retries should be bounded by:

```text
attempt count
remaining deadline
tenant quota
provider health
request risk
idempotency
cost budget
```

Retry good candidates:

```text
network reset before provider accepted request
transient 500
429 with retry-after and enough deadline
temporary connection timeout
```

Do not retry blindly:

```text
invalid request
policy refusal
context window exceeded without changing input
side-effecting tool action
already long-running generation near deadline
```

---

### 3. Backoff and Jitter

Exponential backoff:

```text
wait 100ms
wait 200ms
wait 400ms
wait 800ms
```

Jitter adds randomness:

```text
wait 100ms +/- random spread
```

Why jitter matters:

```text
without jitter, many clients retry at the same time
```

That synchronized retry is a thundering herd.

It can keep a recovering provider down.

---

### 4. Idempotency

Idempotency means repeating the same request does not repeat the side effect.

For GenAI:

```text
generating text twice is costly but usually safe
sending an email twice is not safe
issuing a refund twice is not safe
creating two tickets may not be safe
```

Use idempotency keys for:

```text
tool actions
job creation
payment/refund workflows
email sending
database writes
long-running async tasks
```

Store:

```text
idempotency_key
request fingerprint
status
result
created_at
expires_at
```

If the same key arrives again:

```text
return stored result or current status
do not run the action twice
```

---

### 5. Cache Stampedes

A cache stampede happens when many requests miss the cache at once and all recompute the same expensive answer.

In GenAI this can mean:

```text
hundreds of identical long-context model calls
```

Prevent with:

```text
single-flight locking
request coalescing
stale-while-revalidate
per-key concurrency limits
jittered TTLs
```

Single-flight:

```text
first request computes
other identical requests wait for result
```

This is especially important for exact response caching and embedding backfills.

---

### 6. Code Sample: Idempotency Table Logic

```python
def handle_action(request, store):
    key = request["idempotency_key"]
    existing = store.get(key)

    if existing:
        if existing["request_hash"] != request["request_hash"]:
            raise ValueError("idempotency key reused for different request")
        return existing["status"], existing.get("result")

    store[key] = {
        "request_hash": request["request_hash"],
        "status": "running",
    }

    try:
        result = perform_side_effect(request)
        store[key].update({"status": "succeeded", "result": result})
        return "succeeded", result
    except Exception as exc:
        store[key].update({"status": "failed", "error": str(exc)})
        raise
```

The principle:

```text
retries may happen
side effects must not duplicate
```

---

### 7. Practical Interview Question

> Your GenAI service times out and clients retry aggressively. Costs spike and providers start returning 429s. What went wrong?

### Strong Answer

The system likely lacks deadline propagation, retry budgets, backoff with jitter, and admission control. If each client retries immediately after timeout, the system multiplies work exactly when capacity is already constrained. For LLM calls, that means duplicate token cost and additional provider pressure.

I would enforce a global request deadline and pass remaining time through retrieval, tools, and model calls. Retries should be bounded by attempt count, remaining deadline, error type, idempotency, provider health, and cost budget. Transient errors can retry with exponential backoff and jitter. Non-retryable errors should fail fast.

For side-effecting tools, I would require idempotency keys and action ledgers so retries cannot send duplicate emails or issue duplicate refunds. I would also add circuit breakers, retry-after handling, and backpressure so overloaded dependencies are not hammered by synchronized retries.

### Active Recall

1. Why should timeouts be based on a propagated deadline?
2. What errors should not be retried blindly?
3. Why does jitter reduce thundering herds?
4. What is an idempotency key?
5. What is a cache stampede?

Final takeaway:

> Timeouts and retries protect reliability only when bounded by deadlines, jitter, idempotency, and backpressure.

---

## Topic P6.2: Scaling, State, and Storage

> **Topic time:** 7h
> Focus: Designing GenAI services so compute scales horizontally while state lives in the right durable, consistent, tenant-aware systems.

Scaling starts with one question:

```text
What can be stateless, and what must be stateful?
```

The central idea:

> Stateless compute is easy to scale. Stateful data is where correctness, privacy, and consistency live.

GenAI systems have more state than they first appear to:

```text
conversation history
retrieval indexes
tool results
agent checkpoints
memory
eval traces
cache entries
tenant permissions
prompt versions
workflow state
```

The architecture works when each state type lives in the right place.

---

## Subtopic P6.2.a: Horizontal Scaling, Load Balancing, and Stateless Service Design

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain how to horizontally scale a GenAI API tier and why stateless services make deploys, failover, and autoscaling safer.

### Add to Knowledge Base

Horizontal scaling means adding more service instances.

Stateless service design means any instance can handle any request because durable state is externalized.

The mental model:

> App servers should be replaceable workers, not memory boxes full of hidden user state.

A stateless GenAI API instance can:

```text
authenticate
load config
call retrieval
call model gateway
stream response
write trace
```

But it should not be the only place storing:

```text
conversation history
agent checkpoint
tenant memory
job status
tool side-effect ledger
```

---

### 1. Stateless API Tier

Stateless API instances can scale behind a load balancer:

```text
client
  -> load balancer
  -> api instance A/B/C
  -> shared stores and gateways
```

Benefits:

```text
easy autoscaling
easy rolling deploys
better failover
less sticky-session dependence
clearer recovery
```

If instance A dies, instance B can continue future requests because state is external.

Streaming complicates this because an active stream is tied to a connection.

But future turns should not depend on the same instance.

---

### 2. Load Balancing

Load balancers must consider:

```text
HTTP request load
long-lived streaming connections
WebSocket/SSE behavior
health checks
connection draining
request body size
idle timeouts
regional routing
```

For streaming endpoints:

```text
idle timeout must exceed expected token gaps
proxy buffering should be disabled
connection draining must allow streams to finish or cancel cleanly
```

If the load balancer kills streams too aggressively, users see partial answers.

---

### 3. Autoscaling Signals

Do not scale only on CPU.

GenAI API tier bottlenecks can be:

```text
open streams
request concurrency
event loop lag
memory per stream
queue age
provider latency
token throughput
gateway saturation
connection count
```

Useful signals:

```text
p95 latency
active requests
active streams
queue age
event loop lag
CPU
memory
error rate
```

Autoscaling should include cooldowns.

Otherwise a temporary provider slowdown can cause unstable scale-up/scale-down loops.

---

### 4. Graceful Shutdown

Rolling deploys must handle active streams.

Graceful shutdown:

```text
1. Mark instance unhealthy for new traffic.
2. Stop accepting new requests.
3. Let active requests finish up to a deadline.
4. Cancel or hand off long-running work if supported.
5. Flush traces and metrics.
6. Exit.
```

Without graceful shutdown, deploys cause partial streams and lost traces.

---

### 5. Code Sample: Stateless Request Handler Shape

```python
async def handle_chat(request, stores, gateway):
    user = await stores.auth.validate(request.token)
    session = await stores.sessions.load(request.session_id, user.id)

    prompt = build_prompt(
        template_version=request.prompt_version,
        conversation=session.recent_messages,
        user_message=request.message,
    )

    response = await gateway.generate(
        route="chat",
        tenant_id=user.tenant_id,
        prompt=prompt,
        trace_id=request.trace_id,
    )

    await stores.sessions.append_message(request.session_id, user.id, request.message, response.text)
    await stores.traces.write(response.trace)
    return response
```

The handler is stateless because state is loaded from and written to external stores.

---

### 6. Practical Interview Question

> How would you horizontally scale a GenAI chat service?

### Strong Answer

I would keep the API tier stateless and put it behind a load balancer. Conversation history, session state, agent checkpoints, job status, caches, and tool side-effect ledgers should live in external stores. Any API instance should be able to serve the next request for a session.

For streaming, I would configure the load balancer for long-lived SSE or WebSocket connections, disable proxy buffering where needed, set appropriate idle timeouts, and use connection draining during deploys. Active streams may be tied to an instance, but future turns should not be.

Autoscaling should not rely only on CPU. I would scale based on active requests, active streams, queue age, p95 latency, event loop lag, memory, and error rate. I would also use graceful shutdown so rolling deploys do not cut off streams or lose traces.

### Active Recall

1. Why are stateless API instances easier to scale?
2. What state should not live only in process memory?
3. Why do streaming endpoints need special load balancer settings?
4. What autoscaling signals matter besides CPU?
5. What is graceful shutdown?

Final takeaway:

> Horizontally scalable GenAI services keep compute stateless and move durable conversation, workflow, cache, and trace state into purpose-built stores.

---

## Subtopic P6.2.b: Where State Lives - Sessions, Memory Stores, and Vector DB Scaling

> **Subtopic time:** 2.5h
> Outcome: You should be able to place each type of GenAI state in the right store and explain the scaling implications.

### Add to Knowledge Base

GenAI systems use many kinds of state.

The mental model:

> State should live where its lifetime, consistency needs, privacy needs, and access pattern make sense.

Do not put all state in one database just because it is convenient.

Do not put all state in the prompt just because the model can see it.

---

### 1. State Taxonomy

| State Type | Example | Typical Store |
|---|---|---|
| Session state | conversation turns, UI state | relational/document DB |
| Short-term context | recent messages, scratchpad | session store, cache, checkpoint |
| Long-term memory | user preferences, durable facts | memory store with review/update rules |
| Agent checkpoint | graph node, state object, pending interrupt | durable checkpoint DB |
| Tool state | action ledger, approval status | relational DB |
| Retrieval state | chunks, embeddings, metadata | vector DB plus source store |
| Cache state | response cache, semantic cache | Redis, vector cache, object store |
| Eval trace state | traces, labels, fixtures | analytics store plus eval registry |
| Config state | prompt/model/routing versions | config service/registry |

Each has different requirements.

---

### 2. Conversation Sessions

Conversation state should support:

```text
append new messages
load recent window
summarize or compact older turns
delete or export user data
audit access
restore after server restart
```

Avoid:

```text
storing long conversation only in browser
storing it only in API instance memory
blindly sending entire history forever
```

Common pattern:

```text
full history in durable store
recent window in prompt
summary memory for older context
trace IDs for debugging
```

---

### 3. Memory Stores

Memory is not just "more context."

Memory can be:

```text
user preference
project fact
past decision
learned correction
tool result
long-term profile
```

Memory should have:

```text
source trace
created_at
updated_at
confidence
scope
tenant/user binding
expiration
delete path
review status
```

Bad memory:

```text
model decides a fact and stores it forever
```

Better memory:

```text
memory writes go through extraction, validation, permission, and review rules
```

---

### 4. Vector DB Scaling

Vector DB state includes:

```text
embeddings
chunk text or references
metadata
ACLs
tenant IDs
document versions
index structures
```

Scaling concerns:

```text
index size
embedding dimension
write rate
query rate
metadata filter selectivity
tenant distribution
hot tenants
replication
sharding
refresh latency
delete behavior
```

Two broad designs:

```text
shared index with tenant and ACL filters
per-tenant indexes or partitions
```

Shared index:

```text
better utilization
easier global ops
more isolation risk
filters must be correct and fast
```

Per-tenant index:

```text
stronger isolation
easier tenant deletion/export
more operational overhead
many small indexes can be inefficient
```

---

### 5. Hot Partitions

A hot partition happens when too much traffic or data targets one shard.

Examples:

```text
one large enterprise tenant dominates queries
one popular public doc is retrieved constantly
one semantic cache key gets hammered
one embedding backfill floods writes
```

Mitigations:

```text
partition by tenant plus sub-shard
replicate hot read partitions
cache popular retrieval results
separate heavy tenants
rate-limit ingestion
schedule backfills
```

---

### 6. Practical Interview Question

> Where would you store conversation state, long-term memory, and vector search data?

### Strong Answer

I would store full conversation history in a durable session store, not in API process memory. The prompt should include only the recent window and any validated summaries needed for the current turn. This allows horizontal scaling, deletion/export workflows, and recovery after instance failure.

Long-term memory should live in a dedicated memory store with metadata: source trace, confidence, scope, tenant/user binding, timestamps, expiration, and review status. I would not let the model write permanent memory without validation.

Vector search data belongs in a vector database with metadata, document versions, tenant and ACL filters, and a source document store. For multitenancy, I would choose shared index with strict filters for many small tenants, or per-tenant indexes/partitions for high-isolation or large enterprise tenants. The choice depends on isolation requirements, query volume, delete/export needs, and operational overhead.

### Active Recall

1. Why should conversation state survive API instance restarts?
2. What metadata should long-term memory include?
3. Why is memory not just more context?
4. What are the tradeoffs between shared and per-tenant vector indexes?
5. What causes hot partitions in GenAI systems?

Final takeaway:

> State placement is the hidden architecture of GenAI systems. Put each state type where its lifetime, consistency, privacy, and access pattern belong.

---

## Subtopic P6.2.c: Consistency, Partitioning, and Multitenancy at the Data Layer

> **Subtopic time:** 2h
> Outcome: You should be able to reason about consistency and tenant isolation for sessions, vector search, permissions, caches, and long-running workflows.

### Add to Knowledge Base

Distributed systems force tradeoffs.

GenAI systems add another concern:

```text
the model can confidently use stale, wrong, or unauthorized state
```

The mental model:

> Data consistency is not abstract in GenAI. It decides which facts, permissions, and memories the model is allowed to reason over.

If consistency is wrong, the answer can be wrong even when the model behaves perfectly.

---

### 1. Consistency Needs by State Type

| State | Consistency Need |
|---|---|
| session append | read-your-writes usually expected |
| tool action ledger | strong consistency for side effects |
| approval state | strong consistency |
| tenant permissions | strong or carefully cached with short TTL |
| vector index updates | eventual consistency often acceptable with disclosure |
| analytics traces | eventual consistency acceptable |
| semantic cache | eventual consistency acceptable, but permission-safe |
| budget counters | strong-ish or bounded-staleness to avoid overspend |

Not every store needs strong consistency.

But some absolutely do.

Do not use eventual consistency for refund approval state.

---

### 2. Read-Your-Writes

Users expect:

```text
I just uploaded a document
Now the assistant can use it
```

But vector indexing may be async.

Options:

```text
block until indexing completes
show "processing" status
query source directly until embedding is ready
use hybrid temporary index
make freshness visible
```

Do not silently pretend the assistant has read a document that is still indexing.

---

### 3. Partitioning Keys

Partition by a key that matches access patterns.

Possible keys:

```text
tenant_id
tenant_id + document_type
tenant_id + user_id
region
corpus_id
time bucket
```

Bad partitioning:

```text
all enterprise tenants in one hot shard
all writes for all tenants into one global partition
partition key that prevents common queries
```

Good partitioning balances:

```text
query efficiency
tenant isolation
hotspot avoidance
delete/export needs
cost
operational complexity
```

---

### 4. Multitenancy

Multitenancy means one system serves multiple tenants.

Isolation surfaces:

```text
auth
session storage
vector search
metadata filters
response cache
semantic cache
memory
traces
tool credentials
budgets
rate limits
logs
```

Common bug:

```text
retrieval filter uses tenant_id
but semantic cache key does not
```

Another common bug:

```text
trace viewer lets support staff see raw tenant content without authorization
```

Tenant isolation must be end-to-end.

---

### 5. ACL-Aware Retrieval

For permissioned retrieval:

```text
1. Authenticate user.
2. Resolve tenant and user permission scope.
3. Build retrieval filters from authorization service.
4. Search only allowed partitions or apply ACL filters.
5. Verify returned chunks are allowed.
6. Include ACL version in trace/cache key.
```

Do not ask the model to ignore unauthorized documents.

The model should never receive them.

---

### 6. Practical Interview Question

> How would you design multitenant vector retrieval safely?

### Strong Answer

I would treat tenant isolation as a data-layer requirement, not a prompt instruction. At query time, the service authenticates the user, resolves tenant and permission scope, and builds retrieval filters or selects tenant-specific partitions. Returned chunks are verified against ACLs before entering the prompt, and the ACL version is included in traces and cache keys.

For many small tenants, a shared index with strict tenant and ACL filters may be efficient. For large or regulated tenants, per-tenant indexes or partitions may be better for isolation, deletion, and performance. I would also isolate response caches, semantic caches, memory, traces, tool credentials, budgets, and logs by tenant.

Consistency depends on state type. Tool approvals and side-effect ledgers need strong consistency. Vector indexing can be eventually consistent if the UI shows processing status or the system has a freshness strategy. The model should never receive unauthorized or stale-sensitive data silently.

### Active Recall

1. Which GenAI state types need strong consistency?
2. Why can vector indexing be eventually consistent in some systems?
3. What is read-your-writes and why does it matter after document upload?
4. Where can multitenancy leak besides vector retrieval?
5. Why should unauthorized docs never enter the prompt?

Final takeaway:

> In GenAI, consistency and multitenancy are answer-quality and security features, not only database details.

---

## Topic P6.3: Reliability and Observability at Scale

> **Topic time:** 6h
> Focus: Defining reliability targets, tracing failures across layers, and testing whether the system survives realistic dependency failures.

Reliability is not:

```text
the model usually works
```

Reliability is:

```text
the system meets defined behavior under expected load and partial failure
```

GenAI reliability includes:

```text
availability
latency
quality
safety
cost
freshness
tool correctness
retrieval correctness
```

The central idea:

> Production GenAI reliability must be measured across the whole workflow, not only the final model call.

---

## Subtopic P6.3.a: SLOs, Error Budgets, and Circuit Breakers for GenAI Services

> **Subtopic time:** 2h
> Outcome: You should be able to define meaningful SLOs for GenAI endpoints and design circuit breakers that prevent unhealthy dependencies from taking down the system.

### Add to Knowledge Base

SLI:

```text
service level indicator
what you measure
```

SLO:

```text
service level objective
the target you promise internally or externally
```

Error budget:

```text
how much unreliability is allowed before you slow launches or mitigate
```

The mental model:

> An SLO turns "the assistant should work well" into measurable operating policy.

---

### 1. GenAI SLIs

Availability:

```text
successful responses / valid requests
```

Latency:

```text
p95 time to first token
p95 end-to-end latency
stream completion rate
```

Quality:

```text
grounded answer rate
citation correctness
schema validity
task success
human acceptance
```

Safety:

```text
unsafe output rate
over-refusal rate
under-refusal rate
secret leakage
cross-tenant leakage
```

Cost:

```text
cost per successful task
tokens per request
budget burn rate
```

Freshness:

```text
indexed document lag
retrieval freshness
cache stale-hit rate
```

GenAI SLOs should include more than uptime.

---

### 2. Example SLOs

For a support RAG assistant:

```text
availability:
  99.9% of valid support requests return a final response or controlled escalation

latency:
  95% of interactive requests have first token under 2.5s
  95% complete under 12s

quality:
  97% of sampled high-confidence answers are grounded in allowed sources
  99% of answers with citations cite accessible documents

safety:
  0 critical cross-tenant leakage incidents
  unsafe output rate below 0.1% on sampled traffic

cost:
  p95 cost per successful support task below $0.05
```

These SLOs are operationally meaningful.

---

### 3. Error Budgets

If the SLO allows 0.1% failures, that is the error budget.

If the service burns budget too fast:

```text
pause risky deployments
disable unstable features
increase fallback use
tighten rate limits
reduce traffic to failing provider
prioritize reliability fixes
```

Error budget policy connects reliability to release decisions.

This is P2 plus production operations.

---

### 4. Circuit Breakers

A circuit breaker stops calling an unhealthy dependency.

States:

```text
closed:
  calls flow normally

open:
  calls are blocked or routed elsewhere

half-open:
  limited probe calls test recovery
```

Open when:

```text
error rate exceeds threshold
timeout rate spikes
429 rate spikes
p95 latency exceeds threshold
schema failures spike
safety guardrail failures spike
```

Actions:

```text
route to fallback
serve cache
degrade response
queue async job
return controlled error
```

Circuit breakers prevent slow or failing dependencies from consuming all capacity.

---

### 5. Circuit Breaker Policy Example

```yaml
provider_circuit_breaker:
  window: 60s
  open_if:
    timeout_rate_gt: 0.20
    error_rate_gt: 0.10
    p95_latency_ms_gt: 15000
  half_open_after: 30s
  half_open_probe_requests: 20
  fallback:
    low_risk: "balanced_backup"
    high_risk: "controlled_escalation"
```

The fallback differs by risk tier.

That detail matters.

---

### 6. Practical Interview Question

> Define SLOs and circuit-breaker behavior for a production GenAI endpoint.

### Strong Answer

I would define SLOs across availability, latency, quality, safety, and cost. For example, 99.9% of valid requests should return a response or controlled escalation, p95 time to first token should be under 2.5 seconds, p95 completion under 12 seconds, groundedness above 97% on sampled RAG answers, zero critical cross-tenant leakage, and cost per successful task below a route-specific threshold.

The circuit breaker would monitor provider and dependency health using error rate, timeout rate, 429 rate, p95 latency, schema failure rate, and safety failure rate. If thresholds are crossed over a rolling window, the circuit opens and traffic routes to compatible fallback, cache, async queue, or graceful degradation. It later half-opens with limited probes.

Fallback must be route-aware. Low-risk FAQ can use a cheaper backup or cache. High-risk legal or tool-action routes may need same-tier fallback or controlled escalation rather than silent downgrade.

### Active Recall

1. What is the difference between an SLI and an SLO?
2. Why do GenAI SLOs need quality and safety, not just uptime?
3. What is an error budget?
4. What are the three circuit breaker states?
5. Why should circuit-breaker fallback depend on risk tier?

Final takeaway:

> SLOs define what reliable means. Circuit breakers protect that reliability when dependencies become slow, expensive, or unhealthy.

---

## Subtopic P6.3.b: Distributed Tracing Across the GenAI Stack

> **Subtopic time:** 2h
> Outcome: You should be able to trace a GenAI request across gateway, retrieval, reranking, tools, model calls, streaming, caches, and output validation.

### Add to Knowledge Base

Distributed tracing follows one request across many services.

For GenAI, a single answer may cross:

```text
frontend
API
gateway
auth
session store
retriever
vector DB
reranker
tool service
model provider
cache
moderation
trace store
```

The mental model:

> A trace is the request's flight recorder.

When something goes wrong, the trace tells you where time, cost, context, and decisions went.

---

### 1. Trace Structure

Trace:

```text
one end-to-end request
```

Span:

```text
one operation inside the trace
```

Example spans:

```text
http.request
auth.validate
session.load
gateway.route
cache.lookup
retrieval.embed_query
retrieval.vector_search
reranker.rank
tool.call
model.generate
stream.forward
output.validate
trace.persist
```

Each span has:

```text
start time
duration
status
attributes
error details
parent span
```

---

### 2. GenAI Trace Attributes

Useful attributes:

```text
tenant_id_hash
route
risk_tier
prompt_version
model_alias
provider
region
input_tokens
cached_tokens
output_tokens
estimated_cost
cache_status
retrieval_top_k
retrieval_scores
doc_ids
reranker_model
tool_names
fallback_reason
retry_count
schema_valid
safety_label
stream_cancelled
```

Avoid raw sensitive text unless explicitly allowed.

Use:

```text
hashes
redacted snippets
document references
sampled content
access-controlled trace views
```

---

### 3. Why Tracing Beats Logs Alone

Logs say:

```text
something happened
```

Traces show:

```text
how operations were connected
where latency occurred
which fallback path ran
which dependency failed first
which retriever result became context
which model version produced output
```

For GenAI debugging, this matters because failure is often cross-layer.

Example:

```text
final answer wrong
```

Trace may reveal:

```text
retrieval returned outdated chunk
reranker placed correct chunk at rank 9
context builder truncated rank 9
model never saw the evidence
```

That is not a model failure.

That is an orchestration and retrieval failure.

---

### 4. Trace-to-Eval Conversion

Traces can seed evals.

A good trace includes enough to create:

```text
input
retrieval snapshot
tool mocks
prompt/config versions
expected output
failure type
latency/cost baseline
```

This connects P6 to P5:

```text
observability -> reproducibility -> regression coverage
```

---

### 5. Code Sample: Span Naming

```python
from contextlib import contextmanager
import time


@contextmanager
def span(name: str, **attrs):
    started = time.time()
    print(f"start span={name} attrs={attrs}")
    try:
        yield
        status = "ok"
    except Exception:
        status = "error"
        raise
    finally:
        duration_ms = int((time.time() - started) * 1000)
        print(f"end span={name} status={status} duration_ms={duration_ms}")


with span("gateway.route", route="support_rag", risk_tier="medium"):
    with span("retrieval.vector_search", top_k=8):
        pass
    with span("model.generate", model_alias="balanced"):
        pass
```

Real systems use tracing libraries.

The naming discipline is the lesson.

---

### 6. Practical Interview Question

> A user reports a wrong answer. What should your distributed trace show?

### Strong Answer

The trace should show the full path: request metadata, tenant and route, prompt version, model alias, gateway routing decision, cache status, retrieval query, filters, top-k chunks, document versions, ACL versions, reranker scores, context builder behavior, tool calls, model generation span, output validation, safety labels, token usage, latency, cost, and final outcome.

I would not rely only on raw logs or final answer text. The trace should let me determine whether the failure came from retrieval, reranking, context truncation, prompt behavior, model behavior, tool output, schema validation, or stale data. Sensitive content should be redacted or referenced by IDs where possible.

If the issue is real, the trace should be convertible into a regression fixture with a frozen retrieval snapshot, tool mocks, prompt/config versions, expected behavior, and grader.

### Active Recall

1. What is the difference between a trace and a span?
2. Which spans belong in a RAG request?
3. Why should traces include token and cost attributes?
4. How can traces diagnose retrieval vs model failure?
5. How do traces feed eval fixtures?

Final takeaway:

> Distributed tracing is how you stop blaming the model blindly and start seeing the actual system path that produced the answer.

---

## Subtopic P6.3.c: Capacity, Failure Injection, and Chaos Basics for LLM Systems

> **Subtopic time:** 2h
> Outcome: You should be able to estimate capacity, test failure paths intentionally, and explain how chaos drills harden GenAI systems before real incidents do.

### Add to Knowledge Base

Capacity planning asks:

```text
How much work can the system handle before it violates SLOs?
```

Failure injection asks:

```text
What happens when dependencies fail in realistic ways?
```

Chaos testing asks:

```text
Can the system survive controlled failure without surprising us?
```

The mental model:

> Do not discover your overload behavior during the outage.

GenAI systems have expensive and slow dependencies, so capacity and failure testing matter a lot.

---

### 1. Capacity Model

Start with workload:

```text
requests per minute
peak multiplier
input tokens/request
output tokens/request
retrieval calls/request
tool calls/request
stream duration
concurrency target
latency SLO
cost budget
```

Estimate:

```text
active_concurrency ~= arrival_rate_per_second * average_duration_seconds
```

Example:

```text
20 requests/sec
average stream duration 15 sec
active streams ~= 300
```

Then add headroom:

```text
burst headroom
retry overhead
fallback overhead
deploy overlap
provider slowdown
tenant spikes
```

---

### 2. Capacity Is Multi-Layer

Capacity bottlenecks can be:

```text
API connections
event loop lag
gateway throughput
queue workers
vector DB QPS
reranker QPS
provider RPM/TPM
self-hosted GPU tokens/sec
tool service limits
trace store writes
cache throughput
```

The slowest layer defines effective capacity.

If the model provider allows 100 QPS but vector DB handles 20 QPS, the system handles 20 QPS.

---

### 3. Failure Injection Scenarios

Test:

```text
provider returns 429
provider latency doubles
provider stream cuts mid-answer
vector DB times out
reranker returns malformed output
tool service returns 500
cache backend unavailable
trace store slow
queue worker crashes
tenant sends 50x traffic
model output schema invalid
region fails
```

For each scenario, define expected behavior:

```text
fallback
degrade
queue
reject
alert
open circuit
preserve trace
avoid duplicate side effects
```

---

### 4. Chaos Drill Rules

Chaos should be controlled.

Rules:

```text
start in staging
define hypothesis
define blast radius
define stop condition
notify owners
monitor SLOs
record timeline
review results
convert surprises into fixes and runbooks
```

Example hypothesis:

```text
If primary model provider returns 429 for 5 minutes,
the gateway opens circuit within 60 seconds,
low-risk traffic falls back to backup model,
high-risk traffic receives controlled escalation,
and p95 latency stays under 12 seconds for admitted traffic.
```

This is testable.

---

### 5. Game Day Checklist

Before:

```text
choose scenario
define expected system behavior
prepare rollback
confirm observability
notify stakeholders
```

During:

```text
inject failure
watch SLOs
watch circuit breakers
watch queues
watch cost and retries
watch user-visible errors
```

After:

```text
compare expected vs actual
fix gaps
update runbooks
add regression tests
add alerts
repeat later
```

---

### 6. Practical Interview Question

> How would you capacity-test and chaos-test a production GenAI assistant?

### Strong Answer

I would model capacity by traffic shape, not just request count: requests per second, input tokens, output tokens, stream duration, retrieval calls, tool calls, provider RPM/TPM, vector DB QPS, queue workers, and gateway throughput. Active concurrency is roughly arrival rate times duration, so long streaming responses can create hundreds or thousands of active connections.

Then I would run load tests that include realistic prompt lengths, retrieval, reranking, tools, streaming, and tracing. I would measure p95 latency, time to first token, queue age, provider rate limits, error rate, cost per successful task, and quality guardrails.

For chaos testing, I would inject controlled failures: provider 429s, provider latency, vector DB timeout, tool failure, cache outage, malformed model output, and region failover. Each test should have a hypothesis, blast-radius limit, stop condition, SLO monitors, and a postmortem. The goal is to verify that circuit breakers, fallbacks, queues, idempotency, and alerts behave before the real incident.

### Active Recall

1. How do you estimate active streaming concurrency?
2. Why is capacity multi-layer in GenAI systems?
3. Name five failure injection scenarios.
4. What should a chaos test hypothesis include?
5. Why should surprises become runbooks and regression tests?

Final takeaway:

> Capacity and chaos testing turn reliability from hope into evidence. You practice failure so production is not the first rehearsal.

---

## Module P6 Checkpoint: Distributed Systems for GenAI Synthesis

> **Checkpoint focus:** Explain how backpressure and queues protect a GenAI service under spikes, describe what stays stateless and where state must live, and define SLOs plus circuit-breaker behavior for a production GenAI endpoint.

By the end of Pro Module P6, you should be able to:

1. Explain how backpressure and queues protect a GenAI service under spikes.
2. Describe what stays stateless and where state must live, and why.
3. Define SLOs and circuit-breaker behavior for a production GenAI endpoint.

---

### 1. The Big Picture

GenAI distributed systems are difficult because requests are:

```text
slow
expensive
streaming
stateful from the user's point of view
dependent on external providers
dependent on retrieval and tools
quality-sensitive
safety-sensitive
cost-sensitive
```

The architecture must control:

```text
concurrency
queueing
backpressure
timeouts
retries
state placement
tenant isolation
observability
SLOs
failure behavior
```

The checkpoint sentence:

> A serious GenAI system is a distributed workflow around a model, and the workflow needs the same reliability discipline as any production distributed system.

---

### 2. Backpressure and Queues Under Spikes

Spike scenario:

```text
normal traffic: 10 requests/sec
launch traffic: 150 requests/sec
provider limit: 50 requests/sec equivalent
average request duration: 12 seconds
```

Without backpressure:

```text
all requests admitted
queues grow silently
clients time out
clients retry
provider gets hammered
cost spikes
latency explodes
```

With backpressure:

```text
1. Gateway classifies traffic by route, tenant, and priority.
2. Interactive and premium traffic get reserved capacity.
3. Background jobs pause.
4. Queue only admits work that can finish before deadline.
5. Low-risk routes serve cache or cheaper model.
6. Excess low-priority traffic receives retry-after.
7. Worker pools enforce provider concurrency limits.
8. Circuit breaker opens if provider becomes unhealthy.
9. Metrics and alerts fire on queue age, 429 rate, and latency.
```

Core insight:

> Backpressure protects the work you can still serve by refusing or delaying work you cannot serve safely.

---

### 3. What Stays Stateless

Keep stateless:

```text
API handlers
request validation
prompt rendering logic
gateway routing logic
stream forwarding
retrieval orchestration
model call orchestration
```

Stateless means:

```text
instance can die
another instance can serve next request
deploys can roll safely
autoscaling is simple
```

Do not keep durable truth only in process memory.

---

### 4. Where State Lives

| State | Where It Should Live |
|---|---|
| conversation history | session DB |
| recent prompt context | built per request from session store |
| long-term memory | memory store with scope, confidence, TTL, review |
| agent checkpoint | durable checkpoint store |
| async job status | job DB/queue |
| side-effect ledger | strongly consistent DB |
| approvals | strongly consistent workflow store |
| vector embeddings | vector DB/index |
| source documents | document/object store |
| response cache | Redis/object cache with tenant-aware keys |
| semantic cache | vector cache with tenant/permission filters |
| traces | observability/analytics store |
| prompt/model configs | registry/config service |
| budgets/quotas | gateway state store or strongly consistent counter system |

State placement principle:

> Put state where the required lifetime, consistency, access pattern, and privacy boundary are explicit.

---

### 5. SLOs for a Production GenAI Endpoint

Example endpoint:

```text
enterprise support RAG assistant
```

SLO set:

```text
availability:
  99.9% of valid requests return answer or controlled escalation

latency:
  p95 time to first token < 2.5s
  p95 completion < 12s

quality:
  groundedness > 97% on sampled answerable RAG requests
  citation correctness > 99% for cited answers

safety:
  0 critical cross-tenant leaks
  unsafe output rate < 0.1% on sampled traffic

cost:
  p95 cost per successful support task < target

freshness:
  95% of uploaded docs searchable within 2 minutes
```

This is stronger than:

```text
99.9% uptime
```

because GenAI can be available and still wrong, unsafe, slow, or too expensive.

---

### 6. Circuit Breaker Behavior

Circuit breakers should exist for:

```text
model provider
specific model deployment
vector DB
reranker
tool service
cache backend
trace store if it blocks request path
```

Open circuit when:

```text
timeout rate too high
error rate too high
429 rate too high
p95 latency too high
malformed response rate too high
guardrail failure rate too high
```

When open:

```text
low-risk routes:
  fallback model, cache, degraded answer

high-risk routes:
  same-tier fallback, queue, controlled escalation, or fail closed

background jobs:
  pause or reschedule
```

Half-open:

```text
send limited probes
close if healthy
reopen if unhealthy
```

The key:

> Fallback is a policy decision, not just a technical retry.

---

### 7. Production Architecture Scenario

System:

```text
multi-tenant GenAI support assistant
RAG over tenant docs
streaming chat
tool actions for ticket creation
model gateway with provider fallbacks
```

Design:

```text
1. Stateless API tier behind load balancer.
2. Streaming configured with cancellation, heartbeats, and drain behavior.
3. Gateway controls auth, quotas, budgets, routing, fallbacks, and provider limits.
4. Queues separate background embeddings, eval jobs, and long reports from chat.
5. Worker pools enforce bounded concurrency and tenant fairness.
6. Session history lives in durable session DB.
7. Agent checkpoints live in checkpoint store.
8. Tool side effects use idempotency keys and action ledger.
9. Vector DB stores embeddings with tenant and ACL filters.
10. Caches are tenant-aware and permission-aware.
11. Traces span API, gateway, retrieval, tools, model, streaming, and output validation.
12. SLOs cover availability, latency, quality, safety, cost, and freshness.
13. Circuit breakers route or degrade by risk tier.
14. Failure injection tests provider 429s, vector DB timeouts, tool failures, and region failover.
```

---

### 8. Interview-Ready Answer

> Explain how you would design a production GenAI endpoint using distributed-systems principles.

I would start by making the API tier stateless and horizontally scalable. Conversation history, workflow checkpoints, tool action ledgers, memory, cache entries, vector indexes, traces, and config versions should live in external stores with explicit consistency and tenant-isolation guarantees. Active streams may be tied to a server connection, but future turns should be able to land on any instance.

For concurrency, I would use async request handling for I/O-heavy work and configure streaming carefully: long-lived connections, cancellation propagation, flow control, proxy timeouts, and graceful shutdown. I would separate interactive traffic from background embedding, eval, and batch jobs using queues and worker pools. Queues absorb bursts, but backpressure decides what to admit, defer, degrade, or reject when capacity is exhausted.

Timeouts and retries would use propagated deadlines, bounded retry budgets, exponential backoff with jitter, and idempotency keys for side-effecting tools. This prevents retry storms, duplicate actions, and thundering-herd recovery.

Reliability would be defined by SLOs across availability, latency, quality, safety, cost, and freshness. Circuit breakers would monitor model providers, vector DBs, tools, rerankers, and caches. If a dependency is unhealthy, low-risk traffic may use cache or fallback, while high-risk traffic uses same-tier fallback, queueing, escalation, or fail-closed behavior.

Finally, I would use distributed traces across gateway, retrieval, tools, model calls, streaming, caches, and validation so failures can be diagnosed by layer and converted into regression fixtures. Capacity tests and chaos drills would prove the design before production incidents do.

---

### 9. Active Recall

1. Why are queues not enough without backpressure?
2. What is the difference between active stream state and durable session state?
3. Which GenAI states need strong consistency?
4. Why should retries use deadline propagation?
5. How do idempotency keys protect tool actions?
6. What SLOs matter besides uptime?
7. When should a circuit breaker fail closed instead of fallback?
8. What spans should a GenAI distributed trace contain?
9. How do you estimate active streaming concurrency?
10. Why should chaos tests include provider latency and vector DB failures?

---

### 10. Final Checkpoint Summary

- One-line summary: GenAI at scale is a distributed system where slow model calls, streaming, state, retrieval, tools, and cost must be controlled explicitly.
- Three keywords: backpressure, state placement, SLOs.
- One interview trap: saying "we will just autoscale" without explaining queues, provider limits, state, deadlines, and downstream bottlenecks.
- One memory trick: admit work carefully, keep compute stateless, put state in the right store, trace everything, and test failure before failure tests you.

Final takeaway:

> P6 completes the pro track by making the infrastructure layer explicit. You are no longer just building GenAI features; you are operating a distributed system where every prompt, token, queue, retry, cache, store, and fallback affects production behavior.

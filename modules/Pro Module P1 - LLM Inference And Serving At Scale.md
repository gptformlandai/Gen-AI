# Pro Module P1 - LLM Inference And Serving At Scale

> **Module time:** 32h
> **Why this module matters:** You cannot claim "scalable production GenAI" if you only know how to call a hosted API. This module is the difference between renting inference and owning it economically. It is also the single biggest gap in most self-taught GenAI engineers.

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic P1.1** | **Inference fundamentals and GPU economics (10h)** | |
| P1.1.a | The two phases of LLM inference: prefill vs decode, and why they cost differently | Done |
| P1.1.b | GPU memory math: weights, KV cache, activations, and batch size limits | Done |
| P1.1.c | Throughput vs latency vs cost: the inference iron triangle | Done |
| P1.1.d | Hardware mental models: VRAM, memory bandwidth, and what actually bottlenecks | Done |
| **Topic P1.2** | **Serving engines and optimization techniques (12h)** | |
| P1.2.a | vLLM, TGI, and TensorRT-LLM: what they optimize and when to choose each | Done |
| P1.2.b | Continuous (in-flight) batching and paged attention intuition | Done |
| P1.2.c | KV cache management, prefix caching, and reuse | Done |
| P1.2.d | Speculative decoding, chunked prefill, and other latency tricks | Done |
| **Topic P1.3** | **Quantization, parallelism, and capacity planning (10h)** | |
| P1.3.a | Quantization mental models: FP16/BF16, INT8, FP8, GPTQ, AWQ, and quality tradeoffs | Done |
| P1.3.b | Tensor, pipeline, and data parallelism for large models | Done |
| P1.3.c | Autoscaling, cold starts, and warm-pool strategies for GPU services | Done |
| P1.3.d | Capacity planning: tokens/sec targets, concurrency, and headroom | Done |
| **Module checkpoint** | LLM inference and serving at scale synthesis | Done |

**Covered so far:**
- P1.1.a - The two phases of LLM inference: prefill vs decode, and why they cost differently: serving mental model, prompt tokens vs output tokens, autoregressive generation, prefill as prompt processing and KV-cache construction, decode as one-token-at-a-time generation, compute-bound vs memory-bandwidth-bound intuition, time-to-first-token vs inter-token latency, batch behavior, KV-cache growth, prompt length economics, output length economics, throughput metrics, cost model, failure modes, capacity planning implications, code sample, mini simulator, hands-on lab, active recall, and interview-ready answer.
- P1.1.b - GPU memory math: weights, KV cache, activations, and batch size limits: VRAM budget mental model, model weight memory, precision bytes, KV-cache formula, grouped-query attention effect, activation and workspace overhead, fragmentation, max context and max batch interaction, concurrency limits, memory headroom, OOM failure modes, sizing calculator, capacity lab, active recall, and interview-ready memory estimate.
- P1.1.c - Throughput vs latency vs cost: the inference iron triangle: tokens/sec vs user latency distinction, TTFT/ITL/end-to-end latency, utilization economics, batching tradeoffs, queueing, SLA-aware throughput, cost per output token, cost per successful request, workload-shape tradeoffs, decision matrix, simulator, hands-on lab, active recall, and interview-ready tradeoff answer.
- P1.1.d - Hardware mental models: VRAM, memory bandwidth, and what actually bottlenecks: accelerator anatomy, VRAM capacity, HBM bandwidth, compute throughput, tensor cores, PCIe/NVLink, CPU/tokenizer bottlenecks, prefill vs decode hardware pressure, memory-bound decode, network and storage effects, bottleneck diagnosis, profiler mindset, lab, active recall, and interview-ready hardware answer.
- P1.2.a - vLLM, TGI, and TensorRT-LLM: what they optimize and when to choose each: serving-engine comparison, vLLM/PagedAttention/continuous batching strengths, TGI production API and maintenance-mode boundary, TensorRT-LLM/NVIDIA optimization path, OpenAI-compatible serving, hardware lock-in tradeoffs, operational maturity, performance-vs-flexibility matrix, engine-selection checklist, lab, active recall, and interview-ready engine choice.
- P1.2.b - Continuous batching and paged attention intuition: static batching vs dynamic serving, in-flight batching, token-level scheduling, prefill/decode mixing, paged KV memory, block tables, fragmentation reduction, fairness and tail latency, scheduler knobs, failure modes, batching simulator, lab, active recall, and interview-ready explanation.
- P1.2.c - KV cache management, prefix caching, and reuse: KV-cache lifecycle, block allocation, eviction, reuse, prefix hashing, shared system prompts, RAG prefix boundaries, cache correctness, tenant/security constraints, hit-rate metrics, memory tradeoffs, cache invalidation, code sketch, lab, active recall, and interview-ready cache answer.
- P1.2.d - Speculative decoding, chunked prefill, and other latency tricks: target/draft model intuition, acceptance rate, n-gram/EAGLE/Medusa-style families, quality preservation caveats, chunked prefill, disaggregated prefill/decode, CUDA graphs, quantized KV cache, output length control, latency trick decision matrix, simulator, lab, active recall, and interview-ready latency answer.
- P1.3.a - Quantization mental models: FP16/BF16, INT8, FP8, GPTQ, AWQ, and quality tradeoffs: precision-as-compression mental model, weight/activation/KV quantization, post-training quantization, calibration, weight-only vs weight-and-activation, FP8 on modern GPUs, INT4/GPTQ/AWQ tradeoffs, quality risk, eval requirements, memory and throughput impact, quantization decision matrix, lab, active recall, and interview-ready quantization answer.
- P1.3.b - Tensor, pipeline, and data parallelism for large models: model-sharding mental model, tensor parallelism, pipeline parallelism, data parallel replicas, expert/context parallel intuition, communication costs, NVLink vs network constraints, latency impact, throughput scaling, failure modes, parallelism selection matrix, lab, active recall, and interview-ready scaling answer.
- P1.3.c - Autoscaling, cold starts, and warm-pool strategies for GPU services: GPU scaling mental model, cold-start anatomy, model loading, container scheduling, compilation/warmup, scale-to-zero tradeoffs, warm pools, queue-based autoscaling, admission control, overload behavior, multi-tenant fairness, cost controls, lab, active recall, and interview-ready autoscaling answer.
- P1.3.d - Capacity planning: tokens/sec targets, concurrency, and headroom: workload-shape planning, prompt/output token demand, p50/p95 modeling, concurrency estimates, TTFT/ITL targets, GPU count sizing, memory headroom, retry/fallback overhead, utilization targets, burst handling, benchmark plan, capacity calculator, lab, active recall, and interview-ready capacity plan.
- Module checkpoint - LLM inference and serving at scale synthesis: GPU memory estimation, rough throughput planning, prefill/decode workload split, KV-cache capacity, vLLM vs TGI vs hosted API decision defense, continuous batching and paged attention throughput explanation, KV reuse and prefix caching economics, capacity planning worksheet, self-hosted vs hosted tradeoff memo, active recall, and interview-ready serving architecture answer.

---

## Topic P1.1: Inference Fundamentals and GPU Economics

> **Topic time:** 10h
> Focus: Understanding what actually happens when an LLM serves a request, why GPU capacity is consumed differently by prompts and generated tokens, and how this changes latency, throughput, batching, cost, and serving architecture.

LLM inference at scale starts with a mental shift:

```text
Calling a model is easy.
Serving a model efficiently is a scheduling, memory, and economics problem.
```

Hosted APIs hide this machinery.

Self-hosting exposes it:

```text
GPU memory
KV cache
batching
prefill
decode
tokens/sec
time to first token
inter-token latency
queueing
utilization
cost per token
```

The central idea of Topic P1.1:

> LLM serving is not one uniform operation. Prompt processing and token generation stress the GPU differently, so production serving must budget them differently.

---

## Subtopic P1.1.a: The Two Phases of LLM Inference - Prefill vs Decode, and Why They Cost Differently

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain the difference between prefill and decode, why prompt tokens and output tokens have different cost profiles, and how this affects latency, throughput, batching, and capacity planning.

### Add to Knowledge Base

Every LLM request has two major phases:

```text
prefill
decode
```

Prefill processes the input prompt.

Decode generates new tokens.

These sound similar because both run the same transformer layers.

But operationally they behave very differently.

Prefill is like reading the whole question and building working memory.

Decode is like writing the answer one word at a time while repeatedly looking back at that working memory.

The simplest version:

```text
prefill:
  process all prompt tokens
  build KV cache
  produce first next-token distribution

decode:
  generate one token
  append its KV cache
  repeat until stop condition
```

The production-serving version:

```text
prefill mainly affects time to first token and prompt-token throughput.
decode mainly affects inter-token latency, output-token throughput, concurrency, and GPU memory pressure.
```

The core mental model:

> Prefill is parallel prompt processing. Decode is sequential token generation.

That one sentence explains a surprising amount of inference economics.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-7 to understand what prefill and decode are and why output tokens are more operationally painful than they look.
- **Intermediate:** Read sections 8-17 to connect phases to GPU utilization, KV cache, batching, time-to-first-token, inter-token latency, and cost.
- **Pro:** Complete the simulator, capacity lab, active recall, and interview answer.

---

### 0. Pre-Question Hook [Beginner]

A user sends:

```text
prompt: 4,000 tokens
answer: 300 generated tokens
```

Which is more expensive?

The beginner answer:

```text
4,000 prompt tokens, because 4,000 is bigger than 300.
```

The better answer:

```text
It depends what we mean by expensive.
```

The 4,000 prompt tokens create a large prefill workload and a large KV cache.

The 300 output tokens create 300 sequential decode steps.

Each decode step reads from the KV cache and cannot be parallelized over output positions for a single request.

So the prompt may dominate:

```text
time to first token
initial compute spike
KV-cache memory allocation
```

The output may dominate:

```text
ongoing GPU occupancy
inter-token latency
request duration
concurrency pressure
cost of long generations
```

This is why inference pricing often separates:

```text
input tokens
output tokens
```

Output tokens are not just "more tokens."

They are tokens produced on the critical path of autoregressive generation.

---

### 1. The Intuition [Beginner]

Imagine an expert reading a long case file and then dictating an answer.

There are two jobs:

```text
read and understand the file
dictate the answer
```

Reading the file can happen quickly if the expert can scan many pages at once.

Dictating the answer happens one word after another.

Even if the expert is very fast, they cannot say word 300 before word 299 exists.

LLM inference has the same shape.

Prefill:

```text
read the prompt all at once
compute hidden states
store attention memory as KV cache
```

Decode:

```text
generate next token
update KV cache
generate next token
update KV cache
repeat
```

The system bottleneck changes:

```text
prefill likes parallel compute
decode is limited by sequential steps and memory movement
```

That is the heart of the economics.

---

### 2. Definition [Beginner]

- **Prefill phase:** The inference phase that processes the entire input prompt in parallel and creates the initial KV cache for all prompt tokens.
- **Decode phase:** The autoregressive phase that generates output tokens one at a time, reusing the KV cache and appending new keys/values for each generated token.
- **KV cache:** Stored key/value tensors from transformer attention layers that let the model avoid recomputing attention history for previous tokens during decode.
- **TTFT:** Time to first token. Heavily affected by prefill, queueing, and scheduling.
- **ITL:** Inter-token latency. The time between generated tokens during decode.

Crisp definition:

```text
Prefill turns prompt tokens into reusable attention state. Decode consumes that state to generate output tokens sequentially.
```

---

### 3. Why This Exists [Beginner]

Transformer decoders generate text autoregressively.

That means:

```text
token N depends on tokens 1 through N-1
```

During prompt processing, the model already has all input tokens.

It can process those prompt positions together.

During generation, the model does not know future output tokens.

It must generate:

```text
output token 1
then output token 2
then output token 3
...
```

Naive decoding would recompute the entire previous sequence for every new token.

That would be extremely wasteful.

The KV cache exists to avoid that.

Instead of recomputing all prior keys and values, the model stores them once and reuses them.

This improves compute efficiency but creates a new cost:

```text
KV-cache memory grows with sequence length and concurrency.
```

So inference serving becomes a tradeoff:

```text
avoid recomputation
but pay memory
and read that memory repeatedly during decode
```

---

### 4. The Request Timeline [Beginner]

A single request moves like this:

```text
1. Request arrives.
2. Tokenizer converts text to token IDs.
3. Scheduler admits request to a batch.
4. Prefill runs over prompt tokens.
5. KV cache is allocated and filled.
6. Model produces first next-token logits.
7. Sampler picks first output token.
8. Decode loop begins.
9. One token is generated per decode step.
10. KV cache grows by one token each step.
11. Generation stops on max tokens, stop sequence, EOS token, or policy/tool condition.
12. Server returns final or streamed output.
```

Two user-visible latency metrics come from this:

```text
time to first token:
  request arrival -> first streamed token

time to final token:
  request arrival -> completed answer
```

Prefill mostly impacts the first.

Decode mostly impacts the second.

---

### 5. Why Prefill Is Different [Intermediate]

Prefill processes the prompt tokens together.

If the prompt has:

```text
N prompt tokens
```

the model computes transformer layer operations across those N positions in one forward pass.

This gives the GPU more parallel work.

That usually means:

```text
high matrix-multiply utilization
better use of tensor cores
large compute blocks
good throughput when batched
```

But prefill can still be expensive because:

```text
long prompts require many operations
attention over prompt positions is heavy
KV cache must be created for every layer and token
large prompts can delay first token
long prompts consume memory before any output appears
```

Prefill pain shows up as:

```text
slow time to first token
queue delays for long prompts
large initial GPU compute spike
KV-cache allocation pressure
```

Operational phrase:

> Prefill is highly parallel but can be a large upfront bill.

---

### 6. Why Decode Is Different [Intermediate]

Decode generates one new token per sequence per step.

For a single request:

```text
you cannot generate token 50 until token 49 exists
```

That makes decode sequential along time.

At every decode step, the model:

```text
reads the current token
uses cached keys/values for all previous tokens
computes attention for the new query
produces next-token logits
samples or selects the next token
stores new KV cache entry
```

Decode often has less parallel work per request than prefill.

To keep the GPU busy, serving systems batch decode steps across many active requests.

If concurrency is low, decode may underutilize the GPU.

If concurrency is high, KV-cache memory may become the limiting factor.

Decode pain shows up as:

```text
low tokens/sec per request
high inter-token latency
long request duration
KV-cache memory pressure
batch scheduling complexity
```

Operational phrase:

> Decode is sequential per request, so servers need concurrency and batching to make it economical.

---

### 7. Prompt Tokens vs Output Tokens [Beginner]

Prompt tokens and output tokens affect different costs.

Prompt tokens:

```text
increase prefill work
increase TTFT
increase initial KV cache size
increase memory held for the whole generation
```

Output tokens:

```text
increase number of decode steps
increase total request duration
increase GPU occupancy over time
increase KV cache one token at a time
increase user-visible generation time
```

Example:

```text
short prompt, long output:
  small prefill
  long decode
  user sees quick first token but waits for final answer

long prompt, short output:
  heavy prefill
  slow first token
  short decode

long prompt, long output:
  heavy prefill
  large KV cache
  long decode
  expensive request
```

This is why "tokens" are not all operationally equal.

---

### 8. KV Cache: The Bridge Between Prefill and Decode [Intermediate]

KV cache is the memory that connects the two phases.

During prefill:

```text
the model computes keys and values for prompt tokens
stores them per layer
```

During decode:

```text
the model reuses stored keys and values
adds one new key/value per generated token per layer
```

KV cache size grows with:

```text
number of layers
hidden dimension / attention heads
sequence length
number of concurrent sequences
bytes per value
```

Simplified memory intuition:

```text
KV cache memory is proportional to:

batch_size * sequence_length * layers * KV_dimension * bytes
```

This matters because GPU VRAM must hold:

```text
model weights
KV cache
temporary activations
runtime overhead
fragmentation/headroom
```

For serving, the KV cache often becomes the practical limit on:

```text
concurrent users
maximum context length
maximum output length
batch size
```

The model weights may fit.

The workload may not.

---

### 9. Compute-Bound vs Memory-Bandwidth-Bound Intuition [Intermediate]

You will often hear:

```text
prefill is more compute-bound
decode is more memory-bandwidth-bound
```

This is a simplification, but it is useful.

Prefill has large matrix operations over many prompt tokens.

That creates enough arithmetic work to keep GPU compute units busy.

Decode has smaller per-step work for each sequence, but it must repeatedly read model weights and KV cache.

When decode batches are small, the GPU may spend more time moving memory than doing math.

Simple intuition:

```text
prefill:
  many tokens at once
  large GEMMs
  good GPU utilization

decode:
  one token per sequence per step
  repeated memory reads
  needs many concurrent sequences to stay efficient
```

Implication:

```text
a server can have high prefill throughput but still poor decode economics
```

That is why output tokens may be priced higher or capacity-planned more carefully.

---

### 10. Time to First Token vs Inter-Token Latency [Intermediate]

Two user-visible metrics:

```text
TTFT = time to first token
ITL = inter-token latency
```

TTFT includes:

```text
queueing
tokenization
scheduling
prefill
first decode step
```

ITL includes:

```text
decode scheduling
one-token forward pass
sampling
streaming overhead
```

Bad TTFT feels like:

```text
the assistant is thinking forever before responding
```

Bad ITL feels like:

```text
the assistant starts, then crawls token by token
```

Optimization differs:

```text
TTFT optimization:
  reduce prompt length
  use prefix caching
  schedule prefill carefully
  chunk prefill
  reduce queueing

ITL optimization:
  improve decode batching
  reduce output length
  use faster model/quantization
  optimize KV cache
  speculative decoding
```

Do not optimize only total latency.

Users experience the shape of latency.

---

### 11. Batching Behavior [Intermediate]

Batching means running multiple requests together.

Prefill batching:

```text
group prompt-processing work
improves GPU utilization
but long prompts can block short ones if scheduling is naive
```

Decode batching:

```text
group one decode step from many active sequences
keeps GPU busy
but active sequences have different lengths and finish at different times
```

The challenge:

```text
prefill work is chunky
decode work is continuous
requests arrive at different times
prompts have different lengths
outputs have different lengths
```

Serving engines optimize this with techniques such as:

```text
continuous batching
in-flight batching
paged attention
chunked prefill
KV-cache block management
```

You will study these later in P1.2.

For now, know the reason they exist:

> Production LLM serving is mostly the art of mixing prefill and decode work so expensive GPUs stay useful without destroying user latency.

---

### 12. Why Output Tokens Often Feel More Expensive [Intermediate]

A common surprise:

```text
output tokens may be more expensive than input tokens
```

Reasons:

1. Decode is sequential for each request.
2. Each output token requires another model forward step.
3. Long outputs keep KV cache alive longer.
4. Long outputs occupy scheduler capacity longer.
5. Decode throughput depends heavily on batching active sequences.
6. Output length is less predictable than prompt length.
7. Output tokens directly extend user wait time.

Prompt tokens are expensive too, especially for long context.

But prompts are processed in a large parallel prefill.

Output tokens are produced one step at a time.

That is why a request with:

```text
1,000 input tokens and 2,000 output tokens
```

can be much harder to serve than:

```text
2,000 input tokens and 100 output tokens
```

even though both have similar total token counts.

---

### 13. Cost Model: What You Should Estimate [Intermediate]

For a rough serving estimate, track:

```text
input tokens
output tokens
concurrent requests
average prompt length
average output length
p95 prompt length
p95 output length
time to first token target
tokens/sec target
GPU hourly cost
GPU memory
model size
KV cache memory per token
utilization
```

Request-level rough cost:

```text
request cost =
  prefill cost for input tokens
  + decode cost for output tokens
  + queueing/utilization overhead
  + serving/runtime overhead
```

Capacity-level rough cost:

```text
monthly cost =
  GPU hourly cost
  * number of GPUs
  * hours running
  / useful utilization
```

Economics question:

```text
Are we paying for idle GPU time, decode bottlenecks, oversized prompts, or long generations?
```

This is why self-hosted inference is not automatically cheaper.

It is cheaper only when workload shape, utilization, and operations justify it.

---

### 14. Serving Metrics You Must Know [Intermediate]

Track these separately:

| Metric | What It Tells You |
|---|---|
| prompt tokens/sec | prefill throughput |
| output tokens/sec | decode throughput |
| TTFT | prefill + queueing user experience |
| ITL | decode smoothness |
| end-to-end latency | total user wait |
| active sequences | current decode concurrency |
| KV-cache usage | memory pressure |
| batch size | scheduler efficiency |
| queue time | overload or scheduling delay |
| GPU utilization | whether hardware is busy |
| memory bandwidth utilization | whether decode is memory-limited |
| request throughput | requests/sec |
| cost per 1K tokens | token economics |
| cost per successful request | product economics |

If someone says:

```text
our model does 10,000 tokens/sec
```

ask:

```text
prompt tokens or output tokens?
batch size?
context length?
latency target?
model size?
hardware?
concurrency?
```

Tokens/sec without workload shape is incomplete.

---

### 15. Practical Examples [Intermediate]

#### Example A: Long Prompt, Short Answer

```text
prompt: 12,000 tokens
output: 100 tokens
```

Likely issue:

```text
slow TTFT
large KV cache
prefill dominates
```

Optimization:

```text
better retrieval/context selection
context compression
prefix caching
chunked prefill
smaller prompt
```

#### Example B: Short Prompt, Long Answer

```text
prompt: 300 tokens
output: 2,000 tokens
```

Likely issue:

```text
long decode
high total latency
capacity tied up
output token cost dominates
```

Optimization:

```text
shorter answer policy
streaming
max token limits
structured concise output
faster decode engine
speculative decoding
```

#### Example C: Many Users, Medium Prompts

```text
prompt: 1,500 tokens average
output: 250 tokens average
concurrency: high
```

Likely issue:

```text
scheduler quality
KV-cache memory
decode batching
queueing
```

Optimization:

```text
continuous batching
right max batch limits
KV-cache paging
autoscaling
admission control
```

---

### 16. Common Misunderstandings [Intermediate]

| Misunderstanding | Why It Is Wrong | Better Mental Model |
|---|---|---|
| total tokens are all that matter | input/output tokens stress serving differently | separate prefill and decode |
| model fits in VRAM, so workload fits | KV cache and concurrency also need VRAM | weights + KV cache + overhead |
| more batching always helps | batching can hurt latency | batch within SLA |
| output tokens are cheap because there are fewer | decode is sequential and holds resources | output tokens drive duration |
| long context is free if model supports it | prefill and KV memory grow | context length is capacity cost |
| self-hosting is always cheaper | idle GPUs and ops cost matter | compare utilization and workload |
| fast first token means fast request | decode can still be slow | track TTFT and ITL separately |
| average latency is enough | tail latency hurts users | track p95/p99 |

---

### 17. Failure Modes [Intermediate]

| Failure Mode | User/System Symptom | Likely Root Cause | Mitigation |
|---|---|---|---|
| slow first token | user waits before stream starts | long prefill, queueing, long prompt | reduce context, prefix cache, prefill scheduling |
| slow streaming | tokens arrive slowly | decode bottleneck | improve batching, reduce output, faster model |
| OOM at concurrency | server crashes or rejects requests | KV cache too large | lower max context/output, improve KV management |
| high GPU cost | cost/request too high | low utilization or long decode | batching, routing, output caps, autoscaling |
| short prompts delayed | small jobs wait behind long prompts | naive scheduling | separate queues or chunked prefill |
| unstable latency | p99 spikes | variable prompt/output lengths | admission control and workload shaping |
| poor throughput | GPU underused | low decode concurrency | continuous batching or aggregate traffic |
| quality drops after optimization | faster route loses capability | unsafe model/quantization choice | eval gates and task-tier routing |

---

### 18. Code Sample: Split Request Cost Into Prefill and Decode [Pro]

This sample is not a hardware benchmark.

It is a mental-model calculator.

```python
from dataclasses import dataclass


@dataclass
class RequestShape:
    input_tokens: int
    output_tokens: int


@dataclass
class ServingAssumption:
    prefill_tokens_per_second: float
    decode_tokens_per_second_per_sequence: float
    queue_ms: int = 0


def estimate_latency_ms(shape: RequestShape, serving: ServingAssumption) -> dict[str, float]:
    prefill_ms = shape.input_tokens / serving.prefill_tokens_per_second * 1000
    decode_ms = shape.output_tokens / serving.decode_tokens_per_second_per_sequence * 1000
    total_ms = serving.queue_ms + prefill_ms + decode_ms
    return {
        "queue_ms": serving.queue_ms,
        "prefill_ms": round(prefill_ms, 1),
        "decode_ms": round(decode_ms, 1),
        "total_ms": round(total_ms, 1),
    }


def main() -> None:
    serving = ServingAssumption(
        prefill_tokens_per_second=20_000,
        decode_tokens_per_second_per_sequence=45,
        queue_ms=150,
    )

    examples = {
        "long_prompt_short_answer": RequestShape(12_000, 100),
        "short_prompt_long_answer": RequestShape(300, 2_000),
        "medium_rag_answer": RequestShape(2_500, 350),
    }

    for name, shape in examples.items():
        print(name, estimate_latency_ms(shape, serving))


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
The long prompt hurts prefill and TTFT.
The long answer hurts decode and total latency.
They are different operational problems.
```

---

### 19. Mini Program: Prefill vs Decode Workload Simulator [Pro]

This simulator classifies workload pressure.

```python
from dataclasses import dataclass


@dataclass
class Workload:
    name: str
    requests_per_minute: int
    avg_input_tokens: int
    avg_output_tokens: int


def analyze(workload: Workload) -> dict[str, float | str]:
    prompt_tokens_per_min = workload.requests_per_minute * workload.avg_input_tokens
    output_tokens_per_min = workload.requests_per_minute * workload.avg_output_tokens

    if workload.avg_input_tokens > workload.avg_output_tokens * 4:
        pressure = "prefill-heavy"
    elif workload.avg_output_tokens > workload.avg_input_tokens:
        pressure = "decode-heavy"
    else:
        pressure = "balanced"

    return {
        "prompt_tokens_per_min": prompt_tokens_per_min,
        "output_tokens_per_min": output_tokens_per_min,
        "pressure": pressure,
    }


def main() -> None:
    workloads = [
        Workload("customer_support_rag", 600, 2500, 250),
        Workload("essay_generation", 120, 500, 1800),
        Workload("chatbot_smalltalk", 3000, 200, 80),
        Workload("contract_qa", 90, 12000, 300),
    ]

    for workload in workloads:
        print(workload.name, analyze(workload))


if __name__ == "__main__":
    main()
```

What to notice:

```text
Different products stress different inference phases.
Serving architecture should match workload shape.
```

---

### 20. Hands-On Lab: Analyze a Serving Workload [Pro]

Pick one product:

```text
RAG support assistant
coding assistant
legal document Q&A
long-form writing assistant
agentic workflow assistant
```

#### Step 1: Estimate Workload Shape

Write:

```text
requests per minute
p50 input tokens
p95 input tokens
p50 output tokens
p95 output tokens
concurrent users
latency SLO
streaming or non-streaming
```

#### Step 2: Classify Phase Pressure

Decide:

```text
prefill-heavy
decode-heavy
balanced
```

Explain why.

#### Step 3: Identify Bottlenecks

For prefill-heavy:

```text
long contexts
slow TTFT
KV-cache allocation
large prompt-token volume
```

For decode-heavy:

```text
long outputs
slow ITL
long GPU occupancy
high output-token cost
```

For balanced:

```text
scheduler design
batching
KV memory
autoscaling
```

#### Step 4: Choose Optimizations

Map:

```text
long prompt -> retrieval pruning / context compression / prefix caching
slow decode -> output limits / faster model / speculative decoding
low utilization -> batching / traffic aggregation
OOM -> shorter context/output / quantization / smaller model
tail latency -> admission control / separate queues
```

#### Step 5: Write the Capacity Statement

Template:

```text
This workload is <prefill-heavy/decode-heavy/balanced>.
The main user-facing metric is <TTFT/ITL/end-to-end>.
The main GPU bottleneck is likely <compute/KV memory/memory bandwidth/scheduler>.
I would first optimize <choice> because <reason>.
I would measure <metrics> before changing architecture.
```

---

### 21. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| treating input and output tokens equally | they map to different phases | model prefill and decode separately |
| optimizing total latency only | hides TTFT vs ITL pain | track both |
| ignoring output length | decode dominates long generations | cap, stream, or route long outputs |
| ignoring prompt length | prefill dominates long RAG/context | prune and compress context |
| assuming high tokens/sec means good UX | throughput may require huge batches | compare with latency SLO |
| assuming model-fit means serving-fit | KV cache limits concurrency | include KV cache in memory math |
| no workload distribution | p95 may be very different from average | measure p50/p95/p99 tokens |
| comparing hosted vs self-hosted by list price | utilization and ops matter | compare cost per successful task |
| one queue for all requests | long prompts block short ones | workload-aware scheduling |
| no admission control | overload causes tail latency/OOM | enforce max context/output/concurrency |

---

### 22. Practical Interview Question [Intermediate]

> You are serving an open-weight chat model. Users send long RAG prompts and expect streamed answers. Explain prefill vs decode, which metrics you would track, and how this affects cost and capacity planning.

---

### 23. Strong Answer [Pro]

LLM inference has two main phases: prefill and decode. In prefill, the server processes the input prompt tokens and builds the KV cache for those tokens. This phase is highly parallel and often uses GPU compute efficiently, but long prompts create a large upfront cost and increase time to first token. In decode, the model generates output tokens autoregressively, one token at a time. Each decode step reuses the KV cache and appends a new entry, so decode is sequential per request and often limited by memory bandwidth and batching efficiency.

For a RAG workload, long retrieved context usually makes prefill important. If users complain that the assistant takes too long to start streaming, I would inspect time to first token, prompt length distribution, prefill tokens/sec, queue time, and KV-cache allocation. I would optimize by reducing unnecessary context, improving retrieval selection, using prefix caching where prompts share common prefixes, and using scheduling techniques such as chunked prefill if the serving engine supports it.

For streamed answers, decode determines how fast tokens arrive after generation starts. I would track inter-token latency, output tokens/sec, active sequences, batch size, GPU utilization, KV-cache usage, and p95/p99 generation latency. If output generations are long, they keep GPU resources and KV cache occupied, so output length can dominate capacity and cost even if prompt length is moderate.

The economic point is that input and output tokens are not operationally identical. Input tokens primarily drive prefill work and KV-cache allocation, while output tokens drive repeated decode steps and request duration. For capacity planning, I would separately estimate prompt-token throughput, output-token throughput, average and p95 sequence lengths, concurrency, memory headroom, and cost per successful request. I would not compare serving options using only total tokens/sec because workload shape, latency SLO, and context/output distribution determine real capacity.

---

### 24. Active Recall [Beginner]

Answer these without looking:

1. What are the two phases of LLM inference?
2. What happens during prefill?
3. What happens during decode?
4. Why can prompt tokens be processed in parallel?
5. Why must output tokens be generated sequentially?
6. What is KV cache?
7. Why does KV cache help decode?
8. Why does KV cache create memory pressure?
9. What is TTFT?
10. What is ITL?
11. Which phase mostly affects TTFT?
12. Which phase mostly affects ITL?
13. Why can output tokens be more operationally expensive?
14. Why can long prompts still be expensive?
15. What does "prefill is more compute-bound" roughly mean?
16. What does "decode is more memory-bandwidth-bound" roughly mean?
17. Why does batching matter for decode?
18. Why is total tokens/sec an incomplete serving metric?
19. What workload is prefill-heavy?
20. What workload is decode-heavy?
21. What metrics should you track for serving?
22. Why is self-hosting not automatically cheaper?
23. What is the first optimization for long RAG prompts?
24. What is the first optimization for long generated answers?
25. What is the final lesson of this subtopic?

Expected answers:

1. Prefill and decode.
2. The model processes the prompt and builds KV cache.
3. The model generates output tokens one at a time.
4. The full prompt is already known.
5. Each generated token depends on previous generated tokens.
6. Stored attention keys and values for previous tokens.
7. It avoids recomputing prior attention state.
8. It grows with sequence length, layers, and concurrency.
9. Time to first token.
10. Inter-token latency.
11. Prefill and queueing.
12. Decode.
13. They require sequential decode steps and keep resources occupied.
14. They create upfront compute and large KV cache.
15. Prefill has large parallel matrix operations.
16. Decode repeatedly reads weights/KV cache with less per-request parallelism.
17. Many active sequences are needed to keep GPU busy.
18. It hides prompt/output split, batch size, latency, context, and hardware.
19. Long prompts with short outputs, such as large-context RAG.
20. Short prompts with long outputs, such as essay generation.
21. TTFT, ITL, prompt tokens/sec, output tokens/sec, queue time, KV usage, GPU utilization.
22. Idle GPUs, poor utilization, ops cost, and workload mismatch can erase savings.
23. Reduce/prune/compress context or use prefix caching.
24. Cap/structure output, stream, use faster decode route, or speculative decoding.
25. Prefill and decode are different economic phases, so serving must budget them separately.

---

### 25. Revision Notes

- **One-line summary:** Prefill processes the known prompt in parallel and builds KV cache; decode generates one token at a time and often dominates output latency and serving economics.
- **Three keywords:** prefill, decode, KV cache.
- **One interview trap:** Saying "the request has 5,000 tokens" without separating input tokens, output tokens, TTFT, ITL, and KV-cache memory.
- **One memory trick:** Prefill reads the case file; decode dictates the answer word by word.

Final takeaway:

> Scalable LLM serving begins when you stop treating inference as one blob and start budgeting prefill, decode, KV cache, TTFT, ITL, throughput, and GPU memory as separate but connected constraints.

---

## Subtopic P1.1.b: GPU Memory Math - Weights, KV Cache, Activations, and Batch Size Limits

> **Subtopic time:** 2.5h
> Outcome: You should be able to estimate why a model fits or does not fit on a GPU, how KV cache limits concurrency, and why "the weights fit" is not the same as "the serving workload fits."

### Add to Knowledge Base

GPU serving capacity starts with a simple VRAM budget:

```text
available VRAM
  = model weights
  + KV cache
  + activations / temporary buffers
  + runtime overhead
  + fragmentation and safety headroom
```

The beginner mistake is:

```text
model has 7B parameters
7B * 2 bytes = 14 GB
therefore a 16 GB GPU can serve it
```

The production answer is:

```text
Maybe it can load.
But serving also needs KV cache, workspaces, kernels, tokenizer/runtime overhead, batching headroom, and memory fragmentation tolerance.
```

The central mental model:

> Model weights decide whether the model can load. KV cache decides how many users and tokens it can serve.

---

### 1. The Memory Buckets [Beginner]

| Bucket | What It Means | Scales With |
|---|---|---|
| weights | model parameters | parameter count and precision |
| KV cache | attention history for active sequences | batch, layers, sequence length, KV heads, head dim, precision |
| activations | temporary tensors during forward pass | batch, sequence length, hidden size, kernels |
| workspace | engine/runtime scratch memory | backend, kernels, compilation choices |
| overhead | framework, CUDA context, fragmentation | runtime and configuration |

For inference, gradients and optimizer state are usually absent.

That is why inference memory is far smaller than training memory.

But KV cache can become enormous at high concurrency or long context.

---

### 2. Weight Memory [Beginner]

Approximate weight memory:

```text
weight_memory_bytes = parameter_count * bytes_per_parameter
```

Common precision sizes:

| Precision | Approx Bytes / Parameter | Notes |
|---|---:|---|
| FP32 | 4 | rarely used for LLM serving |
| FP16 | 2 | common inference baseline |
| BF16 | 2 | common on modern accelerators |
| FP8 | 1 | supported on newer hardware/workflows |
| INT8 | 1 | quantized inference |
| INT4 | 0.5 | aggressive quantization |

Examples:

```text
7B params at FP16:
  7B * 2 bytes = about 14 GB

13B params at FP16:
  about 26 GB

70B params at FP16:
  about 140 GB
```

This is only weights.

Serving needs more memory.

---

### 3. KV Cache Formula [Intermediate]

For decoder-only transformers, a useful approximate KV cache formula is:

```text
KV cache bytes =
  batch_size
  * sequence_length
  * num_layers
  * 2
  * num_kv_heads
  * head_dim
  * bytes_per_kv_value
```

Why `2`?

```text
one tensor for keys
one tensor for values
```

What counts as sequence length?

```text
prompt tokens + generated tokens so far
```

This means long outputs keep growing KV cache.

This also means long prompts consume KV memory before output begins.

---

### 4. GQA and MQA Matter [Intermediate]

Modern models often use:

```text
MHA: multi-head attention
GQA: grouped-query attention
MQA: multi-query attention
```

The key serving effect:

```text
KV cache depends on KV heads, not always query heads.
```

GQA/MQA reduce KV-cache memory because multiple query heads share fewer key/value heads.

Two models with similar parameter counts can have different KV-cache economics.

When estimating memory, do not only ask:

```text
How many parameters?
```

Ask:

```text
How many layers?
How many KV heads?
What head dimension?
What max context?
What KV precision?
```

---

### 5. Batch Size Limits [Intermediate]

Batch size in LLM serving is not a fixed number like image classification.

It depends on active tokens.

Approximate serving constraint:

```text
available KV memory
  >= sum(sequence_length for active requests) * KV bytes per token
```

This means:

```text
10 users with 1,000-token contexts
```

may be easier than:

```text
2 users with 100,000-token contexts
```

Batch is limited by:

```text
VRAM capacity
KV-cache block management
max context length
output length
scheduler policy
latency SLO
fragmentation
```

The real question is not:

```text
What batch size fits?
```

The real question is:

```text
How many active tokens can I hold while meeting latency?
```

---

### 6. Activations and Workspace [Intermediate]

During inference, activation memory is smaller than training but not zero.

Prefill can use more temporary memory because it processes many prompt tokens together.

Decode usually has smaller activations per step but keeps KV cache alive.

Runtime overhead can include:

```text
CUDA context
compiled kernels
attention workspaces
sampling buffers
communication buffers
graph capture memory
framework allocator reservations
```

Practical rule:

```text
Do not allocate 100 percent of VRAM on paper.
Keep headroom.
```

Common planning headroom:

```text
10 to 20 percent minimum
more when workloads are spiky or engine behavior is unknown
```

---

### 7. Quick Estimate Example [Pro]

Suppose:

```text
model: 7B
precision: FP16
GPU: 24 GB
weights: about 14 GB
runtime/headroom: 3 GB
available for KV: about 7 GB
```

If KV cache costs roughly:

```text
0.5 MB per token
```

then total active tokens:

```text
7 GB / 0.5 MB = about 14,000 active tokens
```

That active-token pool could be:

```text
14 users * 1,000 tokens
7 users * 2,000 tokens
2 users * 7,000 tokens
1 user * 14,000 tokens
```

This is why context length and concurrency are tied together.

These numbers are illustrative. Use model-specific architecture for real sizing.

---

### 8. Failure Modes

| Failure Mode | Symptom | Root Cause | Fix |
|---|---|---|---|
| model loads but OOMs under traffic | crashes during generation | KV cache grows beyond budget | reduce context/output/concurrency |
| long prompts starve users | high TTFT and queueing | prefill memory/compute pressure | context pruning, chunked prefill |
| batch size lower than expected | poor throughput | KV memory or fragmentation | paged KV, lower max tokens |
| works in dev, fails in prod | variable p95 lengths | tested average only | plan for p95/p99 token lengths |
| high latency after memory pressure | scheduler thrashing | over-admission | admission control and headroom |

---

### 9. Code Sample: Rough VRAM Budget Calculator

```python
from dataclasses import dataclass


@dataclass
class ModelSpec:
    params_billion: float
    layers: int
    kv_heads: int
    head_dim: int
    weight_bytes: float
    kv_bytes: float


def weight_gb(spec: ModelSpec) -> float:
    return spec.params_billion * 1_000_000_000 * spec.weight_bytes / 1e9


def kv_bytes_per_token(spec: ModelSpec) -> int:
    return int(spec.layers * 2 * spec.kv_heads * spec.head_dim * spec.kv_bytes)


def max_active_tokens(vram_gb: float, spec: ModelSpec, overhead_gb: float) -> int:
    remaining_bytes = (vram_gb - weight_gb(spec) - overhead_gb) * 1e9
    return max(0, int(remaining_bytes / kv_bytes_per_token(spec)))


def main() -> None:
    llama_like_7b = ModelSpec(
        params_billion=7,
        layers=32,
        kv_heads=8,
        head_dim=128,
        weight_bytes=2,
        kv_bytes=2,
    )

    print("weights_gb:", round(weight_gb(llama_like_7b), 2))
    print("kv_bytes_per_token:", kv_bytes_per_token(llama_like_7b))
    print("active_tokens_on_24gb:", max_active_tokens(24, llama_like_7b, overhead_gb=3))


if __name__ == "__main__":
    main()
```

Use this as a thinking tool, not a benchmark.

Real serving also depends on backend, kernels, fragmentation, batch policy, quantization, and hardware.

---

### 10. Practical Interview Question

> A 7B model in FP16 has roughly 14 GB of weights. Can we serve it on a 24 GB GPU for a chat workload with 8K context and many concurrent users?

### Strong Answer

Maybe, but the weights fitting is only the first check. I would budget VRAM for weights, KV cache, activations, runtime overhead, and headroom. The 14 GB weights leave about 10 GB before overhead. After runtime and safety headroom, the remaining memory must hold KV cache for all active sequences. KV cache scales with layers, KV heads, head dimension, precision, sequence length, and concurrency. An 8K context at multiple concurrent users can consume memory quickly, especially if outputs are long. I would estimate KV bytes per token, multiply by total active tokens, reserve headroom, then benchmark p50 and p95 prompt/output distributions. If memory is tight, I would reduce max context, use quantization, lower max output tokens, use paged KV, or choose a larger GPU.

### Active Recall

1. What are the main VRAM buckets during inference?
2. Why is "weights fit" not enough?
3. What variables control KV-cache memory?
4. Why does GQA reduce KV-cache pressure?
5. Why does batch size depend on sequence length?
6. What causes OOM during decode?
7. Why should you keep memory headroom?
8. What is the first thing to check when concurrency is lower than expected?

Final takeaway:

> GPU serving memory is a dynamic budget: weights load the model, KV cache holds active history, and the practical batch limit is the number of active tokens you can keep in VRAM while preserving latency headroom.

---

## Subtopic P1.1.c: Throughput vs Latency vs Cost - The Inference Iron Triangle

> **Subtopic time:** 2.5h
> Outcome: You should be able to reason about serving tradeoffs using throughput, latency, and cost together, instead of optimizing a single metric in isolation.

### Add to Knowledge Base

Inference serving is governed by an iron triangle:

```text
throughput
latency
cost
```

You can often improve one by hurting another.

Examples:

```text
larger batches -> better throughput and lower cost per token, but worse latency
smaller batches -> better latency, but worse GPU utilization
larger model -> better quality, but higher latency and cost
quantized model -> lower cost and memory, possible quality risk
more retries -> better success rate, worse latency and cost
more GPUs -> better capacity, higher fixed cost
```

The central mental model:

> Throughput is how much work the system completes. Latency is how long one user waits. Cost is what you pay to achieve both at a target quality.

---

### 1. Definitions

| Metric | Meaning |
|---|---|
| throughput | requests/sec or tokens/sec served |
| latency | time a request takes |
| TTFT | time to first token |
| ITL | time between output tokens |
| p95 latency | 95 percent of requests finish faster than this |
| utilization | how busy the GPU is |
| cost/request | infrastructure spend per request |
| cost/success | spend per completed useful task |

Throughput without latency is incomplete.

Latency without cost is incomplete.

Cost without quality is incomplete.

---

### 2. Why Batching Creates the Tradeoff

GPU inference wants big batches.

Users want fast responses.

Batching improves:

```text
GPU utilization
tokens/sec
cost per token
```

Batching can hurt:

```text
queue time
TTFT
p95 latency
fairness for short requests
```

The production question:

```text
How much batching can we use before violating user latency SLO?
```

This is why serving systems tune:

```text
max batch tokens
max waiting time
prefill/decode scheduling
admission control
separate queues
```

---

### 3. Cost Is Utilization Times Hardware Price

Self-hosted cost depends heavily on utilization.

If a GPU costs:

```text
$X per hour
```

and it is only productively used 20 percent of the time, effective cost per useful token is much higher.

Hosted APIs charge mostly per token.

Self-hosted GPUs charge mostly per time.

So the economic question changes:

```text
hosted API:
  How many tokens did I use?

self-hosted:
  How many GPUs did I keep running, and how well did I use them?
```

Self-hosting wins when:

```text
traffic is steady enough
utilization is high
model/quality needs are stable
ops cost is justified
latency/control requirements matter
```

Hosted wins when:

```text
traffic is bursty
ops team is small
model quality changes often
utilization would be low
time-to-market matters more than unit economics
```

---

### 4. Workload Shape Changes the Triangle

| Workload | Main Pressure |
|---|---|
| long-context RAG | prefill, KV memory, TTFT |
| long-form generation | decode, ITL, output-token cost |
| short classification | overhead, batching, request/sec |
| agent workflow | many small model/tool calls, tail latency |
| batch summarization | throughput and cost, latency relaxed |
| realtime chat | TTFT and ITL, stricter latency |

Never compare systems with only:

```text
tokens/sec
```

Ask:

```text
at what input/output length?
at what concurrency?
at what p95 latency?
at what cost?
at what quality?
```

---

### 5. Decision Matrix

| Goal | Likely Move | Tradeoff |
|---|---|---|
| lower TTFT | reduce prompt, prefix cache, prefill scheduling | may reduce context |
| lower ITL | faster model, quantization, speculative decode | possible quality/complexity risk |
| higher throughput | larger batches, continuous batching | p95 latency may rise |
| lower cost | higher utilization, smaller/quantized model | quality or latency may suffer |
| better quality | larger model, more retrieval, rerank | cost and latency rise |
| fewer timeouts | more GPUs/headroom | fixed cost rises |
| lower tail latency | admission control, separate queues | lower peak utilization |

---

### 6. Code Sample: Throughput/Latency/Cost Tradeoff Sketch

```python
from dataclasses import dataclass


@dataclass
class ServingConfig:
    name: str
    batch_size: int
    tokens_per_second: int
    p95_latency_ms: int
    gpu_hourly_cost: float


def cost_per_million_tokens(config: ServingConfig) -> float:
    tokens_per_hour = config.tokens_per_second * 3600
    return config.gpu_hourly_cost / tokens_per_hour * 1_000_000


def main() -> None:
    configs = [
        ServingConfig("low_latency", 4, 1200, 900, 3.0),
        ServingConfig("balanced", 16, 3000, 1800, 3.0),
        ServingConfig("throughput", 64, 5200, 4200, 3.0),
    ]

    for config in configs:
        print(config.name, round(cost_per_million_tokens(config), 3), "usd / 1M tokens")


if __name__ == "__main__":
    main()
```

This shows the shape:

```text
throughput mode can be cheaper per token
but may be unacceptable for interactive latency
```

---

### 7. Practical Interview Question

> Your team wants to increase batch size because GPU utilization is low, but product complains about latency. How do you reason about it?

### Strong Answer

I would separate throughput from user latency. Larger batches can increase tokens/sec and reduce cost per token, but they may add queue time and worsen TTFT or p95 latency. I would start from the product SLO: p95 TTFT, p95 end-to-end latency, and target cost per successful request. Then I would benchmark batch sizes with realistic prompt/output distributions. If utilization is low but latency is strict, I might use continuous batching, shorter max queue delay, separate queues for short and long prompts, prefix caching, or autoscaling rather than simply increasing batch size. The right batch size is not the one with maximum throughput; it is the one that meets latency and quality targets at acceptable cost.

### Active Recall

1. What are the three sides of the inference iron triangle?
2. Why does batching reduce cost per token?
3. Why can batching hurt latency?
4. Why is utilization central to self-hosting economics?
5. Why is cost per successful task better than cost per request?
6. What workload is throughput-optimized?
7. What workload is latency-optimized?
8. What question should you ask after hearing "tokens/sec"?

Final takeaway:

> Inference serving is an optimization problem under constraints: maximize useful throughput only while meeting latency SLO, quality threshold, and cost budget.

---

## Subtopic P1.1.d: Hardware Mental Models - VRAM, Memory Bandwidth, and What Actually Bottlenecks

> **Subtopic time:** 2.5h
> Outcome: You should be able to look at an LLM serving workload and reason whether it is constrained by VRAM capacity, memory bandwidth, compute, interconnect, CPU overhead, storage, or scheduling.

### Add to Knowledge Base

An inference GPU is not just "a faster CPU."

It is a package of constraints:

```text
VRAM capacity
HBM memory bandwidth
compute throughput
tensor cores
interconnect
kernel efficiency
power limits
```

The central mental model:

> VRAM decides what fits. Memory bandwidth decides how fast decode can move data. Compute decides how fast large matrix work can run. Interconnect decides how painful multi-GPU serving becomes.

---

### 1. Hardware Buckets

| Component | What It Controls |
|---|---|
| VRAM capacity | model size, KV cache, batch/concurrency |
| HBM bandwidth | weight/KV reads, especially decode |
| compute/Tensor Cores | matmul-heavy prefill and large batches |
| PCIe | CPU-GPU transfer, weaker multi-GPU path |
| NVLink/NVSwitch | high-bandwidth GPU-GPU communication |
| CPU | tokenization, request handling, sampling overhead |
| storage/network | model loading, distributed serving, data movement |

Different bottlenecks require different fixes.

---

### 2. Prefill vs Decode Hardware Pressure

Prefill:

```text
large parallel matrix operations
often benefits from compute throughput
long prompts can stress memory and temporary buffers
```

Decode:

```text
small repeated steps
reads weights and KV cache repeatedly
often constrained by memory bandwidth
needs batching to improve utilization
```

If prefill is slow:

```text
reduce prompt tokens
improve batching
use optimized kernels
use chunked prefill
use stronger compute hardware
```

If decode is slow:

```text
increase decode batching
use faster/quantized model
optimize KV cache
use speculative decoding
reduce output length
use hardware with higher memory bandwidth
```

---

### 3. VRAM Capacity Bottleneck

Symptoms:

```text
OOM
low max concurrency
cannot support long context
batch size capped
frequent request rejection
```

Fixes:

```text
quantize weights
quantize KV cache
reduce max context
reduce max output
use GQA/MQA models
improve paged KV management
use tensor parallelism
move to larger VRAM GPU
```

Capacity bottlenecks are about fitting.

Bandwidth bottlenecks are about speed.

---

### 4. Memory Bandwidth Bottleneck

Symptoms:

```text
GPU compute utilization low
decode tokens/sec poor
adding compute does not help much
larger batches improve efficiency until memory saturates
```

Why:

```text
decode repeatedly streams model weights and KV cache
the GPU waits on memory movement
```

Fixes:

```text
quantization to reduce bytes moved
KV-cache optimization
better batching
fused kernels
speculative decoding
hardware with higher HBM bandwidth
```

---

### 5. Compute Bottleneck

Symptoms:

```text
prefill is slow
large batch GEMMs saturate compute
GPU utilization high during prompt processing
```

Fixes:

```text
use optimized kernels
use tensor cores effectively
use lower precision
use a smaller model
use more GPUs
reduce prompt/context length
```

Compute bottlenecks often appear in prefill-heavy workloads or very large batches.

---

### 6. Interconnect Bottleneck

Multi-GPU serving introduces communication.

Tensor parallelism may require:

```text
all-reduce
all-gather
activation movement
KV/cache communication depending on architecture
```

Symptoms:

```text
scaling from 1 GPU to 2/4/8 GPUs is poor
GPUs wait on communication
latency rises with tensor parallel size
```

Fixes:

```text
use NVLink/NVSwitch when possible
choose parallelism carefully
avoid over-sharding small models
use data parallel replicas for throughput when model fits
benchmark real workload
```

---

### 7. CPU and System Bottlenecks

Not every bottleneck is the GPU.

CPU/system issues:

```text
slow tokenization
JSON/request overhead
sampling on CPU
Python scheduling overhead
logging/tracing too much
slow model loading from storage
container startup latency
network overhead
```

Symptoms:

```text
GPU utilization low
queue grows
CPU high
TTFT high before GPU work starts
```

Fixes:

```text
batch tokenization
use efficient runtimes
reduce logging payloads
warm models
use faster storage
profile request path
```

---

### 8. Bottleneck Diagnosis Table

| Symptom | Likely Bottleneck | First Check |
|---|---|---|
| OOM with long contexts | VRAM/KV cache | active tokens and KV bytes/token |
| slow first token | prefill/queueing | prompt length and queue time |
| slow stream after first token | decode bandwidth/scheduler | ITL and active sequences |
| poor multi-GPU scaling | interconnect | NCCL/communication metrics |
| GPU idle, requests slow | CPU/scheduler | CPU, queue, tokenizer metrics |
| high cost, low traffic | utilization | GPU idle time |
| p99 spikes | queueing/mixed workload | length distribution and admission |

---

### 9. Practical Interview Question

> A model fits in VRAM, but throughput is poor and GPUs show low compute utilization during generation. What might be bottlenecking?

### Strong Answer

If the model fits but decode throughput is poor with low compute utilization, I would suspect memory bandwidth, KV-cache behavior, scheduler inefficiency, or low decode concurrency rather than raw compute. Decode is sequential per request and often memory-bandwidth-bound because the system repeatedly reads weights and KV cache. I would inspect ITL, output tokens/sec, active sequences, KV-cache usage, batch size, memory bandwidth utilization, queue time, and CPU overhead. Fixes might include continuous batching, better KV-cache management, quantization, output length limits, speculative decoding, or using hardware with higher memory bandwidth. If concurrency is low, the GPU may simply not have enough decode work to stay busy.

### Active Recall

1. What does VRAM capacity control?
2. What does memory bandwidth control?
3. Why is decode often memory-bandwidth-bound?
4. Why is prefill often compute-heavy?
5. What does NVLink help with?
6. How can CPU bottleneck GPU serving?
7. What metric separates prefill pain from decode pain?
8. What should you check before buying bigger GPUs?

Final takeaway:

> Hardware reasoning is bottleneck reasoning: first identify whether the workload is limited by capacity, bandwidth, compute, interconnect, CPU, or scheduling, then choose the matching optimization.

---

## Topic P1.2: Serving Engines and Optimization Techniques

> **Topic time:** 12h
> Focus: Understanding what modern LLM serving engines optimize, why they exist, how they trade flexibility against performance, and which optimizations change real throughput and latency.

Serving engines exist because naive transformer inference wastes expensive hardware.

They optimize:

```text
request scheduling
batching
KV-cache memory
attention kernels
model loading
parallelism
quantization
streaming
metrics
API serving
```

The central idea:

> A serving engine is a scheduler plus memory manager plus optimized kernel/runtime stack around the model.

---

## Subtopic P1.2.a: vLLM, TGI, and TensorRT-LLM - What They Optimize and When to Choose Each

> **Subtopic time:** 3h
> Outcome: You should be able to compare vLLM, Hugging Face TGI, and TensorRT-LLM without hype, and choose an engine based on workload, hardware, team maturity, model support, latency target, and operational needs.

### Add to Knowledge Base

Three names show up often:

```text
vLLM
Text Generation Inference (TGI)
TensorRT-LLM
```

They all serve LLMs.

They are not identical.

The central mental model:

> vLLM optimizes high-throughput flexible serving, TGI packages production-friendly Hugging Face-style serving, and TensorRT-LLM pushes NVIDIA-optimized performance when you can accept more hardware/runtime specificity.

Important current note:

```text
Hugging Face now states TGI is in maintenance mode.
```

That does not erase its learning value or deployed history, but it changes greenfield recommendation strategy.

---

### 1. What a Serving Engine Actually Does

| Responsibility | Examples |
|---|---|
| request API | OpenAI-compatible endpoints, streaming |
| scheduler | batching, fairness, prefill/decode mixing |
| memory manager | KV-cache allocation, eviction, paging |
| kernels | attention, sampling, quantization kernels |
| model loader | Hugging Face weights, quantized formats |
| parallelism | tensor/data/pipeline/expert parallel |
| observability | metrics, tracing, logs |
| deployment | containers, CLI, Kubernetes patterns |

You are not only choosing speed.

You are choosing an operating model.

---

### 2. vLLM Mental Model

vLLM became popular because it attacked a core serving bottleneck:

```text
KV-cache memory waste
```

Its signature idea is PagedAttention:

```text
manage KV cache in blocks, similar to virtual memory pages
```

Strengths:

```text
high-throughput serving
continuous batching
PagedAttention / KV efficiency
OpenAI-compatible server
wide model support
fast iteration
strong community adoption
many modern features such as prefix caching, quantization, speculative decoding, parallelism
```

Good fit:

```text
you want flexible open-weight serving
you need high throughput quickly
you want OpenAI-compatible API surface
you run many standard transformer architectures
you want strong community/default choice
```

Watch-outs:

```text
fast-moving project
feature support varies by model/backend
benchmark your exact workload
advanced tuning still requires systems knowledge
```

---

### 3. TGI Mental Model

TGI is Hugging Face's text-generation serving stack.

It historically provided:

```text
simple launcher
streaming
Prometheus metrics
OpenTelemetry tracing
tensor parallelism
continuous batching
Flash/Paged Attention support
quantization support
Hugging Face ecosystem fit
```

Good fit:

```text
you are in Hugging Face infrastructure
you want a simple production-oriented serving wrapper
you operate models already supported by TGI
you inherit an existing TGI deployment
```

Watch-outs:

```text
maintenance-mode status matters for greenfield bets
new optimization work may move elsewhere
compare against vLLM/SGLang/TensorRT-LLM for new systems
```

Interview-safe phrasing:

> I would still understand TGI because it shaped open-source LLM serving and may exist in production, but for a new project I would check its maintenance status and compare it carefully against vLLM or TensorRT-LLM.

---

### 4. TensorRT-LLM Mental Model

TensorRT-LLM is NVIDIA's LLM inference optimization stack.

It focuses on:

```text
NVIDIA GPU performance
optimized kernels
in-flight batching
paged attention
KV-cache management
quantization such as FP8/FP4 on supported hardware
multi-GPU and multi-node inference
speculative decoding
TensorRT/Triton/Dynamo ecosystem integration
```

Good fit:

```text
you standardize on NVIDIA GPUs
you need maximum performance
you have infra maturity to build/test/tune engines
you serve high-volume or high-value workloads
you can invest in hardware-specific optimization
```

Watch-outs:

```text
more NVIDIA-specific
may require more build/tuning complexity
less plug-and-play than simple API serving
model/version/hardware support must be checked carefully
```

---

### 5. Selection Matrix

| Situation | Likely Choice |
|---|---|
| fast open-weight serving baseline | vLLM |
| OpenAI-compatible high-throughput API with broad community | vLLM |
| existing Hugging Face/TGI deployment | maintain or evaluate migration |
| greenfield Hugging Face-only simple stack | compare TGI status vs vLLM |
| maximum NVIDIA performance | TensorRT-LLM |
| multi-node NVIDIA serving with heavy tuning | TensorRT-LLM |
| small team, uncertain workload | hosted API or vLLM |
| bursty low-volume workload | hosted API often wins |
| strict custom kernels/hardware optimization | TensorRT-LLM |

---

### 6. Practical Interview Question

> When would you choose vLLM, TGI, TensorRT-LLM, or a hosted API?

### Strong Answer

I would choose based on workload, hardware, team maturity, and economics. For flexible open-weight serving with high throughput and broad model support, vLLM is often the default starting point because it combines continuous batching, PagedAttention-style KV efficiency, and an OpenAI-compatible serving surface. TGI is important historically and may fit existing Hugging Face deployments, but for a greenfield project I would account for its maintenance-mode status and compare it with newer serving engines. TensorRT-LLM is attractive when the organization is committed to NVIDIA GPUs and wants maximum performance with advanced optimizations like in-flight batching, paged attention, quantization, multi-GPU serving, and speculative decoding, but it may require more hardware-specific tuning. A hosted API is still the right choice when traffic is bursty, ops maturity is low, quality changes quickly, or utilization would be too low to justify GPUs.

### Active Recall

1. What does vLLM optimize?
2. What is PagedAttention trying to reduce?
3. What did TGI package well?
4. Why does TGI maintenance mode matter?
5. What does TensorRT-LLM optimize for?
6. When is a hosted API still better?
7. Why is engine choice not only a benchmark decision?

Final takeaway:

> Choose serving engines by workload and operating model: vLLM for flexible high-throughput open serving, TensorRT-LLM for NVIDIA-tuned performance, TGI mostly for existing/HF-aligned deployments, and hosted APIs when utilization or ops maturity does not justify ownership.

---

## Subtopic P1.2.b: Continuous (In-Flight) Batching and Paged Attention Intuition

> **Subtopic time:** 3h
> Outcome: You should be able to explain why naive batching wastes GPU capacity, how continuous batching improves serving throughput, and why paged attention makes KV-cache memory manageable under dynamic workloads.

### Add to Knowledge Base

Classic batching assumes:

```text
collect requests
run batch
finish batch
start next batch
```

LLM generation does not fit this cleanly.

Requests:

```text
arrive continuously
have different prompt lengths
generate different output lengths
finish at different times
```

Continuous batching says:

```text
keep a running batch of active sequences
add new requests as slots free up
schedule prefill and decode work dynamically
```

Paged attention says:

```text
store KV cache in blocks instead of one huge contiguous reservation
```

The central mental model:

> Continuous batching keeps the GPU fed; paged attention keeps KV memory from becoming a fragmented mess.

---

### 1. Static Batching Problem

Static batch:

```text
batch 8 requests
wait until all 8 finish
then start next 8
```

Problem:

```text
one long generation makes seven completed requests wait
new requests cannot join efficiently
GPU slots are wasted
latency becomes unfair
```

LLM serving needs dynamic batches because generation lengths are unpredictable.

---

### 2. Continuous Batching Intuition

At each scheduling step:

```text
some requests need prefill
some active requests need one decode step
some requests finish
new waiting requests can enter
```

The engine tries to pack useful work into each GPU step while respecting:

```text
max batch tokens
KV memory
fairness
latency SLO
priority
prefill/decode balance
```

This improves:

```text
throughput
GPU utilization
cost per token
request admission
```

But can hurt:

```text
tail latency
short-request fairness
predictability
debuggability
```

---

### 3. Paged Attention Intuition

Naive KV cache allocation:

```text
reserve max sequence length for every request
```

Waste:

```text
most requests do not use max length
finished requests leave gaps
variable lengths fragment memory
```

Paged attention:

```text
split KV cache into fixed-size blocks
map logical token positions to physical blocks
allocate blocks as sequence grows
free blocks when request ends
share blocks for common prefixes when safe
```

Analogy:

```text
Operating systems do not require every process to occupy one huge contiguous physical memory region.
Paged KV cache applies a similar idea to attention memory.
```

---

### 4. Why They Work Together

Continuous batching creates dynamic scheduling.

Dynamic scheduling creates dynamic memory pressure.

Paged attention makes dynamic memory pressure manageable.

Together they allow:

```text
more active requests
less KV memory waste
higher throughput under mixed lengths
better utilization for real traffic
```

---

### 5. Failure Modes

| Failure Mode | Symptom | Fix |
|---|---|---|
| prefill blocks decode | streaming stalls | chunked prefill / scheduling policy |
| too much batching | high TTFT | max wait time / priority queues |
| too little batching | high cost | increase concurrency / continuous batching |
| KV fragmentation | low usable batch | paged KV |
| long requests dominate | p99 spikes | max tokens, separate queues, fairness |

---

### 6. Mini Simulator: Static vs Continuous Slots

```python
def static_batches(lengths: list[int], batch_size: int) -> int:
    total_steps = 0
    for i in range(0, len(lengths), batch_size):
        total_steps += max(lengths[i:i + batch_size])
    return total_steps


def idealized_continuous(lengths: list[int], batch_size: int) -> int:
    # Lower bound intuition: total token work spread over available slots.
    return (sum(lengths) + batch_size - 1) // batch_size


def main() -> None:
    decode_lengths = [20, 20, 20, 200, 30, 30, 30, 30]
    print("static:", static_batches(decode_lengths, batch_size=4))
    print("idealized_continuous:", idealized_continuous(decode_lengths, batch_size=4))


if __name__ == "__main__":
    main()
```

Lesson:

```text
static batches waste slots when requests have different output lengths
continuous scheduling can use freed slots sooner
```

---

### 7. Practical Interview Question

> Explain continuous batching and paged attention to a backend engineer who understands queues and memory allocation.

### Strong Answer

Continuous batching is dynamic request scheduling for autoregressive generation. Instead of forming a fixed batch and waiting for every sequence to finish, the server keeps an active set of sequences, runs decode steps for them, adds new requests when capacity opens, and mixes prefill/decode work according to policy. This keeps the GPU utilized under variable request lengths. Paged attention solves the memory side: KV cache is allocated in blocks rather than one large contiguous max-length region per request. That reduces fragmentation and wasted memory, enabling larger effective batches and higher throughput. The tradeoff is scheduler complexity, fairness, and tail-latency tuning.

### Active Recall

1. Why does static batching waste capacity for LLMs?
2. What does continuous batching add?
3. What does paged attention manage?
4. Why do variable output lengths matter?
5. How can batching hurt TTFT?
6. What is the relationship between continuous batching and KV-cache memory?

Final takeaway:

> Continuous batching solves the scheduling problem of dynamic generation; paged attention solves the memory problem created by dynamic, variable-length KV cache.

---

## Subtopic P1.2.c: KV Cache Management, Prefix Caching, and Reuse

> **Subtopic time:** 3h
> Outcome: You should be able to explain how KV cache is allocated, reused, evicted, and shared, and when prefix caching can materially reduce TTFT and cost.

### Add to Knowledge Base

KV cache is both the key to efficient decode and one of the biggest serving constraints.

The serving engine must decide:

```text
where KV blocks live
when to allocate them
when to free them
whether a prefix can be reused
whether cached state is still correct
which request gets memory during pressure
```

The central mental model:

> KV cache is working memory for active and reusable context. Manage it well and serving gets cheaper; manage it poorly and VRAM disappears.

---

### 1. KV Cache Lifecycle

```text
request admitted
-> prefill creates KV for prompt tokens
-> decode appends KV per generated token
-> request finishes
-> KV blocks freed or retained if reusable
```

Memory pressure comes from:

```text
long prompts
long outputs
many concurrent requests
prefix retention
fragmentation
multi-sampling / beam search
```

---

### 2. Prefix Caching

Prefix caching reuses KV cache for repeated prompt prefixes.

Common repeated prefixes:

```text
system prompt
developer instructions
tool schema block
organization policy preamble
few-shot examples
shared RAG document prefix
agent scaffold
```

If many requests begin with the same prefix, the engine can avoid recomputing that prefix during prefill.

Benefits:

```text
lower TTFT
lower prefill compute
higher throughput
better cost for repeated workloads
```

Risks:

```text
incorrect reuse if prefix differs subtly
tenant/security leakage if cache scope is wrong
memory spent retaining prefixes
low hit rate wastes complexity
```

---

### 3. Cache Correctness

A prefix can be reused only when the tokenized prefix is identical and the relevant execution context matches.

Cache key should include:

```text
model version
tokenizer version
prompt token IDs
LoRA/adapters if any
sampling-independent context
tenant/security scope when relevant
cache policy version
```

Do not share cached KV across tenants unless the prefix is truly public and safe.

Never let prefix caching bypass:

```text
authorization
policy
secret handling
model versioning
```

---

### 4. Eviction and Memory Pressure

When KV memory is scarce, the engine may need to:

```text
reject new requests
evict reusable prefixes
pause/resume requests
offload KV cache
reduce max tokens
use lower precision KV cache
route to another replica
```

Eviction policy depends on:

```text
hit rate
prefix size
tenant priority
request priority
latency SLO
memory pressure
```

---

### 5. Metrics

Track:

```text
KV-cache usage percent
active KV blocks
free KV blocks
prefix cache hit rate
prefix cache saved tokens
eviction count
OOM/rejection count
TTFT with and without prefix hit
cache hit by tenant/workload
```

If prefix hit rate is low, the memory spent retaining prefixes may not be worth it.

---

### 6. Practical Interview Question

> When does prefix caching help, and what can go wrong?

### Strong Answer

Prefix caching helps when many requests share identical token prefixes, such as a common system prompt, tool schema, few-shot block, or stable agent scaffold. It saves prefill work because the server can reuse KV cache for that prefix instead of recomputing it. It mainly improves TTFT and prefill throughput. The risks are correctness and security: reuse must be tied to exact token IDs, model/tokenizer versions, adapter state, and tenant or visibility scope. It can also waste VRAM if the prefix is large but hit rate is low. I would measure hit rate, saved prefill tokens, TTFT improvement, and eviction pressure before relying on it.

### Active Recall

1. What does KV cache store?
2. When does KV cache grow?
3. What is prefix caching?
4. Which workloads benefit most?
5. Why must cache keys include model/tokenizer version?
6. Why is tenant scope important?
7. What metric tells you prefix caching is useful?

Final takeaway:

> KV reuse is a performance feature only when it is also a correctness feature: reuse identical safe prefixes, measure hit-rate value, and never let cache scope bypass authorization or version boundaries.

---

## Subtopic P1.2.d: Speculative Decoding, Chunked Prefill, and Other Latency Tricks

> **Subtopic time:** 3h
> Outcome: You should understand the main latency-improvement techniques, what phase they target, and when their added complexity is worth it.

### Add to Knowledge Base

Latency tricks target different problems.

```text
speculative decoding -> decode speed
chunked prefill -> prefill/decode interference
prefix caching -> repeated prefill
quantization -> memory and speed
CUDA graphs -> kernel launch overhead
disaggregated serving -> separate prefill and decode resources
output control -> reduce decode work
```

The central mental model:

> Latency optimization only works when it targets the phase that is actually hurting the workload.

---

### 1. Speculative Decoding

Speculative decoding uses a fast draft mechanism to propose tokens and a stronger target model to verify them.

Common draft sources:

```text
small draft model
n-gram speculation
Medusa-style heads
EAGLE-style draft models
multi-token prediction
```

If many proposed tokens are accepted, the target model effectively produces multiple tokens per expensive verification step.

Best fit:

```text
decode-heavy workloads
low to moderate batch sizes
draft model is much cheaper
acceptance rate is high
quality must match target distribution or pass eval
```

Watch-outs:

```text
low acceptance rate reduces gain
draft model consumes resources
large batches may reduce benefit
implementation complexity rises
not all models/routes support it equally
```

---

### 2. Chunked Prefill

Long prefill can block decode work and hurt streaming smoothness.

Chunked prefill splits long context processing into chunks so the scheduler can interleave:

```text
some prefill work
some decode work
more prefill work
```

Best fit:

```text
long-context RAG
mixed workloads with short and long prompts
strict TTFT/ITL fairness
prefill blocking decode
```

Tradeoff:

```text
better scheduling fairness
possible overhead and tuning complexity
```

---

### 3. Other Tricks

| Technique | Targets | Core Idea |
|---|---|---|
| prefix caching | TTFT | reuse shared prompt KV |
| output caps | total latency/cost | prevent long decode |
| concise schema | decode | force shorter structured outputs |
| quantization | memory/speed | move fewer bytes |
| CUDA graphs | overhead | reuse captured execution graphs |
| disaggregated prefill/decode | utilization | use different resources for different phases |
| guided decoding | correctness | constrain outputs, sometimes at latency cost |
| KV offload | capacity | trade memory pressure for transfer overhead |

---

### 4. Latency Trick Decision Matrix

| Symptom | Likely Trick |
|---|---|
| slow first token, repeated prompt | prefix caching |
| slow first token, huge context | context pruning or chunked prefill |
| decode stream crawls | speculative decoding or faster model |
| GPU underused during decode | continuous batching |
| KV OOM | paged KV, shorter context, quantized KV |
| high kernel overhead | CUDA graphs / optimized runtime |
| high cost from long answers | output caps and concise schemas |

---

### 5. Practical Interview Question

> The assistant starts streaming quickly for short prompts but long RAG prompts make everyone else's streaming worse. What optimization would you consider?

### Strong Answer

That sounds like long prefill interfering with decode scheduling. I would first measure TTFT, ITL, prompt length distribution, queue time, and whether decode stalls during long prefill. Then I would reduce context if possible, but if long prompts are required I would consider chunked prefill so the engine can split context processing and interleave it with decode work. I would also look at separate queues, prefix caching for shared prompt scaffolds, and admission control. Speculative decoding would help only if decode is the bottleneck, so I would not start there unless ITL remains the issue after prefill is addressed.

### Active Recall

1. What does speculative decoding speed up?
2. What is acceptance rate?
3. What does chunked prefill solve?
4. When does prefix caching help?
5. Why are output caps latency optimizations?
6. Why should you measure before choosing a trick?
7. What trick targets repeated shared prompts?

Final takeaway:

> Latency tricks are phase-specific tools: use prefix caching for repeated prefill, chunked prefill for long-context scheduling, speculative decoding for decode-heavy workloads, and output control when the cheapest token is the one you never generate.

---

## Topic P1.3: Quantization, Parallelism, and Capacity Planning

> **Topic time:** 10h
> Focus: Understanding how to fit larger models, make them cheaper, spread them across hardware, scale serving fleets, and estimate the number of GPUs needed for a real workload.

Topic P1.3 is where serving knowledge becomes production planning.

The central idea:

> Capacity planning is model math plus workload math plus reliability headroom.

---

## Subtopic P1.3.a: Quantization Mental Models - FP16/BF16, INT8, FP8, GPTQ, AWQ, and Quality Tradeoffs

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain quantization as a memory/bandwidth optimization, compare common quantization families, and describe when quality risk is acceptable.

### Add to Knowledge Base

Quantization means representing model computation with fewer bits.

Why it matters:

```text
less weight memory
less memory bandwidth
larger models fit
larger batches fit
lower cost per token
sometimes faster inference
```

But:

```text
lower precision can reduce quality
some hardware accelerates some formats better than others
some methods quantize only weights
some quantize activations or KV cache too
```

The central mental model:

> Quantization is compression for inference math. It buys capacity and speed by spending numerical precision.

---

### 1. Precision Map

| Format | Rough Bytes | Mental Model |
|---|---:|---|
| FP32 | 4 | training/reference precision |
| FP16 | 2 | common inference baseline |
| BF16 | 2 | wider exponent, robust training/inference |
| FP8 | 1 | modern GPU accelerated low precision |
| INT8 | 1 | common quantized inference |
| INT4 | 0.5 | aggressive weight compression |
| FP4 | 0.5 | emerging hardware-specific path |

Do not ask only:

```text
How many bits?
```

Ask:

```text
weights only or activations too?
KV cache quantized?
hardware supports it natively?
calibration needed?
quality measured on our tasks?
```

---

### 2. Common Families

| Method | What It Usually Means | Fit |
|---|---|---|
| FP16/BF16 | half precision baseline | quality-safe default |
| INT8 | lower precision, often calibrated | cost/perf with moderate risk |
| FP8 | hardware-supported on newer GPUs | high-performance modern serving |
| GPTQ | post-training weight quantization | compress open-weight models |
| AWQ | activation-aware weight quantization | INT4-ish weight compression with quality focus |
| bitsandbytes | practical quantization tooling | experimentation/prototyping |
| quantized KV | reduce KV-cache memory | long-context/concurrency pressure |

Exact support depends on engine, model architecture, and hardware.

---

### 3. Weight-Only vs W8A8 vs KV Quantization

Weight-only quantization:

```text
weights use fewer bits
activations may stay FP16/BF16
often easier to preserve quality
helps model fit and memory bandwidth
```

Weight+activation quantization:

```text
weights and activations lower precision
can speed kernels more
needs stronger calibration/support
more quality risk
```

KV-cache quantization:

```text
KV cache uses fewer bits
helps long context and concurrency
can affect attention quality
must be evaluated on long-context tasks
```

---

### 4. Quality Risk

Quantization errors show up as:

```text
slightly worse reasoning
format/schema errors
worse code generation
long-context degradation
math errors
retrieval-answer brittleness
tool-call argument mistakes
more refusals or less stable style
```

Do not validate with one demo.

Evaluate:

```text
task success
groundedness
schema validity
tool-call correctness
long-context recall
language/domain slices
safety and refusal behavior
```

---

### 5. Decision Matrix

| Situation | Recommendation |
|---|---|
| first production baseline | FP16/BF16 if cost allows |
| memory does not fit | weight quantization or more GPUs |
| decode bandwidth bottleneck | quantization may help |
| long-context KV OOM | quantized KV or shorter context |
| high-stakes reasoning | be conservative, require eval |
| batch summarization | quantization often acceptable |
| strict schema/tool planning | test heavily before aggressive quantization |

---

### 6. Practical Interview Question

> Would you use INT4/AWQ/GPTQ quantization for a production RAG assistant?

### Strong Answer

I would not decide by format alone. Quantization can reduce weight memory and memory bandwidth, which can let a larger model fit or improve cost, but it can also change quality. For a RAG assistant, I would evaluate grounded accuracy, citation precision, schema validity, and refusal/safety behavior on the actual workload. Weight-only INT4 methods such as GPTQ or AWQ may be acceptable for lower-risk summarization or high-volume support answers if evals pass. For high-stakes answers or tool planning, I would be more conservative, perhaps using BF16/FP16 or FP8 on supported hardware. I would also consider whether KV-cache memory, not weights, is the true bottleneck.

### Active Recall

1. Why does quantization help inference?
2. What is the risk of quantization?
3. What is weight-only quantization?
4. Why might KV quantization matter?
5. Why is hardware support important?
6. What should you evaluate after quantization?
7. When is aggressive quantization risky?

Final takeaway:

> Quantization is not a free speed switch; it is a precision-for-capacity tradeoff that must be validated on the exact quality, safety, and schema demands of the workload.

---

## Subtopic P1.3.b: Tensor, Pipeline, and Data Parallelism for Large Models

> **Subtopic time:** 2.5h
> Outcome: You should be able to explain the main inference parallelism strategies and choose between them based on model fit, throughput, latency, and interconnect constraints.

### Add to Knowledge Base

Parallelism exists because:

```text
one GPU may not fit the model
one GPU may not provide enough throughput
one GPU may not meet latency
```

The central mental model:

> Split the model when it does not fit; replicate the model when it fits but you need more throughput.

---

### 1. Data Parallelism

Data parallel inference:

```text
each GPU/replica holds a full model copy
requests are distributed across replicas
```

Best fit:

```text
model fits on one GPU
need more throughput
want simpler scaling
traffic can be load balanced
```

Pros:

```text
simple
good fault isolation
scales request throughput
```

Cons:

```text
does not help fit larger model
requires full weight copy per GPU
```

---

### 2. Tensor Parallelism

Tensor parallelism splits model tensors across GPUs within a layer.

Best fit:

```text
model too large for one GPU
need lower latency than pipeline-only
fast GPU interconnect available
```

Cost:

```text
communication during layer computation
```

Needs:

```text
NVLink/NVSwitch or strong interconnect for good scaling
```

Too much tensor parallelism can hurt latency if communication dominates.

---

### 3. Pipeline Parallelism

Pipeline parallelism splits layers across GPUs.

Example:

```text
GPU 1 holds layers 1-20
GPU 2 holds layers 21-40
```

Best fit:

```text
very large models
memory fit across GPUs
batch/throughput workloads where pipeline bubbles can be amortized
```

Tradeoff:

```text
pipeline bubbles
more complex scheduling
latency may rise for single request
```

---

### 4. Combining Strategies

Large serving deployments may combine:

```text
tensor parallelism inside a replica
pipeline parallelism across layer groups
data parallelism across replicas
expert parallelism for MoE models
context parallelism for very long contexts
```

Example:

```text
70B model uses tensor parallel 4 to fit one replica
deployment runs 8 such replicas for throughput
```

---

### 5. Selection Matrix

| Need | Strategy |
|---|---|
| model fits, need more QPS | data parallel |
| model does not fit, fast interconnect | tensor parallel |
| model too deep/large, memory split by layers | pipeline parallel |
| MoE model with many experts | expert parallel |
| extreme context length | context/KV parallel techniques |
| low-latency small model | avoid unnecessary parallelism |

---

### 6. Practical Interview Question

> A 70B model does not fit on one GPU. How would you serve it?

### Strong Answer

First I would estimate weight memory, KV cache, context length, and concurrency. If the model does not fit on one GPU, I would shard it. Tensor parallelism is often the first option when fast interconnect is available because it splits layer tensors across GPUs, but it adds communication during each layer. Pipeline parallelism can split layers across GPUs, but it may add pipeline bubbles and latency. Once I have one working model replica, I would use data parallel replicas to scale request throughput. The final choice depends on hardware interconnect, latency SLO, batch size, context length, and serving engine support. I would benchmark the actual workload because poor communication can erase the benefit of more GPUs.

### Active Recall

1. What does data parallelism do?
2. What does tensor parallelism split?
3. What does pipeline parallelism split?
4. Why does interconnect matter?
5. Which strategy scales throughput when model fits?
6. Which strategy helps model fit?
7. Why can parallelism hurt latency?

Final takeaway:

> Parallelism is not "add GPUs"; it is choosing whether to replicate requests, shard tensors, split layers, or combine strategies while paying communication and scheduling costs.

---

## Subtopic P1.3.c: Autoscaling, Cold Starts, and Warm-Pool Strategies for GPU Services

> **Subtopic time:** 2.5h
> Outcome: You should be able to design GPU autoscaling behavior that handles traffic bursts without pretending GPU services behave like ordinary stateless web servers.

### Add to Knowledge Base

GPU inference services are slow to start compared with normal web containers.

Cold start can include:

```text
node provisioning
container image pull
GPU device plugin scheduling
model weight download
weight loading into VRAM
kernel compilation / graph capture
engine build
warmup requests
health checks
```

The central mental model:

> GPU autoscaling is slow-capacity management, not instant elasticity.

---

### 1. Why Scale-to-Zero Is Hard

Scale-to-zero saves money.

But for LLM serving it may cause:

```text
minute-level cold starts
huge first-request latency
model loading storms
cache misses
unready engines receiving traffic
```

Good for:

```text
dev/test
batch jobs
low-priority async workloads
very low traffic
```

Risky for:

```text
interactive chat
strict p95 latency
enterprise SLAs
high-value workflows
```

---

### 2. Warm Pools

A warm pool keeps capacity ready before traffic arrives.

Levels:

```text
warm node: GPU VM exists
warm container: server container running
warm model: weights loaded into VRAM
warm engine: kernels/graphs compiled
warm cache: common prefixes loaded
```

The warmer it is, the faster it responds.

The warmer it is, the more it costs while idle.

---

### 3. Autoscaling Signals

Do not scale only on CPU.

Useful signals:

```text
request queue depth
waiting time
active sequences
KV-cache usage
GPU memory usage
GPU utilization
tokens/sec saturation
TTFT p95
ITL p95
timeout rate
admission rejection rate
```

Scale before users feel pain.

GPU startup is too slow for purely reactive scaling in many interactive workloads.

Use forecasting when possible.

---

### 4. Overload Behavior

When capacity is insufficient:

```text
queue with deadline
admit based on priority
reject early with retry-after
route to hosted fallback
degrade low-risk requests
protect high-priority tenants
cap max context/output
```

Do not let the system:

```text
queue forever
OOM
accept work it cannot finish
starve all users equally
```

---

### 5. Practical Interview Question

> How would you autoscale a self-hosted LLM service for bursty traffic?

### Strong Answer

I would not treat GPU autoscaling like stateless HTTP autoscaling. Cold start includes node provisioning, image pull, model download, weight loading, kernel compilation, and warmup, so reactive scaling may be too late for interactive traffic. I would keep a warm pool sized for baseline and near-term forecast demand, then scale additional replicas based on queue depth, waiting time, active sequences, KV-cache usage, TTFT/ITL, and timeout rate. During overload I would use admission control, priority queues, max context/output limits, graceful degradation, or hosted fallback. For very bursty low-utilization workloads, a hosted API may be economically better than keeping idle GPUs warm.

### Active Recall

1. Why are GPU cold starts slow?
2. What is a warm pool?
3. What is the tradeoff of warm capacity?
4. Why is CPU utilization a weak autoscaling signal?
5. What should happen under overload?
6. When is hosted API better?
7. Why is forecasting useful?

Final takeaway:

> GPU autoscaling is about buying readiness: keep enough warm capacity for latency promises, add capacity before queues explode, and use admission/degradation when cold starts cannot arrive in time.

---

## Subtopic P1.3.d: Capacity Planning - Tokens/sec Targets, Concurrency, and Headroom

> **Subtopic time:** 2.5h
> Outcome: You should be able to estimate GPU capacity needs from workload shape, latency SLO, memory limits, concurrency, and reliability headroom.

### Add to Knowledge Base

Capacity planning answers:

```text
How many GPUs do we need?
Which model/precision?
How much traffic can one replica handle?
What concurrency is safe?
How much headroom protects p95/p99?
When do we autoscale?
When should we use hosted fallback?
```

The central mental model:

> Capacity is not requests/sec. Capacity is prompt-token load, output-token load, active KV memory, latency target, and headroom.

---

### 1. Inputs to Collect

Collect workload distribution:

```text
requests per second
p50/p95/p99 prompt tokens
p50/p95/p99 output tokens
concurrency
traffic burst factor
streaming requirements
TTFT target
ITL target
end-to-end latency target
quality/model tier
tenant priority
retry/fallback rate
```

Do not plan from averages only.

P95 token lengths often drive memory and latency.

---

### 2. Token Demand

Prompt-token demand:

```text
prompt_tokens_per_second =
  requests_per_second * avg_input_tokens
```

Output-token demand:

```text
output_tokens_per_second =
  requests_per_second * avg_output_tokens
```

Burst-adjusted:

```text
required_tokens_per_second =
  demand * burst_factor * headroom_factor
```

Separate prefill and decode demand.

---

### 3. Concurrency Estimate

Little's Law intuition:

```text
concurrency ~= arrival_rate * average_request_duration
```

If:

```text
10 requests/sec
average duration 6 sec
```

then:

```text
about 60 active requests
```

Active KV memory depends on:

```text
sum(prompt + generated tokens for active requests)
```

So long outputs increase duration and concurrency.

---

### 4. Headroom

Headroom protects against:

```text
traffic bursts
p95/p99 long prompts
long outputs
retries
node failures
rolling deploys
provider fallback loss
fragmentation
hot tenants
```

Common planning:

```text
target 50 to 70 percent steady utilization for interactive services
reserve extra for bursts and failover
run hotter for batch jobs
```

Exact target depends on SLO and economics.

---

### 5. Capacity Calculator Sketch

```python
from dataclasses import dataclass
import math


@dataclass
class Workload:
    requests_per_second: float
    avg_input_tokens: int
    avg_output_tokens: int
    avg_duration_seconds: float
    burst_factor: float
    headroom_factor: float


@dataclass
class Replica:
    prompt_tokens_per_second: int
    output_tokens_per_second: int
    max_concurrency: int


def plan(workload: Workload, replica: Replica) -> dict[str, int]:
    prompt_demand = workload.requests_per_second * workload.avg_input_tokens
    output_demand = workload.requests_per_second * workload.avg_output_tokens
    concurrency = workload.requests_per_second * workload.avg_duration_seconds

    multiplier = workload.burst_factor * workload.headroom_factor

    by_prompt = math.ceil(prompt_demand * multiplier / replica.prompt_tokens_per_second)
    by_output = math.ceil(output_demand * multiplier / replica.output_tokens_per_second)
    by_concurrency = math.ceil(concurrency * multiplier / replica.max_concurrency)

    return {
        "replicas_by_prompt": by_prompt,
        "replicas_by_output": by_output,
        "replicas_by_concurrency": by_concurrency,
        "required_replicas": max(by_prompt, by_output, by_concurrency),
    }


def main() -> None:
    workload = Workload(
        requests_per_second=8,
        avg_input_tokens=1800,
        avg_output_tokens=250,
        avg_duration_seconds=5,
        burst_factor=1.5,
        headroom_factor=1.3,
    )
    replica = Replica(
        prompt_tokens_per_second=30000,
        output_tokens_per_second=1800,
        max_concurrency=40,
    )
    print(plan(workload, replica))


if __name__ == "__main__":
    main()
```

This is not a substitute for benchmarking.

It is a planning frame.

---

### 6. Benchmark Plan

Benchmark with:

```text
realistic prompt/output distributions
p50/p95/p99 lengths
streaming and non-streaming modes
concurrency sweeps
batching configs
quantization variants
parallelism variants
failure/retry overhead
```

Measure:

```text
TTFT
ITL
end-to-end latency
prompt tokens/sec
output tokens/sec
GPU memory
KV-cache usage
queue time
timeouts
cost per successful request
```

---

### 7. Practical Interview Question

> How would you capacity-plan a self-hosted 8B or 70B LLM service for an enterprise RAG assistant?

### Strong Answer

I would start with workload shape, not model size alone. I need request rate, prompt length distribution, output length distribution, concurrency, burst factor, TTFT/ITL targets, and p95 latency SLO. Then I estimate prompt-token demand, output-token demand, and active sequence memory. I would benchmark one replica on the target engine and hardware to measure prompt tokens/sec, output tokens/sec, max safe concurrency, KV-cache usage, and p95 latency. Required replicas are the maximum of prompt throughput, decode throughput, and concurrency/memory constraints, multiplied by burst and headroom factors. For a 70B model I would also choose tensor/pipeline parallelism to fit one replica, then data-parallel replicas for throughput. Finally I would include headroom for retries, rolling deploys, node failures, and hot tenants, and compare the resulting cost against a hosted baseline.

### Active Recall

1. Why is requests/sec insufficient for capacity planning?
2. What token distributions should you collect?
3. How do you estimate prompt-token demand?
4. How do you estimate output-token demand?
5. What does Little's Law estimate?
6. Why do long outputs increase concurrency?
7. Why plan with p95/p99?
8. What constraints determine required replicas?
9. Why does headroom matter?
10. What should a benchmark include?

Final takeaway:

> Capacity planning for LLM serving means estimating prefill demand, decode demand, active KV memory, concurrency, latency SLO, and failure headroom, then validating the estimate with workload-realistic benchmarks.

---

## Module P1 Checkpoint: LLM Inference and Serving at Scale Synthesis

### Module Checkpoint

By the end of Pro Module P1, you should be able to:

1. Estimate the GPU memory and rough throughput for serving a given open-weight model.
2. Justify vLLM vs TGI vs a hosted API for a specific workload using cost and latency.
3. Explain how continuous batching and KV cache reuse change real throughput.

This checkpoint is not about memorizing serving-engine names.

It is about being able to say:

> "Given this model, context length, output length, traffic shape, latency target, GPU type, and team maturity, I can estimate what will fit, what will bottleneck, what it may cost, and which serving strategy I would choose."

The target module sentence:

> "LLM serving is GPU memory math plus prefill/decode throughput math plus scheduling economics."

---

### Add to Knowledge Base: The Full Module P1 Mental Model

LLM serving is not:

```text
load model
send prompt
get answer
```

At scale, it is:

```text
workload shape
-> model/precision choice
-> weight memory estimate
-> KV-cache capacity estimate
-> prefill throughput estimate
-> decode throughput estimate
-> serving engine choice
-> batching and scheduling policy
-> cache/reuse strategy
-> autoscaling and warm capacity
-> cost and latency validation
```

The full module mental model:

```text
Weights decide whether the model loads.
KV cache decides how much concurrency fits.
Prefill decides how fast the model starts answering.
Decode decides how fast it keeps answering.
Batching decides whether the GPU is economical.
Engine choice decides how much of this complexity you own.
```

---

### 1. Checkpoint Outcome 1: Estimate GPU Memory and Rough Throughput

A serving estimate has two major parts:

```text
memory fit
throughput fit
```

Memory fit asks:

```text
Can this GPU or GPU group hold the model, KV cache, activations, runtime overhead, and headroom?
```

Throughput fit asks:

```text
Can this serving setup process the required prompt tokens and output tokens within latency and cost targets?
```

#### Memory Estimation Recipe

Step 1: Estimate weight memory.

```text
weight_memory_bytes = parameter_count * bytes_per_parameter
```

Examples:

```text
8B at FP16/BF16:
  8B * 2 bytes = about 16 GB

70B at FP16/BF16:
  70B * 2 bytes = about 140 GB

8B at INT4 weight-only:
  8B * 0.5 bytes = about 4 GB plus quantization metadata
```

Step 2: Estimate KV cache per token.

```text
KV bytes per token =
  num_layers
  * 2
  * num_kv_heads
  * head_dim
  * bytes_per_kv_value
```

Step 3: Estimate active tokens.

```text
active_tokens =
  sum(prompt_tokens + generated_tokens_so_far for active requests)
```

Step 4: Estimate KV memory.

```text
KV_memory = active_tokens * KV_bytes_per_token
```

Step 5: Add overhead and headroom.

```text
required_VRAM =
  weights
  + KV cache
  + activations/workspace
  + runtime overhead
  + fragmentation/headroom
```

Practical checkpoint rule:

> If your estimate uses only parameter count, it is not a serving estimate. It is only a loading estimate.

#### Throughput Estimation Recipe

Separate prefill and decode demand.

```text
prompt_tokens_per_second =
  requests_per_second * average_input_tokens

output_tokens_per_second =
  requests_per_second * average_output_tokens
```

Then compare to measured or benchmarked per-replica capacity:

```text
replicas_by_prefill =
  required_prompt_tokens_per_second / prompt_tokens_per_second_per_replica

replicas_by_decode =
  required_output_tokens_per_second / output_tokens_per_second_per_replica

replicas_by_concurrency =
  required_active_requests / max_safe_active_requests_per_replica
```

Required replicas:

```text
max(replicas_by_prefill, replicas_by_decode, replicas_by_concurrency)
* burst_factor
* headroom_factor
```

The bottleneck is whichever number is largest.

#### Worked Example: 8B RAG Assistant

Assume:

```text
model: 8B
precision: BF16
GPU: 24 GB
average prompt: 2,000 tokens
average output: 300 tokens
traffic: 5 requests/sec
average duration: 5 sec
burst/headroom multiplier: 2x
```

Memory:

```text
weights ~= 16 GB
remaining before overhead ~= 8 GB
after runtime/headroom maybe 4-5 GB available for KV
```

If KV cache budget supports only a limited active-token pool, concurrency may be tight.

Concurrency:

```text
active requests ~= arrival_rate * duration
active requests ~= 5 * 5 = 25

active tokens roughly:
25 * (2,000 prompt + partial generation)
```

Throughput demand:

```text
prompt demand = 5 * 2,000 = 10,000 prompt tokens/sec
output demand = 5 * 300 = 1,500 output tokens/sec
with 2x burst/headroom:
20,000 prompt tokens/sec
3,000 output tokens/sec
```

Decision:

```text
If one 24 GB replica cannot hold enough KV cache for p95 contexts, use lower max context, quantization, a larger VRAM GPU, more replicas, or a smaller model.
If decode capacity is below 3,000 output tokens/sec, add replicas or improve batching/quantization/speculative decoding.
```

The exact answer requires benchmarking, but the estimate tells you what to benchmark and what is likely to break.

---

### 2. Checkpoint Outcome 2: Justify vLLM vs TGI vs Hosted API

Engine choice is not a brand preference.

It is an operating decision.

You compare:

```text
latency SLO
throughput target
traffic shape
model choice
hardware
GPU utilization
team maturity
feature needs
cost per successful task
time to production
```

#### Fast Comparison

| Option | Best When | Watch Out |
|---|---|---|
| vLLM | flexible open-weight serving, high throughput, OpenAI-compatible serving, broad community | benchmark exact model/features |
| TGI | existing Hugging Face-aligned deployment or inherited stack | maintenance-mode status matters for greenfield |
| TensorRT-LLM | maximum NVIDIA GPU performance and team can tune hardware-specific stack | more complexity and hardware specificity |
| hosted API | bursty traffic, low ops maturity, fast start, model quality changes quickly | token cost and less infra control |

The user specifically asked vLLM vs TGI vs hosted API.

The mature answer can mention TensorRT-LLM, but should still answer the requested comparison.

#### Decision Frame

Choose hosted API when:

```text
traffic is bursty or low
GPU utilization would be poor
team lacks serving infra maturity
time-to-market matters most
quality depends on proprietary frontier models
ops burden is not justified
```

Choose vLLM when:

```text
open-weight model meets quality target
traffic is steady enough for GPU utilization
cost per token matters
you need OpenAI-compatible serving
you want continuous batching and paged KV efficiency
you can operate GPU services
```

Choose TGI when:

```text
you already run Hugging Face/TGI
your model and deployment pattern are well-supported
team values its production wrapper and HF integration
migration cost outweighs benefit
```

For greenfield:

```text
check TGI maintenance status and compare carefully with vLLM or other active engines
```

#### Example Decision: Internal RAG Assistant

Workload:

```text
steady enterprise traffic
average 2K prompt tokens
300 output tokens
p95 latency under 8 seconds
cost pressure high
open-weight model passes eval
team has Kubernetes/GPU experience
```

Likely choice:

```text
vLLM
```

Why:

```text
steady traffic can utilize GPUs
OpenAI-compatible endpoint simplifies app integration
continuous batching improves throughput
paged KV improves memory use
open-weight model quality is enough
self-hosted cost may beat hosted API at utilization
```

Why not hosted:

```text
unit token cost may be higher at steady volume
less control over batching/caching/model variant
```

Why not TGI:

```text
unless already deployed or strongly HF-aligned, maintenance-mode status reduces greenfield appeal
```

#### Example Decision: Low-Volume Legal Prototype

Workload:

```text
10 users
bursty traffic
quality must be high
no GPU ops team
uncertain model choice
```

Likely choice:

```text
hosted API
```

Why:

```text
low utilization makes self-hosted GPUs expensive
hosted API avoids cold-start and ops burden
quality may require stronger hosted model
```

---

### 3. Checkpoint Outcome 3: Continuous Batching and KV Cache Reuse Change Real Throughput

Naive throughput thinking:

```text
one request at a time
one batch at a time
one contiguous KV allocation per request
```

Modern serving thinking:

```text
many active sequences share GPU steps
new requests join while old requests continue
KV cache is block-managed
common prefixes can be reused
```

#### Continuous Batching Impact

Continuous batching improves real throughput because:

```text
completed sequences leave the active batch immediately
new sequences can enter without waiting for the longest generation
decode steps from many users keep GPU busy
prefill and decode can be scheduled together
```

It changes the economics from:

```text
batch throughput on clean benchmark
```

to:

```text
serving throughput under variable live traffic
```

But it has tradeoffs:

```text
queueing policy matters
fairness matters
long prompts can disrupt decode
latency SLO can limit batching aggressiveness
```

#### Paged KV Impact

Paged KV / paged attention improves real throughput because:

```text
less KV memory is wasted
fragmentation is reduced
more active tokens fit
variable-length sequences are easier to manage
batch size can increase under real workloads
```

The more variable your sequence lengths, the more valuable good KV management becomes.

#### Prefix/KV Reuse Impact

Prefix caching improves throughput when prompts share stable prefixes:

```text
system prompt
tool schemas
few-shot examples
agent scaffold
common policy preamble
```

It changes throughput by reducing repeated prefill work.

Benefits:

```text
lower TTFT
less prompt-token compute
more capacity for useful work
```

But only if:

```text
tokenized prefixes are identical
model/tokenizer versions match
security/tenant scope is correct
hit rate is high enough
memory retained for prefixes is worth it
```

Checkpoint sentence:

> Continuous batching increases GPU occupancy; paged KV increases usable memory; prefix caching removes repeated prefill.

---

### 4. Full Serving Design Review Template

Use this when asked to design or defend a self-hosted inference service.

#### Workload

```text
task:
model:
quality threshold:
requests/sec:
p50/p95 prompt tokens:
p50/p95 output tokens:
streaming:
TTFT target:
ITL target:
p95 end-to-end target:
burst factor:
tenant priority:
```

#### Memory Estimate

```text
weights:
KV bytes/token:
expected active tokens:
KV memory:
activation/runtime overhead:
headroom:
fits on GPU:
parallelism needed:
```

#### Throughput Estimate

```text
prompt tokens/sec demand:
output tokens/sec demand:
measured prompt tokens/sec per replica:
measured output tokens/sec per replica:
max safe concurrency per replica:
replicas by prompt:
replicas by decode:
replicas by concurrency:
required replicas:
```

#### Engine Choice

```text
hosted API vs self-hosted:
vLLM/TGI/TensorRT-LLM choice:
reason:
risks:
benchmark required:
fallback:
```

#### Optimization Plan

```text
continuous batching:
paged KV:
prefix caching:
quantization:
parallelism:
autoscaling:
warm pool:
admission control:
```

#### Economics

```text
GPU hourly cost:
expected utilization:
cost per 1M tokens:
cost per successful request:
hosted baseline:
break-even volume:
```

---

### 5. Common Checkpoint Mistakes

| Mistake | Why It Fails | Better Approach |
|---|---|---|
| only counting weights | ignores KV cache and overhead | estimate full VRAM budget |
| using average tokens only | p95 drives OOM and tail latency | collect p50/p95/p99 |
| combining input/output tokens | hides prefill vs decode bottlenecks | separate prompt and output demand |
| choosing vLLM because popular | brand preference is not architecture | benchmark workload and ops fit |
| rejecting hosted API always | self-hosting can be idle and expensive | compare utilization and ops cost |
| choosing TGI blindly | current maintenance status matters | use for existing/HF-fit cases after review |
| maximizing batch size | can violate TTFT/p95 latency | batch within SLA |
| enabling prefix cache globally | can create correctness/security risk | scope by token/model/tenant policy |
| ignoring warmup/cold start | autoscaling arrives too late | warm pool and admission control |
| reporting tokens/sec alone | incomplete without latency/context/batch | report workload-shaped throughput |

---

### 6. Checkpoint Interview Answer

If asked:

> How would you estimate and justify serving an open-weight LLM at scale?

Answer:

I would start by separating the problem into memory fit, throughput fit, and operating economics.

For memory, I would estimate model weight memory from parameter count and precision, then add KV cache, activations, runtime overhead, fragmentation, and headroom. The important part is KV cache: it scales with layers, KV heads, head dimension, precision, sequence length, and active concurrency. A model fitting in VRAM does not mean the workload fits. Long context and high concurrency can exhaust KV memory even if weights load successfully.

For throughput, I would separate prefill and decode. Prompt tokens drive prefill and time to first token. Output tokens drive decode, inter-token latency, and request duration. I would estimate prompt tokens/sec demand and output tokens/sec demand from request rate and token distributions, then compare those to benchmarked per-replica capacity. I would also estimate concurrency with arrival rate times request duration, then check whether active tokens fit in KV memory. The required GPU count is the maximum of prompt throughput, decode throughput, and concurrency constraints, multiplied by burst and headroom factors.

For engine choice, I would compare hosted API, vLLM, and TGI based on workload and team maturity. If traffic is bursty, quality depends on proprietary models, or the team cannot operate GPUs, hosted API may be the best option. If an open-weight model passes evals and traffic is steady enough to utilize GPUs, vLLM is often a strong default because it offers high-throughput serving, continuous batching, paged KV efficiency, and OpenAI-compatible APIs. TGI may be reasonable for existing Hugging Face-aligned deployments, but for greenfield I would account for its maintenance-mode status and compare carefully.

Finally, I would explain throughput optimizations. Continuous batching improves real throughput by keeping active decode work on the GPU and admitting new requests as old ones finish. Paged KV reduces memory waste and fragmentation, allowing more active tokens to fit. Prefix caching reduces repeated prefill work when requests share identical safe prefixes. These optimizations change real serving throughput because live traffic has variable prompt lengths, output lengths, and arrival times.

The final decision would be validated with workload-realistic benchmarks measuring TTFT, ITL, p95/p99 latency, prompt tokens/sec, output tokens/sec, KV memory, queue time, GPU utilization, and cost per successful request.

---

### 7. Checkpoint Active Recall

Answer these without looking:

1. Why is parameter count alone insufficient for GPU memory planning?
2. What are the major VRAM buckets during inference?
3. What formula estimates weight memory?
4. What variables control KV-cache memory?
5. Why does active token count matter more than simple batch size?
6. How do prompt tokens and output tokens stress serving differently?
7. What is TTFT mostly affected by?
8. What is ITL mostly affected by?
9. How do you estimate prompt-token demand?
10. How do you estimate output-token demand?
11. How do you estimate active request concurrency?
12. What determines the required number of replicas?
13. When does hosted API beat self-hosting?
14. When does vLLM make sense?
15. When might TGI make sense?
16. Why does TGI maintenance status matter?
17. What does continuous batching improve?
18. What does paged attention / paged KV improve?
19. When does prefix caching help?
20. Why can prefix caching be unsafe if scoped incorrectly?
21. What metrics should a benchmark report?
22. Why is tokens/sec alone incomplete?
23. Why does self-hosting require utilization?
24. Why does warm capacity matter for GPU services?
25. What is the final lesson of Module P1?

Expected answers:

1. It ignores KV cache, activations, runtime overhead, fragmentation, and headroom.
2. Weights, KV cache, activations/workspace, runtime overhead, headroom.
3. Parameter count times bytes per parameter.
4. Layers, KV heads, head dimension, precision, sequence length, concurrency.
5. KV memory depends on all active prompt plus generated tokens.
6. Prompt tokens drive prefill/TTFT; output tokens drive decode/ITL/duration.
7. Queueing and prefill.
8. Decode throughput and scheduling.
9. Requests/sec times average or percentile input tokens.
10. Requests/sec times average or percentile output tokens.
11. Arrival rate times average request duration.
12. Max of prompt throughput, decode throughput, and concurrency/memory constraints with headroom.
13. Bursty/low traffic, low ops maturity, proprietary quality needs, poor GPU utilization.
14. Open-weight model passes evals, steady traffic, GPU ops capability, need high-throughput API.
15. Existing HF/TGI deployment or strong Hugging Face integration after review.
16. It affects greenfield roadmap and feature investment confidence.
17. GPU occupancy and live-traffic throughput under variable requests.
18. KV memory waste, fragmentation, and usable active-token capacity.
19. Many requests share identical safe prompt prefixes.
20. It may leak or reuse state across wrong model, tenant, tokenizer, or permission context.
21. TTFT, ITL, p95/p99 latency, prompt/output tokens/sec, KV usage, queue time, cost.
22. It hides latency, context length, batch size, hardware, and input/output split.
23. GPUs cost by time, so idle capacity destroys economics.
24. Cold starts can be too slow for interactive SLOs.
25. Serving at scale is prefill/decode math plus KV memory plus scheduling economics.

---

### 8. Final Module P1 Readiness Rubric

You are ready to move on when you can do all of this:

| Skill | Ready Signal |
|---|---|
| prefill/decode reasoning | separate prompt cost from output-token cost |
| memory estimation | estimate weights, KV cache, overhead, and headroom |
| bottleneck diagnosis | identify VRAM, bandwidth, compute, interconnect, CPU, or scheduling limits |
| engine choice | defend vLLM, TGI, TensorRT-LLM, or hosted API by workload |
| batching reasoning | explain continuous batching without hand-waving |
| KV reuse | explain prefix caching benefits and correctness risks |
| quantization | describe memory/speed gain and quality risk |
| parallelism | choose data/tensor/pipeline parallelism for fit vs throughput |
| autoscaling | explain warm pools, cold starts, and admission control |
| capacity planning | produce a rough GPU count and benchmark plan |

Final checkpoint sentence:

> A scalable inference engineer does not ask only "Which model?" They ask "What prompt/output distribution, KV-cache footprint, batching policy, latency SLO, utilization target, engine stack, and failure headroom make this model economically serveable?"

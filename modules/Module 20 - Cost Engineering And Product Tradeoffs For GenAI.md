# Module 20 - Cost Engineering And Product Tradeoffs For GenAI

> **Module time:** 24h
> **Why this module matters:** Strong GenAI engineers do not just make systems work. They make them affordable, fast enough, and worth deploying. This module teaches you to reason about token growth, latency, caching, model routing, product value, and cost-quality trade-offs like an engineer who has to operate the system after the demo.

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic 20.1** | **Token economics and usage analysis (8h)** | |
| 20.1.a | Prompt token accounting and token growth across turns | Done |
| 20.1.b | Retrieval context expansion and tool output explosion | Done |
| 20.1.c | Cost per request, cost per session, and cost per successful task | Done |
| 20.1.d | Logging and reviewing token consumption by system layer | Done |
| **Topic 20.2** | **Latency budgeting and pipeline design (8h)** | |
| 20.2.a | End-to-end latency decomposition across retrieval, reranking, tools, and generation | Done |
| 20.2.b | Streaming, batching, concurrency, and timeout budgets | Done |
| 20.2.c | Should you rerank or increase top-k: tradeoff reasoning | Done |
| 20.2.d | Should you compress context or use a larger model: tradeoff reasoning | Done |
| **Topic 20.3** | **Cost-quality-product decision frameworks (8h)** | |
| 20.3.a | When GenAI is justified vs when deterministic logic is better | Done |
| 20.3.b | Model routing, fallback tiers, and dynamic quality tiers | Done |
| 20.3.c | Retrieval cost vs generation cost vs engineering cost | Done |
| 20.3.d | ROI framing for product, platform, and enterprise systems | Done |
| **Module checkpoint** | Cost engineering and product tradeoffs synthesis | Done |

**Covered so far:**
- 20.1.a - Prompt token accounting and token growth across turns: token-as-metered-bandwidth mental model, input/output/cached token definitions, prompt component accounting, multi-turn conversation growth, quadratic history-cost intuition, response-as-future-input effect, RAG context token budget, tool/schema token overhead, hidden repeated prompt costs, cost formulas with variable pricing, per-request vs per-session cost, token trace schema, growth simulation code sample, conversation cost mini program, hands-on token audit lab, active recall, and interview-ready token economics answer.
- 20.1.b - Retrieval context expansion and tool output explosion: evidence-expansion mental model, top-k and chunk-size multiplication, parent-child expansion cost, metadata and citation overhead, reranker candidate vs final context distinction, tool-result verbosity, API payload trimming, agent observation bloat, repeated tool schemas and results, context packing budgets, field selection, result summarization, compression risks, cost-quality trade-offs, context expansion trace schema, retrieval expansion code sample, tool-output budget mini program, hands-on context/tool audit lab, active recall, and interview-ready context explosion answer.
- 20.1.c - Cost per request, cost per session, and cost per successful task: unit-economics mental model, request/session/task definitions, model-call cost formulas, multi-call workflow accounting, agent step cost, retry and failure cost, evaluation and guardrail cost, amortized indexing and ingestion cost, marginal vs average cost, cost per successful task, value-per-task reasoning, conversion and containment funnels, quality-adjusted cost, product KPI mapping, cost trace schema, unit economics calculator code sample, task-cost simulator mini program, hands-on unit economics lab, active recall, and interview-ready cost analysis answer.
- 20.1.d - Logging and reviewing token consumption by system layer: layer-attribution mental model, trace hierarchy, token categories, request/session/task correlation IDs, product/orchestration/prompt/memory/retrieval/tool/model/guardrail layer accounting, prompt-version and retrieval-version tagging, attribution schema, sampling vs full logging, privacy-safe token observability, token review dashboards, slice analysis, anomaly detection, optimization decision tree, aggregator code sample, layer-cost review mini program, hands-on observability lab, active recall, and interview-ready instrumentation answer.
- 20.2.a - End-to-end latency decomposition across retrieval, reranking, tools, and generation: stopwatch and critical-path mental models, latency vocabulary, user-perceived vs backend latency, serial vs parallel pipeline math, retrieval latency decomposition, reranking latency, tool latency, generation latency, first-token vs full-response latency, guardrail and evaluator latency, p50/p95/p99 analysis, fan-out and tail latency, timeout and fallback budgets, trace schema, span aggregation code sample, critical-path mini program, hands-on latency budget lab, active recall, and interview-ready latency decomposition answer.
- 20.2.b - Streaming, batching, concurrency, and timeout budgets: four-latency-lever mental model, streaming vs completion latency, progressive UX, backpressure, batching throughput trade-offs, dynamic batching, embedding and reranking batch patterns, bounded concurrency, parallel fan-out, rate limits, queueing, head-of-line blocking, timeout hierarchy, deadline propagation, retries, cancellation, fallbacks, circuit breakers, interaction trade-offs, observability schema, bounded-concurrency code sample, timeout-budget simulator, hands-on latency control lab, active recall, and interview-ready pipeline design answer.
- 20.2.c - Should you rerank or increase top-k: tradeoff reasoning: recall-vs-precision mental model, candidate top-k vs final context top-k distinction, retrieval failure taxonomy, when increasing top-k helps, when reranking helps, when both are needed, latency and token-cost equations, context-window pressure, reranker candidate budgets, two-stage retrieval, conditional reranking, business-risk reasoning, metrics such as recall@k, MRR, nDCG, answer groundedness, cost per successful task, experiment design, decision matrix, trace schema, retrieval tradeoff calculator, rerank-vs-top-k simulator, hands-on evaluation lab, active recall, and interview-ready retrieval tradeoff answer.
- 20.2.d - Should you compress context or use a larger model: tradeoff reasoning: evidence-preservation mental model, compression types, larger-context model trade-offs, lossless vs lossy reduction, extractive vs abstractive compression, query-focused compression, map-reduce and hierarchical summarization, long-context failure modes, cost and latency equations, compression latency, cache interactions, when compression helps, when larger context helps, when both are needed, when neither fixes the issue, safety and citation risks, decision matrix, metrics, trace schema, context budget calculator, compression-vs-large-context simulator, hands-on experiment lab, active recall, and interview-ready context strategy answer.
- 20.3.a - When GenAI is justified vs when deterministic logic is better: uncertainty-vs-rules mental model, GenAI fit criteria, deterministic fit criteria, judgment/variation/ambiguity vs exactness/repeatability/auditability, risk and reversibility, hybrid design patterns, rules-first and model-assisted systems, cost-quality-latency-value framing, automation levels, confidence thresholds, human review, decision matrix, ROI and failure-cost reasoning, anti-patterns, trace schema, decision router code sample, ROI simulator, hands-on product decision lab, active recall, and interview-ready justification answer.
- 20.3.b - Model routing, fallback tiers, and dynamic quality tiers: triage mental model, model-tier vocabulary, route-by-difficulty and route-by-risk patterns, cheap-first vs strong-first decisions, confidence thresholds, escalation, fallback taxonomy, quality tiers, latency and budget-aware routing, user-plan and task-value routing, evaluation-driven routing, safety and compliance constraints, router failure modes, observability schema, model router code sample, dynamic-tier simulator, hands-on routing policy lab, active recall, and interview-ready model-routing answer.
- 20.3.c - Retrieval cost vs generation cost vs engineering cost: iceberg mental model, cost categories, online vs offline cost, retrieval infrastructure, embedding and indexing cost, vector database cost, reranking cost, storage and refresh cost, generation token cost, tool and guardrail cost, engineering build and maintenance cost, observability/eval/security cost, buy-vs-build reasoning, fixed vs variable cost, marginal vs average cost, total cost of ownership, cost allocation schema, TCO calculator code sample, architecture cost simulator, hands-on TCO lab, active recall, and interview-ready cost-comparison answer.
- 20.3.d - ROI framing for product, platform, and enterprise systems: value-language mental model, ROI formula, product ROI, platform ROI, enterprise ROI, revenue and retention framing, labor savings, risk reduction, developer productivity, shared capability leverage, adoption and change-management costs, payback period, opportunity cost, leading and lagging metrics, attribution risk, pilot-to-production measurement, ROI decision memo schema, ROI calculator code sample, portfolio simulator, hands-on ROI lab, active recall, and interview-ready executive framing answer.
- Module checkpoint - Cost engineering and product tradeoffs synthesis: unified system-budget mental model, token/retrieval/reranking/generation/engineering cost integration, end-to-end budget schema, decision trees for top-k/rerank/context compression/model routing, cost-quality-latency-risk tradeoff matrix, less-GenAI decision framework, TCO and ROI synthesis, production review checklist, architecture memo template, checkpoint simulator, hands-on design review lab, active recall, and interview-ready module defense.

---

## Topic 20.1: Token Economics and Usage Analysis

> **Topic time:** 8h
> Focus: Understanding where tokens come from, how they grow, why multi-turn systems become expensive, and how to measure usage before optimizing blindly.

GenAI cost engineering starts with accounting.

Before choosing a cheaper model, adding caching, trimming context, or routing requests, you need to know:

```text
what tokens are being sent
what tokens are being generated
what tokens are repeated
what tokens are useful
what tokens are waste
what tokens grow with each turn
```

The central idea:

> You cannot optimize a GenAI system you cannot account for.

---

## Subtopic 20.1.a: Prompt Token Accounting and Token Growth Across Turns

> **Subtopic time:** 2h
> Outcome: You should be able to estimate and explain how prompt tokens accumulate in single-turn and multi-turn GenAI systems, why conversations get expensive over time, and how to instrument token usage before making optimization decisions.

### Add to Knowledge Base

Tokens are the metered unit of most LLM systems.

You pay in tokens.

You wait on tokens.

You hit context limits in tokens.

You debug cost spikes in tokens.

You optimize prompts, retrieval, memory, schemas, tool calls, and model routing by understanding tokens.

The most important mental model:

> A prompt is not just the user's latest message. It is the full payload sent to the model.

That payload may include:

```text
system/developer instructions
few-shot examples
conversation history
retrieved documents
tool definitions
tool results
memory summaries
output schema
the latest user message
```

In multi-turn systems, the expensive part is that old content often gets resent.

Today's assistant answer becomes tomorrow's input tokens.

That is why naive chat history can grow from:

```text
small per-turn cost
```

to:

```text
large cumulative session cost
```

even when each user message is short.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 and learn what counts as input, output, and repeated tokens.
- **Intermediate:** Read sections 7-15 and practice multi-turn growth math.
- **Pro:** Complete the hands-on lab, use the mini program, and prepare the interview-ready token economics answer.

---

### 0. Pre-Question Hook [Beginner]

Imagine a user sends this message:

```text
"Can I get a refund after canceling my annual plan?"
```

That user message may be only a few dozen tokens.

But the actual model request may contain:

```text
system instructions: 900 tokens
developer rules: 600 tokens
conversation history: 3,000 tokens
retrieved policy chunks: 5,000 tokens
tool schemas: 2,000 tokens
output schema: 700 tokens
latest user message: 20 tokens
```

The user thinks:

```text
I asked one short question.
```

The system pays for:

```text
12,000+ input tokens
```

Then the model writes a 500-token answer.

On the next turn, that 500-token answer may be included in the conversation history and become input cost too.

So the first cost-engineering question is:

```text
What exactly did we send to the model?
```

---

### 1. The Intuition [Beginner]

Think of tokens like shipping weight.

Every request ships a box to the model.

The box can contain:

```text
instructions
examples
history
retrieved context
tool definitions
schemas
latest user request
```

The model sends a box back:

```text
generated output
tool call arguments
structured JSON
answer text
```

You usually pay for both directions:

```text
input tokens + output tokens
```

The mistake is assuming the box contains only the user's latest message.

In real systems, the box often contains a lot of repeated material.

Cost engineering starts by opening the box.

---

### 2. Definition [Beginner]

- **Token:** A piece of text or data representation used by a model tokenizer. Tokens are not exactly words; one word may be one token, many tokens, or part of a token depending on language, spelling, symbols, and tokenizer.
- **Input tokens:** Tokens sent to the model as prompt/context/messages/tool definitions.
- **Output tokens:** Tokens generated by the model.
- **Cached input tokens:** Tokens a provider/runtime may bill or process differently when repeated and cacheable. Availability and pricing are provider-specific.
- **Prompt token accounting:** Measuring and attributing input tokens to prompt components.
- **Token growth across turns:** The increase in per-request and cumulative token usage as conversation history, tool results, retrieved context, and prior outputs accumulate.

Core idea:

```text
token cost = what you send + what the model generates + what you repeat over time
```

---

### 3. Why It Exists [Beginner]

Token accounting exists because GenAI systems can become expensive quietly.

Naive system:

```text
Send full prompt.
Send full history.
Send top 10 retrieved chunks.
Send all tool schemas.
Ask for detailed answer.
Repeat every turn.
```

This works in a demo.

It can become costly in production.

Common surprises:

| Surprise | Why It Happens |
|---|---|
| Short user messages cost a lot | system prompt, history, tools, and context dominate |
| Long chats get expensive | prior turns are resent as input |
| RAG cost spikes | retrieved chunks are large or repeated |
| Agent cost spikes | tool schemas and tool results are repeatedly included |
| JSON output costs more than expected | structured output can be verbose |
| Summaries save less than expected | summary plus recent history may still be large |
| Bigger context window increases spend | teams fill available context without measuring value |

Token accounting prevents optimization theater.

Instead of saying:

```text
Use cheaper model.
```

you can say:

```text
70% of input tokens are repeated retrieved context, 18% are tool schemas,
and only 3% are latest user input. We should optimize context packing before model routing.
```

That is a stronger engineering answer.

---

### 4. Reality: Where Tokens Appear In Real Systems [Intermediate]

Tokens appear in more places than beginners expect.

| System Area | Token Source |
|---|---|
| Chat assistant | system prompt, history, user turns, assistant turns |
| RAG | retrieved chunks, citations, source metadata, query rewrites |
| Agents | tool definitions, tool call arguments, tool results, planning text |
| LangGraph workflows | state summaries, node prompts, retry prompts, approval payloads |
| Document AI | OCR text, extracted tables, page summaries, schemas |
| Evaluation | test prompts, judge prompts, rubrics, candidate outputs |
| Observability | trace summaries, debug prompts, replay fixtures |
| Fine-tuning/data generation | synthetic examples, teacher outputs, labels |

Cost engineering is therefore not only:

```text
make prompt shorter
```

It is:

```text
measure token usage by system component
```

This is why token traces matter.

---

### 5. Basic Cost Formula [Intermediate]

Do not hard-code provider prices in architecture reasoning.

Prices change.

Use variables:

```text
input_price_per_million
output_price_per_million
cached_input_price_per_million
```

Basic request cost:

```text
input_cost = input_tokens / 1_000_000 * input_price_per_million
output_cost = output_tokens / 1_000_000 * output_price_per_million
request_cost = input_cost + output_cost
```

If cached tokens are priced separately:

```text
request_cost =
    uncached_input_tokens / 1_000_000 * input_price_per_million
  + cached_input_tokens / 1_000_000 * cached_input_price_per_million
  + output_tokens / 1_000_000 * output_price_per_million
```

Session cost:

```text
session_cost = sum(request_cost for every model call in the user session)
```

Product cost:

```text
daily_cost = average_session_cost * daily_sessions
monthly_cost = daily_cost * active_days_per_month
```

Cost per successful task:

```text
cost_per_success = total_model_cost / successful_tasks
```

This is often more useful than raw token cost.

Cheap failures are still waste.

---

### 6. Prompt Component Accounting [Intermediate]

A prompt should be broken into components.

Example:

| Component | Example | Token Behavior |
|---|---|---|
| system instructions | role, safety, style, policy | repeated every call |
| developer/task instructions | task contract, routing rules | repeated per node/call |
| few-shot examples | demonstrations | repeated unless cached/removed |
| conversation history | prior user/assistant turns | grows across turns |
| retrieved context | chunks, metadata, citations | changes per query, often large |
| tool definitions | names, descriptions, schemas | repeated in tool-capable calls |
| tool results | API responses, search results | can become history/context |
| output schema | JSON schema or format instructions | repeated per structured call |
| latest user input | current request | usually small |
| model output | answer/tool call JSON | generated now, may become future input |

Instrument token usage like:

```json
{
  "request_id": "req_20_001",
  "total_input_tokens": 12340,
  "components": {
    "system_prompt": 920,
    "developer_instructions": 610,
    "few_shot_examples": 1400,
    "conversation_history": 3100,
    "retrieved_context": 4920,
    "tool_schemas": 980,
    "output_schema": 370,
    "latest_user_message": 40
  },
  "output_tokens": 520
}
```

This trace instantly shows where to optimize.

---

### 7. Single-Turn vs Multi-Turn Cost [Intermediate]

Single-turn request:

```text
system prompt + user message + context -> output
```

Multi-turn chat:

```text
turn 1:
    system + user_1 -> assistant_1

turn 2:
    system + user_1 + assistant_1 + user_2 -> assistant_2

turn 3:
    system + user_1 + assistant_1 + user_2 + assistant_2 + user_3 -> assistant_3
```

The important part:

```text
assistant_1 is output in turn 1
assistant_1 becomes input in turn 2
```

So generated tokens can be paid for twice:

```text
once as output
again as future input
```

This is why verbose assistant answers increase future cost.

The system is not only paying to say the words.

It may pay to remember them later.

---

### 8. Token Growth Across Turns [Intermediate]

Assume:

```text
S = fixed system/developer prompt tokens
U = average user message tokens per turn
A = average assistant answer tokens per turn
n = number of turns
```

If each call includes full prior conversation history:

Turn 1 input:

```text
S + U
```

Turn 2 input:

```text
S + U + A + U
```

Turn 3 input:

```text
S + U + A + U + A + U
```

General turn t input:

```text
S + t * U + (t - 1) * A
```

Cumulative input over n turns:

```text
n * S + U * n(n + 1) / 2 + A * n(n - 1) / 2
```

Cumulative output:

```text
n * A
```

The cumulative input grows roughly quadratically with turn count when full history is resent.

Plain English:

> Every turn carries the weight of many previous turns.

That is why long conversations need memory strategy, summarization, truncation, retrieval, or state design.

---

### 9. Worked Example [Intermediate]

Assume:

```text
system/developer prompt = 1,000 tokens
average user message = 100 tokens
average assistant answer = 300 tokens
turns = 6
```

Per-turn input:

| Turn | Input Formula | Input Tokens | Output Tokens |
|---|---|---:|---:|
| 1 | 1000 + 1*100 + 0*300 | 1,100 | 300 |
| 2 | 1000 + 2*100 + 1*300 | 1,500 | 300 |
| 3 | 1000 + 3*100 + 2*300 | 1,900 | 300 |
| 4 | 1000 + 4*100 + 3*300 | 2,300 | 300 |
| 5 | 1000 + 5*100 + 4*300 | 2,700 | 300 |
| 6 | 1000 + 6*100 + 5*300 | 3,100 | 300 |

Cumulative:

```text
input tokens = 12,600
output tokens = 1,800
total tokens = 14,400
```

Now add RAG context:

```text
retrieved context = 4,000 tokens per turn
```

New cumulative input:

```text
12,600 + 6 * 4,000 = 36,600
```

One design choice tripled input cost.

This is why "just retrieve more chunks" is not free.

---

### 10. Hidden Token Growth Sources [Intermediate]

Token growth often hides in places engineers do not inspect.

| Hidden Source | Why It Grows |
|---|---|
| conversation history | prior turns included every call |
| verbose assistant answers | become future history |
| tool results | long API responses added to context |
| tool schemas | repeated for every tool-capable call |
| retrieved documents | large chunks repeated each turn |
| memory summaries | summary plus raw history both included |
| few-shot examples | copied into every request |
| chain-of-thought-like scratchpads | internal reasoning text stored in state/history |
| structured schemas | large JSON schema repeated |
| error retries | failed calls pay tokens too |
| evaluators/judges | every eval may call another model |

Cost debugging question:

```text
Which repeated token block appears in every call?
```

Often the biggest win is not shortening the user prompt.

It is removing repeated blocks that do not help the task.

---

### 11. Token Budget By Product Surface [Intermediate]

Different product surfaces deserve different token budgets.

| Product Surface | Token Strategy |
|---|---|
| search autocomplete | tiny prompts, low latency, minimal output |
| customer support answer | moderate retrieval, concise cited answer |
| legal/policy RAG | higher retrieval recall, citations, slower acceptable |
| coding assistant | larger context may be justified |
| long-running agent | state summaries, tool scoping, checkpointed memory |
| document extraction | schema plus source text, tight validation |
| internal analyst assistant | can tolerate more tokens if task value is high |

Cost engineering is product-specific.

The question is not:

```text
How do we minimize tokens?
```

The better question:

```text
How many tokens are worth spending for this product outcome?
```

---

### 12. Per-Request vs Per-Session Cost [Pro]

A request may look cheap.

A session may not.

Example:

```text
request cost = $0.002
average session = 18 model calls
daily sessions = 50,000
```

Daily model cost:

```text
0.002 * 18 * 50,000 = $1,800/day
```

Monthly:

```text
~$54,000/month
```

The exact numbers depend on provider pricing, but the pattern matters:

```text
small request cost * many calls * many users = real budget
```

For agents, count:

```text
planning calls
tool-selection calls
tool-result interpretation calls
retry calls
validation/repair calls
final answer calls
evaluator calls
```

An "agent task" may be many model calls.

Always estimate:

```text
cost per successful task
```

not just:

```text
cost per model call
```

---

### 13. Cost Is Not Only Money [Intermediate]

Tokens affect:

| Dimension | Token Effect |
|---|---|
| cost | more tokens usually cost more |
| latency | longer inputs and outputs can take longer |
| context risk | more context can add noise/conflicts |
| quality | too little context can miss evidence |
| privacy | more context may expose more data |
| reliability | long prompts can bury instructions |
| throughput | large requests consume more capacity |
| observability | token attribution helps explain spikes |

Cost engineering is trade-off engineering.

Token reduction is good only if it does not break:

- quality
- safety
- answerability
- citations
- product value

Strong sentence:

> "I would reduce tokens by removing low-value repeated context, not by blindly cutting evidence needed for correctness."

---

### 14. Practical Optimization Levers [Intermediate]

After accounting, optimization becomes targeted.

| Token Driver | Optimization Lever |
|---|---|
| long system prompt | compress stable instructions, remove duplication |
| few-shot examples | keep only high-value examples or route by task |
| long history | summarize, window, or store structured state |
| verbose assistant answers | set concise answer contract |
| repeated RAG chunks | retrieve fewer/better chunks, parent-child retrieval |
| large chunks | improve chunking and context packing |
| tool schemas | expose tools only where needed |
| long tool results | summarize or select fields |
| large output schema | simplify schema, split task |
| retries | fix validation, tool errors, and model/schema mismatch |
| evaluator calls | sample, batch, or use deterministic checks where possible |

Do not optimize before measuring.

The order:

```text
measure -> attribute -> rank drivers -> experiment -> verify quality -> deploy
```

---

### 15. Token Trace Schema [Pro]

A production token trace should include:

```json
{
  "request_id": "req_20_001",
  "session_id": "session_77",
  "turn_index": 4,
  "model": "model_name_or_route",
  "prompt_template_version": "support_answer_v3",
  "input_tokens": 9800,
  "output_tokens": 420,
  "cached_input_tokens": 3000,
  "token_components": {
    "system_prompt": 850,
    "developer_instructions": 420,
    "conversation_history": 2500,
    "retrieved_context": 4300,
    "tool_schemas": 900,
    "output_schema": 450,
    "latest_user_message": 80,
    "other_overhead": 300
  },
  "latency_ms": 1850,
  "estimated_cost": 0.0,
  "task_success": true,
  "quality_tags": ["grounded", "cited"],
  "optimization_notes": []
}
```

Do not treat `estimated_cost` as permanent unless it is computed from current pricing configuration.

Store:

```text
tokens
model route
pricing version
component attribution
```

Then compute cost from pricing tables separately.

This avoids stale cost math when prices change.

---

### 16. Code Sample: Simple Token Growth Estimator

This estimator uses token counts you provide.

It does not need a tokenizer.

```python
def estimate_full_history_tokens(turns, system_tokens, user_tokens_per_turn, assistant_tokens_per_turn):
    rows = []
    cumulative_input = 0
    cumulative_output = 0

    for turn in range(1, turns + 1):
        input_tokens = (
            system_tokens
            + turn * user_tokens_per_turn
            + (turn - 1) * assistant_tokens_per_turn
        )
        output_tokens = assistant_tokens_per_turn

        cumulative_input += input_tokens
        cumulative_output += output_tokens

        rows.append(
            {
                "turn": turn,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cumulative_input": cumulative_input,
                "cumulative_output": cumulative_output,
            }
        )

    return rows


def main():
    rows = estimate_full_history_tokens(
        turns=6,
        system_tokens=1000,
        user_tokens_per_turn=100,
        assistant_tokens_per_turn=300,
    )

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
Even if each turn is small, cumulative input grows quickly when full history is resent.
```

---

### 17. Mini Program: Conversation Cost Simulator

This mini program estimates cost using variable prices.

Use current provider pricing in your own environment when applying it.

```python
def request_cost(input_tokens, output_tokens, input_price_per_million, output_price_per_million):
    input_cost = input_tokens / 1_000_000 * input_price_per_million
    output_cost = output_tokens / 1_000_000 * output_price_per_million
    return input_cost + output_cost


def simulate_conversation(
    turns,
    system_tokens,
    user_tokens,
    assistant_tokens,
    rag_tokens_per_turn,
    input_price_per_million,
    output_price_per_million,
):
    total_cost = 0.0
    total_input = 0
    total_output = 0

    for turn in range(1, turns + 1):
        history_tokens = turn * user_tokens + (turn - 1) * assistant_tokens
        input_tokens = system_tokens + history_tokens + rag_tokens_per_turn
        output_tokens = assistant_tokens

        cost = request_cost(
            input_tokens,
            output_tokens,
            input_price_per_million,
            output_price_per_million,
        )

        total_cost += cost
        total_input += input_tokens
        total_output += output_tokens

        print(
            f"turn={turn} input={input_tokens} output={output_tokens} "
            f"cost=${cost:.6f}"
        )

    print("---")
    print(f"total_input={total_input}")
    print(f"total_output={total_output}")
    print(f"total_cost=${total_cost:.6f}")


if __name__ == "__main__":
    simulate_conversation(
        turns=6,
        system_tokens=1000,
        user_tokens=100,
        assistant_tokens=300,
        rag_tokens_per_turn=4000,
        input_price_per_million=1.00,
        output_price_per_million=3.00,
    )
```

Expected lesson:

```text
RAG context and history growth can dominate cost even when the user messages are small.
```

---

### 18. Hands-On Lab: Token Audit For One GenAI Flow [Pro]

#### Build

Choose one flow:

```text
support RAG answer
agent with tools
document extraction
chat assistant
evaluation judge
```

For one request, estimate:

```text
system prompt tokens
developer/task instruction tokens
few-shot tokens
conversation history tokens
retrieved context tokens
tool schema tokens
tool result tokens
output schema tokens
latest user message tokens
output tokens
```

#### Break

Create three versions:

1. Full version: everything included.
2. Lean version: remove duplicated or low-value context.
3. Risky version: remove too much evidence or schema.

#### Measure

For each version, record:

```text
input tokens
output tokens
estimated cost
latency expectation
answer quality
citation quality
safety risk
```

#### Defend

Write:

```text
The biggest token driver is <component>.
I would reduce it by <change>.
I would not reduce <component> because it protects <quality/safety>.
The success metric is <cost/latency target> without degrading <quality metric>.
```

This is how cost work becomes product-aware instead of reckless.

---

### 19. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| counting only user message | misses most input tokens | account for full rendered prompt |
| ignoring output tokens | generation can be expensive and becomes future input | track output and future-history impact |
| ignoring multi-turn growth | session cost surprises you | model per-session cost |
| adding more context blindly | raises cost and can add noise | measure context usefulness |
| sending all tool schemas | repeated overhead | expose tools by node/task |
| storing all history forever | quadratic input growth | summarize/window/structured state |
| optimizing only price | may hurt latency or quality | optimize cost per successful task |
| hard-coding prices in docs | prices change | use pricing variables/config |
| no component attribution | cannot choose targeted optimizations | log token components |

---

### 20. Practical Interview Question [Intermediate]

> You are designing a multi-turn RAG assistant. Users ask short questions, but model costs are much higher than expected. How would you analyze prompt token accounting and token growth across turns?

---

### 21. Strong Answer [Pro]

I would start by measuring the full rendered request, not just the latest user message. For each model call, I would break input tokens into components: system and developer instructions, few-shot examples, conversation history, retrieved context, tool definitions, tool results, output schema, and latest user input. I would also track output tokens because verbose answers become future input in multi-turn conversations.

Then I would model per-turn and per-session growth. In a naive full-history chat, turn `t` includes the fixed prompt, all user messages so far, and all previous assistant answers. That means cumulative input grows roughly quadratically with the number of turns. If we add RAG context every turn, retrieved chunks can dominate cost even when user messages are short.

I would instrument traces with token component attribution, model route, prompt version, context builder version, latency, quality tags, and pricing version. Then I would identify the biggest token drivers. For example, if retrieved context is 60% of input tokens, I would tune retrieval and context packing before worrying about the latest user message. If tool schemas are large, I would expose tools only in nodes that need them. If history dominates, I would use summarization, sliding windows, or structured state.

I would not blindly cut tokens. I would compare cost reduction against answer quality, citation correctness, safety, and task success. The product metric should be cost per successful task, not just cost per model call. A cheaper request that fails more often can be more expensive in practice.

---

### 22. Active Recall [Beginner]

Answer these without looking:

1. What is a token?
2. What are input tokens?
3. What are output tokens?
4. Why is the user's latest message not the full prompt?
5. What prompt components should be accounted for?
6. Why do assistant answers affect future cost?
7. Why can full-history chat create quadratic cumulative input growth?
8. What is the basic cost formula with variable prices?
9. Why should pricing be stored as configuration?
10. What is cost per successful task?
11. Why can RAG context dominate cost?
12. Why can tool schemas dominate agent cost?
13. Why is output schema not free?
14. What is a token trace?
15. Why is component attribution important?
16. What are hidden token growth sources?
17. Why is minimizing tokens not always correct?
18. What is the difference between per-request and per-session cost?
19. What should be optimized before changing models?
20. What is the final lesson of token accounting?

Expected answers:

1. A model tokenizer unit, not exactly a word.
2. Tokens sent to the model in prompt/context/messages/tools/schema.
3. Tokens generated by the model.
4. The full request may include instructions, history, context, tools, schemas, and memory.
5. System, developer, examples, history, RAG context, tools, results, schema, user input.
6. They are often resent as conversation history in later turns.
7. Each turn includes many previous turns, so cumulative input grows with repeated history.
8. Input tokens times input rate plus output tokens times output rate.
9. Provider pricing changes, but token traces remain useful.
10. Total model cost divided by successful completed tasks.
11. Retrieved chunks are often thousands of tokens per turn.
12. Tool definitions and JSON schemas may be repeated in many calls.
13. Schema text and structured output both consume tokens.
14. A log of token usage by request and component.
15. It shows which part of the prompt is actually driving cost.
16. History, retrieved context, tool results, schemas, retries, judges, summaries.
17. Cutting needed evidence or constraints can reduce cost but harm quality/safety.
18. Per-request is one model call; per-session includes all calls in a user workflow.
19. Measure and reduce low-value repeated tokens, context packing, history, tools, retries.
20. Open the box: measure what you send, what you generate, and what you repeat.

---

### 23. Revision Notes

- **One-line summary:** Token accounting means measuring all input, output, and repeated tokens by component so cost can be optimized without damaging quality.
- **Three keywords:** input, output, repetition.
- **One interview trap:** Estimating cost from the latest user message instead of the full rendered prompt and session.
- **One memory trick:** System, history, context, tools, schema, user, output, repeat.

Final takeaway:

> Token cost is not caused by the user's latest message alone. It is caused by the full prompt payload, generated output, and everything you choose to repeat across turns.

---

## Subtopic 20.1.b: Retrieval Context Expansion and Tool Output Explosion

> **Subtopic time:** 2h
> Outcome: You should be able to explain why RAG and tool-using systems often cost more than expected, trace where context expands, and design budgets that keep evidence useful without flooding the model.

### Add to Knowledge Base

Most GenAI cost surprises come from expansion.

A user asks one short question.

The system expands it into:

```text
rewritten queries
top-k retrieved chunks
parent documents
metadata
citations
reranker candidates
tool schemas
tool calls
tool results
agent observations
summaries
validation retries
```

The expansion may be useful.

But if it is uncontrolled, cost and latency climb quickly.

The core mental model:

> Retrieval and tools are evidence systems. Evidence is valuable, but every piece of evidence has a token carrying cost.

RAG failure mode:

```text
retrieve too little -> missing evidence -> wrong answer
retrieve too much -> high cost + noisy context -> worse answer
```

Tool failure mode:

```text
return too little -> model lacks facts
return too much -> model pays to read irrelevant JSON
```

Cost engineering is not about starving the model.

It is about sending the smallest sufficient evidence package.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 and learn why RAG/tool systems expand.
- **Intermediate:** Read sections 7-15 and practice context/tool-output budgeting.
- **Pro:** Complete the hands-on lab, use the mini program, and prepare the interview-ready answer.

---

### 0. Pre-Question Hook [Beginner]

User asks:

```text
"Can contractors download SOC2 evidence?"
```

The user message is tiny.

The RAG pipeline may add:

```text
query rewrite: 30 tokens
10 retrieved chunks * 700 tokens = 7,000 tokens
metadata per chunk = 1,000 tokens
citations/source labels = 500 tokens
parent sections for top 3 chunks = 4,500 tokens
tool schema for compliance lookup = 1,200 tokens
tool result = 2,500 tokens
output schema = 500 tokens
```

One short question became:

```text
17,000+ tokens before answer generation
```

Now multiply by:

```text
multi-turn history
agent retries
evaluation judges
daily traffic
```

This is why context expansion must be designed, not guessed.

---

### 1. The Intuition [Beginner]

Retrieval is like packing a briefcase for the model.

Too little:

```text
the model lacks the evidence
```

Too much:

```text
the model has to sort through a messy pile
```

Tool calls are similar.

If a tool returns an entire customer record when the model only needs:

```text
plan_type
account_status
contract_start_date
```

then the system pays for:

```text
addresses
notes
audit logs
internal IDs
unused metadata
raw nested JSON
```

The cost problem is not the tool call itself.

It is the size of the observation you feed back to the model.

Key intuition:

```text
Retrieval expands evidence.
Tools expand observations.
Agents repeat both.
```

---

### 2. Definition [Beginner]

- **Retrieval context expansion:** The increase in prompt tokens caused by retrieved chunks, metadata, parent sections, citations, reranking candidates, and context reconstruction.
- **Tool output explosion:** The increase in prompt tokens caused by verbose tool results, raw API payloads, repeated observations, error traces, and untrimmed JSON.
- **Evidence budget:** A token budget allocated to the context or tool results needed to support a task.
- **Context packing:** Selecting, ordering, trimming, and formatting evidence before sending it to the model.
- **Core idea:** Retrieval and tools should return enough evidence to solve the task, but not raw, unbounded data.

Short version:

```text
Useful evidence is not the same as unlimited evidence.
```

---

### 3. Why It Exists [Beginner]

This topic exists because RAG and tool systems often look cheap in diagrams.

Diagram:

```text
query -> retrieve -> answer
```

Actual prompt:

```text
query
system prompt
chat history
retrieved chunk 1
retrieved chunk 2
...
retrieved chunk 10
source metadata
tool schemas
tool results
output schema
```

Agent diagram:

```text
think -> tool -> observe -> answer
```

Actual session:

```text
planner call
tool schema tokens
tool call JSON
tool raw result
observation summary
next planner call with prior observation
retry call
final answer call
```

The cost is in the expanded payload.

If engineers do not budget expansion, they often respond by:

```text
using cheaper models
```

when the better first fix is:

```text
stop sending 8,000 low-value tokens every call
```

---

### 4. Retrieval Expansion Formula [Intermediate]

Basic retrieval context size:

```text
retrieval_context_tokens =
    top_k * average_chunk_tokens
  + top_k * average_metadata_tokens
  + citation_format_tokens
```

If parent expansion is used:

```text
retrieval_context_tokens =
    child_top_k * avg_child_chunk_tokens
  + parent_top_k * avg_parent_section_tokens
  + metadata_tokens
```

If multiple query rewrites are used:

```text
retrieval_work_tokens =
    rewrite_prompt_tokens
  + rewrite_output_tokens
  + retrieval_context_tokens
```

If reranking is model-based, distinguish:

```text
reranker_candidate_tokens != final_answer_context_tokens
```

Reranker may process:

```text
50 candidates * 300 tokens = 15,000 tokens
```

Final answer may receive:

```text
5 chunks * 600 tokens = 3,000 tokens
```

Both matter.

Do not account only for final context if reranking uses a model.

---

### 5. Top-k and Chunk Size Multiplication [Intermediate]

The fastest way to grow RAG cost:

```text
increase top-k
increase chunk size
increase metadata
```

Example:

| top-k | avg chunk tokens | chunk tokens |
|---:|---:|---:|
| 3 | 500 | 1,500 |
| 5 | 500 | 2,500 |
| 10 | 500 | 5,000 |
| 10 | 900 | 9,000 |
| 20 | 900 | 18,000 |

Cost intuition:

```text
top_k doubles -> context roughly doubles
chunk size doubles -> context roughly doubles
both double -> context roughly quadruples
```

But quality does not necessarily double.

More context can:

- include more relevant evidence
- include more irrelevant evidence
- bury the decisive chunk
- introduce conflicts
- increase latency
- increase cost
- increase privacy exposure

Strong engineering question:

```text
What is the marginal quality gain of each extra chunk?
```

---

### 6. Parent-Child Expansion Cost [Intermediate]

Parent-child retrieval is often useful:

```text
retrieve small child chunks
send larger parent sections for context
```

But it can expand quickly.

Example:

```text
retrieve 8 child chunks * 180 tokens = 1,440 tokens
expand to 5 parent sections * 1,200 tokens = 6,000 tokens
metadata/citation = 800 tokens
```

Final context:

```text
6,800 tokens
```

Potential issue:

```text
multiple child chunks may map to the same parent
```

Without deduplication:

```text
same parent section repeated
```

Mitigation:

- deduplicate parent sections
- cap parent expansions
- include only relevant parent windows
- preserve heading path instead of full parent when enough
- send parent summary plus cited child span

Good rule:

```text
Expand only when the child chunk is insufficient to answer.
```

---

### 7. Metadata and Citation Overhead [Intermediate]

Metadata is useful.

It helps with:

- source authority
- freshness
- permissions
- section path
- citation
- conflict resolution

But metadata can become verbose.

Bad metadata packing:

```json
{
  "id": "contractor_soc2_restrictions#2",
  "source": {
    "internal_document_uuid": "a-long-id",
    "crawler_job_id": "job-2026-06-25-08-45-22",
    "raw_storage_path": "s3://...",
    "embedding_model_version": "..."
  },
  "acl": {
    "long_nested_acl_details": "..."
  }
}
```

Better model-facing metadata:

```text
Evidence ID: contractor_soc2_restrictions#2
Source: Contractor Compliance Access Policy
Authority: Official policy
Effective: 2026-04-01
Applies to: contractors
```

Internal metadata belongs in traces.

Model-facing metadata should be:

```text
minimal, useful, and task-relevant
```

---

### 8. Reranker Candidate Cost vs Final Context Cost [Pro]

Reranking can improve quality.

It can also add hidden cost.

Two different budgets:

```text
candidate budget:
    how much text the reranker sees

final context budget:
    how much text the answer model sees
```

Example:

```text
first-stage retrieval returns 80 chunks
reranker sees top 40 chunks * 250 tokens = 10,000 tokens
answer model sees top 5 chunks * 700 tokens = 3,500 tokens
```

If the reranker is cross-encoder or LLM-based, candidate cost matters.

Reranker optimization levers:

- pre-trim chunks for reranker
- rerank summaries or titles first
- rerank fewer candidates
- use cheaper reranker
- use lexical filters before reranking
- rerank only high-risk/high-value queries
- cache rerank results for repeated queries

Quality caution:

```text
Do not reduce reranker candidates without measuring recall and final answer quality.
```

---

### 9. Tool Output Explosion [Intermediate]

Tool output explosion happens when the system feeds raw tool/API responses back into the model.

Example raw customer tool result:

```json
{
  "customer_id": "C-44",
  "name": "Example Corp",
  "plan": "enterprise",
  "billing_history": [... 200 records ...],
  "support_tickets": [... 80 tickets ...],
  "audit_log": [... 500 events ...],
  "internal_notes": "...",
  "feature_flags": {...},
  "permissions": {...},
  "metadata": {...}
}
```

Question:

```text
"Is this customer eligible for enterprise support escalation?"
```

Needed fields:

```json
{
  "customer_id": "C-44",
  "plan": "enterprise",
  "support_status": "active",
  "escalation_allowed": true
}
```

The model does not need the whole customer universe.

Tool output should be shaped for the next decision.

---

### 10. Tool Result Field Selection [Intermediate]

Design tools to return task-shaped outputs.

Bad tool design:

```text
get_customer_everything(customer_id)
```

Better:

```text
get_customer_escalation_status(customer_id)
```

Or:

```text
get_customer(customer_id, fields=["plan", "support_status", "escalation_allowed"])
```

Field-selection rules:

```text
return stable IDs
return decision-relevant fields
return source/effective timestamps when needed
return typed status/error fields
omit raw internal logs unless requested
summarize lists before sending to model
```

Tool output budget:

```text
max_observation_tokens_per_tool
max_total_tool_observation_tokens_per_task
```

If a tool result exceeds budget:

```text
summarize deterministically
select top fields
ask a narrower tool
route to pagination
do not dump raw payload into context
```

---

### 11. Agent Observation Bloat [Intermediate]

Agents often accumulate observations:

```text
tool result 1
tool result 2
tool result 3
planner notes
error messages
retry outputs
final answer draft
```

Then each next step receives all prior observations.

This creates a loop:

```text
tool output becomes observation
observation becomes history
history becomes next prompt
next prompt costs more
```

Observation bloat signs:

- same tool result repeated across turns
- long JSON pasted into every planner call
- error stack traces included repeatedly
- old observations no longer relevant
- tool results not summarized into state
- state stores raw payload instead of selected fields

Fix pattern:

```text
raw tool result -> structured state fields -> concise observation summary
```

Example:

```text
Raw:
    4,000-token ticket history

State:
    ticket_id=T-1042
    customer_plan=enterprise
    latest_issue=billing dispute
    escalation_allowed=true

Observation to model:
    "Ticket T-1042 belongs to an active enterprise customer and is eligible for billing escalation."
```

---

### 12. Repeated Tool Schemas [Intermediate]

Tool schemas can be large.

If every call exposes every tool:

```text
30 tools * large JSON schemas = huge repeated overhead
```

Better:

```text
node-scoped tool exposure
```

Examples:

| Node | Tools Exposed |
|---|---|
| retrieve_policy | search_policy, get_policy |
| load_ticket | get_ticket, search_customer |
| eligibility_check | get_customer_plan, get_contract |
| execute_action | update_ticket_status only after approval |

Benefits:

- fewer tokens
- less tool confusion
- safer side-effect boundaries
- easier debugging

Cost and safety align here.

Reducing visible tools often improves both.

---

### 13. Context Packing Budgets [Pro]

Create explicit budgets.

Example:

```text
total input budget: 12,000 tokens

system/developer: 1,500
conversation state: 1,500
retrieved evidence: 5,000
tool schemas: 1,000
tool observations: 1,500
output schema: 500
reserved margin: 1,000
```

Budgeting forces trade-offs.

If retrieved evidence needs 8,000 tokens, something else must shrink:

- history window
- tool schemas
- output schema
- chunk count
- metadata verbosity

Budget questions:

```text
What is the max context per request?
What is the max context per session?
What is the max tool output per call?
What is the max retrieved evidence per answer?
What is the max output length?
What happens when budget is exceeded?
```

No budget means accidental expansion.

---

### 14. Compression and Summarization Risks [Pro]

Summarization can reduce tokens.

It can also remove decisive facts.

Compression risks:

| Compression | Risk |
|---|---|
| summarize retrieved chunks | loses exact evidence/citation |
| summarize tool results | drops fields needed for decision |
| summarize conversation history | loses user constraints |
| truncate long chunks | removes exception at end |
| select top sentences | misses table/header meaning |
| compress JSON to prose | loses type precision |

Safe compression patterns:

- preserve source IDs
- preserve exact quoted spans for critical claims
- preserve numeric/date fields exactly
- preserve permission/scope metadata
- preserve uncertainty and missing fields
- validate compressed output against task schema
- keep raw payload in trace, not prompt

Strong sentence:

> "I would compress observations for the model, but keep raw evidence available for audit and replay."

---

### 15. Cost-Quality Trade-off Matrix [Intermediate]

| Change | Cost Impact | Quality Risk | When Worth It |
|---|---|---|---|
| reduce top-k | lower | missing evidence | low-risk or high-precision queries |
| smaller chunks | lower per chunk | missing context | when heading/parent context preserved |
| parent expansion | higher | less missing context | complex policy/code/table questions |
| remove metadata | lower | weaker citations/conflict handling | only if metadata not used |
| summarize tool result | lower | missing key fields | if schema preserves decision fields |
| node-scoped tools | lower | missing tool if route wrong | when graph routing is reliable |
| citations-only fallback | lower generation risk | less user-friendly | when answer synthesis is risky |
| model reranker | higher | better ranking | high-value or high-risk answers |

Cost engineering principle:

```text
Cut low-value tokens first.
Protect high-value evidence tokens.
```

---

### 16. Context Expansion Trace Schema [Pro]

Trace both requested and included evidence.

```json
{
  "request_id": "req_20_102",
  "query": "Can contractors download SOC2 evidence?",
  "retrieval": {
    "child_top_k": 12,
    "avg_child_tokens": 180,
    "parent_sections_added": 4,
    "avg_parent_tokens": 950,
    "metadata_tokens": 420,
    "final_retrieval_context_tokens": 6380
  },
  "tools": {
    "visible_tool_schema_tokens": 1250,
    "tool_calls": [
      {
        "tool_name": "get_compliance_access_status",
        "raw_result_tokens": 2400,
        "model_facing_result_tokens": 220,
        "fields_selected": ["role", "allowed_actions", "source_policy_id"]
      }
    ],
    "total_model_facing_tool_tokens": 220
  },
  "budget": {
    "retrieval_budget": 5000,
    "tool_observation_budget": 1000,
    "budget_exceeded": true
  }
}
```

This trace answers:

```text
Where did the context expand?
Was the expansion intentional?
Did raw tool output get trimmed?
Did retrieval exceed its budget?
```

---

### 17. Code Sample: Retrieval Expansion Estimator

```python
def estimate_retrieval_context(
    top_k,
    avg_chunk_tokens,
    metadata_tokens_per_chunk,
    parent_sections,
    avg_parent_tokens,
    citation_overhead_tokens,
):
    chunk_tokens = top_k * avg_chunk_tokens
    metadata_tokens = top_k * metadata_tokens_per_chunk
    parent_tokens = parent_sections * avg_parent_tokens

    total = chunk_tokens + metadata_tokens + parent_tokens + citation_overhead_tokens

    return {
        "chunk_tokens": chunk_tokens,
        "metadata_tokens": metadata_tokens,
        "parent_tokens": parent_tokens,
        "citation_overhead_tokens": citation_overhead_tokens,
        "total_retrieval_context_tokens": total,
    }


estimate = estimate_retrieval_context(
    top_k=10,
    avg_chunk_tokens=600,
    metadata_tokens_per_chunk=80,
    parent_sections=3,
    avg_parent_tokens=1200,
    citation_overhead_tokens=300,
)

print(estimate)
```

Expected lesson:

```text
Top-k, chunk size, metadata, and parent expansion multiply quickly.
```

---

### 18. Mini Program: Tool Output Budget Checker

```python
def trim_tool_result(raw_result, allowed_fields):
    return {field: raw_result[field] for field in allowed_fields if field in raw_result}


def estimate_tokens_from_chars(text):
    # Rough planning estimate only. Real systems should use the model tokenizer.
    return max(1, len(text) // 4)


def check_tool_budget(tool_name, raw_result, allowed_fields, max_tokens):
    model_result = trim_tool_result(raw_result, allowed_fields)

    raw_tokens = estimate_tokens_from_chars(str(raw_result))
    model_tokens = estimate_tokens_from_chars(str(model_result))

    return {
        "tool_name": tool_name,
        "raw_tokens_estimate": raw_tokens,
        "model_facing_tokens_estimate": model_tokens,
        "saved_tokens_estimate": raw_tokens - model_tokens,
        "within_budget": model_tokens <= max_tokens,
        "model_facing_result": model_result,
    }


def main():
    raw_customer = {
        "customer_id": "C-44",
        "plan": "enterprise",
        "support_status": "active",
        "escalation_allowed": True,
        "billing_history": ["invoice"] * 200,
        "audit_log": ["event"] * 500,
        "internal_notes": "Long internal notes..." * 100,
    }

    report = check_tool_budget(
        tool_name="get_customer",
        raw_result=raw_customer,
        allowed_fields=["customer_id", "plan", "support_status", "escalation_allowed"],
        max_tokens=120,
    )

    print(report)


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
Tools can return rich raw data internally while exposing only decision-relevant fields to the model.
```

---

### 19. Hands-On Lab: Context and Tool Output Audit [Pro]

#### Build

Choose one flow:

```text
RAG answer
support agent
document extraction
workflow assistant
```

Measure:

```text
top-k
average chunk tokens
metadata tokens
parent expansion tokens
reranker candidate tokens
final context tokens
tool schema tokens
raw tool result tokens
model-facing tool result tokens
conversation observation tokens
```

#### Break

Create three versions:

1. **Naive:** send top-k chunks and raw tool results.
2. **Budgeted:** cap retrieval context and trim tool fields.
3. **Too aggressive:** over-trim context and tool results.

#### Measure

For each version:

```text
total input tokens
estimated cost
latency expectation
answer correctness
citation support
tool decision correctness
missing-evidence rate
```

#### Defend

Write:

```text
The biggest expansion source was <retrieval/tool/observation>.
I reduced it by <field selection/context packing>.
I protected quality by preserving <evidence/metadata/schema>.
The success metric is <cost reduction> while maintaining <quality threshold>.
```

---

### 20. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| increasing top-k blindly | cost/noise rises quickly | measure marginal recall gain |
| sending raw tool JSON | pays for irrelevant fields | return model-facing selected fields |
| counting only final context | reranker may process many candidates | account for reranker candidate cost |
| expanding every parent | repeated parent sections bloat context | deduplicate and cap parent expansion |
| removing all metadata | weakens citations/freshness/permissions | keep compact task-relevant metadata |
| summarizing everything | may drop exact evidence | preserve spans, IDs, numbers, dates |
| exposing all tools | schema tokens and tool confusion rise | node-scope tools |
| storing raw observations in history | every next call pays again | convert to structured state |
| optimizing cost without eval | can destroy quality | test recall, citation, task success |

---

### 21. Practical Interview Question [Intermediate]

> Your RAG and tool-using assistant has acceptable answer quality, but cost and latency are much higher than expected. Traces show large retrieval context and verbose tool outputs. How would you analyze and reduce the expansion without breaking quality?

---

### 22. Strong Answer [Pro]

I would first separate retrieval expansion from tool output expansion. For retrieval, I would measure top-k, average chunk size, metadata overhead, parent-section expansion, reranker candidate tokens, and final answer context tokens. I would not only measure the final prompt, because a model-based reranker may process many more tokens than the answer model sees.

Then I would evaluate whether each piece of context contributes to quality. If increasing top-k from 5 to 10 adds many tokens but little expected-source recall, I would lower top-k or use a better reranker. If parent expansion is adding full sections repeatedly, I would deduplicate parents, cap expansions, or include only relevant windows. If metadata is verbose, I would keep model-facing metadata compact while preserving full metadata in traces.

For tools, I would stop sending raw API payloads into the model. I would design task-shaped tool outputs or allow field selection, so the model receives stable IDs, decision-relevant fields, source timestamps, typed status, and errors, not full audit logs or irrelevant nested JSON. In agents, I would convert raw tool results into structured state and concise observations so the same large payload is not repeated in every planning step.

I would set explicit budgets: max retrieval context tokens, max tool observation tokens, max visible tool schemas, and max total input tokens per workflow. Then I would compare a naive version, a budgeted version, and an over-trimmed version using answer correctness, citation support, tool decision correctness, missing-evidence rate, latency, and cost per successful task.

The goal is not to minimize context blindly. It is to send the smallest sufficient evidence package. I would cut low-value repeated tokens first and protect high-value evidence, permissions, citations, and exact fields needed for correctness.

---

### 23. Active Recall [Beginner]

Answer these without looking:

1. What is retrieval context expansion?
2. What is tool output explosion?
3. Why can top-k and chunk size multiply cost quickly?
4. Why is parent-child retrieval sometimes expensive?
5. What metadata should be model-facing?
6. Why distinguish reranker candidate cost from final context cost?
7. Why should raw API payloads usually not go directly to the model?
8. What is task-shaped tool output?
9. What is agent observation bloat?
10. Why do repeated tool observations increase future cost?
11. How does node-scoped tool exposure reduce cost?
12. What is a context packing budget?
13. What should happen when a tool result exceeds budget?
14. What are risks of summarizing retrieved evidence?
15. What fields should be preserved during compression?
16. What does "smallest sufficient evidence package" mean?
17. What should a context expansion trace include?
18. Why is cost-quality evaluation necessary after trimming?
19. What is a dangerous context optimization?
20. What is the final lesson of this subtopic?

Expected answers:

1. Token growth caused by retrieved chunks, metadata, parents, citations, and context reconstruction.
2. Token growth caused by verbose tool/API responses and repeated observations.
3. Total chunk tokens are roughly top-k times average chunk size.
4. Small child chunks may expand into large parent sections, sometimes duplicated.
5. Evidence ID, source title, authority, effective date, scope, compact citation metadata.
6. Rerankers may process many more candidates than the answer model receives.
7. They contain irrelevant fields, logs, nested data, and sometimes sensitive information.
8. A tool response containing only fields needed for the next decision.
9. Accumulation of large tool results, observations, errors, and notes across agent steps.
10. They become part of history/state sent into later model calls.
11. It reduces repeated schema tokens and limits tool confusion.
12. A planned token allocation across instructions, history, evidence, tools, schema, and margin.
13. Trim fields, summarize safely, paginate, or ask narrower tools.
14. It can remove exact evidence, numbers, dates, citations, or exceptions.
15. Source IDs, exact spans, numeric/date fields, permissions, scope, uncertainty.
16. Enough evidence to solve and verify the task without low-value bloat.
17. Retrieval top-k/chunks/parents/metadata, tool schema/result tokens, budgets, overages.
18. Token cuts can harm recall, citations, decisions, safety, or task success.
19. Cutting evidence or metadata that protects correctness and safety.
20. Control expansion deliberately; evidence is valuable, but every evidence token should earn its place.

---

### 24. Revision Notes

- **One-line summary:** Retrieval and tools can expand a short user request into a large model payload, so budget, trim, and pack evidence deliberately.
- **Three keywords:** expansion, evidence, budget.
- **One interview trap:** Reducing context blindly without measuring missing-evidence rate or tool decision correctness.
- **One memory trick:** Top-k multiplies chunks; tools multiply observations; agents repeat both.

Final takeaway:

> RAG and tools are powerful because they add evidence. They become expensive when evidence expansion is unbounded, repeated, or poorly shaped for the decision the model actually needs to make.

---

## Subtopic 20.1.c: Cost per Request, Cost per Session, and Cost per Successful Task

> **Subtopic time:** 2h
> Outcome: You should be able to reason about GenAI cost at three levels: one model request, one user session, and one completed successful task. You should also be able to explain why the cheapest request is not always the cheapest product outcome.

### Add to Knowledge Base

Most GenAI cost conversations start too small.

They ask:

```text
How much does one model call cost?
```

That matters, but it is not enough.

A product rarely sells:

```text
one model call
```

A product sells:

```text
an answered support question
a completed workflow
a resolved ticket
a reviewed invoice
a generated report
a successful search session
```

So you need three cost units:

```text
cost per request
cost per session
cost per successful task
```

The most important mental model:

> A cheap model call that fails often can be more expensive than a costly model call that completes the task reliably.

This is why strong GenAI engineers reason in product units, not just token units.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 and learn the three cost units.
- **Intermediate:** Read sections 7-15 and practice workflow and success-rate math.
- **Pro:** Complete the hands-on lab, use the mini program, and prepare the interview-ready cost analysis answer.

---

### 0. Pre-Question Hook [Beginner]

Imagine two systems for resolving support questions.

System A:

```text
cost per model request: $0.002
average model requests per session: 8
task success rate: 50%
```

System B:

```text
cost per model request: $0.008
average model requests per session: 3
task success rate: 90%
```

Which one is cheaper?

Naive answer:

```text
System A, because one request is cheaper.
```

Product answer:

```text
System A session cost = 0.002 * 8 = $0.016
System A cost per successful task = 0.016 / 0.50 = $0.032

System B session cost = 0.008 * 3 = $0.024
System B cost per successful task = 0.024 / 0.90 = $0.0267
```

System B has more expensive requests but cheaper successful outcomes.

That is the core skill.

---

### 1. The Intuition [Beginner]

Think about rideshare.

You do not only ask:

```text
How much does one minute of driving cost?
```

You ask:

```text
How much does it cost to get the passenger to the destination?
```

If a cheap route gets lost, loops, and needs support intervention, it is not cheap.

GenAI is similar.

One request is like one minute of driving.

A session is the whole trip.

A successful task is arriving at the destination.

The best cost metric depends on what the product promises.

---

### 2. Definition [Beginner]

- **Cost per request:** The cost of one model call or one API request, including input, output, cached tokens, tool-related model calls, or other billable units depending on the boundary chosen.
- **Cost per session:** The total GenAI cost across all model calls and supporting operations in one user session or workflow attempt.
- **Cost per successful task:** Total GenAI cost divided by the number of tasks that meet the product's success criteria.
- **Task success:** A product-defined completion event, such as correct answer with citation, ticket resolved, invoice extracted and validated, or workflow completed safely.
- **Core idea:** Request cost measures model usage. Session cost measures user interaction. Successful-task cost measures product value.

Short version:

```text
request = one call
session = one user journey
successful task = one useful outcome
```

---

### 3. Why It Exists [Beginner]

This distinction exists because GenAI systems can hide cost in workflow shape.

Examples:

| Looks Cheap | Actually Expensive Because |
|---|---|
| small model | more retries, repairs, or escalations |
| low top-k retrieval | missing evidence causes failed answers |
| no reranker | bad context causes more follow-up turns |
| no tool call | model guesses and user re-asks |
| no validation | bad output requires human correction |
| short answer | user needs multiple clarifying turns |
| cheap agent planner | loops and calls tools repeatedly |

The product cares about:

```text
Did the user accomplish the task?
How long did it take?
How much did it cost?
Was it safe and correct?
```

Not only:

```text
Was each call cheap?
```

---

### 4. Cost Unit Boundaries [Intermediate]

Before calculating, define the boundary.

#### Request Boundary

Could mean:

```text
one answer model call
one embedding call
one reranker call
one judge/evaluator call
one tool-interpretation call
one full API request to your backend
```

Be explicit.

#### Session Boundary

Could mean:

```text
one chat conversation
one support case
one document upload
one workflow run
one user visit
one agent thread
```

#### Task Boundary

Could mean:

```text
answer accepted by user
ticket resolved
form submitted correctly
invoice extracted with no critical validation errors
workflow completed with approval
report generated and downloaded
```

Bad metric:

```text
cost per request = $0.003
```

Better metric:

```text
cost per resolved support question = $0.041
```

The second metric can guide product decisions.

---

### 5. Basic Formulas [Intermediate]

Cost per request:

```text
request_cost =
    input_tokens / 1_000_000 * input_price_per_million
  + output_tokens / 1_000_000 * output_price_per_million
  + other_billable_units
```

Cost per session:

```text
session_cost =
    sum(model_call_costs)
  + sum(embedding_costs)
  + sum(reranker_costs)
  + sum(tool_related_model_costs)
  + sum(evaluator_or_guardrail_costs)
```

Average session cost:

```text
avg_session_cost = total_cost / total_sessions
```

Cost per successful task:

```text
cost_per_success = total_cost / successful_tasks
```

Or:

```text
cost_per_success = avg_session_cost / task_success_rate
```

when each session is one task attempt.

If sessions can contain multiple tasks:

```text
cost_per_success = total_session_cost / successful_task_count
```

---

### 6. One Request Is Not One Task [Intermediate]

A single user task may involve many calls.

RAG answer:

```text
query rewrite call
embedding call
retrieval
reranker call
answer model call
citation validator call
optional repair call
```

Agent workflow:

```text
router call
planner call
tool-selection call
tool-result interpretation call
approval summary call
final response call
retry calls
```

Document AI:

```text
OCR or extraction call
field normalization call
validation repair call
human-review summary call
final structured output call
```

The accounting unit should match the product unit.

If the product promises:

```text
"resolve a support issue"
```

then the cost unit should be:

```text
cost per resolved support issue
```

not:

```text
cost per answer model call
```

---

### 7. Success Rate Changes Cost [Intermediate]

Failure increases cost in two ways:

```text
1. failed attempts still cost money
2. failed attempts often trigger retries, follow-ups, or human review
```

If:

```text
avg_session_cost = $0.04
task_success_rate = 80%
```

then:

```text
cost_per_success = 0.04 / 0.80 = $0.05
```

If success drops to 50%:

```text
cost_per_success = 0.04 / 0.50 = $0.08
```

Same session cost.

Much worse outcome economics.

This is why quality metrics and cost metrics cannot be separated.

Strong sentence:

> "I would optimize cost per successful task, because cheaper failed sessions are not product savings."

---

### 8. Multi-Call Workflow Accounting [Intermediate]

Example support assistant session:

| Step | Cost |
|---|---:|
| route query | $0.0005 |
| rewrite query | $0.0008 |
| rerank candidates | $0.0040 |
| answer generation | $0.0120 |
| citation validation | $0.0020 |
| repair unsupported claim | $0.0060 |
| final answer | included above |

Session cost:

```text
0.0005 + 0.0008 + 0.0040 + 0.0120 + 0.0020 + 0.0060 = $0.0253
```

If success rate is 75%:

```text
cost_per_success = 0.0253 / 0.75 = $0.0337
```

If the repair call improves success from 60% to 75%, it may be worth it.

If it barely improves success, it may be waste.

This is the product trade-off.

---

### 9. Retry And Failure Cost [Intermediate]

Retries are not free.

A failing structured-output flow:

```text
initial extraction call = $0.010
parse failure
repair call = $0.006
second parse failure
fallback call = $0.004
human review summary = $0.003
```

Failed task cost:

```text
$0.023 before human labor
```

If this happens often, the right fix may be:

- simpler schema
- stronger structured-output model
- deterministic parser
- smaller extraction units
- better validation prompt
- route hard documents to human review earlier

Retry accounting fields:

```text
retry_count
retry_reason
retry_cost
success_after_retry
failure_after_retry
```

Strong question:

```text
Are retries buying success or just spending more before failing?
```

---

### 10. Human Review And Escalation Cost [Pro]

Cost per successful task may include human review.

Even if you are only tracking model cost, product cost often includes:

```text
human reviewer time
support agent time
escalation cost
manual correction
customer churn risk
compliance review
```

Example:

```text
model session cost = $0.04
human review rate = 10%
human review cost = $1.50 per reviewed case
```

Expected human cost per session:

```text
0.10 * 1.50 = $0.15
```

Total expected cost per session:

```text
0.04 + 0.15 = $0.19
```

The human review cost dominates.

This does not mean human review is bad.

It means you should account for it.

Sometimes spending more model cost to reduce safe-review volume is profitable.

Sometimes human review is required for risk.

---

### 11. Guardrail And Evaluation Cost [Intermediate]

Guardrails can add cost.

Examples:

```text
input classifier
retrieval safety filter
citation validator
claim support judge
toxicity/policy classifier
structured-output repair call
post-answer evaluator
```

These costs are justified when they reduce:

- unsafe outputs
- wrong answers
- human review
- legal risk
- bad automation
- user distrust

Guardrail ROI question:

```text
Does this guardrail reduce expected failure cost more than it adds model cost?
```

Example:

```text
claim-support validator adds $0.002 per answer
but reduces unsupported-answer escalations by 8%
and each escalation costs $1.00
```

Expected avoided cost:

```text
0.08 * 1.00 = $0.08
```

Validator is likely worth it.

---

### 12. Amortized Ingestion And Indexing Cost [Pro]

Some costs happen offline:

```text
embedding documents
chunking pipeline
index building
reranker training/eval
synthetic eval generation
batch summarization
cache warming
```

These should be amortized.

Example:

```text
monthly embedding/indexing cost = $2,000
monthly successful retrieval-backed answers = 500,000
```

Amortized ingestion cost per successful answer:

```text
2000 / 500000 = $0.004
```

If online answer cost is:

```text
$0.018
```

true model-related cost per success may be:

```text
0.018 + 0.004 = $0.022
```

Offline costs matter most when:

- corpus changes frequently
- embeddings are expensive
- reindexing is common
- many tenants have small traffic
- index versions are duplicated

---

### 13. Marginal Cost vs Average Cost [Intermediate]

Average cost:

```text
total cost / total volume
```

Marginal cost:

```text
extra cost of one more request/session/task
```

Why it matters:

```text
fixed monthly ingestion cost may be high
but marginal cost per extra query may be low
```

Example:

```text
fixed index cost = $2,000/month
online cost per answer = $0.02
```

At 10,000 answers/month:

```text
average cost = 2000 / 10000 + 0.02 = $0.22
```

At 500,000 answers/month:

```text
average cost = 2000 / 500000 + 0.02 = $0.024
```

Same online system.

Very different unit economics.

This is why usage volume affects product decisions.

---

### 14. Cost Per Successful Task vs Value Per Task [Pro]

Cost is only half the product story.

You also need value.

Example:

```text
cost per successful support answer = $0.05
estimated avoided support labor = $3.00
```

Good economics.

Another example:

```text
cost per generated social caption = $0.03
user willingness to pay per caption = $0.01
```

Bad economics unless bundled or subsidized.

Value-per-task sources:

- labor saved
- revenue increased
- risk reduced
- user retention improved
- faster workflow completion
- higher conversion
- better quality or compliance

Product viability question:

```text
value_per_success > cost_per_success + operational_margin
```

Cost engineering is not about being cheap.

It is about being worth it.

---

### 15. Quality-Adjusted Cost [Pro]

Two systems may have the same cost per success but different quality.

Example:

| System | Cost per Success | Citation Accuracy | User Trust |
|---|---:|---:|---:|
| A | $0.04 | 70% | low |
| B | $0.05 | 95% | high |

If citations matter, B may be better.

Quality-adjusted metrics:

```text
cost per correct answer
cost per grounded answer
cost per cited correct answer
cost per approved workflow
cost per validated extraction
cost per non-escalated resolution
```

For RAG:

```text
cost_per_grounded_answer = total_cost / grounded_correct_answers
```

For agents:

```text
cost_per_safe_completion = total_cost / completed_workflows_with_no_policy_or_tool_error
```

For document AI:

```text
cost_per_validated_document = total_cost / documents_passing_required_validation
```

The denominator matters.

Choose a denominator that represents product value.

---

### 16. Funnel View Of GenAI Unit Economics [Intermediate]

Think in funnels.

Support assistant:

```text
sessions started
-> answerable sessions
-> correct retrieval
-> grounded answer
-> user accepts answer
-> no escalation
```

Each stage has:

```text
dropoff
cost
latency
failure reason
```

Example:

```text
10,000 sessions
8,000 answerable
7,000 retrieve correct evidence
6,500 produce grounded answer
5,500 accepted by user
```

If total cost is $400:

```text
cost per session = 400 / 10000 = $0.04
cost per accepted answer = 400 / 5500 = $0.073
```

The second number is more honest.

Funnel thinking shows whether to optimize:

- retrieval
- generation
- UX
- answerability routing
- human escalation
- model cost

---

### 17. Cost Trace Schema [Pro]

```json
{
  "request_id": "req_cost_001",
  "session_id": "session_123",
  "task_id": "support_case_456",
  "workflow_type": "support_rag_answer",
  "model_calls": [
    {
      "step": "query_rewrite",
      "input_tokens": 800,
      "output_tokens": 60,
      "estimated_cost": 0.0
    },
    {
      "step": "answer_generation",
      "input_tokens": 7200,
      "output_tokens": 420,
      "estimated_cost": 0.0
    },
    {
      "step": "citation_validation",
      "input_tokens": 1600,
      "output_tokens": 80,
      "estimated_cost": 0.0
    }
  ],
  "non_model_costs": {
    "embedding_lookup": 0.0,
    "human_review_expected_cost": 0.0,
    "amortized_indexing_cost": 0.0
  },
  "outcome": {
    "task_success": true,
    "grounded": true,
    "user_accepted": true,
    "human_escalated": false
  },
  "pricing_version": "pricing_config_2026_06",
  "total_estimated_cost": 0.0
}
```

Important:

```text
store usage and pricing version separately
```

This lets you recompute costs when pricing changes.

---

### 18. Code Sample: Unit Economics Calculator

```python
def cost_per_success(total_cost, successful_tasks):
    if successful_tasks == 0:
        return None
    return total_cost / successful_tasks


def summarize_unit_economics(total_cost, sessions, successful_tasks):
    return {
        "total_cost": total_cost,
        "sessions": sessions,
        "successful_tasks": successful_tasks,
        "cost_per_session": total_cost / sessions if sessions else None,
        "task_success_rate": successful_tasks / sessions if sessions else None,
        "cost_per_success": cost_per_success(total_cost, successful_tasks),
    }


summary = summarize_unit_economics(
    total_cost=400.0,
    sessions=10_000,
    successful_tasks=5_500,
)

print(summary)
```

Expected output:

```text
{
  'total_cost': 400.0,
  'sessions': 10000,
  'successful_tasks': 5500,
  'cost_per_session': 0.04,
  'task_success_rate': 0.55,
  'cost_per_success': 0.07272727272727272
}
```

Expected lesson:

```text
Cost per session can look fine while cost per successful task reveals waste.
```

---

### 19. Mini Program: Task Cost Simulator

```python
def model_call_cost(input_tokens, output_tokens, input_rate, output_rate):
    return input_tokens / 1_000_000 * input_rate + output_tokens / 1_000_000 * output_rate


def workflow_cost(calls, input_rate, output_rate, human_review_rate, human_review_cost):
    model_total = 0.0

    for call in calls:
        model_total += model_call_cost(
            input_tokens=call["input_tokens"],
            output_tokens=call["output_tokens"],
            input_rate=input_rate,
            output_rate=output_rate,
        )

    expected_human_cost = human_review_rate * human_review_cost

    return {
        "model_cost": model_total,
        "expected_human_cost": expected_human_cost,
        "total_expected_session_cost": model_total + expected_human_cost,
    }


def compare_systems():
    systems = {
        "cheap_many_steps": {
            "calls": [
                {"input_tokens": 2000, "output_tokens": 200},
                {"input_tokens": 3000, "output_tokens": 300},
                {"input_tokens": 2500, "output_tokens": 250},
                {"input_tokens": 2000, "output_tokens": 200},
            ],
            "success_rate": 0.55,
            "human_review_rate": 0.25,
        },
        "costlier_fewer_steps": {
            "calls": [
                {"input_tokens": 5000, "output_tokens": 500},
                {"input_tokens": 2000, "output_tokens": 150},
            ],
            "success_rate": 0.85,
            "human_review_rate": 0.08,
        },
    }

    for name, config in systems.items():
        costs = workflow_cost(
            calls=config["calls"],
            input_rate=1.0,
            output_rate=3.0,
            human_review_rate=config["human_review_rate"],
            human_review_cost=1.50,
        )
        cost_per_success_value = costs["total_expected_session_cost"] / config["success_rate"]

        print(name)
        print(f"  session_cost=${costs['total_expected_session_cost']:.4f}")
        print(f"  success_rate={config['success_rate']:.2f}")
        print(f"  cost_per_success=${cost_per_success_value:.4f}")


if __name__ == "__main__":
    compare_systems()
```

Expected lesson:

```text
The lower-token workflow is not always cheaper after success rate and human review are included.
```

---

### 20. Hands-On Lab: Unit Economics For One GenAI Product Flow [Pro]

#### Build

Choose one product flow:

```text
support RAG answer
ticket triage agent
invoice extraction
research assistant
coding assistant
document Q&A
```

Define:

```text
request boundary
session boundary
successful task boundary
```

Then estimate:

```text
model calls per session
input/output tokens per call
guardrail/evaluator calls
retry rate
human review rate
success rate
daily sessions
value per successful task
```

#### Break

Compare three designs:

1. Cheap model, more retries.
2. Stronger model, fewer calls.
3. Routed design: cheap model for easy cases, strong model for hard cases.

#### Measure

For each design:

```text
cost per request
cost per session
success rate
cost per successful task
expected human review cost
latency
quality/safety metric
value margin
```

#### Defend

Write:

```text
I would choose <design> because it has the best cost per successful task
under the required quality and safety constraints.
The cheapest request is not best because <reason>.
The key metric I would monitor is <metric>.
```

---

### 21. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| optimizing cost per call only | ignores retries and failures | optimize cost per successful task |
| ignoring human review cost | product cost is understated | include expected review/escalation cost |
| ignoring offline ingestion | RAG cost is understated | amortize embedding/indexing |
| ignoring guardrail cost | safety path is not free | include validators/judges/classifiers |
| counting failed sessions as cheap | failures still cost and hurt UX | include success rate |
| comparing models by token price only | stronger model may need fewer calls | compare workflow outcome cost |
| no task success definition | denominator is vague | define product success criteria |
| no pricing version | historical cost becomes hard to interpret | store usage and pricing config |
| ignoring value per task | cheap may still be unprofitable | compare cost to product value |

---

### 22. Practical Interview Question [Intermediate]

> You have two GenAI designs. One uses a cheap model with more retries and lower success. The other uses a more expensive model with fewer calls and higher success. How do you decide which is better economically?

---

### 23. Strong Answer [Pro]

I would not decide from cost per model request alone. I would define the product unit first: for example, a resolved support question, a validated invoice, or a completed workflow. Then I would calculate cost per request, cost per session, and cost per successful task for both designs.

For each design, I would include all model calls in the workflow: routing, retrieval-related calls, answer generation, tool interpretation, guardrails, validators, repair calls, retries, and any evaluator calls. I would also include expected human review or escalation cost if failed or uncertain cases require humans. For RAG systems, I would consider amortized ingestion and indexing cost if it materially affects unit economics.

Then I would divide total cost by successful outcomes, not just sessions. A design with a cheaper request can be worse if it needs more calls, fails more often, or pushes more cases to human review. I would compare quality-adjusted cost, such as cost per grounded answer or cost per safe completed workflow.

The better design is the one with acceptable quality, safety, and latency at the best cost per successful task, relative to the value of that task. If the stronger model costs more per call but reduces retries and human review enough, it may be economically better. I would validate this with production traces, success metrics, and slice-level monitoring rather than relying on token price alone.

---

### 24. Active Recall [Beginner]

Answer these without looking:

1. What is cost per request?
2. What is cost per session?
3. What is cost per successful task?
4. Why is one model call not always one task?
5. Why can cheap calls create expensive workflows?
6. What is task success?
7. What is the formula for cost per success?
8. Why does success rate affect economics?
9. How do retries affect cost?
10. Why should human review cost be included?
11. What are guardrail costs?
12. What is amortized ingestion cost?
13. What is marginal cost?
14. What is average cost?
15. Why compare cost to value per task?
16. What is quality-adjusted cost?
17. What is cost per grounded answer?
18. What should a cost trace include?
19. Why store pricing version separately?
20. What is the final lesson of unit economics?

Expected answers:

1. Cost of one model/API call under a defined boundary.
2. Total GenAI cost across one user journey or workflow attempt.
3. Total cost divided by successful product outcomes.
4. Tasks often require many model calls, tools, validators, and retries.
5. They may need more steps, fail more often, or trigger human review.
6. Product-defined completion event that meets quality/safety criteria.
7. Total cost divided by successful tasks, or avg session cost divided by success rate.
8. Failed sessions still cost money and reduce useful outcomes.
9. They add more calls and may still fail.
10. It can dominate model cost and reflects real product operations.
11. Costs from classifiers, validators, judges, repair calls, and safety checks.
12. Offline embedding/indexing cost spread across successful uses.
13. Extra cost of one more request/session/task.
14. Total cost divided by total volume.
15. A system is worth deploying only if value exceeds cost with margin.
16. Cost divided by outcomes that meet quality/safety criteria.
17. Total cost divided by correct grounded answers.
18. Session/task ID, model calls, tokens, non-model costs, outcome, pricing version.
19. Prices change; usage traces should remain reusable.
20. Optimize the economics of successful outcomes, not isolated model calls.

---

### 25. Revision Notes

- **One-line summary:** Product cost engineering compares request cost, session cost, and cost per successful task so optimization follows outcomes, not isolated calls.
- **Three keywords:** request, session, success.
- **One interview trap:** Choosing the cheapest model call without accounting for retries, failures, review, and task success.
- **One memory trick:** One call is usage; one session is journey; one success is value.

Final takeaway:

> The real GenAI unit cost is not what one call costs. It is what the product spends to create one successful, safe, valuable outcome.

---

## Subtopic 20.1.d: Logging and Reviewing Token Consumption by System Layer

> **Subtopic time:** 2h
> Outcome: You should be able to instrument a GenAI system so token usage is attributed to product, orchestration, prompt, memory, retrieval, tool, model, guardrail, and evaluation layers. You should also be able to review traces and decide which layer deserves optimization first.

### Add to Knowledge Base

Most teams discover token cost too late.

They see:

```text
monthly LLM bill is high
latency increased
context windows are near limit
agent traces are huge
retrieval answers feel bloated
```

Then they ask:

```text
Which prompt is expensive?
Which feature is expensive?
Which retrieval setting is expensive?
Which agent step is repeating context?
Which guardrail is worth its cost?
Which user segment is driving the bill?
```

If token usage was not logged by layer, the team can only guess.

The core mental model:

> Token logging is cost observability. Layer attribution turns "the LLM is expensive" into "retrieval expansion in invoice workflows adds 68 percent of input tokens after turn three."

This is the difference between junior cost cutting and senior cost engineering.

Junior reaction:

```text
Use a cheaper model.
```

Senior reaction:

```text
Show me the token trace by layer, route, prompt version, retrieval configuration, tool output size, user segment, and task outcome.
```

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand why token usage must be attributed.
- **Intermediate:** Read sections 7-15 to learn schemas, dashboards, and review workflows.
- **Pro:** Complete the lab and practice the interview answer so you can explain token observability like a production engineer.

---

### 0. Pre-Question Hook [Beginner]

A support RAG assistant has this average model request:

```text
input tokens: 18,000
output tokens: 700
```

The team wants to reduce cost.

One engineer says:

```text
Shorten the system prompt.
```

Another says:

```text
Use a smaller model.
```

Both may be right, but neither knows.

Now break the 18,000 input tokens down:

| Layer | Tokens |
|---|---:|
| system instructions | 900 |
| tool schemas | 1,700 |
| conversation history | 4,200 |
| retrieval chunks | 8,600 |
| citations and metadata | 1,100 |
| tool observations | 1,000 |
| user message | 500 |

Now the optimization path is clearer.

The biggest input token source is retrieval chunks.

The second biggest is conversation history.

Shortening the system prompt may help, but it is not the main lever.

This is why layer logging exists.

---

### 1. The Intuition [Beginner]

Think of a restaurant bill.

If the receipt only says:

```text
Total: $184
```

you cannot reason well.

If it says:

```text
food: $92
drinks: $48
tax: $16
tip: $28
```

you know where the money went.

GenAI token logging is the receipt for your system.

But a good receipt does more than say:

```text
input tokens: 18,000
output tokens: 700
```

It says:

```text
retrieval context: 8,600
history: 4,200
tool schemas: 1,700
guardrail context: 1,200
```

That breakdown lets you optimize the expensive layer without damaging the useful layer.

---

### 2. Definition [Beginner]

- **Token logging:** Recording token usage and related metadata for each model call or token-consuming operation.
- **Layer attribution:** Assigning tokens to the system layer that created them, such as prompt, retrieval, memory, tool output, guardrail, or generation.
- **Token review:** A recurring analysis process that identifies waste, regressions, and cost-quality trade-offs from token traces.
- **Core idea:** Do not only log total tokens. Log where tokens came from, why they were included, and whether they contributed to success.

Short version:

```text
token logging tells you how much
layer attribution tells you where
outcome logging tells you whether it was worth it
```

---

### 3. Why It Exists [Beginner]

Layer-level token logging exists because GenAI costs are distributed across many invisible contributors.

The user sees:

```text
one answer
```

The system may execute:

```text
router call
query rewrite call
embedding call
retrieval
reranking
tool selection
tool call
tool result summarization
answer generation
citation validation
safety check
repair call
memory update
```

Without layer-level logs, you cannot answer:

- Did the cost come from user demand or internal workflow design?
- Did retrieval context improve success or just add bulk?
- Did memory reduce repeated turns or inflate every request?
- Did tool schemas get sent repeatedly when only one tool was needed?
- Did the guardrail prevent expensive failures or add low-value overhead?
- Did a prompt version accidentally double context length?
- Did one tenant, route, or file type cause the spike?

Strong statement:

> You cannot manage token economics from aggregate billing alone. Billing tells you what happened financially. Traces tell you what happened architecturally.

---

### 4. The System Layers To Track [Intermediate]

A useful GenAI token trace usually separates these layers.

| Layer | What It Includes | Common Token Waste |
|---|---|---|
| product/UX layer | user message, attachments, selected mode, task type | verbose user-provided data copied repeatedly |
| routing layer | intent detection, model routing, task classification | routing prompts that are too large |
| instruction layer | system/developer prompt, policies, style rules | long global prompts used for every task |
| schema/tool layer | tool definitions, JSON schemas, function descriptions | sending all tools when only a subset is relevant |
| memory layer | conversation history, summaries, user profile, long-term memory | stale turns, repeated summaries, irrelevant memories |
| retrieval layer | chunks, titles, metadata, citations, parent docs | high top-k, large chunks, redundant documents |
| tool-output layer | API/database/search results, logs, errors | raw payloads instead of compact fields |
| orchestration layer | planner notes, state, intermediate observations | agent scratchpad and repeated state bloat |
| model output layer | final answer, reasoning-visible output, structured output | excessive verbosity or oversized JSON |
| guardrail/eval layer | classifiers, validators, judges, repair calls | checking easy cases with expensive validators |
| cache layer | cached prompt segments or reused responses | cache misses due to unstable prompt text |
| offline ingestion layer | embedding, summarization, indexing, synthetic eval | frequent reprocessing without version control |

Important:

```text
Some layers do not consume tokens directly every time,
but they cause token consumption elsewhere.
```

Example:

```text
bad chunking causes retrieval bloat
bad tool schema causes tool-selection errors
bad memory policy causes history growth
bad orchestration causes repeated calls
```

---

### 5. Token Categories [Intermediate]

At minimum, log these categories:

```text
input_tokens
output_tokens
cached_input_tokens
reasoning_tokens if exposed by provider
embedding_input_tokens
reranker_input_tokens if token based
guardrail_input_tokens
guardrail_output_tokens
tool_schema_tokens
tool_result_tokens
retrieval_context_tokens
history_tokens
memory_tokens
system_instruction_tokens
user_message_tokens
```

Why categories matter:

```text
input tokens explain context size
output tokens explain generation cost and latency
cached tokens explain savings
retrieval tokens explain evidence expansion
history tokens explain session growth
tool tokens explain agent overhead
guardrail tokens explain safety cost
```

Do not assume all tokens have equal value.

Useful tokens:

```text
evidence needed for answer
schema needed for valid output
policy needed for safety
history needed for continuity
```

Waste tokens:

```text
irrelevant retrieved chunks
old conversation turns
unused tool schemas
raw tool payload fields
duplicated metadata
verbose internal notes
```

The review goal is not:

```text
minimize tokens
```

The goal is:

```text
maximize useful outcome per token
```

---

### 6. Trace Hierarchy [Intermediate]

A production trace should connect token usage across levels.

Useful hierarchy:

```text
organization
tenant
user
session
task
workflow run
step/span
model call
prompt segment
```

Example:

```text
tenant_id = acme_health
session_id = sess_123
task_id = support_case_456
workflow_run_id = run_789
span_id = retrieval_answer_generation
model_call_id = call_abc
prompt_version = support_rag_v12
retrieval_config_version = rag_top8_parent_v3
```

Why this matters:

| Question | Needed ID |
|---|---|
| Which customers are expensive? | tenant_id |
| Which journeys are expensive? | session_id |
| Which outcomes are expensive? | task_id |
| Which graph step is expensive? | span_id |
| Which prompt caused regression? | prompt_version |
| Which retrieval config caused bloat? | retrieval_config_version |
| Which model route caused spend? | model_name and route |

Without correlation IDs, you cannot connect cost to architecture or product outcome.

---

### 7. What To Log Per Model Call [Intermediate]

For every model call, log:

```json
{
  "trace_id": "trace_001",
  "session_id": "sess_001",
  "task_id": "task_001",
  "span_id": "answer_generation",
  "parent_span_id": "rag_workflow",
  "layer": "model_generation",
  "component": "support_answerer",
  "operation": "generate_grounded_answer",
  "model": "model_name_from_config",
  "prompt_version": "support_rag_v12",
  "pricing_version": "pricing_2026_06",
  "input_tokens": 12600,
  "output_tokens": 580,
  "cached_input_tokens": 4200,
  "estimated_cost": 0.0,
  "latency_ms": 2400,
  "status": "success"
}
```

Then log the prompt-segment breakdown:

```json
{
  "model_call_id": "call_001",
  "segments": [
    {
      "name": "system_instructions",
      "layer": "instruction",
      "tokens": 850
    },
    {
      "name": "conversation_history",
      "layer": "memory",
      "tokens": 3100
    },
    {
      "name": "retrieved_chunks",
      "layer": "retrieval",
      "tokens": 6900
    },
    {
      "name": "tool_schemas",
      "layer": "tool_schema",
      "tokens": 1200
    },
    {
      "name": "user_message",
      "layer": "product_input",
      "tokens": 550
    }
  ]
}
```

This lets you answer:

```text
Which layer inflated the prompt?
Which segment changed after deployment?
Which segment can be cached?
Which segment predicts success?
```

---

### 8. What To Log Per Retrieval Step [Intermediate]

Retrieval token usage is often the largest input cost.

Log:

```json
{
  "span_id": "retrieve_context",
  "layer": "retrieval",
  "query_tokens": 42,
  "query_rewrite_tokens": 180,
  "top_k": 8,
  "candidate_count": 80,
  "returned_chunk_count": 8,
  "avg_chunk_tokens": 720,
  "retrieval_context_tokens": 5760,
  "metadata_tokens": 640,
  "citation_tokens": 220,
  "deduped_chunk_count": 2,
  "dropped_chunk_count": 6,
  "retrieval_config_version": "hybrid_top8_rerank_v4"
}
```

Review questions:

- Are chunks too large?
- Is top-k too high?
- Are parent documents expanding too aggressively?
- Are duplicate chunks being sent?
- Is metadata useful or noisy?
- Does reranking reduce final context?
- Are hard queries justifiably larger than easy queries?
- Is more context improving answer quality?

Retrieval token review should always connect to quality:

```text
more retrieval tokens are good only if they increase grounded success
```

---

### 9. What To Log Per Tool Step [Intermediate]

Tool usage creates two kinds of token cost:

```text
tool schema tokens sent to the model
tool result tokens included in later prompts
```

Log:

```json
{
  "span_id": "crm_lookup",
  "layer": "tool_output",
  "tool_name": "get_customer_account",
  "tool_schema_tokens": 380,
  "raw_result_bytes": 46000,
  "raw_result_estimated_tokens": 9200,
  "selected_result_tokens": 850,
  "fields_returned": ["account_id", "plan", "renewal_date", "open_tickets"],
  "fields_dropped_count": 47,
  "tool_result_summary_tokens": 210,
  "used_by_next_step": true
}
```

The most important fields:

```text
raw_result_estimated_tokens
selected_result_tokens
used_by_next_step
```

These expose whether the system is dumping raw API payloads into the model.

Strong rule:

> Tools should return decision-shaped data, not database-shaped data.

---

### 10. What To Log Per Memory Step [Intermediate]

Memory can reduce cost or explode cost.

Good memory:

```text
compresses useful context
removes stale details
preserves user/task facts
reduces repeated explanation
```

Bad memory:

```text
keeps every turn
adds irrelevant profile facts
duplicates retrieved evidence
stores summaries that keep growing
```

Log:

```json
{
  "span_id": "memory_pack",
  "layer": "memory",
  "history_turn_count": 18,
  "raw_history_tokens": 9200,
  "included_history_tokens": 2400,
  "summary_tokens": 620,
  "long_term_memory_tokens": 350,
  "dropped_history_tokens": 6800,
  "memory_policy_version": "rolling_summary_v5"
}
```

Review questions:

- How fast does history grow by turn?
- Does summary size stabilize?
- Are old tool observations being repeated?
- Are retrieved chunks copied into memory?
- Does memory improve task success or only add tokens?

Memory should have a budget.

Example:

```text
conversation history budget: 2,000 tokens
working memory budget: 1,000 tokens
long-term user memory budget: 500 tokens
retrieval evidence budget: 6,000 tokens
```

Without budgets, memory becomes a silent tax.

---

### 11. What To Log Per Guardrail And Evaluation Step [Pro]

Guardrails and evaluators are important, but they also cost tokens.

Log:

```json
{
  "span_id": "citation_validator",
  "layer": "guardrail_eval",
  "validator_type": "claim_support",
  "input_tokens": 1800,
  "output_tokens": 120,
  "trigger_policy": "run_on_rag_answers",
  "triggered_repair": true,
  "prevented_failure_type": "unsupported_claim",
  "estimated_cost": 0.0
}
```

Review questions:

- Which guardrails run on every request?
- Which guardrails are conditional?
- Which guardrails catch real failures?
- Which guardrails trigger repair loops?
- Which guardrails are redundant with deterministic validation?
- Which guardrails should be moved to cheaper classifiers or rules?

Strong idea:

```text
guardrails should be evaluated by avoided failure cost, not only added token cost
```

---

### 12. Layer-Level Cost Dashboard [Intermediate]

A useful dashboard has at least four views.

#### 1. Cost By Layer

```text
retrieval context: 44%
conversation memory: 21%
tool schemas/results: 14%
model output: 9%
guardrails/evals: 7%
instructions: 5%
```

This tells you where tokens are going.

#### 2. Cost By Product Flow

```text
support_rag_answer
invoice_extraction
research_summary
sales_email_draft
ticket_triage_agent
```

This tells you which feature is expensive.

#### 3. Cost By Outcome

```text
successful tasks
failed tasks
human escalated tasks
retried tasks
unsupported-answer tasks
```

This tells you whether cost created value.

#### 4. Cost Regression By Version

```text
prompt_version
retrieval_config_version
tool_schema_version
memory_policy_version
model_route_version
graph_version
```

This tells you what changed.

Good dashboard questions:

- Did token usage increase after a deployment?
- Did success improve enough to justify it?
- Which layer caused the increase?
- Is the increase concentrated in one route or tenant?
- Is output verbosity growing?
- Are cache hit rates dropping?

---

### 13. Slice Analysis [Pro]

Average token usage hides expensive slices.

Do not only review:

```text
average input tokens = 9,400
```

Also review:

```text
p50 input tokens
p90 input tokens
p99 input tokens
tokens by tenant
tokens by workflow type
tokens by model route
tokens by document type
tokens by language
tokens by turn number
tokens by success/failure outcome
```

Example:

```text
p50 input tokens: 7,000
p90 input tokens: 18,000
p99 input tokens: 62,000
```

The average may look acceptable while p99 is dangerous.

Common expensive slices:

- long sessions
- large uploaded documents
- multilingual queries with weaker retrieval
- tenants with verbose metadata
- agent loops after tool failures
- rare document formats
- low-confidence retrieval routes
- users who paste entire logs

Senior review habit:

> Always ask for p90/p99 and failure slices before optimizing the average.

---

### 14. Anomaly Detection [Intermediate]

Token spikes usually come from a change.

Common causes:

| Spike Pattern | Likely Cause |
|---|---|
| input tokens doubled after deploy | prompt or retrieval config changed |
| output tokens slowly rising | verbosity drift or response format change |
| retrieval tokens spiking for one tenant | tenant corpus has large chunks or metadata |
| tool tokens spiking | raw API response included in prompt |
| memory tokens rising by turn | summary policy not compressing |
| guardrail tokens rising | validator now runs on more cases |
| cache savings dropped | unstable prompt prefix or cache key changed |
| p99 tokens exploded | rare loop, large document, or tool failure path |

Simple anomaly rules:

```text
alert if average input tokens increase more than 25% day over day
alert if p95 input tokens exceed budget
alert if output tokens increase while success does not
alert if retry token share exceeds threshold
alert if failed tasks consume more than successful tasks
alert if one layer exceeds its budget for a route
```

Do not only alert on total cost.

Alert on architecture signals.

---

### 15. Review Cadence [Intermediate]

Token review should be regular.

Daily review:

```text
major cost spikes
p95/p99 token outliers
failed-task token waste
provider/model route anomalies
```

Weekly review:

```text
cost by layer
cost by workflow
success-adjusted cost
top expensive tenants/routes
prompt and retrieval version regressions
```

Before release:

```text
compare token distribution against previous version
run eval set with token traces
check p90/p99 context size
verify cache hit rate
confirm guardrail costs and catches
```

After release:

```text
monitor cost, quality, latency, and failure slices together
```

Cost review without quality review is dangerous.

Quality review without cost review is incomplete.

---

### 16. Optimization Decision Tree [Pro]

When token cost is high, ask in this order.

#### Step 1: Which layer is largest?

```text
instructions
history
memory
retrieval
tools
guardrails
output
agent loops
```

#### Step 2: Is the layer useful?

```text
Does it improve success?
Does it reduce risk?
Does it reduce follow-up turns?
Does it reduce human review?
```

#### Step 3: Can it be reduced safely?

Options:

```text
trim
summarize
dedupe
route conditionally
cache
compress
paginate
retrieve fewer but better chunks
send fewer tools
use structured field selection
use deterministic validation
use smaller model for simple checks
```

#### Step 4: Did the metric improve?

Validate:

```text
cost per successful task
latency
groundedness
tool success
human escalation
user acceptance
safety catch rate
```

Never declare victory from token reduction alone.

---

### 17. Privacy And Security In Token Logs [Pro]

Token logs can accidentally become sensitive data logs.

Bad practice:

```text
store full prompts and full tool outputs forever
```

Safer practice:

```text
store counts, hashes, IDs, versions, and redacted samples
```

Recommended fields:

```text
token counts by segment
prompt version
retrieval document IDs
chunk IDs
tool name
tool field names
redaction status
model name
outcome labels
cost estimate
latency
```

Be careful with:

- user messages
- retrieved private documents
- tool responses from internal systems
- PII/PHI/secrets
- raw agent scratchpads
- uploaded documents
- customer-specific metadata

Practical pattern:

```text
full prompt logging disabled by default
redacted prompt sampling for debugging
short retention for raw traces
long retention for aggregated metrics
strict access control for trace viewers
```

Strong sentence:

> Observability should not create a second data leak surface.

---

### 18. Sampling vs Full Logging [Intermediate]

You do not always need to store every full trace.

Full metrics logging:

```text
store token counts and layer attribution for every request
```

Sampled rich traces:

```text
store redacted prompt segment examples for a small percentage
```

Always log:

```text
counts
layer
component
version
status
latency
outcome
cost estimate
```

Sample:

```text
redacted prompt text
redacted retrieved chunks
tool result examples
agent trajectories
failure paths
```

Increase sampling for:

- failures
- expensive outliers
- new releases
- new tenants
- low-confidence routes
- human escalations
- safety incidents

This gives you enough visibility without storing excessive sensitive data.

---

### 19. Code Sample: Token Event Aggregator

This example shows how layer attribution can turn raw token events into a useful review summary.

```python
from collections import defaultdict


def summarize_by_layer(events):
    summary = defaultdict(lambda: {
        "input_tokens": 0,
        "output_tokens": 0,
        "estimated_cost": 0.0,
        "calls": 0,
    })

    for event in events:
        layer = event["layer"]
        summary[layer]["input_tokens"] += event.get("input_tokens", 0)
        summary[layer]["output_tokens"] += event.get("output_tokens", 0)
        summary[layer]["estimated_cost"] += event.get("estimated_cost", 0.0)
        summary[layer]["calls"] += 1

    return dict(summary)


events = [
    {
        "layer": "instruction",
        "input_tokens": 900,
        "output_tokens": 0,
        "estimated_cost": 0.001,
    },
    {
        "layer": "retrieval",
        "input_tokens": 8600,
        "output_tokens": 0,
        "estimated_cost": 0.009,
    },
    {
        "layer": "memory",
        "input_tokens": 4200,
        "output_tokens": 0,
        "estimated_cost": 0.004,
    },
    {
        "layer": "model_generation",
        "input_tokens": 0,
        "output_tokens": 700,
        "estimated_cost": 0.003,
    },
    {
        "layer": "guardrail_eval",
        "input_tokens": 1500,
        "output_tokens": 120,
        "estimated_cost": 0.002,
    },
]


for layer, stats in summarize_by_layer(events).items():
    total_tokens = stats["input_tokens"] + stats["output_tokens"]
    print(
        layer,
        "tokens=",
        total_tokens,
        "cost=",
        round(stats["estimated_cost"], 4),
    )
```

Expected lesson:

```text
Once tokens are grouped by layer, the expensive layer becomes visible.
```

---

### 20. Mini Program: Layer Cost Review

This mini program simulates a token review across multiple product flows.

```python
from collections import defaultdict


def percent(part, whole):
    return 0 if whole == 0 else round(part / whole * 100, 2)


def review_token_events(events):
    by_layer = defaultdict(int)
    by_flow = defaultdict(int)
    by_outcome = defaultdict(int)

    total_tokens = 0

    for event in events:
        tokens = event.get("input_tokens", 0) + event.get("output_tokens", 0)
        total_tokens += tokens
        by_layer[event["layer"]] += tokens
        by_flow[event["workflow_type"]] += tokens
        by_outcome[event["outcome"]] += tokens

    print("Total tokens:", total_tokens)
    print()

    print("Tokens by layer")
    for layer, tokens in sorted(by_layer.items(), key=lambda item: item[1], reverse=True):
        print(f"  {layer:20s} {tokens:7d} ({percent(tokens, total_tokens)}%)")

    print()
    print("Tokens by workflow")
    for flow, tokens in sorted(by_flow.items(), key=lambda item: item[1], reverse=True):
        print(f"  {flow:20s} {tokens:7d} ({percent(tokens, total_tokens)}%)")

    print()
    print("Tokens by outcome")
    for outcome, tokens in sorted(by_outcome.items(), key=lambda item: item[1], reverse=True):
        print(f"  {outcome:20s} {tokens:7d} ({percent(tokens, total_tokens)}%)")


sample_events = [
    {
        "workflow_type": "support_rag",
        "layer": "retrieval",
        "input_tokens": 9000,
        "output_tokens": 0,
        "outcome": "success",
    },
    {
        "workflow_type": "support_rag",
        "layer": "memory",
        "input_tokens": 4200,
        "output_tokens": 0,
        "outcome": "success",
    },
    {
        "workflow_type": "support_rag",
        "layer": "model_generation",
        "input_tokens": 0,
        "output_tokens": 650,
        "outcome": "success",
    },
    {
        "workflow_type": "invoice_ai",
        "layer": "tool_output",
        "input_tokens": 12000,
        "output_tokens": 0,
        "outcome": "failed",
    },
    {
        "workflow_type": "invoice_ai",
        "layer": "guardrail_eval",
        "input_tokens": 2500,
        "output_tokens": 180,
        "outcome": "failed",
    },
    {
        "workflow_type": "research_agent",
        "layer": "orchestration",
        "input_tokens": 5000,
        "output_tokens": 1200,
        "outcome": "human_escalated",
    },
]


if __name__ == "__main__":
    review_token_events(sample_events)
```

Expected output shape:

```text
Total tokens: 34730

Tokens by layer
  tool_output            12000 (34.55%)
  retrieval               9000 (25.91%)
  orchestration           6200 (17.85%)
  memory                  4200 (12.09%)
  guardrail_eval          2680 (7.72%)
  model_generation         650 (1.87%)
```

Expected lesson:

```text
Layer review points to optimization candidates, but outcome review tells whether the tokens created value.
```

---

### 21. Hands-On Lab: Build A Token Review Sheet [Pro]

#### Build

Choose one GenAI flow:

```text
support RAG assistant
invoice extraction
research agent
coding assistant
sales proposal generator
document Q&A system
```

Create a table with one row per model call or token-consuming step:

```text
session_id
task_id
workflow_type
step_name
layer
model
prompt_version
retrieval_config_version
input_tokens
output_tokens
cached_input_tokens
estimated_cost
latency_ms
status
task_success
failure_reason
```

#### Review

Answer:

1. Which layer has the most input tokens?
2. Which layer has the most output tokens?
3. Which layer has the most cost?
4. Which layer grows with conversation turn number?
5. Which layer is highest in failed tasks?
6. Which prompt or retrieval version changed token usage?
7. Which p90 or p99 cases are extreme?
8. Which tokens can be cached?
9. Which tokens can be removed without lowering success?
10. Which tokens protect quality or safety and should remain?

#### Optimize

Choose one improvement:

```text
reduce top-k from 10 to 6
dedupe retrieved chunks
summarize old history
send only relevant tool schemas
trim raw tool payloads
make validators conditional
cap output length by task type
cache stable prompt prefixes
```

Then measure:

```text
token reduction
cost reduction
latency change
success rate change
quality change
safety change
human escalation change
```

#### Defend

Write:

```text
The largest token source was <layer>.
We reduced it by <change>.
The cost impact was <number or estimate>.
The quality impact was <metric>.
I would ship / not ship because <reason>.
```

---

### 22. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| logging only total tokens | hides the expensive layer | log prompt segments and system layers |
| logging cost without outcome | cannot tell waste from useful spend | join token logs with task success |
| logging prompts without privacy controls | creates sensitive data risk | store counts, IDs, versions, and redacted samples |
| ignoring failed tasks | failures can consume many tokens | review token usage by outcome |
| optimizing average only | p99 can dominate cost and latency risk | review p50, p90, p99, and slices |
| no version tags | regressions are hard to trace | log prompt, retrieval, graph, and tool versions |
| not separating retrieval from memory | both look like context bloat | attribute tokens by segment |
| not tracking cacheable tokens | misses easy savings | log stable prefixes and cache hit rate |
| not tracking tool output size | raw payloads silently bloat prompts | log raw vs selected result tokens |
| cutting safety tokens blindly | can increase risk and escalations | evaluate avoided failure cost |

---

### 23. Practical Interview Question [Intermediate]

> Your GenAI product's monthly bill doubled after a release. The product team says traffic only increased by 15 percent. How would you debug token consumption and decide what to optimize?

---

### 24. Strong Answer [Pro]

I would start by separating traffic growth from token growth. If traffic increased 15 percent but cost doubled, then either average tokens per task increased, expensive routes became more common, cache hit rate dropped, retries increased, or a new layer started consuming more tokens.

I would inspect token traces by system layer: instructions, memory, retrieval context, tool schemas, tool outputs, orchestration state, model output, guardrails, and evaluation calls. I would slice this by workflow type, prompt version, retrieval configuration, model route, tenant, turn number, task outcome, and p90/p99 usage. I would especially compare the old and new release versions to identify which layer changed.

If retrieval tokens grew, I would inspect top-k, chunk size, parent expansion, metadata, deduplication, and whether the extra context improved grounded-answer success. If memory tokens grew, I would inspect history retention and summary policy. If tool tokens grew, I would check whether raw API payloads are being passed into later prompts. If guardrail tokens grew, I would check whether validators are running on too many low-risk cases. If output tokens grew, I would inspect response format and verbosity.

I would not optimize by blindly switching to a cheaper model. I would first identify the layer causing the regression, then run a controlled experiment that reduces that layer while measuring cost per successful task, latency, quality, safety, and human escalation. The fix might be prompt trimming, retrieval packing, tool field selection, memory compaction, conditional guardrails, caching, or route-specific model selection depending on the trace.

The final recommendation should be backed by metrics: which layer caused the increase, what changed in the release, how much cost the fix saves, and whether task success and safety remain acceptable.

---

### 25. Active Recall [Beginner]

Answer these without looking:

1. Why is aggregate billing not enough for GenAI cost engineering?
2. What is layer attribution?
3. Name five layers that can contribute tokens.
4. Why should token logs include task outcome?
5. Why should prompt version be logged?
6. Why should retrieval config version be logged?
7. What is the difference between total token logging and segment logging?
8. What should be logged for retrieval context?
9. What should be logged for tool output?
10. Why can memory become a silent tax?
11. Why review p90 and p99 token usage?
12. What can cause cache hit rate to drop?
13. Why is failed-task token usage important?
14. Why should guardrail cost be reviewed with avoided failure cost?
15. What privacy risk comes from full prompt logging?
16. What should always be logged even if full prompts are sampled?
17. What is a token regression?
18. Why should cost review include quality metrics?
19. What is the optimization decision tree?
20. What is the final lesson of token observability?

Expected answers:

1. It shows spend but not which architecture layer caused it.
2. Assigning tokens to the layer that created or required them.
3. Instructions, memory, retrieval, tools, orchestration, output, guardrails.
4. To distinguish useful spend from waste.
5. To trace cost regressions to prompt changes.
6. To trace retrieval bloat or quality changes.
7. Total logging gives one number; segment logging shows where tokens came from.
8. Top-k, chunk count, chunk tokens, metadata tokens, citations, config version.
9. Tool schema tokens, raw result size, selected result tokens, fields returned.
10. It can grow every turn and repeat stale context.
11. Expensive outliers can dominate cost and latency risk.
12. Unstable prompt prefixes, changing dynamic text, or bad cache keys.
13. Failed tasks can consume tokens without creating product value.
14. Some guardrails are worth cost if they prevent expensive failures.
15. Logs may store PII, secrets, private docs, or tool data.
16. Counts, layers, versions, IDs, status, latency, outcome, estimated cost.
17. Token usage increasing after a release or config change.
18. Token cuts can reduce correctness, groundedness, safety, or user acceptance.
19. Identify biggest layer, judge usefulness, reduce safely, validate outcome.
20. Token observability turns cost from a bill into an architecture signal.

---

### 26. Revision Notes

- **One-line summary:** Log token usage by system layer so you can connect cost to architecture, release changes, and task outcomes.
- **Three keywords:** attribution, traces, slices.
- **One interview trap:** Saying "switch to a cheaper model" before identifying which layer caused the cost increase.
- **One memory trick:** The bill says how much; the trace says where; the outcome says whether it mattered.

Final takeaway:

> Senior GenAI cost engineering starts with token observability: measure tokens by layer, version, route, and outcome before choosing what to cut.

---

## Topic 20.2: Latency Budgeting and Pipeline Design

> **Topic time:** 8h
> Focus: Understanding where GenAI latency comes from, how pipeline stages add or overlap, how to build latency budgets, and how to trade quality, cost, and response time without guessing.

Latency is the time version of cost.

Cost asks:

```text
Where did the tokens and dollars go?
```

Latency asks:

```text
Where did the user's waiting time go?
```

In GenAI systems, latency rarely comes from one place.

It comes from:

```text
network hops
auth and request setup
query rewriting
embedding
retrieval
reranking
tool calls
database calls
orchestration decisions
model generation
guardrails
validators
repair loops
streaming behavior
frontend rendering
```

The central idea:

> You cannot optimize latency from a stopwatch total. You need a stage-by-stage trace and a clear budget for the user experience you are trying to deliver.

---

## Subtopic 20.2.a: End-to-End Latency Decomposition Across Retrieval, Reranking, Tools, and Generation

> **Subtopic time:** 2h
> Outcome: You should be able to decompose total GenAI latency into pipeline stages, identify the critical path, distinguish serial from parallel work, and explain how retrieval, reranking, tools, and generation shape user-perceived response time.

### Add to Knowledge Base

A GenAI product can feel slow even when each individual component seems reasonable.

Example:

```text
query rewrite: 450 ms
embedding: 120 ms
vector search: 180 ms
reranking: 900 ms
tool call: 700 ms
answer generation first token: 900 ms
answer generation completion: 5,500 ms
citation validation: 650 ms
frontend rendering: 200 ms
```

No single number looks outrageous.

But the user may wait:

```text
8 to 10 seconds for final answer
```

The mistake is treating latency as one blob:

```text
The model is slow.
```

The better engineering question is:

```text
Which stages are on the critical path, which can run in parallel, which can be skipped for easy cases, and which are only needed after the user already sees useful progress?
```

Latency decomposition turns vague slowness into a design problem.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand end-to-end latency and pipeline stages.
- **Intermediate:** Read sections 7-15 to learn critical paths, p95/p99 latency, timeouts, and stage budgets.
- **Pro:** Complete the lab and practice the interview answer so you can discuss latency like a production systems engineer.

---

### 0. Pre-Question Hook [Beginner]

Two RAG assistants both take 6 seconds to finish.

System A:

```text
first token appears after 700 ms
streaming answer completes at 6 seconds
```

System B:

```text
nothing appears for 5.5 seconds
full answer appears at 6 seconds
```

Same total latency.

Very different user experience.

Why?

Because users perceive latency in stages:

```text
time to acknowledge
time to first useful progress
time to first token
time to usable partial answer
time to final answer
time to verified final answer
```

A latency budget must account for both:

```text
backend completion time
user-perceived waiting time
```

---

### 1. The Intuition [Beginner]

Think of a restaurant.

The total wait for a meal includes:

```text
getting seated
ordering
kitchen prep
cooking
plating
server delivery
payment
```

If dinner takes 40 minutes, saying:

```text
The restaurant is slow.
```

is not diagnostic.

You need to know:

```text
Was the kitchen slow?
Was the server slow?
Was the order delayed?
Did one dish block the whole table?
Could drinks arrive while food cooks?
```

GenAI pipelines are the same.

Retrieval, reranking, tools, and generation are like different stations in the kitchen.

Some are serial.

Some can overlap.

Some block the answer.

Some can happen after the answer is already streaming.

Latency engineering is the discipline of finding the wait path that matters.

---

### 2. Definition [Beginner]

- **End-to-end latency:** Total time from the user's request to the system's useful response or completed task.
- **Stage latency:** Time spent in one pipeline stage, such as retrieval, reranking, a tool call, or model generation.
- **Critical path:** The longest chain of dependent stages that determines total completion time.
- **User-perceived latency:** The delay the user feels before feedback, first token, partial value, or final value.
- **Latency budget:** A target allocation of time across stages so the whole product meets its response-time goal.
- **Core idea:** Break total latency into stages, identify dependencies, and optimize the stages that actually control user experience.

Short version:

```text
latency decomposition = where the wait went
critical path = what the user is really waiting on
budget = how much wait each stage is allowed to spend
```

---

### 3. Why It Exists [Beginner]

Latency decomposition exists because GenAI workflows are multi-stage systems.

A simple chat completion might involve:

```text
frontend request
backend auth
prompt assembly
model call
stream response
```

A production RAG or agent system might involve:

```text
intent classification
query rewrite
embedding
hybrid retrieval
metadata filtering
reranking
context packing
tool calls
LLM planning
answer generation
citation validation
safety guardrails
repair call
memory write
analytics logging
```

Without decomposition, teams make the wrong fixes:

| Symptom | Naive Fix | Better Diagnosis |
|---|---|---|
| answer feels slow | use smaller model | first-token latency may be blocked by reranking |
| p95 latency high | reduce average tokens | p95 may be caused by one slow tool |
| agent slow | reduce prompt | loop count and serial tools may dominate |
| RAG slow | lower top-k | vector search may be fast; reranker may be slow |
| final answer slow | remove citations | generation token count may dominate |

Strong statement:

> Latency is not a model property. It is a pipeline property.

---

### 4. Latency Vocabulary [Beginner]

Use precise language.

| Term | Meaning |
|---|---|
| TTFB | time to first byte from backend or provider |
| TTFT | time to first generated token |
| TTLT | time to last token |
| end-to-end latency | user request to final usable result |
| server latency | backend processing time excluding frontend render |
| queue time | time waiting before execution starts |
| network latency | request/response travel time |
| stage latency | time inside one component |
| critical path latency | sum of dependent stages that block completion |
| tail latency | high-percentile latency such as p95 or p99 |
| perceived latency | what the user feels, often improved by streaming/progress |

Important distinction:

```text
time to first token affects perceived responsiveness
time to last token affects task completion
```

For chat UX:

```text
TTFT is emotionally important.
```

For automation:

```text
final completion time is operationally important.
```

---

### 5. The Basic Latency Equation [Intermediate]

For a fully serial pipeline:

```text
total_latency =
    auth_latency
  + routing_latency
  + retrieval_latency
  + reranking_latency
  + tool_latency
  + generation_latency
  + validation_latency
  + response_delivery_latency
```

But most serious systems are not purely serial.

If two stages run in parallel:

```text
parallel_latency = max(stage_a_latency, stage_b_latency)
```

not:

```text
stage_a_latency + stage_b_latency
```

Example:

```text
retrieve user profile: 250 ms
retrieve relevant docs: 700 ms
```

If serial:

```text
950 ms
```

If parallel:

```text
700 ms
```

The critical path is the chain that cannot be overlapped.

This is why graph and workflow design matters.

---

### 6. Typical GenAI Latency Pipeline [Intermediate]

A retrieval-backed answer may look like this:

```text
1. receive request
2. authenticate and load session
3. classify route
4. rewrite query
5. embed query
6. retrieve candidates
7. apply metadata filters
8. rerank candidates
9. pack context
10. generate answer
11. stream tokens
12. validate citations
13. maybe repair answer
14. log trace and update memory
```

Not every stage should block the user.

Blocking before generation:

```text
auth
route
retrieval
reranking if needed
context packing
```

Can often happen while or after generation:

```text
analytics logging
memory write
some evaluations
some citation checks
```

Can sometimes be conditional:

```text
query rewrite
reranking
tool calls
high-cost guardrails
repair calls
```

Strong design question:

```text
Does this stage need to be on the critical path for every request?
```

---

### 7. Retrieval Latency Decomposition [Intermediate]

Retrieval latency is not one thing.

It may include:

```text
query normalization
query rewrite model call
embedding call
vector index search
sparse search
metadata filtering
permission filtering
deduplication
parent document expansion
chunk hydration from storage
network hop to vector database
```

Example:

| Retrieval Stage | Latency |
|---|---:|
| query rewrite | 400 ms |
| embedding | 90 ms |
| vector search | 80 ms |
| sparse search | 120 ms |
| permission filter | 60 ms |
| chunk hydration | 180 ms |
| dedupe and pack | 40 ms |

If serial:

```text
970 ms
```

If vector and sparse search run in parallel after embedding:

```text
400 + 90 + max(80, 120) + 60 + 180 + 40 = 890 ms
```

If query rewrite can be skipped for simple queries:

```text
490 ms saved for easy cases
```

Retrieval optimization is often about:

- avoiding unnecessary rewrites
- running dense and sparse search in parallel
- reducing remote round trips
- caching embeddings for repeated queries
- retrieving fewer but better candidates
- hydrating only needed fields
- moving permission filters earlier
- reducing parent expansion

---

### 8. Reranking Latency Decomposition [Intermediate]

Reranking often improves quality but adds latency.

Reranker latency depends on:

```text
candidate count
query length
chunk length
model type
batching strategy
network overhead
hardware placement
```

Example:

```text
retrieve 80 candidates
rerank top 80
send top 8 to generation
```

Reranking 80 candidates may cost much more latency than vector search itself.

Reranking design choices:

| Design | Latency | Quality |
|---|---:|---|
| no reranker | low | may return weaker context |
| rerank top 20 | moderate | often enough for simple queries |
| rerank top 100 | high | better for ambiguous/hard queries |
| conditional rerank | variable | strong trade-off if routing is good |
| lightweight first-stage rerank plus heavy second-stage rerank | controlled | useful for high-value cases |

Good question:

```text
Does reranking improve cost per successful task enough to justify its latency?
```

Reranking should be measured by:

```text
latency added
answer success gained
groundedness gained
follow-up turns reduced
human review reduced
```

---

### 9. Tool Latency Decomposition [Intermediate]

Tool latency is often unpredictable.

A tool step may include:

```text
model decides tool call
backend validates tool arguments
service request sent
external API executes
database query runs
result is transformed
result is summarized or filtered
model interprets result
```

For agents, tools often create serial chains:

```text
think -> call tool A -> observe -> think -> call tool B -> observe -> answer
```

That is expensive in latency because each step waits for the previous step.

Common tool latency problems:

- slow external APIs
- multiple sequential tools
- over-broad database queries
- large payload transformation
- tool failure and retry
- rate-limit backoff
- model call before and after every tool
- tool result too large to process quickly

Tool design latency principle:

> Prefer fewer, decision-shaped tools over many chatty tools.

Example:

Bad:

```text
get_user()
get_plan()
get_invoices()
get_open_tickets()
get_renewal_date()
```

Better for a specific workflow:

```text
get_customer_support_context(account_id)
```

The better tool may do more backend work, but it reduces agent round trips.

---

### 10. Generation Latency Decomposition [Intermediate]

Generation latency has two main parts:

```text
prefill time
decode time
```

Prefill is the model processing the input context.

Decode is generating output tokens.

Rough intuition:

```text
long input context increases time to first token
long output increases time to last token
```

Important:

```text
retrieval bloat affects generation latency even after retrieval is done
```

If you send 20,000 input tokens to the model, the model must process them before generating.

Generation latency drivers:

- model size and provider performance
- input token count
- output token count
- output format complexity
- structured JSON constraints
- temperature/search settings
- provider queueing
- streaming support
- cache hit rate for stable prefixes

Optimization levers:

- reduce irrelevant context
- cache stable prompt prefixes
- cap output length by task
- stream early
- split long generation into sections only when useful
- use smaller/faster model for simple responses
- avoid asking for verbose hidden formatting when not needed
- use structured outputs only where they add value

Strong distinction:

```text
shorter input improves TTFT
shorter output improves TTLT
```

---

### 11. Guardrail And Validation Latency [Intermediate]

Guardrails can run:

```text
before generation
during retrieval
after generation
after tool calls
before external action
```

Some guardrails must block:

```text
permission checks
unsafe action approval
PII policy for external sharing
payment or mutation confirmation
```

Some can be async or conditional:

```text
quality scoring
non-critical analytics evaluation
post-hoc monitoring
low-risk style checks
```

Latency budget question:

```text
Does this check need to block the user, or can it run in the background?
```

Danger:

```text
Do not move safety-critical checks off the critical path just to look fast.
```

Mature design:

```text
cheap deterministic checks first
conditional model-based checks for uncertain or high-risk cases
async monitoring for non-blocking quality signals
```

---

### 12. User-Perceived Latency [Beginner]

Users do not experience backend spans directly.

They experience:

```text
did the app respond?
is something happening?
can I read partial output?
can I stop or edit?
do I trust the final answer?
```

Ways to improve perceived latency:

- stream generated text
- show retrieval progress for long research tasks
- show selected sources early
- display a concise partial answer before full explanation
- let the user cancel long runs
- move non-critical logging and memory writes off the critical path
- provide progressive results for multi-step workflows

But do not fake progress.

Good progress:

```text
Searching internal docs
Checking policy source
Drafting answer
Verifying citations
```

Bad progress:

```text
Loading...
Thinking...
Almost done...
```

Perceived latency is not cosmetic.

It affects user trust and completion rate.

---

### 13. p50, p95, And p99 Latency [Intermediate]

Average latency is not enough.

You need percentiles.

```text
p50 = median user experience
p95 = slow experience seen by 5 percent of requests
p99 = painful outliers
```

Example:

```text
p50: 2.2 seconds
p95: 9.8 seconds
p99: 31 seconds
```

The product may feel fine in demos but painful in production.

Tail latency often comes from:

- slow tools
- provider queueing
- rare large documents
- retry loops
- large retrieval contexts
- cache misses
- long conversations
- rate limits
- high fan-out
- cold starts

Review latency by slice:

```text
workflow type
tenant
model route
document type
query complexity
turn number
success/failure outcome
tool used
retrieval config version
```

Strong sentence:

> p50 tells you how the happy path feels. p95 and p99 tell you whether the system is operationally serious.

---

### 14. Fan-Out And Tail Latency [Pro]

Fan-out means one user request calls many downstream services or tools.

Example:

```text
search docs
search tickets
search CRM
search billing
search product catalog
```

If all must finish before answering:

```text
total wait = slowest dependency
```

The more services you call, the higher the chance one is slow.

This is tail-latency amplification.

Simple intuition:

```text
one dependency has small chance of being slow
many dependencies have a larger chance that at least one is slow
```

Fan-out mitigation:

- parallelize independent calls
- set per-tool timeouts
- degrade gracefully when low-priority tools fail
- return partial evidence with clear uncertainty
- use cached/stale data where acceptable
- avoid fan-out for simple requests
- route high-value cases to deeper workflows
- combine backend queries into one service where appropriate

But beware:

```text
parallel fan-out reduces median latency but can increase load and cost
```

This is a cost-latency trade-off.

---

### 15. Latency Budgeting [Intermediate]

A latency budget assigns time targets to stages.

Example for interactive RAG:

```text
target time to first token: 2.0 seconds
target time to final answer: 6.0 seconds
```

Budget:

| Stage | Budget |
|---|---:|
| backend setup/auth | 100 ms |
| route/query rewrite | 300 ms |
| embedding | 150 ms |
| retrieval and filtering | 300 ms |
| reranking | 600 ms |
| context packing | 100 ms |
| model first token | 550 ms |
| streaming completion | 4,000 ms |

Total before first token:

```text
100 + 300 + 150 + 300 + 600 + 100 + 550 = 2,100 ms
```

This misses the 2.0 second TTFT target.

Options:

- skip rewrite for simple queries
- rerank fewer candidates
- start source display before answer generation
- use faster model for first draft
- cache query embeddings for repeated queries
- reduce input context to improve prefill
- stream a short answer first, then expand if requested

Budgeting makes trade-offs explicit.

---

### 16. Timeout And Fallback Budgets [Pro]

Every slow stage needs a timeout policy.

Example:

```text
reranker budget: 700 ms
if reranker exceeds 700 ms:
  use vector search order
  mark answer confidence lower
  maybe ask clarifying question
```

Tool timeout example:

```text
CRM lookup budget: 800 ms
billing lookup budget: 1200 ms
product docs search budget: 500 ms
```

Fallback options:

```text
use cached data
use partial result
skip non-critical enrichment
ask user to continue
escalate to async workflow
return "I can answer with available sources, but billing data is unavailable"
```

Bad fallback:

```text
silently hallucinate missing tool data
```

Good fallback:

```text
answer only from available evidence and clearly state missing sources
```

Latency engineering must preserve correctness.

---

### 17. Latency Trace Schema [Pro]

```json
{
  "trace_id": "trace_latency_001",
  "session_id": "sess_123",
  "task_id": "task_456",
  "workflow_type": "support_rag_answer",
  "target_ttft_ms": 2000,
  "target_ttl_ms": 6000,
  "actual_ttft_ms": 2300,
  "actual_ttl_ms": 7200,
  "spans": [
    {
      "span_id": "route",
      "parent_span_id": "root",
      "layer": "routing",
      "start_ms": 0,
      "end_ms": 180,
      "status": "success"
    },
    {
      "span_id": "retrieve",
      "parent_span_id": "root",
      "layer": "retrieval",
      "start_ms": 180,
      "end_ms": 780,
      "status": "success"
    },
    {
      "span_id": "rerank",
      "parent_span_id": "root",
      "layer": "reranking",
      "start_ms": 780,
      "end_ms": 1480,
      "status": "success"
    },
    {
      "span_id": "generate",
      "parent_span_id": "root",
      "layer": "generation",
      "start_ms": 1480,
      "first_token_ms": 2300,
      "end_ms": 7200,
      "input_tokens": 9000,
      "output_tokens": 700,
      "status": "success"
    }
  ],
  "outcome": {
    "task_success": true,
    "user_accepted": true,
    "fallback_used": false
  }
}
```

Must-have fields:

```text
workflow_type
stage/layer
start/end times
TTFT
TTLT
input/output tokens
model and config versions
timeout/fallback status
task outcome
```

Latency traces should join with token traces.

Why?

```text
tokens often explain model latency
retrieval config explains retrieval latency
tool choice explains tail latency
outcome explains whether delay was worth it
```

---

### 18. Code Sample: Span Latency Decomposition

```python
def duration(span):
    return span["end_ms"] - span["start_ms"]


def summarize_latency(spans):
    by_layer = {}

    for span in spans:
        layer = span["layer"]
        by_layer[layer] = by_layer.get(layer, 0) + duration(span)

    total_serial_time = sum(by_layer.values())
    wall_clock_time = max(span["end_ms"] for span in spans) - min(span["start_ms"] for span in spans)

    return {
        "by_layer": by_layer,
        "total_serial_time_ms": total_serial_time,
        "wall_clock_time_ms": wall_clock_time,
    }


spans = [
    {"layer": "routing", "start_ms": 0, "end_ms": 150},
    {"layer": "embedding", "start_ms": 150, "end_ms": 260},
    {"layer": "vector_search", "start_ms": 260, "end_ms": 360},
    {"layer": "sparse_search", "start_ms": 260, "end_ms": 430},
    {"layer": "reranking", "start_ms": 430, "end_ms": 980},
    {"layer": "generation", "start_ms": 980, "end_ms": 5200},
]


print(summarize_latency(spans))
```

Expected lesson:

```text
The sum of stage durations can differ from wall-clock latency when stages overlap.
```

Here, vector search and sparse search overlap.

The user waits for wall-clock time, not naive sum-of-spans.

---

### 19. Mini Program: Critical Path Calculator

This mini program models dependencies between pipeline stages.

```python
def compute_finish_times(stages):
    finish_times = {}

    for name, stage in stages.items():
        dependencies = stage.get("depends_on", [])
        dependency_finish = 0

        if dependencies:
            dependency_finish = max(finish_times[dep] for dep in dependencies)

        finish_times[name] = dependency_finish + stage["duration_ms"]

    return finish_times


def main():
    stages = {
        "route": {
            "duration_ms": 150,
            "depends_on": [],
        },
        "embed_query": {
            "duration_ms": 120,
            "depends_on": ["route"],
        },
        "vector_search": {
            "duration_ms": 100,
            "depends_on": ["embed_query"],
        },
        "sparse_search": {
            "duration_ms": 180,
            "depends_on": ["route"],
        },
        "merge_results": {
            "duration_ms": 50,
            "depends_on": ["vector_search", "sparse_search"],
        },
        "rerank": {
            "duration_ms": 700,
            "depends_on": ["merge_results"],
        },
        "generate_answer": {
            "duration_ms": 4200,
            "depends_on": ["rerank"],
        },
        "log_analytics": {
            "duration_ms": 200,
            "depends_on": ["generate_answer"],
        },
    }

    finish_times = compute_finish_times(stages)

    for name, finish_time in finish_times.items():
        print(f"{name:16s} finishes at {finish_time} ms")

    critical_completion = finish_times["generate_answer"]
    full_backend_completion = max(finish_times.values())

    print()
    print("User-visible answer complete:", critical_completion, "ms")
    print("Backend fully complete:", full_backend_completion, "ms")


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
Not every backend task should define user-visible latency.
```

In this example, analytics logging can finish after the answer is complete.

---

### 20. Hands-On Lab: Build A Latency Budget For One GenAI Flow [Pro]

#### Build

Choose one flow:

```text
support RAG answer
research assistant
invoice extraction
agentic tool workflow
document Q&A
coding assistant
```

Define the user experience target:

```text
time to acknowledgement
time to first useful progress
time to first token
time to final answer
time to verified final answer
```

Create a latency budget:

```text
auth/session load
route/classify
query rewrite
embedding
retrieval
reranking
tool calls
context packing
generation TTFT
generation TTLT
validation
memory write
logging
frontend render
```

#### Trace

For 10 sample requests, record:

```text
stage latency
input tokens
output tokens
candidate count
tool count
retry count
success/failure outcome
fallback used
```

#### Analyze

Answer:

1. What is the p50 latency?
2. What is the p95 latency?
3. Which stage dominates p50?
4. Which stage dominates p95?
5. Which stages are serial?
6. Which stages can run in parallel?
7. Which stages can be conditional?
8. Which stages can move after first token?
9. Which stages can move after final answer?
10. Which latency increase improves quality enough to keep?

#### Optimize

Try one change:

```text
parallelize dense and sparse retrieval
skip query rewrite for simple queries
rerank fewer candidates
cache stable prompt prefix
trim retrieved context
make tool calls parallel
create a workflow-specific aggregate tool
stream earlier
move memory write async
make validator conditional
```

Measure:

```text
TTFT change
TTLT change
p95 change
cost change
success change
quality/safety change
```

#### Defend

Write:

```text
The critical path was <path>.
The largest latency contributor was <stage>.
The optimization changed <stage> from <before> to <after>.
The user-visible impact was <impact>.
I would ship / not ship because <quality and safety reason>.
```

---

### 21. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| blaming the model for all latency | retrieval/tools/reranking may dominate | decompose by stage |
| optimizing average latency only | p95/p99 may be the real pain | review percentiles and slices |
| summing parallel spans | overstates wall-clock latency | compute critical path |
| ignoring TTFT | users care about first visible progress | measure TTFT and TTLT separately |
| moving safety checks async blindly | can create unsafe fast responses | keep blocking checks for high-risk actions |
| reranking every query heavily | adds latency to easy cases | make reranking conditional or tiered |
| allowing unbounded tool calls | agents become serial and slow | cap steps and aggregate tools |
| no timeout policy | one slow dependency blocks all users | define timeouts and fallbacks |
| no version tags | regressions are hard to locate | log prompt/retrieval/tool/model versions |
| optimizing latency without quality | fast wrong answers are not wins | measure cost, latency, quality, and safety together |

---

### 22. Practical Interview Question [Intermediate]

> You are designing a production RAG assistant. Users complain that answers take too long. The pipeline includes query rewriting, embedding, retrieval, reranking, tool calls, answer generation, and citation validation. How would you decompose and improve latency without hurting answer quality?

---

### 23. Strong Answer [Pro]

I would start by instrumenting the full request path with spans for each stage: request setup, routing, query rewrite, embedding, retrieval, filtering, reranking, tool calls, context packing, answer generation, citation validation, repair, memory write, and logging. I would measure both time to first token and time to final answer, then review p50, p95, and p99 latency by workflow type, query complexity, tenant, model route, tool usage, retrieval config, and task outcome.

Then I would identify the critical path. I would not just sum every span, because some work may run in parallel or after the response. If dense and sparse search are independent, I would run them in parallel. If memory write or analytics logging is not needed for the answer, I would move it off the user-visible path. If a tool is slow and non-critical, I would add a timeout and fallback instead of blocking every request.

For retrieval, I would break down query rewrite, embedding, vector search, sparse search, filtering, chunk hydration, and reranking. If reranking dominates, I would test reranking fewer candidates or running it only for ambiguous queries. If retrieval context is large, I would reduce redundant chunks and pack context better, because large input also increases model prefill time. For tools, I would avoid many sequential calls by creating workflow-specific aggregate tools or parallelizing independent calls.

For generation, I would measure first-token latency separately from completion latency. Long input context mostly hurts first-token latency, while long output hurts final completion. I would use streaming to improve perceived latency, but I would still keep correctness-critical validation where it belongs. For safety or citation checks, I would decide which checks must block and which can be conditional or async.

I would ship only changes that improve latency while preserving groundedness, success rate, and safety. The final recommendation would include the before/after latency budget, the critical path change, p95 impact, cost impact, and any quality trade-off.

---

### 24. Active Recall [Beginner]

Answer these without looking:

1. What is end-to-end latency?
2. What is stage latency?
3. What is the critical path?
4. What is user-perceived latency?
5. What is the difference between TTFT and TTLT?
6. Why is latency a pipeline property?
7. Why can two systems with the same total latency feel different?
8. What are common retrieval latency components?
9. Why can reranking dominate retrieval latency?
10. Why are tool calls dangerous for latency?
11. What is prefill time?
12. What is decode time?
13. Which tokens mostly affect first-token latency?
14. Which tokens mostly affect completion latency?
15. Why are p95 and p99 important?
16. What is fan-out?
17. Why does fan-out amplify tail latency?
18. What is a latency budget?
19. What is a timeout fallback?
20. What is the final lesson of latency decomposition?

Expected answers:

1. User request to useful response or task completion.
2. Time spent in one component or pipeline step.
3. Longest dependent chain that determines completion time.
4. The wait the user actually feels before progress or value.
5. First generated token vs final generated token.
6. Many stages contribute beyond the model call.
7. Streaming and early progress change perception.
8. Rewrite, embedding, search, filters, hydration, dedupe, packing.
9. It may score many candidates with a heavier model.
10. They add external dependency time and serial agent loops.
11. Model processing input context before generation.
12. Model producing output tokens.
13. Long input context.
14. Long output length.
15. They expose slow real-user experiences and outliers.
16. One request calling many downstream services.
17. More dependencies increase the chance one is slow.
18. Target time allocation across pipeline stages.
19. A bounded wait followed by a safe degraded behavior.
20. Measure the wait by stage and optimize the critical path, not the vague total.

---

### 25. Revision Notes

- **One-line summary:** End-to-end GenAI latency is the critical path across retrieval, reranking, tools, generation, and validation, not just model speed.
- **Three keywords:** stages, critical path, percentiles.
- **One interview trap:** Saying "use a faster model" before measuring retrieval, reranking, tools, and generation separately.
- **One memory trick:** Cost asks where money went; latency asks where waiting went.

Final takeaway:

> Serious GenAI latency work starts by decomposing the full pipeline, finding the critical path, and optimizing only the waits that matter for user value, quality, and safety.

---

## Subtopic 20.2.b: Streaming, Batching, Concurrency, and Timeout Budgets

> **Subtopic time:** 2h
> Outcome: You should be able to explain how streaming, batching, concurrency, and timeout budgets shape GenAI latency. You should also be able to choose the right lever for interactive UX, high-throughput workloads, tool-heavy agents, and production failure handling.

### Add to Knowledge Base

After you decompose latency by stage, you need controls.

Four of the most important controls are:

```text
streaming
batching
concurrency
timeout budgets
```

They solve different latency problems.

Streaming improves perceived responsiveness.

Batching improves throughput and cost efficiency, sometimes at the expense of per-request latency.

Concurrency overlaps independent work, but can overload dependencies if unbounded.

Timeout budgets prevent one slow stage from consuming the whole user experience.

The core mental model:

> Streaming changes what the user feels. Batching changes how work is grouped. Concurrency changes what can happen at the same time. Timeout budgets decide when waiting stops.

A mature GenAI system uses all four deliberately.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand the four latency levers and what each one is for.
- **Intermediate:** Read sections 7-16 to reason about trade-offs, queues, backpressure, deadlines, and fallbacks.
- **Pro:** Complete the lab and practice the interview answer so you can defend pipeline latency design under production constraints.

---

### 0. Pre-Question Hook [Beginner]

A RAG assistant takes 7 seconds to produce a final answer.

You have four possible changes:

```text
stream tokens as soon as generation begins
batch embedding requests across users
run dense search and sparse search concurrently
timeout a slow CRM lookup after 800 ms
```

Which one improves latency?

Answer:

```text
all of them can improve something, but not the same thing
```

Streaming may not reduce total backend time, but it reduces perceived waiting.

Batching may improve throughput under load, but it may add small queue delay.

Concurrency may reduce critical-path time by overlapping independent stages.

Timeouts may reduce p95/p99 latency by preventing slow dependencies from blocking the whole request.

The senior skill is not knowing these words.

The senior skill is choosing the right lever for the bottleneck.

---

### 1. The Intuition [Beginner]

Imagine a busy coffee shop.

Streaming is like handing the customer part of the order as soon as it is ready:

```text
Here is your coffee; the sandwich is still coming.
```

Batching is like making several similar drinks together:

```text
Prepare four lattes in one efficient run.
```

Concurrency is like having different workers handle different tasks at the same time:

```text
one person takes payment while another makes coffee
```

Timeouts are like deciding not to wait forever for one ingredient:

```text
If oat milk is not available in 30 seconds, ask the customer or use the fallback.
```

GenAI pipelines need the same operational thinking.

Without these controls, systems become:

```text
slow for users
expensive under load
fragile when dependencies are slow
unpredictable at p95 and p99
```

---

### 2. Definition [Beginner]

- **Streaming:** Sending partial model output or progress events to the user before the full task is complete.
- **Batching:** Grouping multiple similar operations together so they can be processed more efficiently.
- **Concurrency:** Running independent operations at the same time instead of sequentially.
- **Timeout budget:** A maximum allowed wait for a request, workflow, stage, tool, or retry.
- **Deadline propagation:** Passing the remaining time budget through downstream calls so each stage knows how much time is left.
- **Core idea:** Latency design is not only about making each stage faster. It is about controlling how work is shown, grouped, overlapped, and bounded.

Short version:

```text
stream for responsiveness
batch for throughput
concur for overlap
timeout for predictability
```

---

### 3. Why It Exists [Beginner]

These controls exist because production GenAI systems face four realities.

#### Reality 1: Users dislike silence

Even if final output takes 8 seconds, the user experience is better if progress starts in 1 second.

#### Reality 2: Providers and models have throughput limits

Embedding, reranking, evaluation, and generation requests can be more efficient when grouped, but grouping creates wait time.

#### Reality 3: Pipelines contain independent work

Retrieval, profile loading, policy loading, and some tool calls do not always need to happen one after another.

#### Reality 4: Dependencies fail slowly

A slow tool can be worse than a failed tool because it blocks the workflow while consuming the budget.

Strong statement:

> Latency control is the art of deciding what the system should do while it waits.

---

### 4. The Four Levers At A Glance [Beginner]

| Lever | Main Benefit | Main Risk | Best For |
|---|---|---|---|
| streaming | improves perceived latency | hard validation and partial-output UX | chat, writing, summarization, research |
| batching | improves throughput and efficiency | adds queue delay | embeddings, reranking, eval jobs, offline processing |
| concurrency | reduces wall-clock time | overload, rate limits, complex failure handling | retrieval fan-out, independent tools, parallel validators |
| timeout budgets | controls tail latency | premature fallback if too aggressive | tools, rerankers, external APIs, long agents |

Do not treat them as interchangeable.

Example:

```text
If total generation takes long because output is long, streaming helps UX.
If vector search and sparse search are independent, concurrency helps wall-clock time.
If reranker throughput is the bottleneck, batching may help.
If a tool p99 is terrible, timeout budgets help.
```

---

### 5. Streaming: What It Actually Improves [Beginner]

Streaming does not necessarily make the model finish faster.

It improves:

```text
time to first visible progress
time to first token
user trust that the system is working
ability to stop early
ability to read while generation continues
```

Streaming mostly affects:

```text
perceived latency
```

not always:

```text
total completion latency
```

Example:

```text
non-streaming:
  user sees nothing for 6 seconds
  full answer appears

streaming:
  first token appears at 1.2 seconds
  answer completes at 6 seconds
```

Same completion time.

Better experience.

Streaming is strongest when:

- output is long
- answer can be consumed progressively
- the user may stop once they have enough
- the product benefits from visible progress
- final validation does not need to block every word

Streaming is weaker when:

- output must be fully validated before display
- output is a small JSON payload
- partial output could be misleading or unsafe
- the task is an automation where only final result matters

---

### 6. Streaming Design Patterns [Intermediate]

#### Pattern 1: Stream Final Answer Tokens

Most common chat pattern:

```text
retrieve -> generate -> stream tokens
```

Good for:

```text
Q&A, writing, summarization, coding help
```

Risk:

```text
unsupported or unsafe content may appear before post-checks finish
```

Mitigation:

```text
perform required pre-checks before streaming
use grounded prompts and citations
use constrained tools
block high-risk flows until validation completes
```

#### Pattern 2: Stream Progress Events

Instead of only tokens, stream stages:

```text
searching docs
checking account status
reranking sources
drafting answer
verifying citations
```

Good for:

```text
research agents, long workflows, tool-heavy tasks
```

Risk:

```text
progress messages can become noise if too vague
```

Good progress events should reflect real stages.

#### Pattern 3: Stream Sources Before Answer

For RAG:

```text
show selected sources first
then stream grounded answer
```

This improves trust and makes waiting feel meaningful.

#### Pattern 4: Stream Draft Then Verify

Useful only when the UX clearly marks the answer as draft.

Bad:

```text
show unverified answer as final
```

Better:

```text
draft visible
verification state visible
final verified state replaces draft
```

Use carefully for domains where correctness matters.

---

### 7. Streaming Risks And Backpressure [Pro]

Streaming creates system design responsibilities.

Common risks:

- user disconnects mid-stream
- downstream model continues generating after disconnect
- frontend cannot render chunks quickly enough
- network buffers accumulate
- post-validation fails after partial content was shown
- logs capture partial/incomplete outputs
- retries duplicate streamed text
- tool events arrive out of order

Backpressure means the consumer cannot keep up with the producer.

Example:

```text
model emits chunks quickly
server queues chunks
client is slow or disconnected
memory usage grows
```

Good streaming systems handle:

```text
client disconnect cancellation
chunk ordering
idempotent events
heartbeat or keepalive events
bounded buffers
final completion marker
error marker
partial-output logging
```

Recommended event structure:

```json
{
  "event_id": 17,
  "trace_id": "trace_123",
  "type": "token",
  "delta": "example text",
  "is_final": false
}
```

Final event:

```json
{
  "event_id": 45,
  "trace_id": "trace_123",
  "type": "complete",
  "finish_reason": "stop",
  "usage": {
    "input_tokens": 8200,
    "output_tokens": 640
  }
}
```

Streaming is a UX feature and a protocol feature.

---

### 8. Batching: Throughput vs Per-Request Latency [Intermediate]

Batching groups similar work.

Common GenAI batching targets:

```text
embedding many chunks
embedding multiple user queries
reranking candidates
evaluating generated answers
classifying requests
offline summarization
batch document extraction
```

Batching improves:

```text
throughput
hardware utilization
provider efficiency
cost efficiency in some systems
```

But batching may hurt:

```text
individual request latency
```

Why?

Because a request may wait for a batch to fill.

Example:

```text
process immediately: 120 ms
wait for batch: 50 ms
process batch: 90 ms
total for first request: 140 ms
```

Throughput improved.

One request waited longer.

Batching is excellent for:

- offline jobs
- ingestion pipelines
- evaluation runs
- high-volume embeddings
- reranking many candidates
- background classification

Batching is risky for:

- interactive first-token path
- low-traffic products where batches do not fill
- high-priority requests mixed with bulk work
- stages with strict timeout budgets

Strong sentence:

> Batching optimizes the system's work; streaming optimizes the user's waiting experience.

---

### 9. Dynamic Batching [Pro]

Dynamic batching waits briefly to collect requests.

Typical policy:

```text
max_batch_size = 32
max_wait_ms = 20
```

Meaning:

```text
run when 32 items arrive
or when oldest item has waited 20 ms
```

This balances:

```text
throughput
latency
fairness
```

For interactive systems, max wait must be small.

For offline systems, max wait can be larger.

Bad dynamic batching:

```text
wait too long for perfect batch size
```

Better:

```text
respect request deadlines and priority classes
```

Priority-aware batching:

```text
interactive user requests
high-priority automation
background ingestion
offline eval
```

Do not batch all classes together blindly.

Otherwise background work can delay user-facing work.

---

### 10. Batching In Retrieval Pipelines [Intermediate]

Batching appears in multiple retrieval stages.

#### Embedding Batches

Offline ingestion:

```text
batch chunks into embedding calls
```

Great fit because users are not waiting.

Online query embeddings:

```text
batch only if traffic is high and wait is tiny
```

Otherwise it can hurt TTFT.

#### Reranking Batches

Rerankers often score:

```text
query + candidate chunk
```

For one query with 80 candidates, batching candidates can improve throughput.

But:

```text
reranking too many candidates increases latency
```

Good pattern:

```text
retrieve many cheaply
rerank a bounded candidate set
send small final context to generation
```

#### Evaluation Batches

Post-hoc eval can often be batched asynchronously:

```text
quality scoring
groundedness judging
toxicity sampling
regression tests
```

Do not put bulk evaluation on the user's critical path unless required.

---

### 11. Concurrency: Overlap Independent Work [Intermediate]

Concurrency reduces wall-clock time by doing independent work at the same time.

Example serial:

```text
load user profile: 250 ms
retrieve docs: 700 ms
load policy config: 150 ms
total: 1100 ms
```

Concurrent:

```text
max(250, 700, 150) = 700 ms
```

Good candidates for concurrency:

- dense and sparse retrieval
- independent tool calls
- loading user/session/config data
- parallel document searches across indexes
- multiple deterministic validators
- prefetching likely context
- post-response logging and memory write

Bad candidates:

- dependent steps
- expensive work that may not be needed
- tools with strict rate limits
- safety checks that must happen in order
- mutations that require transaction ordering

Concurrency question:

```text
Can these steps run at the same time without changing correctness?
```

If yes, consider parallelism.

If no, keep sequence clear.

---

### 12. Bounded Concurrency [Pro]

Concurrency must be bounded.

Unbounded concurrency causes:

```text
provider rate-limit errors
database overload
tool outages
memory pressure
retry storms
noisy-neighbor problems
```

Bad:

```text
for every candidate:
    call reranker asynchronously with no limit
```

Better:

```text
use a concurrency limit
```

Common controls:

```text
semaphores
worker pools
connection pools
rate limiters
per-tenant quotas
per-tool concurrency caps
queue depth limits
bulkheads
```

Bulkhead idea:

```text
limit each dependency separately so one slow tool does not consume all workers
```

Example:

```text
CRM tool max concurrency: 20
billing tool max concurrency: 10
retrieval max concurrency: 100
offline eval max concurrency: 5
```

Bounded concurrency protects p95 and p99.

---

### 13. Queueing And Head-Of-Line Blocking [Intermediate]

When demand exceeds capacity, requests wait in queues.

Queue time is latency.

A system can be slow even if processing time is fast.

Example:

```text
model call execution: 1.5 seconds
queue wait: 4 seconds
total: 5.5 seconds
```

Head-of-line blocking happens when one slow job blocks later jobs.

Example:

```text
large document extraction enters same queue as quick chat answers
quick answers wait behind large job
```

Fixes:

- separate queues by priority or workflow
- separate worker pools for interactive and batch jobs
- cap job size
- chunk large jobs
- use deadlines to drop stale work
- avoid mixing background ingestion with user-facing requests

Important:

```text
batching can create head-of-line blocking if batch classes are mixed badly
```

Queue design is latency design.

---

### 14. Timeout Budgets [Intermediate]

A timeout is not just a number.

It is a product decision.

Example:

```text
total user-facing deadline: 6 seconds
retrieval budget: 900 ms
reranker budget: 700 ms
tool budget: 1200 ms
generation TTFT budget: 2000 ms
final answer budget: 6000 ms
```

Timeout budgets force trade-offs:

```text
wait longer for quality
or return sooner with fallback
```

Good timeout design includes:

```text
overall request deadline
per-stage timeout
retry budget
fallback behavior
cancellation
logging
user-facing explanation when needed
```

Bad timeout design:

```text
every service uses its own default timeout
retries ignore the user's remaining deadline
slow tools continue running after user disconnect
fallback silently fabricates missing data
```

Strong sentence:

> A timeout without a fallback is just a delayed failure.

---

### 15. Deadline Propagation [Pro]

Deadline propagation means every downstream stage receives the remaining time.

Example:

```text
overall deadline: 6000 ms
already spent: 1700 ms
remaining: 4300 ms
```

A downstream tool should not start a 5000 ms attempt.

It should know:

```text
remaining_budget_ms = 4300
my_max_timeout_ms = min(default_tool_timeout_ms, remaining_budget_ms - safety_margin)
```

This avoids impossible work.

Deadline-aware retries:

```text
do not retry if the retry cannot finish within remaining budget
```

Deadline-aware generation:

```text
reduce max output tokens if little time remains
```

Deadline-aware retrieval:

```text
skip slow reranker if retrieval budget is nearly exhausted
```

Deadline propagation turns latency from hope into control.

---

### 16. Retries, Cancellation, And Fallbacks [Pro]

Retries can improve reliability but harm latency.

Retry only when:

```text
failure is likely transient
remaining deadline is sufficient
operation is idempotent or safe to repeat
retry does not overload the dependency
```

Bad retry:

```text
tool times out after 2 seconds
retry same tool for 2 seconds
then retry again
user waits 6 seconds and gets nothing
```

Better:

```text
tool budget is 2 seconds total
one fast retry only if first failure occurs quickly
fallback after budget expires
```

Cancellation matters.

Cancel work when:

- user disconnects
- request deadline expires
- another branch already produced sufficient answer
- safety policy blocks the workflow
- parent workflow is cancelled

Fallback options:

```text
use cached result
use partial evidence
skip optional enrichment
ask a clarifying question
defer to async job
escalate to human
return answer with stated limitation
```

Never fallback by pretending missing information exists.

---

### 17. Circuit Breakers And Load Shedding [Pro]

Timeout budgets protect individual requests.

Circuit breakers protect the system.

Circuit breaker:

```text
if dependency is failing or too slow, stop calling it temporarily
```

Load shedding:

```text
drop, defer, or degrade lower-priority work when the system is overloaded
```

GenAI examples:

```text
disable expensive reranking during incident
skip non-critical evaluators
route easy tasks to faster model
defer offline embedding jobs
turn off deep research mode temporarily
serve cached answers for common questions
limit agent max steps
```

This is not giving up.

It is preserving core product behavior under stress.

Incident principle:

```text
degrade optional quality before breaking essential availability
```

But:

```text
do not degrade safety-critical checks
```

---

### 18. How The Four Levers Interact [Intermediate]

These levers can help or hurt each other.

| Combination | Useful Pattern | Risk |
|---|---|---|
| streaming + validation | stream after required pre-checks | post-check may fail after content shown |
| batching + timeout | efficient throughput within max wait | batch wait can consume deadline |
| concurrency + rate limits | overlap independent calls | overload and retries |
| concurrency + timeouts | slow branches stop blocking | partial results need honest UX |
| batching + priority queues | efficient and fair | poor priority design delays users |
| streaming + cancellation | user can stop early | backend must cancel provider/tool work |
| retries + deadlines | recover transient failures | retry storm or deadline overrun |

Design rule:

```text
optimize the whole control loop, not one lever in isolation
```

Example:

```text
Increasing concurrency may reduce latency until rate limits trigger.
Then retries increase, queues grow, and p99 gets worse.
```

Every lever has a saturation point.

---

### 19. Latency Control Trace Schema [Pro]

```json
{
  "trace_id": "trace_latency_control_001",
  "workflow_type": "support_rag_answer",
  "overall_deadline_ms": 6000,
  "ttft_ms": 1400,
  "ttlt_ms": 5200,
  "streaming_enabled": true,
  "events_streamed": 96,
  "batching": {
    "embedding_batch_size": 8,
    "embedding_batch_wait_ms": 12,
    "rerank_batch_size": 40,
    "rerank_batch_wait_ms": 0
  },
  "concurrency": {
    "parallel_branches": ["dense_search", "sparse_search", "profile_load"],
    "max_tool_concurrency": 4,
    "rate_limited": false
  },
  "timeouts": [
    {
      "stage": "rerank",
      "budget_ms": 700,
      "actual_ms": 620,
      "timed_out": false
    },
    {
      "stage": "crm_lookup",
      "budget_ms": 800,
      "actual_ms": 800,
      "timed_out": true,
      "fallback": "used_cached_account_summary"
    }
  ],
  "outcome": {
    "task_success": true,
    "fallback_used": true,
    "user_accepted": true
  }
}
```

Why log these fields?

```text
streaming fields explain perceived latency
batch fields explain queue wait and throughput
concurrency fields explain fan-out and overload
timeout fields explain p95/p99 and fallback quality
outcome fields explain whether the trade-off worked
```

---

### 20. Code Sample: Bounded Concurrent Tool Calls

This example shows how to run independent tools concurrently without allowing unlimited fan-out.

```python
import asyncio


async def call_tool(name, latency_ms, timeout_ms):
    await asyncio.sleep(latency_ms / 1000)
    return {
        "tool": name,
        "latency_ms": latency_ms,
        "status": "success",
    }


async def call_with_timeout(tool, semaphore):
    async with semaphore:
        try:
            return await asyncio.wait_for(
                call_tool(
                    name=tool["name"],
                    latency_ms=tool["latency_ms"],
                    timeout_ms=tool["timeout_ms"],
                ),
                timeout=tool["timeout_ms"] / 1000,
            )
        except asyncio.TimeoutError:
            return {
                "tool": tool["name"],
                "latency_ms": tool["timeout_ms"],
                "status": "timeout",
                "fallback": tool["fallback"],
            }


async def main():
    tools = [
        {
            "name": "dense_search",
            "latency_ms": 180,
            "timeout_ms": 500,
            "fallback": "skip_dense",
        },
        {
            "name": "sparse_search",
            "latency_ms": 260,
            "timeout_ms": 500,
            "fallback": "skip_sparse",
        },
        {
            "name": "crm_lookup",
            "latency_ms": 1200,
            "timeout_ms": 800,
            "fallback": "use_cached_profile",
        },
    ]

    semaphore = asyncio.Semaphore(2)
    results = await asyncio.gather(
        *(call_with_timeout(tool, semaphore) for tool in tools)
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

Expected lesson:

```text
Concurrency should be parallel, bounded, timeout-aware, and fallback-aware.
```

---

### 21. Mini Program: Timeout Budget Simulator

This mini program compares serial execution, concurrent execution, and timeout-limited execution.

```python
def serial_latency(stages):
    return sum(stage["latency_ms"] for stage in stages)


def concurrent_latency(stages):
    return max(stage["latency_ms"] for stage in stages)


def timeout_limited_latency(stages):
    return max(min(stage["latency_ms"], stage["timeout_ms"]) for stage in stages)


def describe_stage(stage):
    timed_out = stage["latency_ms"] > stage["timeout_ms"]
    actual = min(stage["latency_ms"], stage["timeout_ms"])

    return {
        "name": stage["name"],
        "actual_wait_ms": actual,
        "timed_out": timed_out,
        "fallback": stage["fallback"] if timed_out else None,
    }


def main():
    independent_tools = [
        {
            "name": "docs_search",
            "latency_ms": 300,
            "timeout_ms": 600,
            "fallback": "use_no_docs",
        },
        {
            "name": "crm_lookup",
            "latency_ms": 1200,
            "timeout_ms": 800,
            "fallback": "use_cached_crm_summary",
        },
        {
            "name": "billing_lookup",
            "latency_ms": 500,
            "timeout_ms": 900,
            "fallback": "omit_billing_details",
        },
    ]

    print("Serial latency:", serial_latency(independent_tools), "ms")
    print("Concurrent latency:", concurrent_latency(independent_tools), "ms")
    print("Timeout-limited concurrent latency:", timeout_limited_latency(independent_tools), "ms")
    print()

    for stage in independent_tools:
        print(describe_stage(stage))


if __name__ == "__main__":
    main()
```

Expected output shape:

```text
Serial latency: 2000 ms
Concurrent latency: 1200 ms
Timeout-limited concurrent latency: 800 ms

{'name': 'docs_search', 'actual_wait_ms': 300, 'timed_out': False, 'fallback': None}
{'name': 'crm_lookup', 'actual_wait_ms': 800, 'timed_out': True, 'fallback': 'use_cached_crm_summary'}
{'name': 'billing_lookup', 'actual_wait_ms': 500, 'timed_out': False, 'fallback': None}
```

Expected lesson:

```text
Concurrency reduces wait to the slowest branch; timeout budgets cap the slowest branch.
```

---

### 22. Hands-On Lab: Design Latency Controls For One Workflow [Pro]

#### Build

Choose one workflow:

```text
support RAG answer
research agent
invoice extraction
tool-using assistant
document Q&A
coding assistant
```

Define:

```text
target TTFT
target TTLT
overall deadline
interactive vs background stages
quality and safety constraints
```

#### Map

List stages:

```text
route
query rewrite
embedding
dense retrieval
sparse retrieval
reranking
tool calls
context packing
generation
validation
memory write
logging
```

For each stage, decide:

```text
streamed or not
batched or not
concurrent or serial
timeout budget
fallback behavior
must block user or can run async
```

#### Stress

Create three scenarios:

1. Normal case.
2. Slow tool case.
3. High traffic case.

For each scenario, answer:

```text
What streams to the user?
What gets batched?
What runs concurrently?
What times out?
What fallback is used?
What is the user told?
What quality or safety risk exists?
```

#### Defend

Write:

```text
I would stream <events/tokens> because <reason>.
I would batch <stage> with max wait <budget> because <reason>.
I would run <branches> concurrently with limit <N> because <reason>.
I would timeout <stage> after <budget> and fallback to <fallback>.
This preserves <quality/safety constraint> while improving <latency metric>.
```

---

### 23. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| assuming streaming reduces backend time | it mostly improves perceived latency | measure TTFT and TTLT separately |
| streaming unsafe drafts as final | users may see unvalidated content | pre-check or clearly mark draft state |
| batching interactive work too aggressively | batch wait hurts responsiveness | use small max wait and priority queues |
| mixing batch and interactive queues | background work delays users | separate queues and worker pools |
| unbounded concurrency | overloads dependencies and triggers retries | use semaphores, pools, and rate limits |
| parallelizing dependent steps | breaks correctness | only overlap independent work |
| no timeout hierarchy | downstream calls consume entire deadline | propagate deadlines |
| retrying after deadline is impossible | increases latency with no chance of success | make retries deadline-aware |
| timeout without fallback | turns slowness into failure | define safe degraded behavior |
| moving safety checks async blindly | fast unsafe behavior is not acceptable | keep critical checks blocking |
| ignoring cancellation | wasted spend after disconnect | cancel child work when parent ends |
| optimizing throughput only | user latency may regress | track p50/p95/p99 and task success |

---

### 24. Practical Interview Question [Intermediate]

> You are building a tool-using RAG assistant. It must feel responsive, handle high traffic, call several external tools, and avoid long tail latency. How would you use streaming, batching, concurrency, and timeout budgets?

---

### 25. Strong Answer [Pro]

I would treat those as four separate controls rather than one generic performance trick. First, I would use streaming to improve perceived latency. For a chat or RAG answer, I would stream progress events during retrieval and then stream answer tokens once required pre-checks are complete. I would measure time to first token separately from time to final answer, because streaming can improve user experience without reducing backend completion time.

Second, I would use batching where throughput matters and where a small queue wait is acceptable. Embedding ingestion, reranking candidates, offline evaluation, and background classification are good candidates. For interactive query embeddings or first-token paths, I would use very small dynamic-batch wait times or avoid batching if traffic is low. I would separate interactive and background queues so batch jobs do not block user-facing requests.

Third, I would use concurrency for independent work. Dense retrieval, sparse retrieval, profile loading, policy loading, and independent tool calls can often run in parallel. But I would bound concurrency with semaphores, worker pools, connection pools, and per-tool limits so the system does not overload dependencies or trigger rate-limit retries. I would also avoid parallelizing steps that have correctness dependencies or mutation ordering.

Fourth, I would define an overall request deadline and per-stage timeout budgets. Slow tools, rerankers, and external APIs should have explicit budgets and safe fallbacks. Deadlines should propagate downstream so retries and tool calls know how much time remains. If a CRM lookup times out, for example, the system might use cached account context or answer only from available evidence while clearly stating the limitation. It should never invent missing tool data.

I would validate the design with traces showing TTFT, TTLT, p50/p95/p99 latency, queue time, batch wait time, concurrency limits, timeout rates, fallback rates, cost, and task success. The goal is not just faster responses; it is predictable latency with acceptable quality, safety, and cost.

---

### 26. Active Recall [Beginner]

Answer these without looking:

1. What does streaming improve most directly?
2. Does streaming always reduce total backend latency?
3. What is batching?
4. What is the main trade-off of batching?
5. What is dynamic batching?
6. Why should interactive and background queues be separated?
7. What is concurrency?
8. Why must concurrency be bounded?
9. What is head-of-line blocking?
10. What is a timeout budget?
11. What is deadline propagation?
12. Why are retries dangerous without deadlines?
13. What is cancellation?
14. What is a safe fallback?
15. What is a circuit breaker?
16. What is load shedding?
17. How can batching hurt latency?
18. How can concurrency hurt p99?
19. Why should streaming include backpressure handling?
20. What is the final lesson of this topic?

Expected answers:

1. Perceived responsiveness and time to visible progress.
2. No, total completion can stay the same.
3. Grouping similar work for efficient processing.
4. Better throughput but possible queue delay.
5. Waiting briefly to collect a batch up to size or time limits.
6. Background jobs can delay user-facing work.
7. Running independent operations at the same time.
8. Unbounded concurrency overloads dependencies and causes retries.
9. A slow job blocking later jobs in the same queue.
10. Maximum allowed wait for a request or stage.
11. Passing remaining time budget to downstream stages.
12. They can consume time with no chance of finishing usefully.
13. Stopping child work when the parent request ends or expires.
14. A degraded behavior that is honest and preserves correctness.
15. A mechanism that temporarily stops calls to a failing dependency.
16. Dropping, deferring, or degrading lower-priority work under overload.
17. Requests may wait for the batch to fill.
18. Too many parallel calls can trigger rate limits, queues, and retries.
19. Slow clients or disconnects can cause buffers and wasted work.
20. Use streaming, batching, concurrency, and timeouts deliberately according to the bottleneck.

---

### 27. Revision Notes

- **One-line summary:** Streaming, batching, concurrency, and timeout budgets are different latency controls that must be matched to the bottleneck and user experience.
- **Three keywords:** stream, batch, bound.
- **One interview trap:** Saying "parallelize everything" without rate limits, deadlines, fallbacks, or correctness ordering.
- **One memory trick:** Streaming shows progress; batching groups work; concurrency overlaps work; timeouts stop waiting.

Final takeaway:

> A production GenAI pipeline feels fast and stays reliable when it streams useful progress, batches only where appropriate, runs independent work concurrently with limits, and gives every slow dependency a deadline plus a safe fallback.

---

## Subtopic 20.2.c: Should You Rerank or Increase Top-k: Tradeoff Reasoning

> **Subtopic time:** 2h
> Outcome: You should be able to decide whether a RAG system should retrieve more candidates, rerank candidates, do both, or do neither. You should reason from retrieval failure type, latency budget, token budget, quality target, and business risk instead of copying a default top-k value.

### Add to Knowledge Base

One of the most common RAG tuning questions is:

```text
Should we increase top-k or add a reranker?
```

This sounds like a small configuration choice.

It is actually a product trade-off involving:

```text
recall
precision
latency
token cost
context-window pressure
answer groundedness
user trust
failure risk
```

Increasing top-k says:

```text
Maybe the right evidence is missing, so retrieve more.
```

Reranking says:

```text
Maybe the right evidence is present but buried, so reorder and filter better.
```

The core mental model:

> Increase top-k when the answer evidence is not making it into the candidate set. Rerank when the evidence is in the candidate set but not reliably placed into the final context.

That sentence is the whole game.

But the architecture details matter.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand top-k, reranking, recall, and precision.
- **Intermediate:** Read sections 7-16 to learn latency/cost trade-offs, decision rules, and metrics.
- **Pro:** Complete the experiment lab and practice the interview answer so you can defend this choice in a design review.

---

### 0. Pre-Question Hook [Beginner]

A RAG system gives weak answers.

The team proposes two fixes:

```text
Option A: increase final top-k from 5 chunks to 12 chunks
Option B: retrieve 40 candidates, rerank them, and send the best 5 chunks
```

Which is better?

Wrong answer:

```text
Always rerank because rerankers are better.
```

Also wrong:

```text
Always increase top-k because more context helps.
```

Better answer:

```text
First inspect whether the correct evidence appears in the candidate set.

If it is absent, increase candidate retrieval breadth or improve retrieval.
If it is present but low-ranked, rerank.
If it is present and high-ranked, the problem may be chunking, prompt, generation, or evaluation.
```

Do not tune blind.

Diagnose the retrieval failure.

---

### 1. The Intuition [Beginner]

Imagine searching a library.

Increasing top-k means:

```text
Bring more books from the shelves.
```

Reranking means:

```text
Ask a specialist librarian to sort the books by relevance.
```

If the right book never came from the shelf, sorting cannot help.

If the right book is in the pile but buried under irrelevant books, bringing even more books may make the pile worse.

You need to know which problem you have:

```text
missing evidence
or badly ordered evidence
```

That is why rerank vs top-k is a diagnostic decision, not a preference.

---

### 2. Definition [Beginner]

- **Top-k retrieval:** Returning the top k items from a retrieval system according to its similarity or ranking score.
- **Candidate top-k:** The number of documents or chunks retrieved before optional reranking.
- **Final context top-k:** The number of chunks actually sent to the generation model.
- **Reranking:** A second-stage ranking step that reorders candidate results using a stronger relevance model or scoring method.
- **Recall:** Whether the needed evidence appears in the retrieved set.
- **Precision:** How much of the retrieved set is actually useful.
- **Core idea:** Top-k controls retrieval breadth. Reranking controls ordering and selection quality.

Critical distinction:

```text
candidate top-k is not the same as final context top-k
```

Example:

```text
retrieve 80 candidates
rerank 80 candidates
send top 8 chunks to the generator
```

This is very different from:

```text
retrieve 80 chunks
send all 80 chunks to the generator
```

The first improves selection.

The second explodes context.

---

### 3. Why This Trade-Off Exists [Beginner]

No retrieval stage is perfect.

Dense vector search may miss:

```text
exact IDs
rare terms
numeric constraints
dates
negations
domain-specific wording
```

Sparse search may miss:

```text
semantic paraphrases
conceptual matches
cross-lingual matches
synonyms
implicit intent
```

Approximate nearest neighbor search may miss:

```text
some true nearest neighbors due to speed/recall trade-offs
```

Chunks may be imperfect:

```text
answer split across chunks
title missing
metadata noisy
context too small
context too large
```

Reranking exists because first-stage retrieval is usually optimized for speed and broad candidate recall.

Top-k tuning exists because no ranker can rerank evidence it never sees.

Strong statement:

> Retrieval is usually a two-stage problem: get a broad enough candidate set, then choose a small enough final context.

---

### 4. Failure Taxonomy: Missing, Buried, Bloated, Or Misused [Intermediate]

Before changing top-k or adding reranking, identify the failure type.

| Failure Type | What Happens | Best First Fix |
|---|---|---|
| missing evidence | correct chunk not in candidates | improve retrieval breadth, hybrid search, metadata filters, chunking |
| buried evidence | correct chunk in candidates but ranked low | reranking |
| bloated context | correct chunk present but many distractors sent | reranking, context packing, lower final top-k |
| misused evidence | correct context sent but answer wrong | prompt, generation, citation policy, model capability |
| fragmented evidence | answer spans multiple chunks | better chunking, parent expansion, section retrieval |
| filtered evidence | metadata/permissions remove relevant docs | filter audit |
| stale evidence | old docs outrank new docs | freshness weighting, metadata policy |

Diagnostic rule:

```text
If the right evidence is absent from candidate retrieval, reranking cannot recover it.
```

Second rule:

```text
If the right evidence is already present but distractors dominate final context, increasing final top-k can make generation worse.
```

---

### 5. When Increasing Top-k Helps [Intermediate]

Increasing top-k helps when recall is the bottleneck.

Good signs:

- relevant docs appear just below the current cutoff
- answer evidence is often missing from retrieved results
- queries are ambiguous or broad
- corpus has many near-duplicate or related chunks
- important evidence is split across chunks
- ANN recall is lower than expected
- metadata filters are broad but ranking is uncertain
- hybrid retrieval needs more candidates before fusion/reranking

Example:

```text
current candidate top-k = 10
gold evidence often appears at rank 12-25
```

Increasing candidate top-k to 30 may help.

But be careful:

```text
increasing final context top-k from 5 to 20
```

may cause:

- higher token cost
- slower generation prefill
- lower answer precision
- more contradictions
- more citation confusion
- more irrelevant distractors

Better pattern:

```text
increase candidate top-k
keep final context top-k bounded
use reranking or filtering to select final chunks
```

---

### 6. When Reranking Helps [Intermediate]

Reranking helps when first-stage retrieval has decent recall but weak ordering.

Good signs:

- gold evidence appears in top 50 but not top 5
- dense retrieval finds semantically related but not exact answer chunks
- sparse retrieval finds keyword matches but noisy results
- hybrid retrieval returns useful candidates in mixed order
- query has subtle intent
- short chunks lack enough context for first-stage scoring
- final answer is distracted by irrelevant chunks

Rerankers can use richer matching:

```text
query-document interaction
cross-encoder scoring
domain-tuned relevance model
LLM-as-reranker for small candidate sets
metadata-aware scoring
freshness or authority signals
```

Reranking usually improves:

```text
precision in final context
groundedness
citation quality
answer focus
cost per successful task
```

But adds:

```text
latency
compute cost
operational complexity
another model/version to evaluate
possible reranker bias
```

Strong sentence:

> Reranking is worth it when the quality gained from better evidence selection exceeds the latency and cost added by the second stage.

---

### 7. When You Need Both [Intermediate]

Many production systems use both:

```text
retrieve broad candidate set
rerank candidates
send small final context
```

Example:

```text
candidate top-k = 80
rerank top 80
final context top-k = 8
```

Why this works:

```text
candidate top-k improves recall
reranking improves precision
small final top-k controls token and generation latency
```

This is the classic two-stage retrieval pattern.

It is useful when:

- corpus is large
- queries are diverse
- first-stage retriever is fast but imperfect
- final context budget is limited
- answer quality depends on exact evidence
- citations matter
- wrong answers are expensive

But both may be overkill for:

- tiny corpora
- low-risk casual search
- simple FAQ retrieval
- very tight latency budgets
- cases where top result is already highly reliable

---

### 8. When Neither Is The Real Fix [Pro]

Sometimes top-k and reranking are distractions.

If the correct evidence is already in final context and the model still answers poorly, fix:

```text
prompt grounding
citation policy
answer format
model choice
context ordering
conflict handling
evaluation
```

If the correct evidence is not chunked well, fix:

```text
chunk boundaries
titles
section hierarchy
parent-child retrieval
metadata enrichment
document parsing
```

If filters remove relevant docs, fix:

```text
metadata schema
permission logic
tenant namespace routing
freshness filters
```

If queries are bad, fix:

```text
query rewriting
multi-query retrieval
clarifying questions
domain synonyms
hybrid retrieval
```

Mature answer:

```text
I would not treat reranking or top-k as a magic knob. I would inspect the retrieval trace and identify the failure layer first.
```

---

### 9. Latency And Cost Equations [Intermediate]

Increasing final top-k affects generation cost and latency.

Approximate:

```text
generation_input_tokens =
    instructions
  + user_query
  + history
  + final_context_top_k * avg_chunk_tokens
  + metadata_tokens
```

If:

```text
avg_chunk_tokens = 700
final_top_k increases from 5 to 12
```

extra context:

```text
(12 - 5) * 700 = 4,900 tokens
```

That increases:

```text
input token cost
time to first token
context-window pressure
chance of distractors
```

Reranking affects retrieval-stage latency and cost.

Approximate:

```text
rerank_latency =
    fixed_overhead
  + candidate_count * per_candidate_score_time
```

Or for batched rerankers:

```text
rerank_latency =
    batch_overhead
  + ceil(candidate_count / batch_size) * batch_time
```

Reranking may reduce final context tokens:

```text
retrieve 80 -> rerank -> send 6
```

So it can add retrieval latency while reducing generation latency and token cost.

This is why the trade-off must be measured end to end.

---

### 10. Context-Window Pressure And Distractors [Intermediate]

More context is not always better.

Increasing final top-k can introduce:

```text
irrelevant chunks
contradictory chunks
near duplicates
old versions
partial evidence
low-authority sources
```

The model may:

- cite weaker sources
- merge contradictory facts
- answer from stale evidence
- miss the key chunk in the middle
- become more verbose
- spend tokens explaining irrelevant details

This is sometimes called:

```text
lost in the middle
```

Practical rule:

```text
Increase candidate breadth before increasing final context breadth.
```

Meaning:

```text
retrieve more candidates if recall is low
but send only the best evidence needed for generation
```

---

### 11. Reranker Candidate Budget [Intermediate]

A reranker needs enough candidates to be useful.

Too few candidates:

```text
reranker has nothing better to choose
```

Too many candidates:

```text
reranker latency and cost grow
```

Candidate budget examples:

```text
small FAQ corpus: rerank 10-20
medium support docs: rerank 30-80
large enterprise search: rerank 50-200 depending on latency and infra
high-risk research: rerank broader, maybe multi-stage
```

These are not universal rules.

They are starting points for experiments.

Better framing:

```text
Choose candidate_k where recall@candidate_k plateaus.
Choose final_k where grounded answer quality plateaus.
```

If recall@40 is almost the same as recall@100, reranking 100 may waste latency.

If answer quality does not improve after final_k=6, sending 12 chunks may waste tokens.

---

### 12. Metrics For The Decision [Pro]

Use retrieval metrics and answer metrics.

Retrieval metrics:

```text
recall@k
precision@k
MRR
nDCG
hit rate
gold chunk rank
duplicate rate
candidate coverage
```

Answer metrics:

```text
grounded answer rate
citation accuracy
unsupported claim rate
answer correctness
user acceptance
human escalation rate
follow-up rate
```

System metrics:

```text
retrieval latency
reranking latency
TTFT
TTLT
input tokens
output tokens
cost per session
cost per successful task
p95 latency
timeout rate
```

Do not decide from retrieval metrics alone.

Example:

```text
recall@20 improves from 86% to 92%
but answer correctness stays flat
and latency doubles
```

That may not be worth shipping.

The product metric decides.

---

### 13. Decision Matrix [Intermediate]

| Observation | Interpretation | Action |
|---|---|---|
| gold evidence absent from top 20 | recall problem | increase candidate top-k, improve retriever, hybrid search |
| gold evidence appears rank 25-60 | ordering problem after broad retrieval | increase candidate top-k and rerank |
| gold evidence in top 5 but answer wrong | generation/prompt problem | improve prompt, model, context formatting |
| final context has many distractors | precision problem | rerank, dedupe, lower final top-k |
| p95 latency too high from reranker | reranker too expensive | reduce candidates, conditional rerank, faster reranker |
| TTFT high due to huge context | final context too large | lower final top-k, compress, pack context |
| easy queries work without rerank | reranking overused | conditional rerank |
| high-risk queries fail without rerank | quality risk | rerank high-risk or ambiguous cases |
| exact keyword queries fail | dense-only weakness | add sparse/hybrid retrieval |
| semantic paraphrases fail | sparse-only weakness | add dense/hybrid retrieval |

One-line decision rule:

```text
Use top-k to improve candidate recall; use reranking to improve final evidence precision.
```

---

### 14. Conditional Reranking [Pro]

Reranking does not have to run for every query.

Run reranking when:

- retriever confidence is low
- top scores are close together
- query is ambiguous
- query is high-risk
- query is long or multi-part
- user is in a paid/high-value workflow
- answer requires citations
- candidate set has mixed sources

Skip reranking when:

- top result is clearly strong
- query maps to exact FAQ
- latency budget is tight
- task is low risk
- cached answer is available
- deterministic lookup is better

Example policy:

```text
if top_score_margin > threshold and source_authority_high:
    skip rerank
else:
    rerank top 50
```

More advanced:

```text
easy query -> retrieve 10, no rerank, final 4
medium query -> retrieve 40, rerank, final 6
hard/high-risk query -> hybrid retrieve 100, rerank, final 8, validate citations
```

This is cost and latency routing applied to retrieval.

---

### 15. Business Risk Reasoning [Pro]

The right choice depends on what failure costs.

Low-risk product:

```text
internal brainstorming assistant
casual content helper
low-stakes FAQ
```

May prefer:

```text
lower latency, modest top-k, no reranker unless quality is poor
```

High-risk product:

```text
medical policy assistant
financial compliance search
legal document Q&A
customer support automation
enterprise knowledge answer with citations
```

May prefer:

```text
broader candidates, reranking, citation validation, tighter source authority
```

Business framing:

```text
If a wrong answer costs more than 500 ms of latency, reranking may be worth it.
If users abandon after 3 seconds and stakes are low, reranking may hurt product value.
```

Strong sentence:

> The retrieval design should match the cost of being wrong, not the elegance of the architecture.

---

### 16. Experiment Design [Pro]

Do not compare only two configurations.

Use a grid:

```text
candidate_k: 10, 20, 50, 100
rerank: off, on
final_k: 4, 6, 8, 12
```

For each query in an evaluation set, log:

```text
gold evidence present in candidates
gold evidence rank before rerank
gold evidence rank after rerank
final context token count
answer correctness
citation correctness
latency
cost
```

Analyze:

```text
Where does recall@candidate_k plateau?
Where does answer quality plateau?
Where does latency become unacceptable?
Which query types benefit from rerank?
Which query types only need higher top-k?
Which query types need chunking or query rewrite?
```

Decision:

```text
Pick the cheapest and fastest configuration that meets quality and safety targets.
```

Not:

```text
Pick the configuration with the highest recall regardless of cost.
```

---

### 17. Trace Schema For Rerank vs Top-k Decisions [Pro]

```json
{
  "trace_id": "trace_retrieval_tradeoff_001",
  "workflow_type": "support_rag_answer",
  "query_type": "policy_question",
  "candidate_k": 50,
  "final_k": 6,
  "rerank_enabled": true,
  "retrieval": {
    "dense_candidates": 50,
    "sparse_candidates": 50,
    "merged_candidates": 72,
    "deduped_candidates": 48,
    "retrieval_latency_ms": 220
  },
  "reranking": {
    "reranker_name": "configured_reranker",
    "candidates_reranked": 48,
    "rerank_latency_ms": 680,
    "gold_rank_before": 19,
    "gold_rank_after": 3
  },
  "generation": {
    "final_context_chunks": 6,
    "final_context_tokens": 4200,
    "ttft_ms": 1700,
    "ttlt_ms": 5200
  },
  "outcome": {
    "answer_correct": true,
    "citations_correct": true,
    "user_accepted": true
  }
}
```

Useful fields:

```text
candidate_k
final_k
gold rank before/after rerank
retrieval latency
rerank latency
final context tokens
answer outcome
```

This trace lets you see whether reranking actually moved the right evidence into the answer context.

---

### 18. Code Sample: Retrieval Tradeoff Calculator

```python
def estimate_final_context_tokens(final_k, avg_chunk_tokens, metadata_tokens_per_chunk):
    return final_k * (avg_chunk_tokens + metadata_tokens_per_chunk)


def estimate_rerank_latency(candidate_k, fixed_ms, per_candidate_ms, batch_size=None, batch_ms=None):
    if batch_size and batch_ms:
        batches = (candidate_k + batch_size - 1) // batch_size
        return fixed_ms + batches * batch_ms

    return fixed_ms + candidate_k * per_candidate_ms


def compare_configs():
    avg_chunk_tokens = 650
    metadata_tokens_per_chunk = 80

    configs = [
        {
            "name": "increase_final_top_k",
            "candidate_k": 12,
            "final_k": 12,
            "rerank": False,
        },
        {
            "name": "rerank_broad_candidates",
            "candidate_k": 60,
            "final_k": 6,
            "rerank": True,
        },
    ]

    for config in configs:
        context_tokens = estimate_final_context_tokens(
            final_k=config["final_k"],
            avg_chunk_tokens=avg_chunk_tokens,
            metadata_tokens_per_chunk=metadata_tokens_per_chunk,
        )

        rerank_latency = 0
        if config["rerank"]:
            rerank_latency = estimate_rerank_latency(
                candidate_k=config["candidate_k"],
                fixed_ms=120,
                per_candidate_ms=8,
            )

        print(config["name"])
        print("  candidate_k:", config["candidate_k"])
        print("  final_k:", config["final_k"])
        print("  final_context_tokens:", context_tokens)
        print("  rerank_latency_ms:", rerank_latency)


if __name__ == "__main__":
    compare_configs()
```

Expected lesson:

```text
Increasing final top-k mainly increases generation input tokens.
Reranking broad candidates mainly adds retrieval-stage latency while controlling final context size.
```

---

### 19. Mini Program: Rerank vs Top-k Simulator

This mini program simulates whether gold evidence is captured and selected.

```python
def evaluate_config(gold_rank_before, candidate_k, final_k, rerank_enabled, gold_rank_after=None):
    gold_in_candidates = gold_rank_before <= candidate_k

    if not gold_in_candidates:
        return {
            "gold_in_candidates": False,
            "gold_in_final_context": False,
            "reason": "candidate recall failure",
        }

    if rerank_enabled:
        if gold_rank_after is None:
            raise ValueError("gold_rank_after is required when rerank is enabled")

        gold_in_final = gold_rank_after <= final_k
        reason = "rerank selected gold" if gold_in_final else "rerank did not lift gold enough"
    else:
        gold_in_final = gold_rank_before <= final_k
        reason = "first-stage rank selected gold" if gold_in_final else "gold buried without rerank"

    return {
        "gold_in_candidates": True,
        "gold_in_final_context": gold_in_final,
        "reason": reason,
    }


def main():
    cases = [
        {
            "name": "low_top_k_no_rerank",
            "gold_rank_before": 18,
            "candidate_k": 10,
            "final_k": 5,
            "rerank_enabled": False,
        },
        {
            "name": "higher_final_top_k_no_rerank",
            "gold_rank_before": 18,
            "candidate_k": 20,
            "final_k": 20,
            "rerank_enabled": False,
        },
        {
            "name": "broad_candidates_with_rerank",
            "gold_rank_before": 18,
            "candidate_k": 50,
            "final_k": 5,
            "rerank_enabled": True,
            "gold_rank_after": 2,
        },
        {
            "name": "rerank_cannot_fix_missing_candidate",
            "gold_rank_before": 70,
            "candidate_k": 50,
            "final_k": 5,
            "rerank_enabled": True,
            "gold_rank_after": None,
        },
    ]

    for case in cases:
        result = evaluate_config(
            gold_rank_before=case["gold_rank_before"],
            candidate_k=case["candidate_k"],
            final_k=case["final_k"],
            rerank_enabled=case["rerank_enabled"],
            gold_rank_after=case.get("gold_rank_after"),
        )

        print(case["name"])
        print(" ", result)


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
Reranking can lift buried evidence, but it cannot recover evidence outside the candidate set.
Increasing final top-k can include buried evidence, but may send too much context to generation.
```

---

### 20. Hands-On Lab: Rerank Or Increase Top-k [Pro]

#### Build

Create a small evaluation set:

```text
30-100 realistic user queries
gold answer or expected behavior
gold source document/chunk IDs
query type labels
business risk label
```

Test configurations:

```text
candidate_k = 10, final_k = 5, rerank = off
candidate_k = 25, final_k = 5, rerank = off
candidate_k = 50, final_k = 5, rerank = on
candidate_k = 100, final_k = 8, rerank = on
candidate_k = 50, final_k = 10, rerank = off
```

#### Measure

For each configuration:

```text
recall@candidate_k
gold rank before rerank
gold rank after rerank
final context token count
answer correctness
citation accuracy
unsupported claim rate
retrieval latency
rerank latency
TTFT
TTLT
cost per successful task
```

#### Diagnose

Classify failures:

```text
missing evidence
buried evidence
bloated context
misused evidence
bad chunking
bad metadata filter
query rewrite needed
```

#### Decide

Write a recommendation:

```text
For easy FAQ queries, use <config>.
For ambiguous policy queries, use <config>.
For high-risk compliance queries, use <config>.
The reason is <quality-latency-cost trade-off>.
```

#### Defend

Use this format:

```text
The bottleneck was <recall/precision/generation>.
Increasing candidate_k improved <metric> from <before> to <after>.
Reranking improved <metric> from <before> to <after>.
The chosen setting adds <latency> but reduces <failure type>.
I would ship it because <business reason>.
```

---

### 21. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| increasing final top-k blindly | adds tokens and distractors | increase candidate_k, then select final context carefully |
| adding reranker when evidence is absent | reranker cannot rank missing evidence | improve first-stage recall first |
| using one top-k for all queries | easy and hard queries need different budgets | route by query difficulty/risk |
| measuring only recall@k | does not prove answer quality improved | measure grounded answer success |
| measuring only answer quality | hides latency and cost regressions | measure cost and latency too |
| reranking too many candidates | p95 latency may spike | find candidate_k plateau |
| sending reranked top 20 by default | final context may still be bloated | tune final_k separately |
| ignoring chunk quality | retrieval knobs cannot fix bad chunks | improve chunking and metadata |
| no gold source labels | cannot diagnose missing vs buried evidence | create retrieval eval set |
| no slice analysis | average hides query-specific failures | evaluate by query type and risk |

---

### 22. Practical Interview Question [Intermediate]

> Your RAG system sometimes gives ungrounded answers. The team suggests increasing top-k from 5 to 20. Another engineer suggests adding a reranker. How would you decide?

---

### 23. Strong Answer [Pro]

I would not choose blindly between increasing top-k and adding a reranker. First I would inspect retrieval traces against a labeled evaluation set. The key question is whether the correct evidence is missing from the candidate set, present but buried, present in final context but ignored, or removed by chunking, metadata, or permission filters.

If the gold evidence is absent from the candidate set, a reranker will not help because it cannot rank documents it never receives. In that case I would improve candidate recall by increasing candidate top-k, using hybrid dense plus sparse retrieval, improving query rewriting, fixing filters, or improving chunking. But I would avoid simply sending all extra chunks to the generator, because increasing final top-k raises token cost, first-token latency, and distractor risk.

If the gold evidence appears in the candidate set but is ranked too low to reach final context, I would add reranking or improve the ranking function. A strong pattern is to retrieve a broader candidate set, rerank it, and send a small final set to the generator. That uses top-k for recall and reranking for precision.

I would compare configurations using recall@candidate_k, gold rank before and after reranking, final context token count, answer correctness, citation accuracy, unsupported claim rate, rerank latency, TTFT, TTLT, and cost per successful task. I would also slice by query type and business risk. Low-risk FAQ queries may not need reranking, while high-risk compliance or policy questions may justify reranking and a broader candidate set.

The final decision should be the cheapest and fastest retrieval configuration that meets groundedness, citation, latency, and safety targets. The goal is not more context or a fancier reranker. The goal is the right evidence in a small, reliable final context.

---

### 24. Active Recall [Beginner]

Answer these without looking:

1. What does increasing top-k usually improve?
2. What does reranking usually improve?
3. What is candidate top-k?
4. What is final context top-k?
5. Why is candidate top-k different from final top-k?
6. When can reranking not help?
7. What does it mean for evidence to be buried?
8. Why can increasing final top-k hurt answer quality?
9. What is recall@k?
10. What is precision@k?
11. Why should answer metrics be measured alongside retrieval metrics?
12. What latency does reranking add?
13. What latency does larger final context add?
14. What is conditional reranking?
15. What query types often benefit from reranking?
16. What query types may not need reranking?
17. Why does business risk matter?
18. What is a good two-stage retrieval pattern?
19. What should a rerank/top-k trace log?
20. What is the final lesson of this topic?

Expected answers:

1. Candidate recall, if the evidence is near the cutoff.
2. Ordering and final context precision.
3. Number of candidates retrieved before reranking/selection.
4. Number of chunks sent to the generator.
5. Candidate top-k is for search breadth; final top-k is for generation context.
6. When correct evidence is not in the candidate set.
7. Correct evidence is retrieved but ranked too low.
8. It adds distractors, contradictions, tokens, and prefill latency.
9. Whether relevant evidence appears in the top k results.
10. How much of the top k is useful/relevant.
11. Better retrieval metrics may not improve final answer outcomes.
12. Second-stage scoring latency over candidates.
13. Model prefill, token cost, and context pressure.
14. Running rerank only when query confidence/risk justifies it.
15. Ambiguous, high-risk, citation-heavy, subtle intent queries.
16. Exact FAQ or high-confidence simple queries.
17. Wrong-answer cost determines how much latency/cost is justified.
18. Retrieve broad candidates, rerank, send small final context.
19. candidate_k, final_k, rerank status, gold ranks, latency, tokens, outcome.
20. Use top-k for recall and reranking for precision after diagnosing the failure.

---

### 25. Revision Notes

- **One-line summary:** Increase candidate top-k when evidence is missing; rerank when evidence is present but buried; keep final context small enough to avoid token and latency bloat.
- **Three keywords:** recall, precision, final context.
- **One interview trap:** Increasing final top-k to fix every RAG failure without checking whether the problem is missing evidence, buried evidence, or generation misuse.
- **One memory trick:** More candidates help search; reranking helps selection; final context feeds generation.

Final takeaway:

> Rerank vs top-k is not a default setting debate. It is a diagnosis: find whether the evidence is missing, buried, bloated, or misused, then spend latency and tokens only where they improve successful grounded answers.

---

## Subtopic 20.2.d: Should You Compress Context or Use a Larger Model: Tradeoff Reasoning

> **Subtopic time:** 2h
> Outcome: You should be able to decide whether a GenAI system should compress context, use a model with a larger context window, do both, or do neither. You should reason from evidence preservation, latency, cost, accuracy, citation needs, and failure risk.

### Add to Knowledge Base

As GenAI systems grow, they hit a familiar wall:

```text
We have more context than we can afford to send.
```

The team then asks:

```text
Should we compress the context?
Or should we use a model with a larger context window?
```

This is not only a token-limit question.

It is a product and architecture question.

Compressing context says:

```text
Keep the payload small by removing or summarizing information.
```

Using a larger model says:

```text
Keep more original evidence available to the model.
```

The core mental model:

> Compression trades completeness for compactness. Larger context trades cost and latency for evidence preservation. The right choice depends on whether the missing value is signal or noise.

If context is noisy, compress or filter.

If context is dense with critical details, preserve more evidence.

If the answer depends on exact wording, citations, numbers, legal clauses, or code, careless compression can be dangerous.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand compression, larger context windows, and why neither is automatically better.
- **Intermediate:** Read sections 7-16 to reason about loss, latency, cost, caching, and evaluation.
- **Pro:** Complete the experiment lab and practice the interview answer so you can defend context strategy in production design reviews.

---

### 0. Pre-Question Hook [Beginner]

A legal document Q&A system retrieves 18 chunks.

The answer model can comfortably handle 8 chunks within the latency budget.

The team proposes:

```text
Option A: summarize the 18 chunks into a compact 2,000-token context
Option B: use a larger-context model and send all 18 chunks
```

Which is better?

Wrong answer:

```text
Always summarize because it is cheaper.
```

Also wrong:

```text
Always use the largest context model because more context is better.
```

Better answer:

```text
If exact wording, citations, exceptions, dates, or numbers matter, compression may remove the evidence needed to answer safely.
If many chunks are irrelevant or repetitive, a larger model may just process more noise at higher cost and latency.
```

The decision depends on evidence density.

Ask:

```text
What must be preserved exactly?
What can be summarized?
What can be dropped?
What can be fetched later?
```

---

### 1. The Intuition [Beginner]

Imagine packing for a trip.

Compression is like packing a smaller suitcase.

You choose:

```text
only the essentials
fold tightly
leave bulky items behind
```

Using a larger context model is like paying for a larger suitcase.

You can bring more:

```text
extra clothes
backup shoes
full-size items
```

But a larger suitcase is not always better.

It costs more, is heavier, and may make it harder to find what you need.

The real question is:

```text
Are you carrying essentials or clutter?
```

For GenAI:

```text
essentials = exact evidence needed for the task
clutter = irrelevant, repeated, stale, or low-value context
```

Compression is good when it removes clutter.

Compression is bad when it removes essentials.

---

### 2. Definition [Beginner]

- **Context compression:** Reducing the amount of context sent to a model through filtering, extraction, summarization, deduplication, or transformation.
- **Larger-context model:** A model with a bigger context window that can accept more input tokens in one request.
- **Lossless reduction:** Removing tokens without losing needed information, such as deduplication or dropping unused fields.
- **Lossy compression:** Rewriting or summarizing information in a way that may remove details.
- **Evidence preservation:** Keeping the exact facts, wording, spans, source IDs, numbers, and constraints needed for correct output.
- **Core idea:** Compression reduces payload size. Larger context preserves more original material. Both must be judged by downstream task success.

Short version:

```text
compress when context is noisy or repetitive
use larger context when original evidence must be preserved
combine them when the corpus is large and some evidence must remain exact
```

---

### 3. Why This Trade-Off Exists [Beginner]

This trade-off exists because context has costs:

```text
input token cost
model prefill latency
context-window limits
attention over noise
lost-in-the-middle behavior
prompt assembly complexity
privacy exposure
```

But context also has value:

```text
evidence
conversation continuity
tool results
source citations
domain definitions
constraints
edge cases
examples
```

If you compress too aggressively:

```text
the model may not have the exact evidence
citations may become unsupported
numbers may be rounded or lost
exceptions may disappear
legal/code details may be distorted
```

If you use a larger context model blindly:

```text
cost rises
latency rises
irrelevant context distracts the model
source conflicts become harder
debugging becomes harder
```

Strong statement:

> Context strategy is not "shorter vs longer." It is "which information deserves to survive into the model call?"

---

### 4. Types Of Context Reduction [Intermediate]

Not all compression is the same.

| Type | What It Does | Risk |
|---|---|---|
| deduplication | removes repeated chunks or repeated tool fields | low if IDs are preserved |
| filtering | removes irrelevant chunks or fields | may remove hidden useful evidence |
| truncation | cuts text after a limit | high risk if important detail is later |
| extraction | keeps exact relevant spans | misses implicit or distributed evidence |
| abstractive summary | rewrites content shorter | may distort facts or omit exceptions |
| query-focused summary | compresses relative to a question | may overfit to current query |
| structured compression | converts text to fields | schema may omit nuance |
| hierarchical summary | summarizes chunks, sections, documents | error can compound across levels |
| map-reduce | processes pieces then combines results | combine step may lose minority evidence |

Best general order:

```text
dedupe before summarize
filter before compress
extract exact spans before abstracting
preserve source IDs throughout
```

Lossless reductions are usually safer than lossy summaries.

---

### 5. Larger Context Is Not Free [Intermediate]

A larger context model can accept more tokens, but it does not make context costless.

Larger context can increase:

```text
input token cost
time to first token
provider queue time
memory pressure
prompt assembly time
debug complexity
evaluation complexity
privacy exposure
```

It can also reduce:

```text
need for preprocessing
compression loss
multi-step summarization
retrieval brittleness
manual context selection effort
```

Larger context is strongest when:

- evidence is dense
- exact wording matters
- answer requires cross-document synthesis
- the task is high value
- compression loss is dangerous
- latency budget allows it
- source conflicts must be shown explicitly

Larger context is weakest when:

- context is mostly noise
- retrieval returns many near duplicates
- user needs fast response
- the answer depends on a few exact facts
- smaller context plus reranking works
- cost per task is tight

Strong warning:

```text
A larger context window is capacity, not relevance.
```

---

### 6. When Compression Helps [Intermediate]

Compression helps when the context is larger than needed and contains removable redundancy.

Good signs:

- many duplicate chunks
- repeated boilerplate
- raw tool payloads with unused fields
- long conversation history with few relevant turns
- retrieved chunks include irrelevant sections
- citations need only a few exact spans
- user needs a fast answer
- final answer requires summary rather than exact extraction

Examples:

```text
compress old chat history into a stable memory summary
extract only account fields needed for a support answer
dedupe repeated policy chunks
summarize long research notes before synthesis
keep exact citations but summarize surrounding context
```

Compression is useful when it improves:

```text
TTFT
input token cost
context focus
cache efficiency
model reliability
```

But only if it preserves the task-critical evidence.

---

### 7. When Compression Is Dangerous [Pro]

Compression is dangerous when the task depends on exact details.

High-risk compression cases:

```text
legal clauses
medical policy
financial terms
code
tables
math
dates
thresholds
exceptions
negations
citations
audit evidence
contract obligations
```

Example:

Original:

```text
Coverage applies unless the claim is filed more than 90 days after discharge.
```

Bad summary:

```text
Coverage applies after discharge.
```

The exception disappeared.

Another example:

Original:

```text
The API returns 429 when per-tenant quota is exceeded, not global quota.
```

Bad summary:

```text
The API returns 429 when quota is exceeded.
```

The operational detail is lost.

Compression failure modes:

- omitting exceptions
- changing numbers
- losing source IDs
- merging conflicting sources
- hiding uncertainty
- deleting minority evidence
- weakening citations
- converting exact language into vague language

Rule:

```text
If you need to cite it, preserve the exact span.
```

---

### 8. When A Larger Model Helps [Intermediate]

A larger-context model helps when preserving original context is more valuable than reducing it.

Good signs:

- answer requires comparing many documents
- evidence is spread across sections
- compression repeatedly loses details
- citation accuracy matters
- source conflicts must be visible
- documents contain tables or code
- the model must reason over long dependency chains
- the workflow is high value enough to justify cost

Examples:

```text
contract review across many clauses
large codebase question with multiple files
clinical policy lookup with exceptions
financial report analysis with tables
research synthesis across several papers
```

Larger context may reduce:

```text
summarization pipeline complexity
compression errors
manual selection brittleness
multi-call orchestration
```

But still needs:

```text
source ordering
deduplication
metadata
clear instructions
conflict handling
answer constraints
evaluation
```

Do not treat larger context as a substitute for retrieval quality.

---

### 9. When You Need Both [Pro]

Many serious systems use both:

```text
compress low-value context
preserve high-value evidence
use a larger context model for hard cases
```

Example RAG strategy:

```text
1. retrieve broad candidates
2. rerank candidates
3. dedupe repeated chunks
4. keep exact top evidence spans
5. compress supporting context
6. send to model with enough context window
```

Example agent strategy:

```text
1. keep current task state exact
2. summarize older observations
3. drop obsolete tool errors
4. preserve approval decisions and IDs
5. use larger context only for complex long-running tasks
```

Example document AI strategy:

```text
1. preserve tables and field evidence exactly
2. summarize surrounding prose
3. keep page numbers and bounding boxes
4. use long context for full-document consistency checks
```

Best pattern:

```text
compress the parts that are not evidence
preserve the parts that are evidence
route hard cases to larger context
```

---

### 10. When Neither Fixes The Problem [Pro]

Sometimes the issue is not context size.

If retrieval missed the right document:

```text
larger model cannot see what was not retrieved
compression cannot create missing evidence
```

Fix:

```text
retrieval, chunking, metadata, query rewrite, hybrid search
```

If the model ignores correct evidence:

```text
larger context may make the problem worse
compression may hide the signal
```

Fix:

```text
prompt grounding, answer schema, citation policy, model choice, evaluation
```

If documents are poorly parsed:

```text
larger context may include broken text
compression may summarize corrupted input
```

Fix:

```text
document parsing, OCR, table extraction, layout preservation
```

If the question is ambiguous:

```text
more context may add conflicting evidence
compression may choose the wrong interpretation
```

Fix:

```text
clarifying question or intent routing
```

Mature answer:

```text
I would first identify whether the bottleneck is missing evidence, too much noise, compression loss, or model reasoning over long context.
```

---

### 11. Cost And Latency Equations [Intermediate]

Using larger context mostly increases input cost and prefill latency.

Approximate:

```text
input_cost =
    input_tokens / 1_000_000 * input_price_per_million
```

Approximate first-token effect:

```text
TTFT grows with input tokens, model size, provider queueing, and cache behavior
```

Compression adds its own cost:

```text
compression_cost =
    compression_input_tokens
  + compression_output_tokens
  + compression_model_latency
```

Then generation cost becomes:

```text
generation_cost_after_compression =
    compressed_context_tokens
  + final_answer_output_tokens
```

Total compressed workflow:

```text
total_cost =
    retrieval_cost
  + compression_call_cost
  + final_generation_cost
```

Total larger-context workflow:

```text
total_cost =
    retrieval_cost
  + final_generation_cost_with_large_input
```

Compression is not free.

It is worth it when:

```text
compression_call_cost + smaller_generation_cost
<
large_context_generation_cost
```

and:

```text
quality and safety remain acceptable
```

---

### 12. Compression Latency Can Backfire [Intermediate]

Compression may reduce final model latency but add a new model call.

Example:

```text
without compression:
  final generation = 5.8 seconds

with compression:
  compression call = 2.0 seconds
  final generation = 3.2 seconds
  total = 5.2 seconds
```

Slight win.

But:

```text
compression call = 3.5 seconds
final generation = 3.2 seconds
total = 6.7 seconds
```

Loss.

Compression helps latency most when:

- compression is cheap and fast
- it can run offline
- it can run in parallel
- it is cached
- it reduces a very large final prompt
- final generation is on the critical path

Compression hurts latency when:

- it adds serial model calls
- it is repeated every turn
- it compresses context that was already small
- it blocks streaming
- it triggers repair or validation calls

Question:

```text
Is compression on the critical path, and is the saved generation time larger than the compression time?
```

---

### 13. Cache Interactions [Pro]

Compression and larger context interact with caching.

Stable context can be cached:

```text
system prompt
policy text
static documentation
tenant instructions
reused summaries
```

Unstable context is harder to cache:

```text
fresh query-specific summaries
dynamic tool results
randomly ordered chunks
changing timestamps
non-deterministic compression
```

Compression can improve caching if:

```text
summaries are generated offline
summary versions are stable
source IDs and version hashes are tracked
```

Compression can hurt caching if:

```text
each request generates a slightly different summary
the prompt prefix changes every time
chunk ordering is unstable
```

Larger context can benefit from caching if:

```text
large stable prefixes are reused across requests
```

But if every request has different retrieved context:

```text
cache benefits may be limited
```

Log:

```text
raw_context_tokens
compressed_context_tokens
compression_cache_hit
prompt_cache_hit
source_version
summary_version
```

---

### 14. Evidence Preservation Strategy [Pro]

Do not compress all context the same way.

Classify context:

| Context Type | Strategy |
|---|---|
| exact answer span | preserve exact text |
| citation source | preserve source ID and location |
| numbers/dates/thresholds | preserve exact values |
| code | preserve exact snippet or file lines |
| table | preserve structured rows/columns |
| repeated boilerplate | dedupe or summarize |
| old conversation turns | summarize |
| raw tool payload | select fields |
| low-confidence evidence | include with uncertainty or drop |
| conflicting evidence | preserve both and instruct conflict handling |

Practical pattern:

```text
exact evidence block
compressed background block
metadata/citation block
instructions for conflict and uncertainty
```

Example prompt context layout:

```text
Exact evidence:
- Source A, lines 12-18: ...
- Source B, table row 4: ...

Compressed background:
- The policy applies to enterprise tenants.
- Renewal exceptions depend on contract tier.

Known uncertainty:
- Billing source was unavailable.
```

This is much safer than one big generic summary.

---

### 15. Long-Context Failure Modes [Pro]

Large context models can still fail.

Failure modes:

- relevant evidence buried among distractors
- model overweights later or earlier sections
- conflicting sources are merged
- old evidence overrides new evidence
- citations point to wrong source
- answer becomes verbose
- model misses a small exception
- tool results and docs conflict
- prompt instructions are diluted

Long-context does not remove the need for:

```text
ordering
sectioning
source labels
deduplication
freshness rules
citation policy
answer constraints
evaluation
```

Good long-context design:

```text
put most relevant evidence first
group by source
include clear headers
include source IDs
separate exact evidence from background
state conflict rules
avoid dumping raw irrelevant context
```

Strong sentence:

> A larger context window lets you include more information; it does not guarantee the model will use the right information.

---

### 16. Decision Matrix [Intermediate]

| Observation | Interpretation | Better Choice |
|---|---|---|
| context has many duplicates | waste | dedupe/compress |
| exact clauses or citations matter | compression risk | preserve exact spans or use larger context |
| answer uses only a few facts | selection problem | retrieve/rerank/extract, not larger model |
| answer needs full-document synthesis | evidence spread out | larger context or hierarchical strategy |
| latency budget is tight | large context may hurt TTFT | compress/filter/cache |
| compression loses exceptions | lossy compression unsafe | larger context or extractive compression |
| model gets distracted by noise | too much context | compress/filter/reorder |
| compression call is slower than saved generation | latency loss | avoid online compression or cache it |
| costs are too high but quality stable after compression | good compression candidate | compress |
| high-value high-risk workflow | correctness dominates | preserve evidence, maybe larger model |

Simple rule:

```text
compress noise
preserve evidence
use larger context for dense high-value evidence
```

---

### 17. Metrics For The Decision [Pro]

Measure more than token count.

Context metrics:

```text
raw_context_tokens
compressed_context_tokens
compression_ratio
exact_span_preservation_rate
source_id_preservation_rate
numeric_value_preservation_rate
context_dedup_rate
```

Quality metrics:

```text
answer correctness
groundedness
citation accuracy
unsupported claim rate
missing exception rate
conflict handling accuracy
```

System metrics:

```text
compression_latency
generation_TTFT
generation_TTLT
total_workflow_latency
input token cost
compression cost
cost per successful task
cache hit rate
fallback rate
```

User/product metrics:

```text
acceptance rate
follow-up rate
human escalation rate
manual correction rate
task completion rate
```

Do not ship compression because:

```text
tokens went down
```

Ship compression because:

```text
tokens went down while correctness, citations, safety, and task success stayed acceptable
```

---

### 18. Experiment Design [Pro]

Compare at least four strategies:

```text
A. small model + raw selected context
B. small model + compressed context
C. larger-context model + raw selected context
D. larger-context model + selective compression
```

For each test query, log:

```text
raw tokens
compressed tokens
compression time
generation time
total latency
cost
answer correctness
citation correctness
exact detail preservation
unsupported claims
failure reason
```

Slice by task type:

```text
simple lookup
multi-document synthesis
legal/policy exception
code question
table/numeric question
conversation-history question
tool-result question
```

Expected findings may differ:

```text
simple lookup -> compression or extraction works
legal exception -> preserve exact text
long research -> hierarchical compression plus larger model
code -> preserve exact snippets
chat memory -> summarize older turns
```

Recommendation format:

```text
Use compression for <slice>.
Use larger context for <slice>.
Use both for <slice>.
Avoid both and fix retrieval for <slice>.
```

---

### 19. Trace Schema For Context Strategy [Pro]

```json
{
  "trace_id": "trace_context_strategy_001",
  "workflow_type": "policy_rag_answer",
  "strategy": "selective_compression_plus_larger_context",
  "model_route": "large_context_for_high_risk",
  "context": {
    "raw_context_tokens": 18200,
    "deduped_context_tokens": 14100,
    "compressed_context_tokens": 6200,
    "compression_ratio": 0.34,
    "exact_evidence_tokens": 2800,
    "summary_tokens": 2200,
    "metadata_tokens": 1200
  },
  "compression": {
    "enabled": true,
    "compression_type": "extractive_plus_query_focused_summary",
    "compression_latency_ms": 950,
    "summary_version": "policy_summary_v6",
    "source_ids_preserved": true
  },
  "generation": {
    "input_tokens": 9200,
    "output_tokens": 640,
    "ttft_ms": 1900,
    "ttlt_ms": 5800
  },
  "quality": {
    "answer_correct": true,
    "citations_correct": true,
    "numeric_values_preserved": true,
    "unsupported_claim": false
  }
}
```

Key fields:

```text
raw tokens
compressed tokens
exact evidence tokens
compression type
compression latency
summary/source versions
quality outcomes
```

This trace lets you answer:

```text
Did compression save tokens?
Did it add latency?
Did it preserve evidence?
Did it improve cost per successful task?
```

---

### 20. Code Sample: Context Budget Calculator

```python
def estimate_input_cost(input_tokens, price_per_million):
    return input_tokens / 1_000_000 * price_per_million


def compare_context_strategies(
    raw_context_tokens,
    compressed_context_tokens,
    fixed_prompt_tokens,
    output_tokens,
    input_price_per_million,
    output_price_per_million,
    compression_call_cost,
):
    raw_input_tokens = fixed_prompt_tokens + raw_context_tokens
    compressed_input_tokens = fixed_prompt_tokens + compressed_context_tokens

    raw_generation_cost = (
        estimate_input_cost(raw_input_tokens, input_price_per_million)
        + estimate_input_cost(output_tokens, output_price_per_million)
    )

    compressed_generation_cost = (
        estimate_input_cost(compressed_input_tokens, input_price_per_million)
        + estimate_input_cost(output_tokens, output_price_per_million)
        + compression_call_cost
    )

    return {
        "raw_input_tokens": raw_input_tokens,
        "compressed_input_tokens": compressed_input_tokens,
        "raw_generation_cost": raw_generation_cost,
        "compressed_total_cost": compressed_generation_cost,
        "cost_delta": compressed_generation_cost - raw_generation_cost,
    }


result = compare_context_strategies(
    raw_context_tokens=18000,
    compressed_context_tokens=6000,
    fixed_prompt_tokens=2000,
    output_tokens=700,
    input_price_per_million=1.0,
    output_price_per_million=3.0,
    compression_call_cost=0.006,
)

print(result)
```

Expected lesson:

```text
Compression must include its own call cost. A smaller final prompt is not automatically cheaper if compression is expensive or repeated.
```

---

### 21. Mini Program: Compression vs Larger Context Simulator

This mini program compares quality-adjusted outcomes for three strategies.

```python
def cost_per_success(total_cost, success_rate):
    if success_rate == 0:
        return None
    return total_cost / success_rate


def strategy_score(strategy):
    total_cost = strategy["generation_cost"] + strategy.get("compression_cost", 0)
    total_latency = strategy["generation_latency_ms"] + strategy.get("compression_latency_ms", 0)
    success_cost = cost_per_success(total_cost, strategy["success_rate"])

    return {
        "name": strategy["name"],
        "total_cost": round(total_cost, 4),
        "total_latency_ms": total_latency,
        "success_rate": strategy["success_rate"],
        "cost_per_success": round(success_cost, 4),
        "risk_note": strategy["risk_note"],
    }


def main():
    strategies = [
        {
            "name": "raw_context_large_model",
            "generation_cost": 0.045,
            "generation_latency_ms": 7200,
            "success_rate": 0.91,
            "risk_note": "higher cost and latency, stronger evidence preservation",
        },
        {
            "name": "compressed_context_small_model",
            "compression_cost": 0.008,
            "compression_latency_ms": 1200,
            "generation_cost": 0.018,
            "generation_latency_ms": 3600,
            "success_rate": 0.78,
            "risk_note": "cheaper, but possible evidence loss",
        },
        {
            "name": "selective_compression_large_model",
            "compression_cost": 0.005,
            "compression_latency_ms": 700,
            "generation_cost": 0.030,
            "generation_latency_ms": 5200,
            "success_rate": 0.90,
            "risk_note": "balanced, preserves exact spans and compresses background",
        },
    ]

    for strategy in strategies:
        print(strategy_score(strategy))


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
The cheapest context strategy may not have the best cost per successful task if compression lowers success rate.
```

---

### 22. Hands-On Lab: Choose A Context Strategy [Pro]

#### Build

Choose one workflow:

```text
policy RAG
legal Q&A
codebase assistant
research synthesis
customer support assistant
long conversation assistant
document extraction
```

Create an evaluation set with:

```text
20-50 realistic tasks
gold answer or expected behavior
gold source spans
numeric/date/exception checks
citation requirements
risk label
```

#### Compare

Test:

```text
raw selected context
lossless reduction only
extractive compression
abstractive compression
query-focused compression
larger-context model
selective compression plus larger-context model
```

#### Measure

For each strategy:

```text
raw_context_tokens
final_input_tokens
compression_latency
generation_TTFT
generation_TTLT
total_cost
answer correctness
citation accuracy
exact value preservation
exception preservation
unsupported claim rate
cost per successful task
```

#### Diagnose

Classify failures:

```text
compression removed evidence
compression distorted evidence
large context distracted model
retrieval missed evidence
model ignored evidence
citations unsupported
latency too high
cost too high
```

#### Decide

Write:

```text
For <slice>, I would use <strategy>.
The reason is <evidence preservation / cost / latency / quality>.
The main risk is <risk>.
The guardrail is <evaluation or trace check>.
```

---

### 23. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| summarizing everything | loses exact evidence | preserve exact spans and summarize background |
| using largest context by default | expensive and noisy | retrieve, dedupe, and pack evidence deliberately |
| ignoring compression latency | extra model call may slow workflow | measure total critical-path latency |
| measuring only token reduction | may hide quality loss | measure correctness and citations |
| compressing code like prose | breaks exact syntax | preserve code snippets and file references |
| compressing legal/policy exceptions | loses critical constraints | use extractive spans for exceptions |
| no source IDs in summaries | citations become unverifiable | preserve source IDs and locations |
| repeated online compression | wastes cost and latency | cache or precompute stable summaries |
| assuming long context fixes retrieval | missing evidence still missing | fix retrieval first |
| ignoring long-context distractors | more context can reduce focus | reorder, dedupe, and mark evidence priority |

---

### 24. Practical Interview Question [Intermediate]

> Your RAG assistant retrieves more context than the current model can handle cheaply. One teammate proposes summarizing all retrieved chunks before generation. Another proposes using a larger-context model. How would you decide?

---

### 25. Strong Answer [Pro]

I would not choose based only on context-window size or token count. I would first inspect what kind of information is in the context and what the task requires. If the answer depends on exact wording, citations, numbers, dates, code, legal clauses, or exceptions, fully abstractive compression is risky because it can remove or distort the evidence. In those cases I would preserve exact spans and source IDs, and consider a larger-context model if the evidence is genuinely dense and high value.

If the context is mostly repetitive, noisy, or filled with unused tool fields, I would compress or reduce it first. I would start with safer reductions: deduplication, filtering, field selection, context packing, and extractive span selection. I would use abstractive summaries mainly for background context, old conversation history, or low-risk synthesis where exact citations are not required.

I would compare multiple strategies: raw selected context, lossless reduction, extractive compression, abstractive compression, larger-context model, and selective compression plus larger context. For each, I would measure final input tokens, compression latency, time to first token, total latency, total cost, answer correctness, citation accuracy, exact value preservation, unsupported claims, and cost per successful task.

I would also check whether the problem is actually context size. If retrieval missed the evidence, neither compression nor a larger model fixes it. If the model ignores correct evidence, prompt grounding or answer format may be the real issue. If the documents are poorly parsed, context strategy will not repair corrupted input.

My default production preference is selective compression: preserve exact task-critical evidence, compress or drop low-value background, and route only hard or high-risk cases to a larger-context model. The final choice should be the cheapest and fastest strategy that preserves the evidence needed for safe, grounded, successful answers.

---

### 26. Active Recall [Beginner]

Answer these without looking:

1. What does context compression trade off?
2. What does a larger-context model trade off?
3. What is lossless reduction?
4. What is lossy compression?
5. Why is summarization risky for citations?
6. When does compression help?
7. When is compression dangerous?
8. When does a larger-context model help?
9. Why is a larger context window not the same as relevance?
10. What should be preserved exactly?
11. Why can compression latency backfire?
12. How can caching affect compression strategy?
13. What are long-context failure modes?
14. What is selective compression?
15. When do you need both compression and larger context?
16. When does neither fix the problem?
17. What metrics should be measured besides token count?
18. Why compare cost per successful task?
19. What should a context strategy trace log?
20. What is the final lesson of this topic?

Expected answers:

1. Completeness for compactness.
2. Cost and latency for evidence preservation.
3. Removing tokens without losing needed information, such as dedupe.
4. Rewriting/summarizing in a way that may lose details.
5. It can remove exact spans or source grounding.
6. When context is noisy, repetitive, old, or too verbose.
7. When exact clauses, code, numbers, dates, or exceptions matter.
8. When evidence is dense, spread out, and must be preserved.
9. More capacity does not ensure the model uses the right evidence.
10. Exact answer spans, source IDs, numbers, dates, code, tables, exceptions.
11. The compression call may cost more time than it saves.
12. Stable summaries can help; request-specific summaries can hurt cacheability.
13. Distractors, conflicts, missed exceptions, bad citations, diluted instructions.
14. Preserving exact evidence while compressing low-value background.
15. Large complex tasks with both dense evidence and noisy background.
16. When retrieval, parsing, prompt, or ambiguity is the actual problem.
17. Correctness, citations, latency, cost, exact value preservation, success rate.
18. Cheaper context is not useful if success rate drops.
19. Raw/compressed tokens, compression type, latency, source versions, quality.
20. Compress noise, preserve evidence, and use larger context only when original evidence earns its cost.

---

### 27. Revision Notes

- **One-line summary:** Compress context when it removes low-value tokens safely; use larger context when task-critical evidence must remain exact and complete.
- **Three keywords:** preserve, compress, route.
- **One interview trap:** Summarizing all context before generation even when the task requires exact citations, numbers, exceptions, code, or legal wording.
- **One memory trick:** Compression packs the suitcase; larger context buys a bigger suitcase; evidence decides what must travel.

Final takeaway:

> Context strategy is evidence strategy: compress the noise, preserve the proof, and pay for larger context only when the original evidence is valuable enough to justify the cost and latency.

---

## Topic 20.3: Cost-Quality-Product Decision Frameworks

> **Topic time:** 8h
> Focus: Making product-level GenAI decisions with engineering discipline: when to use models, when to use deterministic logic, how to compare quality against cost, and how to defend trade-offs in real teams.

Cost engineering is not only about reducing spend.

It is about choosing the right kind of system for the product outcome.

Sometimes the right answer is:

```text
use a stronger model
```

Sometimes:

```text
use a cheaper model with routing
```

Sometimes:

```text
do not use GenAI at all
```

The central idea:

> A strong GenAI engineer does not force models into every workflow. They choose models only where uncertainty, language, variation, or judgment makes deterministic logic insufficient.

---

## Subtopic 20.3.a: When GenAI Is Justified vs When Deterministic Logic Is Better

> **Subtopic time:** 2h
> Outcome: You should be able to decide whether a product feature should use GenAI, deterministic logic, or a hybrid design. You should justify the choice using ambiguity, risk, cost, latency, auditability, maintenance, user value, and failure tolerance.

### Add to Knowledge Base

The most expensive GenAI mistake is not using the wrong model.

It is using a model where a rule, query, parser, workflow, or classifier would have been simpler, cheaper, faster, safer, and more reliable.

GenAI is powerful when the input is:

```text
messy
ambiguous
natural language
variable
semantic
open-ended
judgment-heavy
```

Deterministic logic is better when the requirement is:

```text
exact
repeatable
auditable
low-latency
low-cost
rule-bound
transactional
highly testable
```

The core mental model:

> Use deterministic logic when the answer can be specified. Use GenAI when the answer must be interpreted.

This is not anti-AI.

It is good engineering.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-7 to learn the difference between model-shaped and rule-shaped problems.
- **Intermediate:** Read sections 8-17 to reason about hybrid systems, risk, confidence, ROI, and product value.
- **Pro:** Complete the lab and practice the interview answer so you can defend when not to use GenAI.

---

### 0. Pre-Question Hook [Beginner]

A product manager asks:

```text
Can we use GenAI to decide whether a user gets a late fee?
```

The policy says:

```text
If payment_date is more than 5 days after due_date, apply late fee.
If customer_tier is enterprise, waive once per quarter.
If dispute_open is true, pause fee.
```

Should this be GenAI?

No.

This is deterministic business logic.

A model could explain the policy, answer questions about it, or help support agents interpret messy user messages.

But the actual fee decision should be:

```text
rules
tests
audit logs
clear exceptions
```

Now change the task:

```text
User writes a long complaint explaining why the late fee is unfair.
Classify the reason, summarize the situation, detect if it mentions financial hardship,
and suggest which policy exceptions might apply.
```

Now GenAI may be justified.

Same product area.

Different task shape.

---

### 1. The Intuition [Beginner]

Think about two workers.

One is a calculator.

One is an analyst.

Use the calculator when:

```text
the formula is known
the input fields are structured
the output must be exact
```

Use the analyst when:

```text
the input is messy
the meaning must be interpreted
the answer may require judgment
```

GenAI is the analyst.

Deterministic logic is the calculator.

If you ask the analyst to do calculator work, you get unnecessary cost and occasional mistakes.

If you ask the calculator to do analyst work, it breaks on nuance.

Good systems use both.

---

### 2. Definition [Beginner]

- **GenAI solution:** A system where a generative or language model interprets, transforms, reasons over, or generates content as part of the workflow.
- **Deterministic logic:** Rules, code, SQL, parsers, finite-state workflows, validations, lookup tables, and algorithms that produce predictable outputs for given inputs.
- **Hybrid design:** A system where deterministic logic handles exact control, validation, routing, and enforcement, while GenAI handles ambiguity, language, summarization, or judgment.
- **Core idea:** Choose the simplest reliable mechanism that satisfies the product requirement.

Short version:

```text
rules for certainty
models for ambiguity
hybrids for real products
```

---

### 3. Why This Decision Exists [Beginner]

GenAI creates new capability, but it also adds:

```text
cost
latency
probabilistic behavior
evaluation complexity
security review
privacy concerns
prompt/version maintenance
model/provider dependency
edge-case uncertainty
harder debugging
```

Deterministic logic adds:

```text
implementation effort
rule maintenance
limited flexibility
brittleness on messy inputs
coverage gaps for open-ended language
```

The decision exists because neither is universally better.

Use the right tool for the failure mode.

If the task fails because:

```text
the input is variable and semantic
```

GenAI may help.

If the task fails because:

```text
the code path is not explicit enough
```

GenAI may make it worse.

Strong statement:

> Model intelligence is not a substitute for system determinism where the business rule is already known.

---

### 4. GenAI Is Justified When [Intermediate]

GenAI is a strong fit when the task involves language, ambiguity, or variation that is hard to encode with rules.

Good signs:

- user input is natural language
- outputs require summarization or generation
- there are many valid phrasings
- task requires semantic matching
- edge cases are hard to enumerate
- data is semi-structured or messy
- human workers currently use judgment
- task benefits from personalization or explanation
- the system needs to synthesize multiple sources
- exact output can be validated afterward

Examples:

```text
summarize support ticket history
draft a response grounded in policy
extract likely fields from messy invoices
classify user intent from free text
convert natural language to a draft SQL query with validation
answer questions over documents with citations
generate a first draft of a product description
explain a complex error message to a user
```

GenAI is especially justified when:

```text
the alternative is expensive human interpretation
```

and:

```text
the model output can be reviewed, validated, constrained, or corrected
```

---

### 5. Deterministic Logic Is Better When [Intermediate]

Deterministic logic is better when the task is rule-bound, exact, repetitive, or high-stakes.

Good signs:

- inputs are structured
- output is known from rules
- correctness must be exact
- latency must be extremely low
- cost per call must be tiny
- decisions need auditability
- system mutates money, access, inventory, or permissions
- rules are maintained by policy/compliance teams
- failures must be explainable line by line
- expected behavior can be covered by tests

Examples:

```text
calculate late fees
apply tax rules
validate JSON schema
check account permissions
route by explicit user settings
deduplicate exact IDs
enforce rate limits
compute shipping price
check password policy
apply deterministic eligibility rules
```

Strong principle:

> If a SQL query, rule engine, parser, or validation function can solve it reliably, start there.

GenAI can still assist around the rule:

```text
explain the rule
summarize why a rule fired
classify messy user messages into rule inputs
generate draft documentation
```

But enforcement should remain deterministic.

---

### 6. The Key Axis: Interpret vs Enforce [Intermediate]

Many systems need both interpretation and enforcement.

Example:

```text
User: "I paid last Friday, but my bank had an outage. Can you waive the fee?"
```

GenAI can interpret:

```text
payment hardship mentioned
bank issue mentioned
waiver requested
date expression found
```

Deterministic logic should enforce:

```text
is payment late?
has waiver already been used this quarter?
is dispute open?
is user eligible?
```

Pattern:

```text
GenAI extracts or summarizes messy input.
Rules validate and decide.
GenAI explains the decision in human language.
```

This gives you:

```text
flexible input handling
auditable decision logic
clear user communication
```

One-line architecture:

```text
model for meaning, code for authority
```

---

### 7. Product Value Test [Intermediate]

Before using GenAI, ask:

```text
What product value does the model create that deterministic logic cannot?
```

Good answers:

- reduces human review time
- handles free-form user language
- improves task completion
- drafts useful content faster
- finds semantic matches rules miss
- summarizes long context
- improves accessibility or explanation
- enables workflows that were impossible before

Weak answers:

```text
because AI is trendy
because the demo looks good
because the rule engine is boring
because users expect AI
because we can prompt it quickly
```

Decision formula:

```text
GenAI is justified when:
  incremental product value
  >
  added cost + latency + risk + maintenance
```

If the incremental value is small, deterministic logic wins.

---

### 8. Risk And Reversibility [Pro]

Risk changes the decision.

Ask:

```text
What happens if the system is wrong?
Can the mistake be reversed?
Who is harmed?
How quickly is it detected?
Can a human review it?
Is there an audit trail?
```

Low-risk, reversible tasks:

```text
draft email
summarize meeting notes
suggest search query
recommend tags
brainstorm ideas
```

GenAI is often fine.

High-risk, hard-to-reverse tasks:

```text
approve loan
deny medical claim
change account permissions
send legal notice
execute payment
delete user data
modify production infrastructure
```

Use deterministic logic and human approval.

GenAI may assist, but should not be the final authority unless the domain has strong validation and governance.

Rule:

```text
The less reversible the outcome, the more deterministic the control path should be.
```

---

### 9. Cost And Latency Test [Intermediate]

Even when GenAI works, it may not be worth it.

Ask:

```text
How many times per day will this run?
What is cost per request?
What is cost per successful task?
What is added latency?
What is user tolerance for delay?
What cheaper deterministic path exists?
```

Example:

```text
Task: classify whether uploaded file extension is allowed.
Rule: extension in allowlist.
Latency: microseconds.
Cost: effectively zero.
```

Using GenAI would be absurd.

Another example:

```text
Task: classify whether a user complaint is about billing, product quality, legal threat, or cancellation risk.
Input: long free-form message.
Rules: brittle keyword matching.
```

GenAI may be worth it if it improves routing and reduces support cost.

Strong question:

```text
Would I still use a model if each call cost real money and added seconds of latency?
```

If no, do not use it.

---

### 10. Quality Test [Intermediate]

A deterministic system is often:

```text
high precision within covered cases
low flexibility outside covered cases
```

A GenAI system is often:

```text
higher flexibility
less predictable exactness
```

Evaluate quality by task type.

For deterministic logic:

```text
unit tests
property tests
golden cases
rules coverage
edge-case tables
```

For GenAI:

```text
eval sets
human ratings
structured validators
groundedness checks
failure taxonomy
slice analysis
```

Decision:

```text
If deterministic logic covers 99.9 percent of cases cheaply and safely, use it.
If rules cover only 60 percent and humans handle the rest, GenAI may help with the ambiguous remainder.
```

This leads to hybrid routing:

```text
rules handle clear cases
GenAI handles unclear cases
humans handle risky uncertain cases
```

---

### 11. Hybrid Patterns [Pro]

Most production GenAI systems should be hybrid.

#### Pattern 1: Rules First, Model On Ambiguity

```text
if structured rule applies:
    use deterministic path
else:
    use GenAI interpretation
```

Good for:

```text
support routing, document processing, eligibility pre-checks
```

#### Pattern 2: Model Extracts, Rules Decide

```text
model extracts fields from messy input
rules validate and make final decision
```

Good for:

```text
invoices, contracts, forms, support requests
```

#### Pattern 3: Model Drafts, Deterministic Validators Check

```text
model creates draft
schema validators, policy rules, and citation checks validate it
```

Good for:

```text
emails, reports, structured outputs, RAG answers
```

#### Pattern 4: Deterministic Workflow, Model Explanation

```text
workflow decides
model explains decision in user-friendly language
```

Good for:

```text
billing, policy, eligibility, compliance workflows
```

#### Pattern 5: Model Suggests, Human Approves

```text
model recommends action
human approves before mutation
```

Good for:

```text
high-risk actions, customer-impacting changes, enterprise workflows
```

Hybrid is often the senior answer.

---

### 12. Automation Levels [Intermediate]

Think in levels of autonomy.

| Level | Description | Example |
|---|---|---|
| L0 | no model | deterministic rule |
| L1 | model assists human | draft summary |
| L2 | model suggests, human approves | recommended refund decision |
| L3 | model acts in low-risk cases | auto-tag ticket |
| L4 | model acts with guardrails and rollback | auto-resolve simple support issue |
| L5 | model fully autonomous | rare, high governance needed |

Most valuable GenAI starts at:

```text
L1 or L2
```

Then moves upward only after:

```text
evals are strong
failure modes are known
guardrails exist
rollback exists
observability exists
business accepts risk
```

Do not jump to autonomy because the demo worked.

---

### 13. Confidence Thresholds And Escalation [Pro]

A good system does not force every case through the same path.

Use confidence and risk:

```text
high confidence + low risk -> deterministic or model automation
medium confidence -> model suggestion with validation
low confidence or high risk -> human review
```

Example:

```text
if rule_match_confidence == 1.0:
    deterministic decision
elif model_confidence > threshold and risk == "low":
    model-assisted automation
else:
    human review
```

Confidence sources:

- retrieval score margin
- classifier confidence
- schema validation pass/fail
- agreement between model and rules
- self-consistency across attempts
- evaluator score
- source authority
- business risk label

Important:

```text
model confidence should be calibrated with real outcomes
```

Do not blindly trust a model's self-reported confidence.

---

### 14. Decision Matrix [Intermediate]

| Task Shape | Better Default | Why |
|---|---|---|
| exact calculation | deterministic | precise, cheap, testable |
| schema validation | deterministic | binary and auditable |
| permission check | deterministic | security-critical |
| free-form summarization | GenAI | language-heavy |
| semantic search answer | GenAI + retrieval | requires interpretation |
| messy field extraction | hybrid | model extracts, rules validate |
| high-risk approval | deterministic + human | audit and safety |
| support email draft | GenAI | variation and language |
| final refund decision | rules or human | customer impact |
| policy explanation | hybrid | rules decide, model explains |
| code formatting | deterministic | tools are exact |
| code explanation | GenAI | language interpretation |

Simple version:

```text
exact outcome -> deterministic
language interpretation -> GenAI
high-risk action -> deterministic control plus approval
messy input to exact decision -> hybrid
```

---

### 15. ROI And Failure-Cost Reasoning [Pro]

GenAI is justified when value exceeds total expected cost.

Expected value:

```text
labor saved
revenue increased
conversion improved
support deflection
faster completion
quality improvement
risk reduction
new capability unlocked
```

Expected cost:

```text
model cost
latency cost
engineering cost
evaluation cost
monitoring cost
human review cost
failure cost
vendor risk
security review
maintenance
```

Simple formula:

```text
expected_net_value =
    value_per_success * success_count
  - model_and_infra_cost
  - human_review_cost
  - expected_failure_cost
  - maintenance_cost
```

Failure cost matters.

Example:

```text
drafting a bad marketing tagline = low cost
giving a wrong medical policy answer = high cost
```

Same model quality can be acceptable in one product and unacceptable in another.

---

### 16. Anti-Patterns [Intermediate]

Common bad GenAI decisions:

| Anti-Pattern | Why It Fails | Better Approach |
|---|---|---|
| model as rule engine | probabilistic output for exact policy | use rules, model explains |
| model as parser for strict format | inconsistent edge cases | use parser/schema, model repairs ambiguous input |
| model as permission checker | security risk | deterministic access control |
| model as database filter | slow and expensive | SQL/filter logic |
| model as calculator | arithmetic mistakes and cost | deterministic calculation |
| all-or-nothing automation | risky rollout | staged autonomy and human review |
| no eval before launch | unknown failure modes | build task-specific evals |
| prompt-only governance | weak control | system constraints, validators, approvals |
| GenAI for low-value high-volume task | bad unit economics | cheaper deterministic path |
| deterministic rules for messy language | brittle UX | use model to interpret, rules to decide |

Interview-grade sentence:

> I would not use GenAI for the part of the system where correctness is already expressible as code.

---

### 17. Product Decision Checklist [Pro]

Before choosing GenAI, answer:

1. What is the exact user outcome?
2. Is the input structured or messy?
3. Is the output exact or open-ended?
4. Can rules solve the core task reliably?
5. What does GenAI improve over rules?
6. What is the cost per successful task?
7. What latency does it add?
8. What is the failure cost?
9. Is the action reversible?
10. Can we validate the output?
11. Can we audit the decision?
12. What confidence threshold routes to human review?
13. What deterministic checks remain?
14. What monitoring detects regressions?
15. What is the rollback path?

If you cannot answer these, you are not ready to automate with GenAI.

---

### 18. Trace Schema For GenAI Justification [Pro]

```json
{
  "decision_id": "decision_genai_fit_001",
  "feature": "support_ticket_triage",
  "task_type": "free_text_intent_classification",
  "chosen_approach": "hybrid",
  "deterministic_path": {
    "used": true,
    "rule_coverage_estimate": 0.42,
    "rules": ["known_form_type", "priority_account", "explicit_category"]
  },
  "genai_path": {
    "used": true,
    "reason": "free-form user language with many category phrasings",
    "model_cost_estimate": 0.0,
    "latency_budget_ms": 800
  },
  "risk": {
    "business_risk": "medium",
    "reversible": true,
    "human_review_required": false,
    "escalate_when_confidence_below": 0.75
  },
  "outcome_metrics": {
    "routing_accuracy": 0.0,
    "manual_review_reduction": 0.0,
    "cost_per_success": 0.0,
    "p95_latency_ms": 0
  },
  "validation": {
    "schema_checks": true,
    "audit_log": true,
    "rollback_available": true
  }
}
```

This trace captures:

```text
why GenAI was used
where deterministic logic remains
what risk controls exist
which metrics prove value
```

That is what a decision record should do.

---

### 19. Code Sample: Deterministic First, Model On Ambiguity

```python
def deterministic_route(message, metadata):
    if metadata.get("form_type") == "refund_request":
        return {
            "route": "refunds",
            "confidence": 1.0,
            "source": "deterministic_form_type",
        }

    if "cancel subscription" in message.lower():
        return {
            "route": "retention",
            "confidence": 0.95,
            "source": "deterministic_keyword",
        }

    return None


def model_route(message):
    # Placeholder for a model call in a real system.
    if "charged twice" in message.lower():
        return {
            "route": "billing",
            "confidence": 0.82,
            "source": "model_semantic_classification",
        }

    return {
        "route": "general_support",
        "confidence": 0.55,
        "source": "model_uncertain",
    }


def route_ticket(message, metadata, review_threshold=0.70):
    deterministic = deterministic_route(message, metadata)

    if deterministic:
        return deterministic

    model_result = model_route(message)

    if model_result["confidence"] < review_threshold:
        return {
            "route": "human_review",
            "confidence": model_result["confidence"],
            "source": model_result["source"],
        }

    return model_result


examples = [
    ("I need to cancel subscription today", {}),
    ("I think I was charged twice after upgrading", {}),
    ("Something weird happened", {}),
    ("Please process this", {"form_type": "refund_request"}),
]

for message, metadata in examples:
    print(route_ticket(message, metadata))
```

Expected lesson:

```text
Use deterministic routes where clear, model interpretation where useful, and human review where confidence is low.
```

---

### 20. Mini Program: GenAI ROI Simulator

This simulator compares deterministic, GenAI, and hybrid designs.

```python
def expected_cost_per_task(config):
    model_cost = config.get("model_cost", 0.0)
    deterministic_cost = config.get("deterministic_cost", 0.0)
    human_review_cost = config["human_review_rate"] * config["human_review_cost"]
    failure_cost = config["failure_rate"] * config["failure_cost"]

    return model_cost + deterministic_cost + human_review_cost + failure_cost


def expected_net_value(config):
    success_value = config["success_rate"] * config["value_per_success"]
    cost = expected_cost_per_task(config)
    return success_value - cost


def main():
    designs = {
        "deterministic_only": {
            "success_rate": 0.62,
            "value_per_success": 1.00,
            "deterministic_cost": 0.001,
            "model_cost": 0.0,
            "human_review_rate": 0.30,
            "human_review_cost": 1.50,
            "failure_rate": 0.08,
            "failure_cost": 2.00,
        },
        "genai_only": {
            "success_rate": 0.82,
            "value_per_success": 1.00,
            "deterministic_cost": 0.0,
            "model_cost": 0.035,
            "human_review_rate": 0.12,
            "human_review_cost": 1.50,
            "failure_rate": 0.06,
            "failure_cost": 2.00,
        },
        "hybrid": {
            "success_rate": 0.86,
            "value_per_success": 1.00,
            "deterministic_cost": 0.001,
            "model_cost": 0.018,
            "human_review_rate": 0.08,
            "human_review_cost": 1.50,
            "failure_rate": 0.03,
            "failure_cost": 2.00,
        },
    }

    for name, config in designs.items():
        print(name)
        print("  expected_cost_per_task:", round(expected_cost_per_task(config), 4))
        print("  expected_net_value:", round(expected_net_value(config), 4))


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
The best design is not always the lowest model cost or the highest automation. It is the best value after success, review, and failure costs.
```

---

### 21. Hands-On Lab: Decide Whether GenAI Is Justified [Pro]

#### Build

Pick one proposed feature:

```text
support ticket triage
invoice approval
contract clause extraction
product recommendation explanation
refund decision
document Q&A
email response drafting
account risk review
```

Describe:

```text
user outcome
input type
output type
failure cost
reversibility
latency target
cost target
audit requirements
human review availability
```

#### Compare

Design three versions:

1. Deterministic-only.
2. GenAI-only.
3. Hybrid.

For each, estimate:

```text
implementation complexity
runtime cost
latency
accuracy/success
human review rate
failure cost
auditability
maintenance burden
rollback path
```

#### Decide

Use this table:

| Criterion | Deterministic | GenAI | Hybrid |
|---|---:|---:|---:|
| handles messy input | | | |
| exact decision quality | | | |
| latency | | | |
| cost per success | | | |
| auditability | | | |
| human review need | | | |
| failure risk | | | |
| maintenance | | | |

#### Defend

Write:

```text
I would choose <approach>.
The task is <rule-shaped/model-shaped/hybrid-shaped>.
The model is justified because <specific value>.
Deterministic logic remains responsible for <specific controls>.
The fallback is <fallback>.
The key success metric is <metric>.
The key risk metric is <metric>.
```

---

### 22. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| using GenAI because it is available | adds cost and risk without value | start from product task shape |
| model decides exact business rules | non-deterministic and hard to audit | rules decide, model explains |
| deterministic logic handles messy text alone | brittle keyword logic | model interprets, rules validate |
| no human review for high risk | unsafe automation | escalate uncertain or high-risk cases |
| comparing only accuracy | ignores cost, latency, and failure impact | use cost-quality-product metrics |
| using GenAI for low-value high-volume tasks | poor unit economics | deterministic or cached path |
| no confidence threshold | all cases treated equally | route by confidence and risk |
| no rollback path | failures become incidents | design fallback and rollback |
| no audit trail | impossible to defend decisions | log rules, model inputs, outputs, versions |
| replacing systems with prompts | weak control plane | combine prompts with validation and workflow |

---

### 23. Practical Interview Question [Intermediate]

> A product manager asks whether your team should use GenAI to automate a customer support workflow. How do you decide whether GenAI is justified or deterministic logic is better?

---

### 24. Strong Answer [Pro]

I would first separate the workflow into parts. I would ask which parts are rule-shaped and which parts are language- or judgment-shaped. If a step is an exact calculation, permission check, eligibility rule, schema validation, database filter, or transactional decision, I would prefer deterministic logic because it is cheaper, faster, testable, and auditable. I would not use a model as a rule engine.

Then I would identify where GenAI creates value. If the workflow involves messy user language, summarizing long ticket histories, classifying intent from free text, drafting responses, semantic search over policies, or explaining decisions in natural language, GenAI may be justified. The model should handle interpretation and generation, while deterministic logic should enforce policies, validate structured outputs, and control risky actions.

I would compare deterministic-only, GenAI-only, and hybrid designs using cost per successful task, latency, quality, human review rate, auditability, failure cost, and reversibility. For low-risk reversible tasks, higher model autonomy may be acceptable. For high-risk or hard-to-reverse actions, I would require deterministic controls and human approval.

My default production design would be hybrid: rules handle clear cases, the model handles ambiguous language or drafts, validators check outputs, and uncertain or high-risk cases escalate to humans. I would launch with evals, traces, confidence thresholds, rollback paths, and monitoring for cost, quality, latency, and failure modes.

The decision is justified only if GenAI adds product value that exceeds its cost, latency, risk, and maintenance burden. Otherwise deterministic logic is the stronger engineering choice.

---

### 25. Active Recall [Beginner]

Answer these without looking:

1. What is the simplest rule for choosing deterministic logic?
2. What is the simplest rule for choosing GenAI?
3. Why should a model not be used as a rule engine?
4. What does "model for meaning, code for authority" mean?
5. Name three tasks that are better deterministic.
6. Name three tasks where GenAI may be justified.
7. What is a hybrid design?
8. Why does reversibility matter?
9. Why does failure cost matter?
10. What is cost per successful task?
11. Why is GenAI risky for permission checks?
12. Why is deterministic logic brittle for messy language?
13. What is confidence-based routing?
14. What should happen to low-confidence high-risk cases?
15. What is staged autonomy?
16. What should deterministic validators check?
17. What metrics compare GenAI vs deterministic designs?
18. What is an anti-pattern in this topic?
19. What should a decision trace record?
20. What is the final lesson of this topic?

Expected answers:

1. Use deterministic logic when the answer can be specified exactly.
2. Use GenAI when the answer must be interpreted from messy language or context.
3. It is probabilistic, costly, slower, and harder to audit.
4. Models interpret messy input; code enforces final decisions.
5. Fee calculation, permission checks, schema validation.
6. Summarization, free-text classification, semantic document Q&A.
7. A system combining model interpretation with deterministic control.
8. Irreversible actions require stronger controls.
9. Same model error can be acceptable or unacceptable depending on impact.
10. Total cost divided by successful outcomes.
11. Security decisions must be exact and auditable.
12. Rules struggle with varied phrasing and implicit meaning.
13. Routing by confidence/risk to rules, model, or human.
14. Escalate to human review or safer fallback.
15. Moving from assistive to autonomous only after evidence and controls.
16. Schema, policy, citations, constraints, permissions, safety.
17. Cost, latency, success rate, review rate, auditability, failure cost.
18. Using GenAI where a simple rule or SQL query works.
19. Why GenAI was used, deterministic controls, risk, metrics, versions.
20. Use GenAI where it creates value from ambiguity; use deterministic logic where correctness is specified.

---

### 26. Revision Notes

- **One-line summary:** GenAI is justified for ambiguity, language, and judgment; deterministic logic is better for exact, repeatable, auditable decisions.
- **Three keywords:** ambiguity, authority, hybrid.
- **One interview trap:** Recommending GenAI for the final decision when the actual business rule can be expressed cleanly in code.
- **One memory trick:** Calculator for rules, analyst for meaning, manager for approval.

Final takeaway:

> The strongest GenAI product decisions often say "use the model here, but not there": models interpret and draft, deterministic systems decide and enforce, and humans approve when risk demands it.

---

## Subtopic 20.3.b: Model Routing, Fallback Tiers, and Dynamic Quality Tiers

> **Subtopic time:** 2h
> Outcome: You should be able to design a model-routing policy that sends easy, low-risk tasks to cheaper/faster paths, hard or high-risk tasks to stronger paths, and degraded or failed requests to safe fallback tiers. You should also be able to explain how dynamic quality tiers balance cost, latency, reliability, and user value.

### Add to Knowledge Base

Once GenAI is justified, the next question is not:

```text
Which one model should we use for everything?
```

The better question is:

```text
Which model, prompt, retrieval depth, tool depth, and validation level should this specific task get?
```

Different requests have different needs.

Some are:

```text
easy
low-risk
short
high-confidence
cheap to retry
```

Others are:

```text
ambiguous
high-risk
long-context
tool-heavy
expensive if wrong
```

Model routing means choosing the right execution path for each request.

Fallback tiers mean defining what happens when the chosen path fails, times out, becomes too expensive, or produces low confidence.

Dynamic quality tiers mean the system can spend more quality budget only when the request deserves it.

The core mental model:

> Do not buy first-class tickets for every request. Route based on task difficulty, risk, user value, and available budget.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-7 to learn model tiers, routing, and fallback basics.
- **Intermediate:** Read sections 8-17 to reason about confidence, risk, latency, product tiers, and observability.
- **Pro:** Complete the lab and practice the interview answer so you can defend a routing policy in a product architecture review.

---

### 0. Pre-Question Hook [Beginner]

A customer support assistant handles two requests.

Request A:

```text
"How do I reset my password?"
```

Request B:

```text
"Our enterprise contract renewal says support is included, but billing charged us twice after a custom amendment. Explain what happened and draft a response."
```

Should both use the same model path?

Probably not.

Request A may use:

```text
cached FAQ
small model
shallow retrieval
no expensive reranking
basic safety checks
```

Request B may need:

```text
stronger model
deeper retrieval
contract-specific sources
tool calls
citation validation
human approval before sending
```

Same product.

Different quality budget.

That is model routing.

---

### 1. The Intuition [Beginner]

Think of hospital triage.

Not every patient goes straight to the operating room.

Some need:

```text
basic checkup
```

Some need:

```text
specialist review
```

Some need:

```text
emergency intervention
```

The triage desk decides where each case should go.

GenAI routing is similar.

The router asks:

```text
How hard is this request?
How risky is this request?
How valuable is this request?
How much time and budget do we have?
What happens if the answer is wrong?
```

Then it chooses the path.

Routing is how you avoid using your most expensive, slowest, strongest system for every small task.

---

### 2. Definition [Beginner]

- **Model routing:** Selecting a model or workflow path based on request features, risk, confidence, user tier, latency budget, cost budget, or task type.
- **Fallback tier:** A secondary path used when the primary path fails, times out, violates quality rules, or becomes unavailable.
- **Dynamic quality tier:** A runtime choice of how much quality budget to spend, such as retrieval depth, model strength, validation level, tool access, or human review.
- **Escalation:** Moving a request to a stronger, slower, costlier, or more human-controlled path.
- **Degradation:** Moving to a simpler, cheaper, cached, partial, or lower-capability path when constraints require it.
- **Core idea:** Match system effort to task value and risk instead of using one fixed path for all requests.

Short version:

```text
routing chooses the first path
fallback handles failure
quality tiers decide how much effort the task deserves
```

---

### 3. Why It Exists [Beginner]

One-size-fits-all GenAI is usually inefficient.

If every request uses the strongest path:

```text
cost rises
latency rises
capacity drops
simple tasks are over-served
```

If every request uses the cheapest path:

```text
hard tasks fail
high-risk answers become unsafe
users lose trust
human escalation increases
```

Routing exists because workloads are mixed.

A production system may serve:

```text
FAQ answers
document Q&A
long research
tool workflows
structured extraction
customer-facing drafts
high-risk policy decisions
internal brainstorming
```

Each deserves a different path.

Strong statement:

> Model routing is cost-quality control at runtime.

---

### 4. Model Tier Vocabulary [Beginner]

Use generic tiers rather than hardcoding brand thinking.

| Tier | Typical Role | Strength | Weakness |
|---|---|---|---|
| deterministic | rules, cache, SQL, parser | cheapest, fastest, exact | limited to specified cases |
| small model | easy classification, simple drafting | cheap and fast | weaker reasoning |
| medium model | common assistant tasks | balanced | may fail on hard cases |
| large/strong model | complex reasoning, long context, high-risk tasks | higher quality | higher cost and latency |
| specialist model | embeddings, reranking, OCR, code, moderation | optimized for one job | narrow scope |
| human tier | approval, review, exception handling | judgment and accountability | slow and expensive |

Routing can choose more than model size.

It can choose:

```text
retrieval depth
reranking on/off
tool access
context compression
validation strictness
human review
output length
streaming behavior
```

This is why "model routing" often means:

```text
workflow routing
```

not only:

```text
model name routing
```

---

### 5. Routing Signals [Intermediate]

Good routers use signals.

Request signals:

```text
task type
query length
language
domain
intent
requested output format
context size
document type
tool requirement
```

Difficulty signals:

```text
retrieval score margin
number of relevant sources
ambiguity
multi-hop requirement
schema complexity
history length
previous failed attempt
```

Risk signals:

```text
customer-facing
financial/legal/medical impact
external action
permission mutation
data sensitivity
compliance policy
irreversibility
```

Business signals:

```text
paid tier
tenant priority
SLA
user value
workflow value
human review cost
cost budget remaining
```

System signals:

```text
provider availability
rate limits
queue depth
p95 latency
timeout budget
cache hit
incident mode
```

The router should combine these signals into a policy.

---

### 6. Common Routing Patterns [Intermediate]

#### Pattern 1: Cheap First, Escalate On Uncertainty

```text
small model tries first
validator checks output
if confidence low or validation fails:
    escalate to stronger model
```

Good for:

```text
high-volume tasks with many easy cases
```

Risk:

```text
two calls on hard cases may add latency
```

#### Pattern 2: Strong First For High-Risk Tasks

```text
if risk is high:
    use strong model and strict validation immediately
```

Good for:

```text
customer-facing, legal, compliance, safety, high-value workflows
```

Risk:

```text
over-routing to strong path increases cost
```

#### Pattern 3: Deterministic First, Model For Ambiguity

```text
rules/cache handle clear cases
model handles unclear cases
```

Good for:

```text
FAQ, routing, eligibility explanations, simple support
```

#### Pattern 4: Retrieval Confidence Routing

```text
if retrieval confidence high:
    shallow RAG
else:
    deeper retrieval + rerank + stronger model
```

Good for:

```text
document Q&A and enterprise search
```

#### Pattern 5: User/Product Tier Routing

```text
free tier -> cheaper model and shorter outputs
paid tier -> stronger model and deeper workflow
enterprise tier -> strongest model, audit, human approval options
```

Good for:

```text
SaaS products with differentiated plans
```

---

### 7. Fallback Taxonomy [Intermediate]

Fallback does not mean "try another model" only.

Fallback types:

| Fallback | Meaning | Example |
|---|---|---|
| retry same path | transient failure recovery | retry provider timeout once |
| alternate model | provider/model issue | use backup model tier |
| stronger escalation | low quality/confidence | rerun with stronger model |
| cheaper degradation | budget/latency pressure | shorter answer or simpler workflow |
| cached response | dependency unavailable | answer from known FAQ/cache |
| partial answer | missing optional tool | answer from available evidence |
| ask clarification | ambiguous request | request narrower query |
| human review | high risk or uncertainty | queue for support agent |
| deterministic fallback | model output invalid | use rules/template |
| async fallback | task too long | continue in background and notify |

Good fallback is:

```text
safe
honest
observable
bounded
product-appropriate
```

Bad fallback:

```text
silently lower quality without telling the user
hallucinate missing tool data
retry until budget is gone
hide validation failure
```

---

### 8. Dynamic Quality Tiers [Intermediate]

Quality tier is not only model strength.

It can include:

```text
model size
retrieval top-k
reranking on/off
context window
compression strategy
tool depth
validation strictness
number of critique/repair loops
human approval
output detail level
```

Example tiers:

| Tier | Path | Use Case |
|---|---|---|
| bronze | cache/rules/small model | simple low-risk tasks |
| silver | medium model + shallow retrieval | normal Q&A |
| gold | strong model + rerank + validation | high-value or ambiguous tasks |
| platinum | strong model + tools + human approval | high-risk external action |

Dynamic quality means:

```text
the system picks a tier per request
```

not:

```text
every user always gets the same path
```

But quality tiering must be aligned with product promises.

Do not secretly degrade paid or high-risk workflows below what the product claims.

---

### 9. Cheap-First vs Strong-First [Pro]

Cheap-first strategy:

```text
try cheaper/faster model
validate
escalate if needed
```

Best when:

- many tasks are easy
- validation is reliable
- retry latency is acceptable
- failure is reversible
- low-cost first pass catches most cases

Strong-first strategy:

```text
use stronger path immediately
```

Best when:

- failure cost is high
- user expects premium quality
- latency budget allows one strong call but not two calls
- validation is hard
- hard cases are common
- output is customer-facing or compliance-sensitive

Counterintuitive point:

```text
Cheap-first can be more expensive for hard workloads
```

because:

```text
cheap call + failed validation + strong call
>
strong call once
```

Decision metric:

```text
expected_cost =
    cheap_path_cost
  + escalation_rate * strong_path_cost
```

If escalation rate is high, strong-first may win.

---

### 10. Confidence Thresholds [Pro]

Routing needs thresholds.

Examples:

```text
if retrieval_score_margin > 0.25:
    shallow_rag
else:
    deep_rag_with_rerank
```

```text
if extraction_validator_passes:
    accept
else:
    escalate_to_stronger_model
```

```text
if risk == "high" and confidence < 0.95:
    human_review
```

Confidence can come from:

- model classifier probability
- retrieval score margin
- agreement between two models
- validator pass/fail
- schema validity
- citation support score
- tool success
- historical success for that route
- uncertainty labels

Important:

```text
confidence must be calibrated against real outcomes
```

Do not trust:

```text
"The model says it is 95% confident"
```

unless that score has been validated.

Thresholds should vary by risk.

Low risk:

```text
accept at lower confidence
```

High risk:

```text
escalate at lower uncertainty
```

---

### 11. Budget-Aware Routing [Intermediate]

Routing should respect budgets.

Budgets:

```text
cost budget
latency budget
token budget
human review budget
provider quota
tenant quota
daily spend limit
```

Example:

```text
if remaining_latency_ms < 1500:
    skip reranker
    use shorter answer
    return partial result with caveat
```

```text
if tenant_monthly_budget_near_limit:
    route low-risk tasks to cheaper path
    preserve strong path for high-risk tasks
```

Budget-aware routing should not violate safety.

Bad:

```text
skip compliance validation because budget is low
```

Better:

```text
defer low-priority optional features, preserve required checks
```

Budget pressure should degrade optional quality before safety.

---

### 12. Availability Fallbacks [Intermediate]

Models and providers can fail.

Failure modes:

```text
timeout
rate limit
provider outage
model overload
invalid output
safety refusal
context length error
tool failure
quota exhausted
```

Availability fallback plan:

```text
primary model
backup model
cached response
async processing
human review
graceful error
```

But backup models are not identical.

You must test:

```text
prompt compatibility
schema compatibility
quality difference
latency difference
cost difference
safety behavior
tool-call behavior
```

Do not assume fallback output is equivalent.

Fallback tiers should be part of evaluation, not only incident response.

---

### 13. Quality Fallbacks [Pro]

Quality fallback happens when the model responds, but the response is not good enough.

Signals:

```text
schema validation fails
citation validator fails
answer unsupported
retrieval confidence low
tool result incomplete
toxicity/safety issue
format invalid
low evaluator score
```

Fallback actions:

```text
repair with same model
rerun with stronger model
retrieve deeper and retry
ask clarifying question
switch to extractive answer
send to human review
return "I do not have enough evidence"
```

Important:

```text
quality fallback should be bounded
```

Example:

```text
max_repair_attempts = 1
max_total_cost = configured budget
max_total_latency = configured deadline
```

Unbounded repair loops are cost and latency traps.

---

### 14. Product Tier Routing [Intermediate]

Product tiers may affect routing.

Example:

| Product Tier | Routing Policy |
|---|---|
| free | small model, shallow retrieval, lower daily quota |
| pro | medium model, reranking for ambiguous queries |
| enterprise | stronger model, audit logs, source validation, human approval |

This can be valid when users understand the product offering.

But be careful.

Quality tiering should not create:

```text
unsafe low-tier behavior
misleading answers
privacy differences
hidden unfairness
compliance gaps
```

Minimum quality and safety should be enforced across all tiers.

Paid tiers can receive:

```text
more depth
more context
more speed
more usage
more auditability
more human support
```

But no tier should receive:

```text
unsafe or knowingly unreliable decisions
```

---

### 15. Evaluation-Driven Routing [Pro]

Routing policies should come from evals.

Build an eval set with slices:

```text
easy FAQ
ambiguous policy
long-context synthesis
tool-required workflow
high-risk customer-facing
low-risk internal
multilingual
structured extraction
edge cases
```

For each route, compare:

```text
small model
medium model
large model
specialist model
hybrid workflow
human review
```

Measure:

```text
success rate
cost per success
latency
validation failure rate
escalation rate
unsupported claim rate
human review rate
user acceptance
```

Then define policies:

```text
easy FAQ -> small model or deterministic
ambiguous policy -> medium model + retrieval
high-risk policy -> strong model + validation
low-confidence -> human review
```

Routing without evals is guesswork with a dashboard.

---

### 16. Router Failure Modes [Pro]

The router itself can fail.

Failure modes:

| Failure | Result | Mitigation |
|---|---|---|
| under-routing | hard task sent to weak path | validators and escalation |
| over-routing | easy task sent to expensive path | cost monitoring and thresholds |
| risk misclassification | unsafe automation | conservative defaults for uncertain risk |
| routing drift | distribution changes | monitoring and eval refresh |
| confidence miscalibration | wrong accept/escalate decisions | calibration against outcomes |
| fallback loop | repeated retries | max attempts and deadlines |
| hidden degradation | user gets worse quality silently | explicit product policy and logging |
| provider-specific prompt mismatch | fallback model breaks format | fallback evals |

Router quality is product quality.

Monitor the router like any model.

---

### 17. Observability For Routing [Intermediate]

Log routing decisions.

Must-have fields:

```text
request_id
task_type
risk_level
user/product tier
chosen_route
candidate_routes
router_version
model_tier
retrieval_tier
validation_tier
confidence
budget_remaining
fallback_used
fallback_reason
escalation_reason
final_outcome
cost
latency
```

Questions logs should answer:

- Which routes are most expensive?
- Which routes fail most often?
- Which fallback fires most?
- Which tasks are under-routed?
- Which tasks are over-routed?
- Did a router version increase cost?
- Did quality improve enough to justify stronger routing?
- Are fallback tiers preserving safety?

Without route observability, dynamic quality becomes invisible complexity.

---

### 18. Routing Policy Schema [Pro]

```json
{
  "routing_decision_id": "route_001",
  "router_version": "router_policy_v7",
  "request": {
    "task_type": "enterprise_policy_question",
    "risk_level": "high",
    "user_tier": "enterprise",
    "estimated_context_tokens": 12000,
    "requires_external_action": false
  },
  "signals": {
    "retrieval_confidence": 0.62,
    "query_ambiguity": "high",
    "tool_required": true,
    "latency_budget_ms": 8000,
    "cost_budget": 0.08
  },
  "chosen_tier": {
    "model_tier": "strong",
    "retrieval_tier": "deep_with_rerank",
    "validation_tier": "strict_citation_check",
    "human_review": false
  },
  "fallback_policy": {
    "on_timeout": "partial_answer_with_sources",
    "on_validation_failure": "escalate_to_human_review",
    "on_provider_failure": "backup_strong_model"
  },
  "outcome": {
    "fallback_used": false,
    "task_success": true,
    "cost": 0.0,
    "latency_ms": 0
  }
}
```

This is a decision record.

It captures:

```text
why this route was chosen
what fallback should happen
whether the choice worked
```

---

### 19. Code Sample: Simple Model Router

```python
def choose_route(task):
    if task["deterministic_match"]:
        return {
            "route": "deterministic",
            "reason": "exact rule or cache match",
        }

    if task["risk"] == "high":
        return {
            "route": "strong_model_strict_validation",
            "reason": "high-risk task requires stronger path",
        }

    if task["requires_tools"]:
        return {
            "route": "medium_model_with_tools",
            "reason": "tool workflow required",
        }

    if task["estimated_tokens"] > 12000:
        return {
            "route": "large_context_model",
            "reason": "large context requirement",
        }

    if task["confidence_from_classifier"] > 0.85:
        return {
            "route": "small_model_fast_path",
            "reason": "easy low-risk task",
        }

    return {
        "route": "medium_model_standard_path",
        "reason": "default balanced path",
    }


tasks = [
    {
        "deterministic_match": True,
        "risk": "low",
        "requires_tools": False,
        "estimated_tokens": 1000,
        "confidence_from_classifier": 0.99,
    },
    {
        "deterministic_match": False,
        "risk": "high",
        "requires_tools": True,
        "estimated_tokens": 9000,
        "confidence_from_classifier": 0.60,
    },
    {
        "deterministic_match": False,
        "risk": "low",
        "requires_tools": False,
        "estimated_tokens": 2000,
        "confidence_from_classifier": 0.91,
    },
]

for task in tasks:
    print(choose_route(task))
```

Expected lesson:

```text
Routing policy should be explicit, explainable, and based on task signals.
```

---

### 20. Mini Program: Dynamic Tier Simulator

This simulator compares fixed strong routing against dynamic routing.

```python
def expected_dynamic_cost(requests, routes):
    total_cost = 0.0
    total_successes = 0

    for request in requests:
        route = routes[request["route"]]
        total_cost += route["cost"]
        total_successes += route["success_rate"]

    return {
        "total_expected_cost": total_cost,
        "expected_successes": total_successes,
        "cost_per_expected_success": total_cost / total_successes if total_successes else None,
    }


def main():
    routes = {
        "small": {
            "cost": 0.004,
            "success_rate": 0.86,
        },
        "medium": {
            "cost": 0.012,
            "success_rate": 0.91,
        },
        "strong": {
            "cost": 0.040,
            "success_rate": 0.96,
        },
        "human_review": {
            "cost": 1.50,
            "success_rate": 0.99,
        },
    }

    dynamic_requests = (
        [{"route": "small"} for _ in range(700)]
        + [{"route": "medium"} for _ in range(230)]
        + [{"route": "strong"} for _ in range(60)]
        + [{"route": "human_review"} for _ in range(10)]
    )

    fixed_strong_requests = [{"route": "strong"} for _ in range(1000)]

    print("dynamic")
    print(expected_dynamic_cost(dynamic_requests, routes))
    print()

    print("fixed strong")
    print(expected_dynamic_cost(fixed_strong_requests, routes))


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
Dynamic routing can reduce cost while preserving quality if the router correctly identifies which requests need stronger tiers.
```

But always check:

```text
under-routed failure rate
high-risk slices
p95 latency
user acceptance
```

---

### 21. Hands-On Lab: Design A Routing Policy [Pro]

#### Build

Choose one product:

```text
support RAG assistant
document AI extractor
coding assistant
research agent
contract review assistant
customer email drafter
workflow automation agent
```

Define request slices:

```text
easy
medium
hard
high-risk
tool-required
long-context
low-confidence
premium user
```

#### Design

Create routes:

```text
deterministic/cache path
small model fast path
standard model path
strong model path
specialist model path
human review path
```

For each route, specify:

```text
entry criteria
model tier
retrieval tier
tool access
validation level
max latency
max cost
fallback policy
success metric
risk metric
```

#### Test

Use an eval set and measure:

```text
route distribution
success rate by route
cost per route
cost per successful task
latency by route
fallback rate
escalation rate
under-routing failures
over-routing waste
```

#### Defend

Write:

```text
I route <slice> to <tier> because <reason>.
I escalate when <condition>.
I fallback to <path> when <failure>.
The policy saves <cost/latency> while preserving <quality/safety metric>.
The main risk is <risk>, monitored by <metric>.
```

---

### 22. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| one strongest model for everything | overpays for easy tasks | route by difficulty and risk |
| cheapest model for everything | hard tasks fail | escalate by confidence and risk |
| fallback only on provider failure | quality failures still ship | fallback on validation and confidence failures |
| unbounded fallback retries | cost and latency spiral | max attempts, deadlines, budgets |
| no router evals | routing policy is guesswork | evaluate route decisions by slice |
| hidden quality degradation | users get worse output unknowingly | define product-tier promises |
| no fallback compatibility tests | backup model breaks schema/prompt | test fallback tiers |
| trusting model confidence blindly | confidence may be miscalibrated | calibrate against outcomes |
| routing ignores latency budget | strong path may miss UX target | include deadline-aware routing |
| routing ignores safety | budget pressure may skip controls | preserve required validation |

---

### 23. Practical Interview Question [Intermediate]

> Your GenAI assistant handles a mix of simple FAQ questions, complex document questions, and high-risk customer-facing workflows. How would you design model routing, fallback tiers, and dynamic quality tiers?

---

### 24. Strong Answer [Pro]

I would not use one model path for every request. I would first define request slices: simple deterministic or cached cases, easy low-risk model cases, normal RAG questions, ambiguous or long-context questions, tool-required workflows, and high-risk customer-facing actions. Each slice should have a different quality budget.

For simple cases, I would use deterministic logic, cache, or a small fast model. For standard cases, I would use a balanced model with normal retrieval. For ambiguous or high-risk cases, I would route to a stronger model, deeper retrieval, reranking, and stricter validation. For external actions or irreversible outcomes, I would require human approval or deterministic enforcement.

Fallbacks should cover both availability and quality. If the primary model times out or is rate-limited, the system can use a compatible backup model, cached response, partial answer, or async path. If validation fails, citations are unsupported, schema is invalid, or retrieval confidence is low, the system should escalate to stronger generation, deeper retrieval, clarification, or human review. Fallbacks must be bounded by cost, latency, and retry limits.

The router should use signals such as task type, risk, user/product tier, retrieval confidence, context size, tool requirement, latency budget, cost budget, and previous validation failures. I would calibrate thresholds with evals rather than trusting model self-confidence. I would monitor route distribution, under-routing failures, over-routing waste, fallback rates, cost per successful task, p95 latency, and quality by slice.

The goal is dynamic quality: spend more only where it improves product outcomes or reduces risk. Easy requests should be cheap and fast. Hard or risky requests should receive stronger paths. No tier should bypass safety or required validation.

---

### 25. Active Recall [Beginner]

Answer these without looking:

1. What is model routing?
2. What is a fallback tier?
3. What is a dynamic quality tier?
4. Why is one model for everything inefficient?
5. What is cheap-first routing?
6. When can cheap-first be worse?
7. What is strong-first routing?
8. Name five routing signals.
9. What is under-routing?
10. What is over-routing?
11. What is quality fallback?
12. What is availability fallback?
13. Why should fallback tiers be evaluated?
14. What is confidence thresholding?
15. Why should model confidence be calibrated?
16. What should budget-aware routing preserve even under pressure?
17. How can product tiers affect routing?
18. What route observability fields matter?
19. What is the biggest router failure mode in high-risk systems?
20. What is the final lesson of this topic?

Expected answers:

1. Choosing model/workflow path based on task signals.
2. A backup or alternate path used after failure, timeout, or low quality.
3. Runtime adjustment of model strength, retrieval depth, validation, and review.
4. Easy tasks are over-served or hard tasks are under-served.
5. Trying cheap path first, then escalating on uncertainty.
6. When many cases escalate, causing two calls and more latency/cost.
7. Using stronger path immediately for high-risk or hard tasks.
8. Task type, risk, context size, retrieval confidence, user tier, latency budget.
9. Sending a hard/risky task to too weak a path.
10. Sending an easy task to too expensive a path.
11. Escalation when output fails validation or confidence checks.
12. Backup when provider/model/tool is unavailable or slow.
13. Backup models/workflows may differ in quality, schema, or safety.
14. Accepting/escalating based on confidence and risk thresholds.
15. Self-reported confidence may not match real correctness.
16. Required safety and compliance validation.
17. Paid tiers may receive deeper, faster, or more auditable paths.
18. Chosen route, router version, signals, fallback reason, cost, latency, outcome.
19. Risk misclassification causing unsafe under-routing.
20. Spend stronger model quality only where difficulty, risk, or product value justifies it.

---

### 26. Revision Notes

- **One-line summary:** Model routing matches task difficulty, risk, value, and budgets to the right model/workflow tier, with bounded fallbacks for failures and low confidence.
- **Three keywords:** route, escalate, fallback.
- **One interview trap:** Treating fallback as only an outage plan instead of also handling low-quality, invalid, unsupported, or risky outputs.
- **One memory trick:** Easy gets fast lane, hard gets specialist, risky gets approval.

Final takeaway:

> Dynamic quality is how GenAI systems stay economical without becoming careless: route easy work cheaply, escalate hard work intelligently, and fallback safely when quality, latency, or availability breaks.

---

## Subtopic 20.3.c: Retrieval Cost vs Generation Cost vs Engineering Cost

> **Subtopic time:** 2h
> Outcome: You should be able to compare the visible cost of model generation with the less obvious costs of retrieval infrastructure, ingestion, indexing, reranking, evaluation, observability, security, and engineering maintenance. You should reason in total cost of ownership, not just model token spend.

### Add to Knowledge Base

Many GenAI cost discussions start with:

```text
How much does the model call cost?
```

That is important.

But it is incomplete.

A serious GenAI system may also pay for:

```text
document ingestion
parsing
chunking
embedding
vector storage
index refresh
metadata filtering
reranking
retrieval evaluation
source synchronization
permissions
observability
guardrails
human review
security review
engineering maintenance
incident response
```

The model bill is often the visible part.

The system cost is the full machine.

The core mental model:

> Generation cost is the meter you see. Retrieval cost is the evidence supply chain. Engineering cost is the cost of keeping the whole thing correct, safe, and operable.

If you ignore retrieval and engineering cost, you will underprice the product and overestimate the ROI.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-7 to understand the three major cost buckets.
- **Intermediate:** Read sections 8-17 to reason about fixed vs variable cost, online vs offline cost, and total cost of ownership.
- **Pro:** Complete the TCO lab and practice the interview answer so you can defend architecture economics in product and design reviews.

---

### 0. Pre-Question Hook [Beginner]

A team builds a RAG assistant.

The model generation cost is:

```text
$0.02 per answer
```

The team says:

```text
Great, every answer costs only two cents.
```

But monthly costs include:

```text
embedding new documents
re-embedding changed documents
vector database storage
reranker calls
document parsing failures
index maintenance
eval runs
trace storage
engineers maintaining the ingestion pipeline
on-call time for search incidents
```

After allocation, the real cost is:

```text
$0.09 per successful grounded answer
```

The model call was not wrong.

It was just not the full cost.

That is the point of this topic.

---

### 1. The Intuition [Beginner]

Think of a restaurant again.

The price of cooking one dish is not only:

```text
gas used by the stove
```

It also includes:

```text
ingredients
storage
prep work
kitchen staff
cleaning
equipment
rent
quality checks
waste
management
```

In GenAI:

```text
generation = cooking the dish
retrieval = sourcing and preparing ingredients
engineering = running the kitchen
```

If you only price the stove flame, your restaurant goes broke.

If you only price model generation, your GenAI product economics are incomplete.

---

### 2. Definition [Beginner]

- **Retrieval cost:** The cost of ingesting, embedding, storing, indexing, searching, filtering, reranking, refreshing, and evaluating evidence.
- **Generation cost:** The cost of model calls that produce or transform user-facing output, including input tokens, output tokens, repair calls, and validators.
- **Engineering cost:** The human and infrastructure cost of building, maintaining, debugging, securing, evaluating, and operating the GenAI system.
- **Total cost of ownership:** The full cost to build and run the system over time, including online runtime, offline processing, infrastructure, labor, quality, security, and incidents.
- **Core idea:** Optimize the product's total cost per successful outcome, not one visible API line item.

Short version:

```text
retrieval finds evidence
generation creates output
engineering keeps the system alive
```

---

### 3. Why This Distinction Exists [Beginner]

GenAI systems are layered.

The user sees:

```text
answer
```

The system may run:

```text
load tenant config
check permissions
rewrite query
embed query
search indexes
hydrate chunks
filter metadata
rerank candidates
pack context
generate answer
validate citations
repair unsupported claims
log traces
update memory
run eval sampling
```

Some costs happen online:

```text
per user request
```

Some happen offline:

```text
before the user asks anything
```

Some happen through engineering effort:

```text
when the system breaks, drifts, needs new data, or enters a new domain
```

Without separating these categories, you cannot answer:

- Is RAG actually cheaper than long-context generation?
- Is reranking worth it?
- Should we buy a managed vector database or operate our own?
- Should we use a larger model instead of complex retrieval?
- Is the product profitable at expected usage volume?
- Does this system need one engineer or a team to maintain?

Strong statement:

> Runtime cost tells you what the system spends. Engineering cost tells you what the organization spends.

---

### 4. The Three Cost Buckets [Beginner]

| Bucket | What It Includes | Common Blind Spot |
|---|---|---|
| retrieval cost | embeddings, vector DB, indexing, filtering, reranking, refresh | offline and infra costs ignored |
| generation cost | answer model, validators, repair, output tokens | repeated calls and failed attempts ignored |
| engineering cost | build, maintenance, evals, monitoring, security, incidents | human ownership treated as free |

All three affect:

```text
cost per request
cost per session
cost per successful task
```

Example:

```text
generation cost per answer = $0.02
retrieval amortized cost per answer = $0.015
reranking cost per answer = $0.006
eval/observability allocation = $0.004
engineering allocation = $0.025
```

True allocated cost:

```text
$0.070 per answer
```

If success rate is 80%:

```text
cost per successful answer = 0.070 / 0.80 = $0.0875
```

That is the product number.

---

### 5. Retrieval Cost Breakdown [Intermediate]

Retrieval cost includes more than vector search.

#### Ingestion

```text
connectors
crawlers
document parsing
OCR
table extraction
HTML/PDF cleanup
deduplication
chunking
metadata extraction
permission mapping
```

#### Embedding

```text
embedding tokens
batch jobs
retry failed documents
embedding model versioning
re-embedding changed content
multi-embedding strategies
```

#### Storage And Indexing

```text
vector storage
metadata storage
raw text storage
index build
index compaction
replication
backups
tenant isolation
```

#### Online Retrieval

```text
query embedding
vector search
sparse search
hybrid fusion
metadata filters
permission filters
chunk hydration
network latency
```

#### Quality Layer

```text
reranking
query rewriting
result deduplication
context packing
retrieval evaluation
gold set maintenance
```

Retrieval can be cheap per query but expensive to keep correct.

---

### 6. Generation Cost Breakdown [Intermediate]

Generation cost includes every model call used to produce or verify output.

Common generation-related calls:

```text
router/classifier call
query rewrite call
answer generation call
tool-use planning call
tool-result interpretation call
structured extraction call
repair call
citation validation call
safety classifier call
quality judge call
summary memory update call
```

Main drivers:

```text
input tokens
output tokens
model tier
number of calls
retry rate
repair rate
validator rate
fallback rate
cache hit rate
```

Generation cost is often easiest to see because providers report usage.

But the visible bill can mislead.

Example:

```text
answer generation = $0.018
repair call happens 30% of the time at $0.010
citation validator always runs at $0.004
```

Expected generation-side cost:

```text
0.018 + 0.30 * 0.010 + 0.004 = $0.025
```

The answer model call was not the full generation path.

---

### 7. Engineering Cost Breakdown [Intermediate]

Engineering cost is the cost teams often undercount.

It includes:

```text
architecture design
prompt/version management
retrieval tuning
connector maintenance
schema changes
evaluation set creation
test automation
observability dashboards
security and privacy review
data governance
incident response
on-call support
regression investigation
cost monitoring
model upgrade work
vendor migration work
documentation
support enablement
```

Engineering cost is especially high when:

- the domain changes frequently
- documents are messy
- permissions are complex
- correctness must be audited
- many tenants need customization
- workflows involve tools and approvals
- evals require expert labels
- failures are expensive
- data pipelines are brittle

Strong sentence:

> A cheap model path that requires constant engineering babysitting may be more expensive than a simpler architecture with higher runtime cost.

---

### 8. Online vs Offline Cost [Intermediate]

Separate online and offline cost.

Online costs happen per request:

```text
query embedding
retrieval
reranking
answer generation
tool calls
validators
logging
```

Offline costs happen outside the request path:

```text
document ingestion
embedding corpus
index building
batch summarization
eval generation
cache warming
monitoring jobs
re-embedding migrations
```

Why this matters:

```text
online cost affects marginal cost and latency
offline cost affects fixed cost and average cost
```

Example:

```text
monthly offline indexing cost = $5,000
online cost per answer = $0.025
```

At 50,000 answers/month:

```text
average cost = 5000 / 50000 + 0.025 = $0.125
```

At 1,000,000 answers/month:

```text
average cost = 5000 / 1000000 + 0.025 = $0.030
```

Same system.

Very different economics.

---

### 9. Fixed vs Variable Cost [Intermediate]

Fixed costs do not grow directly with each request.

Examples:

```text
engineering team
base vector database cluster
evaluation infrastructure
security review
monitoring dashboards
minimum provider commitments
```

Variable costs grow with usage.

Examples:

```text
model tokens
query embeddings
reranker calls
tool API calls
storage growth
human review per case
```

Why it matters:

```text
High fixed cost systems need enough usage volume to be economical.
High variable cost systems may look easy to start but become expensive at scale.
```

RAG often has:

```text
moderate/high fixed setup cost
lower marginal evidence reuse if traffic is high
```

Pure long-context generation often has:

```text
lower retrieval infrastructure cost
higher per-request token cost
```

The right choice depends on volume and evidence reuse.

---

### 10. Marginal vs Average Cost [Pro]

Average cost:

```text
total cost / total requests or successes
```

Marginal cost:

```text
extra cost of serving one more request
```

Example:

```text
engineering + infra fixed cost = $30,000/month
variable cost per successful answer = $0.04
monthly successful answers = 100,000
```

Average cost:

```text
30000 / 100000 + 0.04 = $0.34
```

Marginal cost:

```text
$0.04
```

Both matter.

Use average cost for:

```text
pricing
profitability
business viability
team planning
```

Use marginal cost for:

```text
usage limits
incremental traffic
per-request routing
serving one more query
```

Interview sentence:

> I would separate average cost for product viability from marginal cost for runtime routing decisions.

---

### 11. Retrieval vs Larger Generation Trade-Off [Pro]

Sometimes teams choose between:

```text
complex retrieval pipeline
```

and:

```text
larger context generation with simpler retrieval
```

Retrieval-heavy design:

Pros:

- smaller final prompts
- potentially lower generation cost
- better citation control
- reusable indexes
- source-level filtering
- tenant and permission controls

Cons:

- ingestion pipeline
- vector DB operations
- chunking complexity
- retrieval evals
- reindexing
- stale data risks
- engineering maintenance

Generation-heavy design:

Pros:

- simpler early architecture
- less index tuning
- fewer retrieval components
- good for small corpora or one-off documents

Cons:

- higher input token cost
- slower TTFT
- context-window pressure
- distractor risk
- less reusable evidence pipeline

Decision:

```text
If evidence is reused many times, retrieval investment can pay off.
If each task has unique small context, larger-generation path may be simpler.
```

---

### 12. Reranking Cost vs Generation Cost [Intermediate]

Reranking can add cost but reduce generation waste.

Example:

Without reranking:

```text
send 15 chunks to generation
final context tokens = 12,000
answer quality = 82%
```

With reranking:

```text
rerank 60 candidates
send 6 chunks to generation
final context tokens = 4,800
answer quality = 89%
```

Reranking adds:

```text
reranker latency
reranker cost
another model/component to maintain
```

But may reduce:

```text
generation input tokens
TTFT
unsupported answers
follow-up turns
human review
```

Decision metric:

```text
reranker ROI =
    avoided generation cost
  + avoided failure cost
  + avoided human review cost
  - reranker cost
```

Reranking is not free.

But neither is sending noisy context to the generator.

---

### 13. Engineering Cost vs Runtime Cost [Pro]

Sometimes runtime cost is higher but engineering cost is lower.

Example A:

```text
complex custom retrieval stack
runtime cost: low
engineering cost: high
```

Example B:

```text
managed search + larger model
runtime cost: higher
engineering cost: lower
```

The better choice depends on:

- team size
- expertise
- uptime needs
- expected volume
- time to market
- compliance requirements
- customization needs
- portability needs
- long-term scale

Startup prototype:

```text
choose simpler managed architecture
```

High-volume enterprise product:

```text
invest in optimized retrieval and routing
```

Compliance-heavy domain:

```text
invest in auditability, evals, and deterministic controls
```

Strong sentence:

> Architecture cost is not only what the cloud bill says. It is also how many engineers must understand and operate the system safely.

---

### 14. Buy vs Build Reasoning [Intermediate]

Buy or use managed services when:

- team is small
- time to market matters
- workload is uncertain
- standard features are enough
- operations burden would distract the team
- vendor reliability is acceptable

Build or self-operate when:

- scale makes managed cost too high
- customization is critical
- data governance requires control
- latency requirements are strict
- vendor lock-in is unacceptable
- internal platform team exists

For vector databases, retrieval services, eval platforms, observability, and guardrail systems, ask:

```text
What do we save in engineering time?
What do we lose in control?
What happens at 10x volume?
What happens if we need to migrate?
What is the operational failure mode?
```

Buy-vs-build is a cost-quality-product decision, not a taste question.

---

### 15. Cost Allocation By Product Feature [Pro]

Shared infrastructure makes cost allocation tricky.

Example shared components:

```text
embedding pipeline
vector database
evaluation platform
trace storage
security review
on-call rotation
```

Allocate costs by:

```text
request volume
token usage
storage usage
tenant count
index size
feature revenue
engineering ownership
support burden
```

Feature-level questions:

- Which feature drives most retrieval traffic?
- Which feature requires most human review?
- Which feature causes most incidents?
- Which feature needs the largest index?
- Which feature has the highest cost per successful task?
- Which feature creates enough revenue/value to justify its cost?

Without allocation, one expensive feature can hide inside platform cost.

---

### 16. Total Cost Of Ownership Formula [Pro]

A practical monthly TCO formula:

```text
monthly_TCO =
    generation_runtime_cost
  + retrieval_runtime_cost
  + offline_ingestion_cost
  + vector_database_cost
  + storage_cost
  + observability_cost
  + evaluation_cost
  + guardrail_cost
  + human_review_cost
  + engineering_labor_cost
  + incident_cost
  + vendor_platform_cost
```

Cost per successful task:

```text
cost_per_success =
    monthly_TCO / successful_tasks
```

Quality-adjusted cost:

```text
cost_per_grounded_success =
    monthly_TCO / grounded_successful_tasks
```

Product viability:

```text
value_per_success
>
cost_per_grounded_success + required_margin
```

This is the business reality.

---

### 17. Decision Matrix [Intermediate]

| Observation | Interpretation | Action |
|---|---|---|
| generation dominates variable cost | prompts/context/output too large | trim, route, cache, compress, smaller model |
| retrieval infra dominates fixed cost | volume may be too low | simplify, managed service, consolidate indexes |
| reranking cost high but success improves | maybe justified | compare cost per successful task |
| engineering maintenance dominates | architecture too complex | simplify, automate, use managed components |
| human review dominates | model/retrieval failures costly | improve quality or route earlier |
| offline ingestion dominates | corpus changes too often | incremental indexing, versioning, refresh policy |
| vector DB storage dominates | too many embeddings/tenants | pruning, compression, tiered storage |
| eval cost ignored | quality risk hidden | budget evals as production cost |
| cost high but value higher | product may be viable | optimize but do not blindly cut |
| cost low but failures high | false economy | improve quality or reduce automation |

One-line rule:

```text
Optimize the biggest cost bucket only after checking that it is not buying essential quality or safety.
```

---

### 18. Cost Trace Schema [Pro]

```json
{
  "month": "2026-06",
  "feature": "enterprise_rag_assistant",
  "usage": {
    "sessions": 120000,
    "successful_tasks": 84000,
    "grounded_successful_tasks": 76000
  },
  "runtime_costs": {
    "generation": 4200.0,
    "query_embedding": 380.0,
    "reranking": 910.0,
    "tool_calls": 600.0,
    "guardrails": 740.0
  },
  "retrieval_infra_costs": {
    "offline_embedding": 1800.0,
    "vector_database": 3200.0,
    "storage": 900.0,
    "index_refresh": 700.0
  },
  "operational_costs": {
    "observability": 650.0,
    "evaluation": 1200.0,
    "human_review": 4800.0,
    "engineering_labor_allocated": 18000.0,
    "incident_cost_allocated": 1500.0
  },
  "quality": {
    "task_success_rate": 0.70,
    "grounded_success_rate": 0.63,
    "human_escalation_rate": 0.08
  }
}
```

This lets you compute:

```text
runtime cost per session
TCO per session
TCO per successful task
TCO per grounded successful task
```

It also prevents the model bill from being treated as the whole product cost.

---

### 19. Code Sample: TCO Calculator

```python
def total_cost(costs):
    total = 0.0

    for category in costs.values():
        if isinstance(category, dict):
            total += sum(category.values())
        else:
            total += category

    return total


def cost_summary(costs, sessions, successful_tasks, grounded_successful_tasks):
    tco = total_cost(costs)

    return {
        "monthly_tco": tco,
        "cost_per_session": tco / sessions if sessions else None,
        "cost_per_success": tco / successful_tasks if successful_tasks else None,
        "cost_per_grounded_success": (
            tco / grounded_successful_tasks if grounded_successful_tasks else None
        ),
    }


costs = {
    "runtime": {
        "generation": 4200,
        "query_embedding": 380,
        "reranking": 910,
        "guardrails": 740,
    },
    "retrieval_infra": {
        "offline_embedding": 1800,
        "vector_database": 3200,
        "storage": 900,
        "index_refresh": 700,
    },
    "operations": {
        "observability": 650,
        "evaluation": 1200,
        "human_review": 4800,
        "engineering_labor_allocated": 18000,
    },
}

summary = cost_summary(
    costs=costs,
    sessions=120000,
    successful_tasks=84000,
    grounded_successful_tasks=76000,
)

print(summary)
```

Expected lesson:

```text
The true product cost includes runtime, retrieval infrastructure, operations, human review, and engineering allocation.
```

---

### 20. Mini Program: Architecture Cost Simulator

This simulator compares two RAG architecture choices.

```python
def monthly_cost(config):
    fixed = config["fixed_engineering"] + config["fixed_infra"]
    variable = config["requests"] * config["variable_cost_per_request"]
    human = config["requests"] * config["human_review_rate"] * config["human_review_cost"]
    failure = config["requests"] * config["failure_rate"] * config["failure_cost"]

    return fixed + variable + human + failure


def cost_per_success(config):
    successes = config["requests"] * config["success_rate"]
    return monthly_cost(config) / successes if successes else None


def main():
    architectures = {
        "simple_large_context": {
            "requests": 100000,
            "fixed_engineering": 8000,
            "fixed_infra": 2000,
            "variable_cost_per_request": 0.080,
            "human_review_rate": 0.06,
            "human_review_cost": 1.50,
            "failure_rate": 0.05,
            "failure_cost": 2.00,
            "success_rate": 0.84,
        },
        "optimized_retrieval_routing": {
            "requests": 100000,
            "fixed_engineering": 22000,
            "fixed_infra": 7000,
            "variable_cost_per_request": 0.030,
            "human_review_rate": 0.03,
            "human_review_cost": 1.50,
            "failure_rate": 0.03,
            "failure_cost": 2.00,
            "success_rate": 0.90,
        },
    }

    for name, config in architectures.items():
        print(name)
        print("  monthly_cost:", round(monthly_cost(config), 2))
        print("  cost_per_success:", round(cost_per_success(config), 4))


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
The architecture with higher fixed engineering cost may win at scale if it lowers variable cost and failures enough.
```

But at lower volume, the simpler architecture may be better.

---

### 21. Hands-On Lab: Total Cost Of Ownership Review [Pro]

#### Build

Choose one system:

```text
support RAG assistant
document AI extractor
research agent
contract review assistant
coding assistant
customer support workflow agent
```

List monthly costs:

```text
generation model calls
query embeddings
reranking
tool calls
guardrails/evaluators
offline document embeddings
vector database
metadata/document storage
index refresh
observability and tracing
evaluation runs
human review
engineering labor
security/compliance review
incident response
```

#### Allocate

Allocate shared costs by:

```text
request volume
storage volume
tenant count
index size
engineering ownership
human review volume
feature revenue
```

#### Compare

Compare two architectures:

1. Simpler architecture with higher generation/runtime cost.
2. More optimized architecture with higher retrieval/engineering cost.

For each:

```text
monthly TCO
cost per session
cost per successful task
cost per grounded successful task
p95 latency
quality/safety metrics
engineering maintenance risk
time to market
```

#### Decide

Write:

```text
The dominant cost bucket is <bucket>.
The current bottleneck is <runtime/retrieval/engineering/human review>.
I would optimize <area> first because <reason>.
I would not optimize <area> yet because it buys <quality/safety/value>.
```

---

### 22. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| counting only generation tokens | ignores retrieval and operations | calculate full TCO |
| ignoring engineering labor | system looks falsely cheap | allocate ownership and maintenance |
| ignoring offline ingestion | RAG cost understated | amortize indexing and embedding |
| comparing architectures at one volume only | fixed/variable trade-off hidden | model multiple volume scenarios |
| treating managed service cost as waste | may save engineering time | compare buy vs build total cost |
| optimizing biggest cost blindly | may harm quality/safety | measure cost per successful task |
| ignoring human review | often dominates product cost | include expected review cost |
| no feature-level allocation | expensive features hide in platform cost | allocate shared costs |
| no incident cost | reliability burden invisible | include on-call and incident impact |
| ignoring eval cost | quality governance unfunded | treat evals as production cost |

---

### 23. Practical Interview Question [Intermediate]

> Your RAG product's model bill looks acceptable, but leadership says the product is still too expensive to operate. How would you compare retrieval cost, generation cost, and engineering cost?

---

### 24. Strong Answer [Pro]

I would start by separating the cost buckets. Generation cost includes the answer model, query rewriting, validators, repair calls, guardrails, and any model calls on the request path. Retrieval cost includes ingestion, parsing, chunking, embeddings, vector storage, metadata storage, index refresh, query embedding, search, reranking, and retrieval evaluation. Engineering cost includes building and maintaining connectors, evals, observability, security controls, prompt and model versions, incident response, and on-call ownership.

Then I would split costs into online and offline, fixed and variable. Online generation and reranking affect marginal cost and latency. Offline ingestion, vector database clusters, eval infrastructure, and engineering teams affect average cost and product viability. At low volume, fixed retrieval and engineering costs can dominate. At high volume, optimized retrieval may pay for itself by reducing generation tokens, failures, and human review.

I would compute monthly total cost of ownership and divide it by sessions, successful tasks, and grounded successful tasks. I would include human review and failure costs because a cheap runtime path that causes more escalations is not actually cheap. I would also allocate shared platform costs to features so expensive workflows do not hide inside infrastructure.

The decision is not always to cut the largest line item. If reranking or evaluation cost improves grounded success and reduces human review, it may be worth keeping. If engineering maintenance dominates, I might simplify the architecture or use managed services even if runtime cost rises. If generation tokens dominate, I would optimize context packing, model routing, caching, and output length.

The final recommendation should compare architectures by TCO, cost per successful task, latency, quality, safety, time to market, and maintenance burden. A senior answer treats the model bill as one component of product economics, not the whole story.

---

### 25. Active Recall [Beginner]

Answer these without looking:

1. What are the three main cost buckets in this topic?
2. What is retrieval cost?
3. What is generation cost?
4. What is engineering cost?
5. Why is model bill alone incomplete?
6. What is online cost?
7. What is offline cost?
8. What is fixed cost?
9. What is variable cost?
10. What is marginal cost?
11. What is average cost?
12. Why can RAG be expensive before users ask questions?
13. Why can engineering cost dominate?
14. When might a managed service be cheaper overall?
15. When might building custom infrastructure be justified?
16. Why include human review in TCO?
17. Why include evaluation in production cost?
18. What is cost per grounded successful task?
19. Why allocate shared costs by feature?
20. What is the final lesson of this topic?

Expected answers:

1. Retrieval, generation, and engineering.
2. Ingestion, embedding, storage, indexing, search, filtering, reranking, refresh.
3. Model calls that generate, transform, validate, or repair outputs.
4. Human and operational cost to build, maintain, secure, debug, and evaluate.
5. It ignores evidence supply chain and ownership cost.
6. Cost incurred on the request path.
7. Cost incurred outside the request path, like indexing.
8. Cost that does not scale directly per request.
9. Cost that grows with usage.
10. Extra cost of serving one more request.
11. Total cost divided by total volume.
12. Documents must be parsed, embedded, indexed, and refreshed.
13. Complex systems require ongoing ownership and incident response.
14. When it saves more engineering effort than it adds in vendor cost.
15. At scale, with strict customization, governance, or latency needs.
16. Failed or uncertain cases often require humans and real money.
17. Quality governance is necessary to operate safely.
18. TCO divided by correct, grounded successful outcomes.
19. To see which product features are truly expensive or profitable.
20. Optimize total cost per successful outcome, not the most visible line item.

---

### 26. Revision Notes

- **One-line summary:** Retrieval cost, generation cost, and engineering cost must be combined into total cost of ownership before making product decisions.
- **Three keywords:** retrieval, generation, ownership.
- **One interview trap:** Saying the product is cheap because the answer model call is cheap while ignoring ingestion, vector storage, reranking, evals, human review, and engineering maintenance.
- **One memory trick:** Generation is the answer, retrieval is the evidence supply chain, engineering is the operating cost.

Final takeaway:

> The real economics of GenAI live in total cost of ownership: model calls matter, but retrieval infrastructure and engineering ownership often decide whether the product is actually affordable.

---

## Subtopic 20.3.d: ROI Framing for Product, Platform, and Enterprise Systems

> **Subtopic time:** 2h
> Outcome: You should be able to explain GenAI return on investment differently for customer-facing products, internal platforms, and enterprise systems. You should connect cost, quality, adoption, risk, and business value into a decision framework that leaders can actually use.

### Add to Knowledge Base

ROI is not just:

```text
Did the model cost less than the human?
```

That is one case, but not the whole picture.

GenAI ROI can come from:

```text
new revenue
higher conversion
better retention
faster task completion
lower support cost
lower manual review cost
reduced risk
developer productivity
platform reuse
better quality
faster decision cycles
```

But GenAI also creates costs:

```text
model usage
retrieval infrastructure
engineering ownership
security review
evaluation
human review
change management
training
incident response
vendor risk
quality failures
```

The core mental model:

> ROI is value minus total cost, but "value" means different things for products, platforms, and enterprises.

A product team asks:

```text
Does this improve customer behavior enough to justify cost?
```

A platform team asks:

```text
Does this shared capability reduce duplicated effort and improve delivery across teams?
```

An enterprise asks:

```text
Does this change business operations safely at meaningful scale?
```

Same technology.

Different ROI language.

---

### Reading Path + Level Tags

- **Beginner:** Read sections 0-6 to understand ROI basics and the three framing lenses.
- **Intermediate:** Read sections 7-16 to learn metrics, attribution, payback, risk, and pilot design.
- **Pro:** Complete the ROI lab and practice the interview answer so you can speak to product, platform, and executive audiences.

---

### 0. Pre-Question Hook [Beginner]

Three teams propose a GenAI assistant.

Product team:

```text
It will help customers answer product questions and upgrade plans.
```

Platform team:

```text
It will provide reusable retrieval, evaluation, and model-routing infrastructure for ten teams.
```

Enterprise operations team:

```text
It will reduce manual invoice review across 8,000 employees.
```

Should ROI be measured the same way?

No.

Product ROI might focus on:

```text
conversion, retention, support deflection, revenue per user
```

Platform ROI might focus on:

```text
reuse, developer velocity, reduced duplicate systems, standard governance
```

Enterprise ROI might focus on:

```text
labor hours saved, cycle time, compliance risk, adoption, process change
```

If you use the wrong ROI frame, you can reject a valuable project or approve a bad one.

---

### 1. The Intuition [Beginner]

Think of buying a vehicle.

A delivery company buys a truck for:

```text
more deliveries per day
```

A city buys a bus for:

```text
shared transport capacity
```

A family buys a car for:

```text
convenience and daily mobility
```

Same category: vehicle.

Different ROI.

GenAI is the same.

A customer-facing product, an internal platform, and an enterprise workflow may all use models, retrieval, tools, and guardrails.

But the business case is different.

Good ROI framing starts by asking:

```text
Who receives the value?
How is that value measured?
What cost and risk did we add?
How will we know it worked?
```

---

### 2. Definition [Beginner]

- **ROI:** Return on investment, usually measured as net value gained relative to total investment.
- **Product ROI:** Value from customer-facing outcomes such as revenue, conversion, retention, usage, satisfaction, and support deflection.
- **Platform ROI:** Value from shared capabilities that reduce repeated engineering work, improve governance, and accelerate multiple product teams.
- **Enterprise ROI:** Value from operational transformation across business processes, such as labor savings, cycle-time reduction, risk reduction, and standardization.
- **Core idea:** ROI is not one metric. It is a framing discipline that connects GenAI system outcomes to business value.

Basic formula:

```text
ROI = (value_created - total_cost) / total_cost
```

But the hard part is:

```text
defining value_created honestly
```

---

### 3. Why ROI Framing Exists [Beginner]

GenAI projects can look impressive in demos and weak in production.

Common failure pattern:

```text
demo works
stakeholders get excited
pilot launches
costs grow
quality issues appear
adoption is lower than expected
workflow does not change
ROI is unclear
```

ROI framing prevents that.

It forces the team to define:

```text
business outcome
baseline
expected lift
total cost
risk
measurement plan
owner
time horizon
go/no-go threshold
```

Strong statement:

> A GenAI project without a measurable value hypothesis is an experiment, not an investment.

Experiments are fine.

But call them experiments and define what would make them graduate.

---

### 4. Product ROI [Intermediate]

Product ROI applies to customer-facing features.

Value sources:

```text
new revenue
upgrade conversion
activation
retention
engagement
support deflection
lower churn
higher customer satisfaction
faster onboarding
premium feature differentiation
```

Example product feature:

```text
AI support assistant inside SaaS dashboard
```

Possible ROI metrics:

```text
percent of questions resolved without support ticket
conversion from free to paid
reduction in time to first value
customer satisfaction score
retention improvement
support tickets avoided
cost per resolved question
```

Product ROI formula:

```text
net_product_value =
    incremental_revenue
  + avoided_support_cost
  + retention_value
  - GenAI_total_cost
  - failure_cost
```

Important:

```text
usage alone is not ROI
```

Users may try a feature because it is novel.

ROI requires behavior or economics to improve.

---

### 5. Platform ROI [Intermediate]

Platform ROI applies to shared infrastructure used by many teams.

Value sources:

```text
faster product delivery
less duplicate engineering
standardized security
standardized evaluation
shared model routing
shared retrieval infrastructure
central observability
lower vendor integration burden
better governance
reusable components
```

Example platform:

```text
internal GenAI platform with model gateway, prompt registry, retrieval service, eval harness, tracing, and policy controls
```

Platform ROI metrics:

```text
number of teams onboarded
time saved per team
duplicate systems retired
integration time reduced
eval coverage improved
incidents reduced
cost visibility improved
security review time reduced
model migration time reduced
```

Platform ROI formula:

```text
net_platform_value =
    engineering_time_saved_across_teams
  + avoided_duplicate_vendor_cost
  + reduced_incident_cost
  + faster_launch_value
  - platform_build_and_run_cost
```

Platform ROI is often indirect.

The platform may not create revenue by itself.

It creates leverage.

Strong sentence:

> A platform is justified when shared leverage is cheaper and safer than every team rebuilding the same capabilities.

---

### 6. Enterprise ROI [Intermediate]

Enterprise ROI applies to large operational workflows.

Value sources:

```text
labor savings
cycle-time reduction
fewer manual errors
better compliance
faster audits
lower training burden
standardized workflows
improved employee productivity
fewer escalations
better decision support
```

Example enterprise system:

```text
invoice review assistant for finance operations
```

Enterprise ROI metrics:

```text
minutes saved per invoice
percentage auto-reviewed
manual review rate
exception handling time
error rate
audit pass rate
cycle time from receipt to approval
employee adoption
process compliance
```

Enterprise ROI formula:

```text
net_enterprise_value =
    labor_hours_saved * fully_loaded_hourly_cost
  + error_cost_avoided
  + cycle_time_value
  + risk_reduction_value
  - total_system_cost
  - change_management_cost
```

Enterprise ROI depends heavily on adoption.

If employees do not change the workflow, the model does not create value.

---

### 7. Baseline And Counterfactual [Pro]

ROI requires a baseline.

Bad claim:

```text
The assistant handled 10,000 questions.
```

Better claim:

```text
The assistant resolved 6,200 questions that previously became support tickets,
reducing ticket volume by 18% at equal or better CSAT.
```

You need a counterfactual:

```text
What would have happened without the GenAI system?
```

Baseline examples:

```text
current support ticket volume
average handling time
manual review cost
conversion rate
churn rate
engineering integration time
incident rate
document processing time
```

Measurement patterns:

- A/B test
- phased rollout
- pre/post comparison with controls
- matched cohorts
- shadow mode
- human baseline comparison
- team productivity benchmark

Without baseline, ROI becomes storytelling.

---

### 8. Leading vs Lagging Metrics [Intermediate]

Lagging metrics show final business value.

Examples:

```text
revenue
retention
cost reduction
ticket volume reduction
cycle-time reduction
```

Leading metrics predict whether ROI might happen.

Examples:

```text
adoption rate
task completion rate
answer acceptance
grounded answer rate
latency
human escalation rate
retry rate
user trust rating
```

Leading metrics are useful during pilots.

Lagging metrics are needed for investment decisions.

Example:

```text
Pilot leading metric:
  72% of users accept AI answer

Business lagging metric:
  support cost per account drops 14%
```

Do not stop at leading metrics.

But do not wait months for lagging metrics before debugging the system.

Use both.

---

### 9. ROI Time Horizon And Payback [Intermediate]

ROI depends on time.

Payback period:

```text
payback_period = upfront_investment / monthly_net_benefit
```

Example:

```text
upfront build cost = $300,000
monthly net benefit = $50,000
payback period = 6 months
```

Short payback is attractive when:

```text
market is uncertain
budget is tight
technology changes fast
```

Longer payback may be acceptable when:

```text
platform leverage is large
enterprise transformation is strategic
compliance value is high
competitive advantage is durable
```

Always define:

```text
pilot horizon
production ROI horizon
scale horizon
```

These are often different.

---

### 10. Adoption And Change-Management Cost [Pro]

GenAI value does not appear automatically when the feature ships.

Adoption costs include:

```text
training users
changing workflow
updating SOPs
supporting rollout
handling distrust
collecting feedback
redesigning UX
manager enablement
governance review
```

Adoption risk:

```text
users do not trust it
users do not know when to use it
managers still require old process
outputs do not fit workflow
quality is good but UX is awkward
```

Enterprise GenAI often fails here.

The model may be good, but the workflow stays unchanged.

ROI question:

```text
What operational behavior must change for value to appear?
```

If the answer is unclear, ROI is fragile.

---

### 11. Risk Reduction ROI [Pro]

Not all ROI is revenue or labor savings.

Some ROI comes from reducing expected loss.

Examples:

```text
fewer compliance violations
fewer incorrect customer answers
fewer manual data-entry errors
fewer missed policy exceptions
faster incident triage
better audit evidence
```

Expected risk value:

```text
expected_loss_reduction =
    baseline_incident_probability * baseline_incident_cost
  - new_incident_probability * new_incident_cost
```

Example:

```text
old expected annual compliance loss = $2,000,000
new expected annual compliance loss = $1,200,000
risk reduction value = $800,000
```

Risk ROI is harder to prove but very real.

Need evidence:

```text
historical incident data
audit findings
error rates
review outcomes
policy coverage
expert evaluation
```

Do not invent risk numbers casually.

Use ranges when uncertain.

---

### 12. Opportunity Cost [Intermediate]

Every GenAI project consumes team capacity.

Opportunity cost asks:

```text
What else could we build with the same people, time, and budget?
```

Example:

```text
GenAI assistant expected value: $400k/year
checkout optimization expected value: $1.2M/year
same team required
```

Even if the GenAI assistant is positive ROI, it may not be the best investment.

Prioritize by:

```text
expected value
confidence
time to value
risk
strategic importance
reuse potential
learning value
```

Product portfolio view:

```text
ROI is not only "is this worth doing?"
It is also "is this the best thing to do now?"
```

---

### 13. Attribution Risk [Pro]

ROI can be hard to attribute.

Example:

```text
retention improved after GenAI assistant launch
```

But other things changed:

```text
pricing changed
support team improved
new onboarding shipped
seasonality shifted
sales targeted better customers
```

Attribution risk means:

```text
we may credit GenAI for value caused by something else
```

Reduce attribution risk with:

- A/B tests
- holdout groups
- phased rollouts
- matched cohorts
- pre-registered success metrics
- stable baselines
- slice analysis
- qualitative feedback tied to behavior

Strong sentence:

> ROI claims need measurement design, not just before-and-after charts.

---

### 14. Pilot-To-Production ROI Gates [Pro]

A good GenAI pilot has graduation gates.

Pilot gate:

```text
Does it work on real tasks?
```

Production gate:

```text
Does it work reliably, safely, and economically?
```

Scale gate:

```text
Does it still work when usage, tenants, and edge cases grow?
```

Example gates:

```text
grounded accuracy >= 90%
p95 latency <= 6 seconds
cost per success <= $0.08
human escalation <= 12%
CSAT no worse than baseline
security review complete
rollback plan tested
adoption target reached
```

If a project misses gates, possible decisions:

```text
iterate
reduce scope
keep as human-assist only
route only low-risk cases
pause investment
cancel
```

Killing a bad GenAI project is also good cost engineering.

---

### 15. ROI By System Type [Intermediate]

| System Type | Main ROI Lens | Key Metrics |
|---|---|---|
| customer support assistant | deflection and satisfaction | ticket reduction, CSAT, cost per resolution |
| sales assistant | revenue productivity | conversion, response time, pipeline influenced |
| document AI | labor and accuracy | minutes saved, error rate, review rate |
| developer assistant | productivity | cycle time, PR throughput, defect rate |
| internal knowledge assistant | time saved | search time, answer acceptance, repeat usage |
| GenAI platform | leverage and governance | teams onboarded, duplicate work avoided |
| compliance assistant | risk reduction | audit findings, policy coverage, error rate |
| research agent | decision speed | synthesis time, source quality, decision cycle time |

Each type needs different ROI evidence.

Do not force every system into:

```text
tokens saved
```

or:

```text
hours saved
```

unless that is the real value driver.

---

### 16. ROI Decision Matrix [Intermediate]

| Situation | ROI Interpretation | Decision |
|---|---|---|
| high user value, high cost, high quality | may be viable premium feature | price or tier appropriately |
| low value, high cost | bad candidate | avoid or simplify |
| high labor savings, low adoption | workflow risk | fix rollout before scaling |
| strong pilot, weak safety | not production ready | add controls or reduce scope |
| platform high cost, many teams reuse | likely leverage | invest if governance works |
| platform high cost, few adopters | weak ROI | reduce scope or improve onboarding |
| enterprise high savings, high change cost | needs executive sponsorship | plan adoption deeply |
| revenue unclear, learning high | experiment | time-box and define learning goals |
| cost low, failure cost high | risky despite cheapness | add validation/human approval |
| high model cost, high retention lift | may be worth it | compare lifetime value impact |

ROI is not only a spreadsheet.

It is a decision about:

```text
value
confidence
risk
timing
strategy
```

---

### 17. ROI Memo Schema [Pro]

```json
{
  "initiative": "enterprise_support_rag_assistant",
  "system_type": "product",
  "value_hypothesis": "reduce support ticket volume while preserving customer satisfaction",
  "baseline": {
    "monthly_tickets": 50000,
    "cost_per_ticket": 4.50,
    "csat": 0.82
  },
  "target": {
    "ticket_reduction": 0.18,
    "csat_minimum": 0.82,
    "cost_per_success_max": 0.10
  },
  "costs": {
    "build_cost": 250000,
    "monthly_runtime_cost": 18000,
    "monthly_platform_cost": 7000,
    "monthly_human_review_cost": 12000,
    "monthly_maintenance_cost": 30000
  },
  "risks": {
    "wrong_answer_risk": "medium",
    "privacy_risk": "medium",
    "adoption_risk": "high",
    "mitigations": ["citations", "human escalation", "eval gates"]
  },
  "measurement_plan": {
    "method": "phased rollout with holdout",
    "leading_metrics": ["answer_acceptance", "groundedness", "latency"],
    "lagging_metrics": ["ticket_volume", "csat", "support_cost"]
  },
  "decision_gates": {
    "pilot": "4 weeks",
    "production": "12 weeks",
    "scale": "6 months"
  }
}
```

This memo makes the investment explicit.

It avoids:

```text
vague AI enthusiasm
```

and creates:

```text
testable business accountability
```

---

### 18. Code Sample: ROI Calculator

```python
def roi(value_created, total_cost):
    if total_cost == 0:
        return None
    return (value_created - total_cost) / total_cost


def payback_period(upfront_cost, monthly_net_benefit):
    if monthly_net_benefit <= 0:
        return None
    return upfront_cost / monthly_net_benefit


def product_roi(
    incremental_revenue,
    avoided_support_cost,
    retention_value,
    monthly_runtime_cost,
    monthly_maintenance_cost,
    monthly_failure_cost,
):
    value = incremental_revenue + avoided_support_cost + retention_value
    cost = monthly_runtime_cost + monthly_maintenance_cost + monthly_failure_cost

    return {
        "monthly_value": value,
        "monthly_cost": cost,
        "monthly_net_value": value - cost,
        "roi": roi(value, cost),
    }


summary = product_roi(
    incremental_revenue=60000,
    avoided_support_cost=35000,
    retention_value=25000,
    monthly_runtime_cost=22000,
    monthly_maintenance_cost=30000,
    monthly_failure_cost=8000,
)

print(summary)
print("payback_months:", payback_period(upfront_cost=300000, monthly_net_benefit=summary["monthly_net_value"]))
```

Expected lesson:

```text
ROI framing requires value, total cost, and time horizon. A positive monthly net value still needs payback analysis.
```

---

### 19. Mini Program: ROI Portfolio Simulator

This simulator compares product, platform, and enterprise proposals.

```python
def score_project(project):
    annual_value = project["monthly_value"] * 12
    annual_cost = project["monthly_cost"] * 12 + project["upfront_cost"]
    net_value = annual_value - annual_cost

    if annual_cost == 0:
        roi_value = None
    else:
        roi_value = net_value / annual_cost

    return {
        "name": project["name"],
        "type": project["type"],
        "annual_value": annual_value,
        "annual_cost_with_upfront": annual_cost,
        "net_value": net_value,
        "roi": roi_value,
        "confidence": project["confidence"],
        "risk": project["risk"],
    }


def main():
    projects = [
        {
            "name": "customer_support_assistant",
            "type": "product",
            "monthly_value": 120000,
            "monthly_cost": 60000,
            "upfront_cost": 300000,
            "confidence": "medium",
            "risk": "medium",
        },
        {
            "name": "shared_genai_platform",
            "type": "platform",
            "monthly_value": 180000,
            "monthly_cost": 110000,
            "upfront_cost": 800000,
            "confidence": "medium",
            "risk": "high adoption dependency",
        },
        {
            "name": "invoice_review_automation",
            "type": "enterprise",
            "monthly_value": 250000,
            "monthly_cost": 90000,
            "upfront_cost": 500000,
            "confidence": "high",
            "risk": "change management",
        },
    ]

    for project in projects:
        score = score_project(project)
        print(score)


if __name__ == "__main__":
    main()
```

Expected lesson:

```text
ROI comparison should include project type, upfront cost, monthly cost, confidence, and risk, not only expected value.
```

---

### 20. Hands-On Lab: Write An ROI Case [Pro]

#### Build

Choose one initiative:

```text
customer-facing RAG assistant
internal GenAI platform
invoice automation system
developer productivity assistant
contract review workflow
enterprise knowledge assistant
support agent copilot
```

Classify it:

```text
product
platform
enterprise
```

#### Baseline

Define current baseline:

```text
volume
current cost
current cycle time
current quality
current failure rate
current human effort
current revenue/conversion/retention if relevant
```

#### Value Hypothesis

Write:

```text
This system will create value by <mechanism>.
We expect <metric> to improve from <baseline> to <target>.
The value is worth approximately <range>.
```

#### Cost Model

Include:

```text
build cost
runtime cost
retrieval/platform cost
human review cost
maintenance cost
security/eval cost
change-management cost
failure cost
```

#### Measurement Plan

Define:

```text
leading metrics
lagging metrics
baseline method
holdout or comparison group
decision gates
go/no-go threshold
```

#### Defend

Write:

```text
This is worth funding if <condition>.
It should not scale if <condition>.
The biggest uncertainty is <uncertainty>.
The first experiment should prove <proof point>.
```

---

### 21. Common Mistakes [Intermediate]

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| using usage as ROI | usage does not prove business value | tie usage to outcome change |
| ignoring baseline | cannot prove improvement | define counterfactual |
| counting gross value only | costs and failures may erase value | compute net value |
| ignoring adoption | workflow may not change | measure and support adoption |
| ignoring change-management cost | enterprise rollout looks too cheap | budget rollout effort |
| using one ROI frame for all systems | product, platform, enterprise value differ | choose the right lens |
| no time horizon | payback unclear | define pilot, production, scale horizons |
| ignoring risk reduction | undervalues compliance/safety systems | estimate expected loss reduction |
| overstating attribution | other changes may explain improvement | use holdouts or phased rollout |
| no kill criteria | bad projects keep running | define gates and stop conditions |

---

### 22. Practical Interview Question [Intermediate]

> Leadership asks whether a GenAI initiative is worth funding. How would you frame ROI differently for a customer-facing product feature, an internal GenAI platform, and an enterprise automation workflow?

---

### 23. Strong Answer [Pro]

I would start by identifying the system type because ROI means different things for product, platform, and enterprise systems. For a customer-facing product feature, I would frame ROI around customer behavior: revenue, conversion, activation, retention, support deflection, satisfaction, and cost per successful user outcome. I would compare those gains against runtime cost, engineering cost, failure cost, and any user trust or safety risk.

For an internal GenAI platform, I would not expect direct revenue from the platform itself. I would measure leverage: teams onboarded, duplicate systems avoided, integration time reduced, shared eval and observability coverage, security review time reduced, model migration speed, and incident reduction. The platform is justified if shared capability is cheaper, safer, and faster than every team building its own stack.

For an enterprise automation workflow, I would frame ROI around operational impact: labor hours saved, cycle-time reduction, manual error reduction, compliance improvement, audit readiness, human review reduction, and process standardization. I would include adoption and change-management cost because enterprise value only appears if the workflow actually changes.

Across all three, I would require a baseline and counterfactual. I would define leading metrics for pilots, such as adoption, acceptance, groundedness, latency, and escalation rate, plus lagging metrics like revenue lift, support cost reduction, or cycle-time improvement. I would include total cost of ownership: model usage, retrieval infrastructure, engineering maintenance, evaluation, observability, security, human review, and incident cost.

Finally, I would define decision gates: what must be true to continue, scale, reduce scope, or stop. A good ROI case is not "AI will save time." It is a measurable value hypothesis with cost, risk, adoption, and proof points.

---

### 24. Active Recall [Beginner]

Answer these without looking:

1. What is the basic ROI formula?
2. Why is value_created hard to define?
3. What is product ROI usually about?
4. What is platform ROI usually about?
5. What is enterprise ROI usually about?
6. Why is usage not enough to prove ROI?
7. What is a baseline?
8. What is a counterfactual?
9. What are leading metrics?
10. What are lagging metrics?
11. What is payback period?
12. Why does adoption matter?
13. What is risk reduction ROI?
14. What is opportunity cost?
15. What is attribution risk?
16. What are pilot-to-production gates?
17. Name three product ROI metrics.
18. Name three platform ROI metrics.
19. Name three enterprise ROI metrics.
20. What is the final lesson of this topic?

Expected answers:

1. Value minus cost divided by cost.
2. Value differs by product, platform, enterprise, risk, and adoption.
3. Customer behavior, revenue, retention, satisfaction, support deflection.
4. Shared leverage, reduced duplicate work, governance, faster delivery.
5. Labor savings, cycle time, error reduction, compliance, process change.
6. People can use a feature without creating business value.
7. Current measured state before the GenAI system.
8. What would have happened without the system.
9. Early signals that predict value, such as adoption or acceptance.
10. Final business outcomes, such as revenue or cost reduction.
11. Upfront investment divided by monthly net benefit.
12. No workflow change means no operational value.
13. Value from lowering expected loss or incident probability.
14. The value of what else the team could have built.
15. Crediting GenAI for outcomes caused by other changes.
16. Criteria for continuing, scaling, reducing scope, or stopping.
17. Conversion, retention, support deflection.
18. Teams onboarded, integration time reduced, duplicate systems retired.
19. Labor hours saved, cycle time reduced, error rate reduced.
20. ROI framing must match the system type and be measured against baseline, cost, adoption, and risk.

---

### 25. Revision Notes

- **One-line summary:** Product ROI measures customer value, platform ROI measures shared leverage, and enterprise ROI measures operational transformation.
- **Three keywords:** value, baseline, adoption.
- **One interview trap:** Claiming ROI from GenAI usage or demo quality without a baseline, counterfactual, total cost model, and adoption plan.
- **One memory trick:** Product sells outcomes, platform sells leverage, enterprise sells process change.

Final takeaway:

> GenAI ROI is not one spreadsheet cell. It is a business argument: define the value lens, measure against a baseline, include total cost and risk, and scale only when the system changes outcomes that matter.

---

## Module 20 Checkpoint: Cost Engineering and Product Tradeoffs Synthesis

### Module Checkpoint

By the end of this module, you should be able to:

1. Explain token, retrieval, and reranking costs as one system budget.
2. Defend whether to rerank, increase top-k, compress context, or route to a different model.
3. Explain when the right product decision is to use less GenAI, not more.

This checkpoint is not about memorizing cost tricks.

It is about thinking like someone who has to ship, price, operate, debug, and defend a GenAI system after the demo.

The central checkpoint sentence:

> Cost engineering is not making the model cheaper. It is spending the right amount of computation, evidence, latency, engineering effort, and risk budget to create a successful product outcome.

---

### 1. The 360-Degree Mental Model

A GenAI system spends budget in five connected places:

```text
1. tokens
2. retrieval
3. reranking
4. generation
5. engineering and operations
```

These are not separate bills.

They trade off against each other.

Example:

```text
More retrieval candidates may improve recall.
Reranking may reduce noisy final context.
Smaller final context may reduce generation cost and TTFT.
Better grounding may reduce human review and follow-up turns.
But the reranker adds latency, cost, and maintenance.
```

That is one system budget.

Naive view:

```text
How do we reduce model cost?
```

Senior view:

```text
Which layer is spending budget, what outcome is it buying, and is there a cheaper safer way to get the same product result?
```

---

### 2. The Unified Budget

A serious budget includes:

| Budget Type | What It Measures | Example |
|---|---|---|
| token budget | context and generation size | input/output/cached tokens |
| latency budget | user waiting time | TTFT, TTLT, p95 |
| retrieval budget | evidence gathering effort | top-k, filters, hydration |
| reranking budget | evidence selection effort | candidate count, reranker latency |
| model budget | reasoning/generation tier | small, medium, strong model |
| tool budget | external calls | CRM, search, billing, code tools |
| validation budget | quality and safety checks | citation validation, schema checks |
| human budget | review and escalation | manual approval rate |
| engineering budget | build and maintenance | evals, tracing, connectors, incidents |
| risk budget | tolerated failure exposure | wrong answer, unsafe action, compliance |

The strongest design is not the one that minimizes every row.

It is the one that spends each row where it creates measurable value.

Example:

```text
High-risk legal answer:
  more retrieval, reranking, citations, validation, maybe human review

Low-risk brainstorming:
  lighter retrieval, cheaper model, shorter validation
```

The budget follows the task.

---

### 3. Outcome 1: Explain Token, Retrieval, and Reranking Costs as One System Budget

Tokens are often the visible meter.

Retrieval and reranking decide what gets put on that meter.

Generation spends the meter to produce an answer.

The relationship:

```text
retrieval breadth -> candidate evidence
reranking -> selected evidence
final context -> input tokens
model generation -> output tokens
answer quality -> retries, follow-ups, human review
```

If retrieval is weak:

```text
the model may answer from missing or irrelevant evidence
```

Then cost appears later as:

```text
failed tasks
repair calls
follow-up turns
human escalations
lost trust
```

If retrieval is too broad and unfiltered:

```text
the model receives too many tokens
```

Then cost appears as:

```text
higher input cost
slower first token
context-window pressure
distractor errors
wrong citations
```

If reranking is well used:

```text
it spends latency/cost before generation to reduce noisy context and improve grounded success
```

If reranking is poorly used:

```text
it adds another expensive step without improving the final answer
```

The correct budget question:

```text
Does this retrieval/reranking spend reduce total cost per successful grounded task?
```

Not:

```text
Does this step add cost?
```

Good steps can add local cost and reduce system cost.

Bad steps can reduce local cost and increase system cost.

---

### 4. System Budget Formula

For one successful grounded task:

```text
cost_per_grounded_success =
    (
      query_embedding_cost
    + retrieval_runtime_cost
    + reranking_cost
    + generation_cost
    + validation_cost
    + expected_retry_cost
    + expected_human_review_cost
    + amortized_ingestion_cost
    + amortized_engineering_and_platform_cost
    )
    / grounded_success_rate
```

The denominator matters.

If you divide by all requests, bad systems look cheap.

If you divide by grounded successful tasks, weak systems expose their waste.

Example:

```text
System A:
  cost per session = $0.03
  grounded success = 50%
  cost per grounded success = $0.06

System B:
  cost per session = $0.045
  grounded success = 90%
  cost per grounded success = $0.05
```

System B spends more per session but less per useful result.

That is the product view.

---

### 5. Budget Trace Schema

A good system trace should make the budget visible.

```json
{
  "task_id": "task_001",
  "workflow_type": "support_rag_answer",
  "risk_level": "medium",
  "route": "standard_rag_with_rerank",
  "retrieval": {
    "candidate_k": 60,
    "final_k": 6,
    "retrieval_latency_ms": 220,
    "retrieval_cost": 0.0,
    "gold_evidence_found": true
  },
  "reranking": {
    "enabled": true,
    "candidates_reranked": 60,
    "rerank_latency_ms": 650,
    "rerank_cost": 0.0,
    "gold_rank_before": 18,
    "gold_rank_after": 3
  },
  "generation": {
    "model_tier": "medium",
    "input_tokens": 8200,
    "output_tokens": 620,
    "ttft_ms": 1900,
    "ttlt_ms": 5600,
    "generation_cost": 0.0
  },
  "validation": {
    "citation_check": true,
    "schema_check": true,
    "validation_cost": 0.0,
    "validation_passed": true
  },
  "outcome": {
    "answer_correct": true,
    "grounded": true,
    "user_accepted": true,
    "human_escalated": false
  }
}
```

This trace answers the checkpoint question:

```text
What did we spend?
Where did we spend it?
What quality did it buy?
Was the outcome worth it?
```

---

### 6. Outcome 2: Defend Rerank vs Top-k vs Compression vs Model Routing

Do not choose knobs by habit.

Choose them by failure diagnosis.

Four common fixes solve different problems:

| Fix | Best When | Main Cost | Main Risk |
|---|---|---|---|
| increase candidate top-k | correct evidence is missing from candidates | retrieval/search work | more candidates to process |
| rerank | correct evidence is present but buried | reranker latency/cost | extra complexity |
| compress context | context contains removable noise/repetition | compression call and loss risk | losing evidence |
| route to different model | task needs different capability, latency, or risk tier | model cost/latency | over-routing or under-routing |

The key word is:

```text
diagnosis
```

Before changing architecture, ask:

```text
Is the evidence missing?
Is the evidence buried?
Is the final context bloated?
Is the model ignoring good evidence?
Is the prompt unclear?
Is the task too hard for this model tier?
Is the product risk high enough to justify stronger controls?
```

Each answer points to a different fix.

---

### 7. Decision Tree: Rerank or Increase Top-k

Start with retrieval traces.

```text
Question: Is gold evidence in the candidate set?
```

If no:

```text
increase candidate top-k
improve retriever
add hybrid dense+sparse retrieval
fix metadata filters
improve chunking
rewrite query
```

If yes, but ranked too low:

```text
rerank candidates
improve ranking features
use hybrid fusion
increase candidate_k then rerank
```

If yes, and already in final context:

```text
do not tune top-k first
inspect prompt, generation, citations, context ordering, model tier
```

If final context has many distractors:

```text
rerank
dedupe
lower final_k
pack context better
```

Strong answer:

> I would increase candidate top-k for recall failures and use reranking for precision failures. I would tune final context top-k separately because sending more chunks to the generator increases tokens, latency, and distractor risk.

---

### 8. Decision Tree: Compress Context or Use a Larger Model

Start with evidence density.

```text
Question: Is the context mostly noise or mostly necessary evidence?
```

If mostly noise:

```text
dedupe
filter
extract exact spans
compress background
drop unused tool fields
summarize old memory
```

If dense evidence:

```text
preserve exact spans
consider larger context
route only hard cases to larger model
use source labels and ordering
```

If exact wording matters:

```text
avoid lossy summary
use extractive compression
preserve citations, line/page IDs, numbers, dates, exceptions
```

If compression call costs more latency than it saves:

```text
avoid online compression
cache summaries
precompute summaries
use selective reduction only
```

Strong answer:

> I would compress noise, not proof. If the task requires exact citations, numbers, code, or policy exceptions, I would preserve exact evidence and route hard cases to a larger-context model only when the value justifies the cost and latency.

---

### 9. Decision Tree: Route to a Different Model

Start with task difficulty and risk.

```text
Question: Is the current route failing because the model is too weak, or because the system gave it the wrong evidence/control?
```

If evidence is bad:

```text
fix retrieval before upgrading model
```

If evidence is good but reasoning fails:

```text
try stronger model or better prompt/schema
```

If task is easy and low-risk:

```text
route to deterministic/cache/small model
```

If task is ambiguous or high-value:

```text
route to medium/strong model with deeper retrieval
```

If task is high-risk or irreversible:

```text
use deterministic control, strict validation, and human approval
```

If provider/model fails:

```text
fallback to compatible backup, cached answer, partial answer, async job, or human review
```

Strong answer:

> Model routing should spend stronger model quality only where difficulty, uncertainty, risk, or product value justifies it. Easy tasks get fast cheap paths; hard tasks get stronger paths; risky tasks get controls and approval.

---

### 10. Decision Matrix: Pick the Fix

| Symptom | Likely Cause | Best First Move |
|---|---|---|
| answer lacks key source | candidate recall failure | increase candidate_k, hybrid retrieval, query rewrite |
| source appears at rank 30 | ranking weakness | rerank broader candidates |
| source in context but answer wrong | generation/prompt issue | improve grounding prompt, model, answer schema |
| context huge and noisy | final context bloat | rerank, dedupe, compress, lower final_k |
| TTFT too slow | input too large or model slow | reduce final context, cache prefix, route model |
| TTLT too slow | output too long | cap output, stream, restructure response |
| reranker p95 high | second-stage too heavy | reduce candidates, conditional rerank |
| compression removes exceptions | lossy compression unsafe | preserve exact spans or larger context |
| small model often escalates | cheap-first inefficient | route hard slice strong-first |
| human review dominates cost | quality/risk failures | improve retrieval/validation or route earlier |
| engineering maintenance dominates | architecture too complex | simplify, managed services, reduce scope |
| product ROI weak | value not proven | reduce GenAI scope or stop |

This table is the working memory for the module.

---

### 11. Outcome 3: Explain When Less GenAI Is the Right Product Decision

The mature move is sometimes:

```text
remove the model from this step
```

or:

```text
use GenAI only as assistance, not authority
```

Use less GenAI when:

- deterministic logic solves the task exactly
- model adds cost but not measurable value
- failure cost is high and validation is weak
- latency budget is too tight
- output must be audited line by line
- workflow requires exact permissions or transactions
- adoption is low and the process does not change
- engineering maintenance outweighs benefit
- users need trust, not novelty
- a cached/template/rules path is good enough

Examples:

| Task | Better Decision |
|---|---|
| permission check | deterministic access control |
| late fee calculation | rules |
| strict schema validation | parser/schema validator |
| exact database filtering | SQL/filter logic |
| payment execution | deterministic workflow plus approval |
| simple FAQ answer | cache or deterministic retrieval first |
| high-risk decision | model assists, human or rules decide |

Less GenAI does not mean less sophistication.

It often means better architecture.

Strong sentence:

> The best GenAI systems know where not to use GenAI.

---

### 12. Cost-Quality-Product Triangle

Every decision lives inside a triangle:

```text
cost
quality
product value
```

With latency and risk as constraints:

```text
cost: can we afford it?
quality: does it work well enough?
product value: does it change an outcome that matters?
latency: does the user wait too long?
risk: what happens if it fails?
```

Bad optimization:

```text
reduce cost and destroy groundedness
```

Also bad:

```text
maximize quality with no ROI
```

Also bad:

```text
ship impressive GenAI that users do not adopt
```

Good optimization:

```text
improve cost per successful safe outcome within the product's latency and risk limits
```

That is the module thesis.

---

### 13. Architecture Review Checklist

Use this checklist before defending a design.

#### Budget

```text
[ ] Do we know input/output/cached tokens by layer?
[ ] Do we know retrieval, reranking, generation, validation, and human review costs?
[ ] Do we know cost per request, session, and successful task?
[ ] Do we know TCO, not just model bill?
```

#### Quality

```text
[ ] Do we know failure types: missing evidence, buried evidence, bloated context, misuse?
[ ] Do we have groundedness and citation metrics?
[ ] Do we measure quality by slice?
[ ] Do we know where retries and repairs happen?
```

#### Latency

```text
[ ] Do we know critical path?
[ ] Do we measure TTFT and TTLT?
[ ] Do we know p50, p95, and p99?
[ ] Do slow tools, rerankers, and models have timeout/fallback policies?
```

#### Product

```text
[ ] Is GenAI justified over deterministic logic?
[ ] Does the feature have a baseline and ROI hypothesis?
[ ] Is adoption required for value?
[ ] Are high-risk actions controlled by rules or humans?
```

#### Operations

```text
[ ] Are routing and fallback decisions logged?
[ ] Are prompt, retrieval, model, and policy versions tracked?
[ ] Is there a rollback path?
[ ] Is the engineering maintenance cost understood?
```

If several answers are no, the system is not yet economically mature.

---

### 14. Interview-Ready Scenario

Scenario:

> You are designing a customer support RAG assistant. The system is accurate but expensive and slow. Leadership asks whether to increase top-k, add reranking, compress context, route to a stronger model, or simplify the system.

Strong answer structure:

1. Define the product outcome.
2. Inspect traces before changing knobs.
3. Diagnose retrieval failure type.
4. Compare retrieval/reranking/generation as one budget.
5. Choose targeted optimization.
6. Preserve quality and safety.
7. Consider less GenAI if deterministic path works.
8. Defend with ROI.

Strong answer:

```text
I would not start by changing top-k or switching models. I would first define the unit of value, such as cost per grounded resolved support question, and inspect traces across retrieval, reranking, generation, validation, retries, and human escalation.

If the correct evidence is missing from candidates, I would improve recall by increasing candidate top-k, adding hybrid retrieval, fixing metadata filters, or improving chunking. If the evidence is present but buried, I would use reranking and keep final context small. If the evidence is already in final context but the answer is wrong, I would look at prompt grounding, answer format, citations, or model capability.

If context is bloated, I would reduce or compress noise, but preserve exact evidence, source IDs, numbers, dates, and exceptions. If the task is genuinely hard or high-risk, I would route it to a stronger model or stricter validation tier. If the task is easy, deterministic, or cacheable, I would use less GenAI.

I would compare choices using cost per grounded success, TTFT, TTLT, p95 latency, citation accuracy, human review rate, and ROI. The right answer is the cheapest reliable workflow that meets product quality and safety constraints, not the most model-heavy architecture.
```

---

### 15. Code Sample: System Budget Comparator

```python
def expected_cost_per_grounded_success(config):
    expected_runtime = (
        config["retrieval_cost"]
        + config["rerank_cost"]
        + config["generation_cost"]
        + config["validation_cost"]
        + config["retry_rate"] * config["retry_cost"]
        + config["human_review_rate"] * config["human_review_cost"]
    )

    total = expected_runtime + config["amortized_platform_cost"]

    if config["grounded_success_rate"] == 0:
        return None

    return total / config["grounded_success_rate"]


configs = {
    "higher_top_k_no_rerank": {
        "retrieval_cost": 0.004,
        "rerank_cost": 0.000,
        "generation_cost": 0.040,
        "validation_cost": 0.004,
        "retry_rate": 0.18,
        "retry_cost": 0.020,
        "human_review_rate": 0.10,
        "human_review_cost": 1.50,
        "amortized_platform_cost": 0.010,
        "grounded_success_rate": 0.74,
    },
    "rerank_small_final_context": {
        "retrieval_cost": 0.006,
        "rerank_cost": 0.008,
        "generation_cost": 0.024,
        "validation_cost": 0.004,
        "retry_rate": 0.08,
        "retry_cost": 0.020,
        "human_review_rate": 0.05,
        "human_review_cost": 1.50,
        "amortized_platform_cost": 0.012,
        "grounded_success_rate": 0.86,
    },
    "route_hard_cases_stronger": {
        "retrieval_cost": 0.007,
        "rerank_cost": 0.010,
        "generation_cost": 0.036,
        "validation_cost": 0.006,
        "retry_rate": 0.04,
        "retry_cost": 0.025,
        "human_review_rate": 0.03,
        "human_review_cost": 1.50,
        "amortized_platform_cost": 0.014,
        "grounded_success_rate": 0.91,
    },
}

for name, config in configs.items():
    print(name, round(expected_cost_per_grounded_success(config), 4))
```

Expected lesson:

```text
The best architecture is not the one with the cheapest model call. It is the one with the best cost per grounded successful outcome under latency and risk constraints.
```

---

### 16. Mini Program: Decision Recommendation Simulator

```python
def recommend_fix(signal):
    if not signal["gold_in_candidates"]:
        return "Improve candidate recall: increase candidate_k, hybrid retrieval, filters, or chunking."

    if signal["gold_rank_before"] > signal["final_k"] and signal["gold_rank_after"] <= signal["final_k"]:
        return "Reranking is useful: evidence was buried and rerank lifts it into final context."

    if signal["final_context_tokens"] > signal["context_budget_tokens"]:
        if signal["exact_evidence_required"]:
            return "Use extractive compression or larger-context routing; preserve exact spans."
        return "Compress, dedupe, or lower final_k to reduce noisy context."

    if signal["answer_wrong_despite_good_context"]:
        if signal["risk_level"] == "high":
            return "Route to stronger model with stricter validation or human review."
        return "Improve prompt, answer schema, or model tier after verifying evidence use."

    if signal["deterministic_solution_available"]:
        return "Use less GenAI: deterministic logic is cheaper, faster, and more auditable."

    return "Current path may be acceptable; optimize only if ROI or latency requires it."


cases = [
    {
        "gold_in_candidates": False,
        "gold_rank_before": None,
        "gold_rank_after": None,
        "final_k": 6,
        "final_context_tokens": 5000,
        "context_budget_tokens": 7000,
        "exact_evidence_required": False,
        "answer_wrong_despite_good_context": False,
        "risk_level": "low",
        "deterministic_solution_available": False,
    },
    {
        "gold_in_candidates": True,
        "gold_rank_before": 22,
        "gold_rank_after": 3,
        "final_k": 6,
        "final_context_tokens": 5200,
        "context_budget_tokens": 7000,
        "exact_evidence_required": False,
        "answer_wrong_despite_good_context": False,
        "risk_level": "medium",
        "deterministic_solution_available": False,
    },
    {
        "gold_in_candidates": True,
        "gold_rank_before": 3,
        "gold_rank_after": 3,
        "final_k": 6,
        "final_context_tokens": 14000,
        "context_budget_tokens": 7000,
        "exact_evidence_required": True,
        "answer_wrong_despite_good_context": False,
        "risk_level": "high",
        "deterministic_solution_available": False,
    },
]

for case in cases:
    print(recommend_fix(case))
```

Expected lesson:

```text
The correct optimization follows the diagnosed failure, not the team's favorite knob.
```

---

### 17. Hands-On Checkpoint Lab

Pick one GenAI system:

```text
support RAG assistant
enterprise knowledge assistant
invoice extraction workflow
contract review assistant
research agent
customer email drafter
```

#### Step 1: Define The Product Unit

```text
request:
session:
successful task:
grounded successful task:
value per success:
failure cost:
```

#### Step 2: Build The Budget

Fill in:

```text
input tokens:
output tokens:
retrieval cost:
reranking cost:
generation cost:
validation cost:
tool cost:
human review cost:
offline ingestion cost:
engineering/platform allocation:
p95 latency:
grounded success rate:
```

#### Step 3: Diagnose Failures

Classify 20 failures:

```text
missing evidence
buried evidence
bloated context
compression loss
model reasoning failure
tool failure
validation failure
routing failure
deterministic logic should have handled it
```

#### Step 4: Recommend Changes

For each failure class:

```text
increase candidate top-k?
rerank?
compress context?
larger model?
different route?
deterministic path?
human review?
```

#### Step 5: Defend The Decision

Write:

```text
The main cost bucket is <bucket>.
The main quality failure is <failure>.
The proposed change is <change>.
It improves <metric>.
It costs <cost/latency>.
It is worth it because <product value>.
It is not worth using more GenAI for <step> because <reason>.
```

---

### 18. Common Checkpoint Mistakes

| Mistake | Why It Is Wrong | Better Approach |
|---|---|---|
| optimizing token cost alone | ignores retrieval, quality, human review, and engineering | optimize cost per grounded success |
| increasing final top-k blindly | adds tokens and distractors | increase candidate recall separately from final context |
| adding reranker without recall check | reranker cannot recover missing evidence | inspect gold evidence in candidates |
| compressing proof | loses citations, numbers, exceptions | preserve exact evidence, compress background |
| using stronger model for retrieval failure | model cannot reason over missing evidence | fix retrieval first |
| using GenAI for deterministic rules | adds cost and audit risk | use code/rules, model may explain |
| ignoring engineering cost | product looks falsely profitable | include TCO |
| treating usage as ROI | usage may not change business outcome | define baseline and counterfactual |
| no route/fallback logs | cannot diagnose over-routing or under-routing | log route, signals, fallback, outcome |
| optimizing average only | p95/p99 may break product experience | analyze slices and tail latency |

---

### 19. Checkpoint Active Recall

Answer these without looking:

1. Why are token, retrieval, and reranking costs one system budget?
2. What is cost per grounded successful task?
3. When should you increase candidate top-k?
4. When should you rerank?
5. Why is final top-k different from candidate top-k?
6. When is context compression dangerous?
7. When should you use a larger-context model?
8. When should you route to a stronger model?
9. When should you avoid routing to a stronger model?
10. Why can reranking reduce generation cost?
11. Why can cheaper generation increase total cost?
12. What does "compress noise, not proof" mean?
13. What does "model for meaning, code for authority" mean?
14. When is less GenAI the right product decision?
15. Why should human review cost be included?
16. Why is engineering cost part of TCO?
17. What is the difference between product ROI and platform ROI?
18. What is the role of baseline and counterfactual?
19. What should a route/fallback trace include?
20. What is the final lesson of Module 20?

Expected answers:

1. Retrieval and reranking decide what tokens generation consumes and what quality/failure costs follow.
2. Total system cost divided by correct grounded successful outcomes.
3. When correct evidence is missing from the candidate set.
4. When correct evidence is present but buried or final context is noisy.
5. Candidate top-k is search breadth; final top-k is what the model reads.
6. When exact citations, numbers, dates, exceptions, legal text, tables, or code matter.
7. When dense original evidence must be preserved and the value justifies cost/latency.
8. When evidence is good but reasoning difficulty, risk, or product value requires more capability.
9. When retrieval, prompt, parsing, rules, or deterministic validation is the real issue.
10. It can select fewer better chunks and reduce noisy input tokens and failures.
11. It may fail more often, retry, escalate, or require human correction.
12. Remove low-value tokens but preserve exact task-critical evidence.
13. Models interpret messy input; deterministic systems make/enforce exact decisions.
14. When rules, SQL, parsers, cache, templates, or human approval are safer/cheaper/better.
15. It often dominates real product cost and reflects failure/uncertainty.
16. Build, maintenance, evals, security, incidents, and ownership are real costs.
17. Product ROI measures customer/business outcomes; platform ROI measures shared leverage.
18. They prove whether GenAI changed the outcome compared with what would have happened.
19. Task signals, chosen route, model/retrieval/validation tiers, fallback reason, cost, latency, outcome.
20. Spend GenAI budget only where it creates measurable successful safe outcomes.

---

### 20. Final Module Defense Answer

If an interviewer asks:

> How do you reason about cost engineering and product tradeoffs for a production GenAI system?

Answer:

```text
I start by defining the product unit: request, session, successful task, and grounded successful task. Then I build a system budget rather than looking only at model tokens. The budget includes retrieval, reranking, generation, validation, tools, retries, human review, offline ingestion, and engineering/platform ownership.

For RAG, I diagnose whether failures are missing evidence, buried evidence, bloated context, compression loss, or generation misuse. If evidence is missing, I improve candidate recall with top-k, hybrid search, filters, chunking, or query rewrite. If evidence is present but buried, I rerank. If final context is bloated, I dedupe, compress low-value background, lower final_k, or pack context better while preserving exact evidence. If evidence is good but reasoning fails, I consider prompt/schema/model routing.

I separate candidate top-k from final context top-k. More candidates help search; more final context increases tokens, latency, and distractor risk. Reranking can add cost locally but reduce total cost per grounded success by improving final evidence selection and reducing retries or human escalation.

For model choice, I route by task difficulty, risk, value, latency, and budget. Easy tasks should use deterministic, cached, or smaller-model paths. Hard or high-risk tasks may deserve stronger models, deeper retrieval, stricter validation, or human approval. Fallbacks handle both availability failures and quality failures.

I also ask whether GenAI is justified at all. If the task is exact, auditable, rule-bound, or security-critical, deterministic logic is often better. The mature product decision is sometimes to use less GenAI: models interpret and draft, but code enforces rules and humans approve high-risk actions.

Finally, I defend the architecture with ROI and TCO: cost per successful grounded task, p95 latency, quality metrics, human review rate, engineering maintenance, adoption, and business value. The goal is not maximum AI usage. The goal is the cheapest reliable system that creates safe, measurable product value.
```

---

### 21. Final Revision Notes

- **One-line summary:** Module 20 teaches you to treat GenAI cost as a full product budget: tokens, retrieval, reranking, generation, latency, engineering, risk, and ROI all connect.
- **Three keywords:** budget, diagnosis, value.
- **One interview trap:** Optimizing one knob, such as model price or top-k, without diagnosing the failure type and measuring cost per grounded successful task.
- **One memory trick:** Evidence decides retrieval; selection decides reranking; proof decides compression; risk decides routing; value decides whether to use GenAI at all.

Final takeaway:

> The highest-signal GenAI product decision is not "which model is best?" It is "what is the cheapest, safest, most maintainable path to a successful outcome, and where does GenAI genuinely earn its place?"

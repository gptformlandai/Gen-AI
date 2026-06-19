# Module 2 - Transformer And Modern LLM Internals

This is the evolving knowledge base for Module 2.

## Quick Topic Index

- [Topic 2.1: Text Processing, Tokens, and Context](#topic-21-text-processing-tokens-and-context)
- [Subtopic 2.1.a: Text Normalization, Segmentation, and Token Boundaries](#subtopic-21a-text-normalization-segmentation-and-token-boundaries)
- [Topic 2.2: Transformer Mechanics](#topic-22-transformer-mechanics)
- [Topic 2.3: From Pretraining to Instruction Following](#topic-23-from-pretraining-to-instruction-following)
- [Module Checkpoint Deep Explanation](#module-checkpoint-deep-explanation)

Covered so far:

- Topic 2.1.a: Text normalization, segmentation, and token boundaries
- Module checkpoint: attention, long-context/tool-heavy failures, and pretraining/SFT/alignment behavior

---

## Topic 2.1: Text Processing, Tokens, and Context

**Topic time:** 6h

Subtopics in this topic:

- 2.1.a Text normalization, segmentation, and token boundaries - 90m
- 2.1.b BPE and SentencePiece intuition - 90m
- 2.1.c Positional information, context windows, and truncation risks - 90m
- 2.1.d Token budgeting for prompts, retrieval context, and tool results - 90m

Learning rule for this module file:

- We cover one subtopic at a time.
- We do not complete the full parent topic in a single pass.
- Each new subtopic is appended only after the previous one is understood.

---

## Subtopic 2.1.a: Text Normalization, Segmentation, and Token Boundaries

### 1) The Intuition (Plain English)

Before a model can reason, it must convert messy human text into machine-consumable units.
This pre-tokenization stage is where many silent bugs start.

- Text normalization cleans and standardizes raw text.
- Segmentation splits text into meaningful units (sentence, word, or chunk boundaries depending on pipeline).
- Token boundaries are the final model-facing pieces after tokenization rules are applied.

Simple mental model:

- Normalization = clean the document
- Segmentation = cut into useful slices
- Token boundaries = convert slices into model symbols

Analogy:

Think of preparing vegetables for a kitchen line.

- Normalization is washing and removing dirt.
- Segmentation is chopping into cooking-size pieces.
- Token boundaries are the exact units each machine on the line accepts.

If these stages are sloppy, the model may look wrong even when the core model is fine.

### 2) Real-World Industry Scenarios

#### Scenario A: Support chatbot with multilingual input

- Product context: users submit mixed-case text, emojis, abbreviations, and non-standard punctuation.
- Constraints: high throughput, predictable behavior across languages, low preprocessing latency.
- What good looks like in production: normalization handles Unicode and casing consistently, segmentation keeps user intent intact, and tokenization remains stable across locales.

Why this matters:

- Minor preprocessing inconsistency can cause large retrieval and response quality drift.

#### Scenario B: Contract analysis pipeline

- Product context: legal PDFs with headers, footers, OCR artifacts, and broken line wraps.
- Constraints: high precision extraction, traceability, noisy input sources.
- What good looks like in production: normalization removes OCR noise safely, segmentation respects clause boundaries, and tokenization does not split critical identifiers unpredictably.

Why this matters:

- Boundary mistakes can break citations, clause linking, and downstream structured extraction.

### 3) System View (Think like a systems engineer)

#### Inputs -> Transformations -> Outputs

- Inputs: raw user text, document text, OCR output, locale metadata.
- Transformations:
  - normalize encoding, whitespace, punctuation, and canonical forms
  - segment into processing units (sentences/chunks/fields)
  - tokenize by model-specific tokenizer
  - attach metadata for offsets and provenance
- Outputs: token IDs, token counts, and boundary maps used by prompt/retrieval/model layers.

#### Observability

What we log and inspect:

- normalized text length delta vs raw text
- segmentation stats (average segment size, boundary errors)
- token count distribution by route and locale
- tokenizer version and model mapping
- mismatch rate between segment boundaries and citation offsets

#### Failure points

- Unicode normalization mismatch creates duplicate or missed matches in retrieval.
- Over-aggressive cleaning removes meaningful symbols (currency, legal markers, code syntax).
- Poor segmentation splits semantic units and degrades relevance.
- Token boundary mismatch between indexing and inference tokenizers causes inconsistency.

### 4) System Design Flavor (practical and concise)

#### Key design question

Are preprocessing rules consistent between indexing time and inference time?

If not, retrieval and generation drift even when prompts and models stay unchanged.

#### Tradeoffs

- Heavy normalization vs fidelity: more cleanup reduces noise but can erase domain meaning.
- Larger segments vs finer segments: larger segments keep context but hurt precision; finer segments improve precision but can lose coherence.
- Generic tokenizer defaults vs domain-tuned processing: defaults are simple, but domain text often needs targeted handling.

#### One scaling consideration

At 10x data volume, preprocessing bugs amplify.

Small boundary errors create widespread indexing mismatch, inflated token spend, and hard-to-debug quality regressions.

### 5) Common Mistakes + Debugging

#### Mistake 1

- Symptom: retrieval quality drops after a pipeline update.
- Likely cause: normalization rules changed in ingestion but not in query path.
- First debugging step: diff normalized query text vs normalized indexed text using the same examples.

#### Mistake 2

- Symptom: token costs increase without obvious prompt changes.
- Likely cause: segmentation now creates longer chunks or duplicates overlapping text.
- First debugging step: compare token histograms and chunk overlap rates before and after the change.

#### Mistake 3

- Symptom: citations point to incorrect spans.
- Likely cause: boundary offsets were computed on raw text but applied to normalized text.
- First debugging step: validate offset mapping tables and ensure every stage preserves alignment metadata.

### 6) Active Recall (Spaced Repetition)

1. What is the difference between normalization and segmentation?
2. Why can token boundary mismatches break retrieval quality?
3. What is one risk of over-aggressive normalization?
4. Why should preprocessing be identical in ingest and query pipelines?
5. What is the first debugging check when token counts suddenly rise?

#### Active Recall Answers

1. Normalization standardizes text format; segmentation divides text into meaningful processing units.
2. If indexing and inference use different boundary behavior, semantic matching and context packing become inconsistent.
3. It can remove meaningful domain symbols and reduce factual precision.
4. Because any mismatch creates representation drift, causing poorer retrieval and unstable generation.
5. Compare segment size and token-count distributions before and after the pipeline change.

### 7) Practice

#### Mini-exercise

You run a RAG pipeline where ingestion normalizes text to lowercase and removes punctuation, but query-time preprocessing keeps punctuation.

1. Name two likely symptoms.
2. Identify which layer will appear broken even if the model is unchanged.
3. Propose one immediate fix and one durable fix.

#### Mini-exercise Answers

1. Likely symptoms: lower retrieval relevance and inconsistent citation spans.
2. Retrieval layer will appear broken, though the root issue is preprocessing mismatch.
3. Immediate fix: align query preprocessing to ingestion rules.
   Durable fix: centralize preprocessing into a shared, versioned library used by both ingestion and query paths.

#### Capstone-style system design question

Design a preprocessing service for a multilingual enterprise RAG platform. Define how normalization, segmentation, tokenizer versioning, and offset tracking are handled so retrieval, citation, and cost tracking remain stable over time.

#### Capstone-style Answer Outline

- Use a shared preprocessing service/library with strict versioning.
- Store raw text, normalized text, and offset maps together for traceability.
- Keep tokenizer version pinned per model family and track migration plans.
- Run regression suites on multilingual and OCR-heavy corpora before rollout.
- Expose preprocessing metrics dashboards (token deltas, boundary drift, citation alignment errors).

### 8) Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect preprocessing parity between ingestion and query paths, especially normalization and tokenizer versions.

Why:

Many apparent model or retrieval failures are actually representation mismatches introduced before the model ever sees the text.

### 9) Curiosity Bridge (Mandatory Ending)

Now that you understand how raw text becomes model-ready units, the next question is how those units are learned and compressed into efficient vocabularies.

That leads directly to BPE and SentencePiece intuition, where we explain why token boundaries look strange and how that impacts cost, context, and multilingual behavior.

---

## Module Checkpoint Deep Explanation

### Why This Checkpoint Matters

This checkpoint is the practical bridge between theory and system debugging.

If you understand these three ideas, you stop treating LLMs as magic text boxes:

- attention explains how the model uses context
- long-context and tool-heavy failures explain why bigger context and more tools do not automatically improve reliability
- pretraining, SFT, and alignment explain why models behave the way they do when answering, refusing, following instructions, or using tools

---

## Checkpoint 1: Explain Attention Clearly to a Beginner and to an Engineer

### Beginner Explanation

Attention is how a model decides which earlier words matter most when predicting the next word.

Imagine reading this sentence:

"The doctor told the patient that she should rest."

To understand who "she" refers to, your brain looks back at earlier words. It pays more attention to "patient" than to unrelated words like "told."

LLM attention works in a similar practical way:

- every token looks at other tokens in the context
- it scores which tokens are more relevant
- it uses those relevance scores to build a better representation
- then the model predicts the next token

Simple mental model:

- tokens are words or word pieces
- attention is relevance scoring between tokens
- the model uses attention to decide what context matters right now

Attention is not memory in the human sense. It does not permanently remember everything. It is a mechanism for using the current context window.

### Engineer Explanation

In a transformer, self-attention lets each token compute a context-aware representation by comparing itself with other tokens.

Each token embedding is projected into three vectors:

- Query (Q): what this token is looking for
- Key (K): what this token offers for matching
- Value (V): the information this token contributes if selected

The attention mechanism computes similarity between Q and K, normalizes those scores, and uses them to take a weighted sum of V.

High-level formula:

```text
Attention(Q, K, V) = softmax((QK^T) / sqrt(d_k)) V
```

Meaning in plain engineering terms:

- QK^T scores how relevant every token is to every other token
- dividing by sqrt(d_k) stabilizes the scale of scores
- softmax turns scores into weights
- multiplying by V combines information from relevant tokens

Multi-head attention repeats this process in parallel so different heads can learn different relationships:

- grammar relationships
- entity references
- formatting patterns
- topic links
- instruction relevance
- code structure

Important reality:

Attention does not guarantee the model uses the right information. It only gives the model a mechanism to relate tokens. If the prompt is overloaded, poorly ordered, contradictory, or missing evidence, attention can still focus on the wrong things.

### Practical Debugging Meaning

When a model ignores important context, do not only ask "is the model smart enough?"

Ask:

- Was the relevant evidence inside the context window?
- Was it near the right instruction?
- Was it buried under irrelevant text?
- Were there conflicting instructions?
- Was the context too long for reliable attention use?

---

## Checkpoint 2: Reason About Why a Model Fails Under Long Context or Tool-Heavy Workloads

### Long-Context Failures

A larger context window means the model can receive more tokens in one request.
It does not mean the model will use all tokens equally well.

Long-context failures happen because the model must decide what matters inside a very large information field.

Common failure patterns:

- relevant evidence is present but buried
- early instructions are diluted by later content
- retrieved chunks contain redundant or conflicting information
- conversation history introduces stale assumptions
- the model summarizes instead of reasoning precisely
- citations point to related text but not answer-bearing text

Important distinction:

- Context capacity is about how much text fits.
- Context usability is about whether the model can reliably use the right part.

Why this happens:

- attention has to distribute relevance across many tokens
- similar-looking chunks compete with each other
- irrelevant text increases distraction
- long prompts often contain hidden contradictions
- token budget gets consumed by context instead of answer generation

First debugging step:

Inspect the rendered prompt and mark where the answer-bearing evidence appears. If the key evidence is missing, retrieval failed. If it is present but buried, context packing failed. If it is present and clear but ignored, prompt/model behavior needs testing.

### Tool-Heavy Workload Failures

Tool-heavy systems fail because the model is no longer just generating text. It is participating in a control loop.

The model may need to:

- choose the right tool
- form correct arguments
- interpret tool results
- decide whether another tool call is needed
- avoid repeating calls
- respect permission boundaries
- recover from tool errors

Common failure patterns:

- wrong tool selected
- right tool selected with bad arguments
- tool result misunderstood
- loop repeats without progress
- tool output floods the context
- permissions are assumed instead of checked
- stale tool results are treated as current truth

Why this happens:

- tool descriptions may be ambiguous
- tool schemas may be too loose
- orchestration may not enforce step limits
- errors may be returned as plain text and misread
- the model may optimize for completing the task instead of asking for approval

First debugging step:

Inspect the tool trace: selected tool, arguments, permission decision, result, error handling, and next model step. Tool-heavy failures are often orchestration or schema failures, not model-only failures.

### Production Mental Model

Long-context problems are usually information-selection failures.

Tool-heavy problems are usually control-flow and boundary failures.

The fix is rarely "use a bigger model" by default. Better fixes often include:

- stronger retrieval/reranking
- context compression
- better context ordering
- stricter tool schemas
- permission checks outside the prompt
- step limits and loop guards
- clearer tool-result formatting
- replay-based evaluation

---

## Checkpoint 3: Describe How Pretraining, SFT, and Alignment Shape Model Behavior

### Pretraining

Pretraining is where the model learns broad language and world patterns by predicting the next token across massive text corpora.

What it teaches:

- grammar
- facts and associations
- style patterns
- code patterns
- reasoning traces seen in data
- broad semantic relationships

What it does not fully teach:

- how to follow user instructions reliably
- how to refuse unsafe requests
- how to format answers for a product
- how to use tools safely
- how to obey your business rules

Mental model:

Pretraining creates the raw capability base.

It gives the model knowledge-shaped behavior, but not necessarily product-safe behavior.

### SFT (Supervised Fine-Tuning)

SFT trains the pretrained model on examples of desired input-output behavior.

For example:

- user asks a question -> assistant gives helpful answer
- user asks for JSON -> assistant returns valid JSON
- user asks for explanation -> assistant explains step by step
- user gives instruction -> assistant follows it

What SFT teaches:

- instruction following
- conversational behavior
- formatting discipline
- task-specific response patterns
- better alignment with expected assistant behavior

Mental model:

SFT turns a raw language model into a more useful assistant.

It teaches the model what good responses should look like.

### Alignment

Alignment shapes model behavior toward human preferences, safety rules, and policy boundaries.

This can involve preference optimization, safety training, refusal examples, reward models, human feedback, or other post-training methods.

What alignment teaches:

- helpfulness
- harmlessness
- refusal behavior
- policy compliance
- uncertainty handling
- safer behavior under adversarial or risky requests

Mental model:

Alignment teaches the model what behavior is acceptable, not just what text is likely.

### How They Stack Together

```text
Pretraining -> broad capability
SFT -> instruction-following assistant behavior
Alignment -> safer, preference-shaped, policy-aware behavior
```

Practical example:

If you ask a raw pretrained model: "Summarize this policy for an employee," it may continue text, imitate random formats, or produce less controlled output.

If you ask an SFT model, it is more likely to answer directly and follow the task.

If you ask an aligned model, it is more likely to follow safety boundaries, avoid unsupported claims, and refuse when needed.

### Common Misdiagnosis

Do not say "the model knows the answer, so it should behave correctly."

Knowing and behaving are different.

- Pretraining affects what patterns the model has learned.
- SFT affects how well it follows tasks.
- Alignment affects whether it behaves safely and acceptably.

This is why a smaller tuned model can outperform a larger raw model on a narrow business task. The smaller model may have better behavior for that task even if the larger model has broader raw capability.

---

## Common Mistakes + Debugging

### Mistake 1

- Symptom: model ignores a key fact in a long prompt.
- Likely cause: context packing or attention usability problem, not necessarily missing capability.
- First debugging step: inspect where the key fact appears in the rendered prompt and test with only the relevant evidence.

### Mistake 2

- Symptom: tool-using assistant loops or calls the wrong API.
- Likely cause: orchestration/tool schema issue rather than pure model weakness.
- First debugging step: inspect tool selection trace, arguments, tool result format, and loop guard behavior.

### Mistake 3

- Symptom: model is knowledgeable but does not follow product instructions.
- Likely cause: task behavior is under-specified or not reinforced by SFT-style examples/prompt structure.
- First debugging step: compare output against examples and add structured output constraints or task demonstrations.

---

## Active Recall (Spaced Repetition)

1. What is attention in one beginner-friendly sentence?
2. What do Q, K, and V mean in self-attention?
3. Why does a larger context window not guarantee better answers?
4. Why are tool-heavy workloads often orchestration problems?
5. What is the difference between pretraining and SFT?
6. What does alignment add beyond SFT?

### Active Recall Answers

1. Attention is how a model decides which tokens in the current context matter most for predicting the next token.
2. Query is what a token is looking for, Key is what other tokens offer for matching, and Value is the information contributed when selected.
3. More context increases capacity, but it can also bury useful evidence, add contradictions, and make context selection harder.
4. Because the system must choose tools, pass arguments, interpret results, enforce permissions, and manage control flow.
5. Pretraining learns broad next-token patterns; SFT teaches the model to follow desired task/assistant examples.
6. Alignment shapes behavior toward human preferences, safety policies, refusal behavior, and acceptable conduct.

---

## Practice

### Mini-exercise

A model has a 128k context window. You provide a 90k-token prompt containing the correct answer, but the model still gives a wrong answer.

1. Why can this happen?
2. What are the first three things you inspect?
3. What fix would you try before switching to a larger model?

### Mini-exercise Answers

1. This can happen because the correct evidence may be buried, contradicted, poorly ordered, or diluted by irrelevant context.
2. Inspect rendered prompt ordering, location of answer-bearing evidence, and retrieval/context packing quality.
3. Try context compression, reranking, better chunk selection, moving key evidence closer to the instruction, or reducing irrelevant context.

### Capstone-style system design question

Design a tool-using GenAI assistant that must inspect logs, query a database, and recommend an incident action. Explain how attention, context packing, tool orchestration, and model post-training behavior affect reliability.

### Capstone-style Answer Outline

- Attention/context packing: keep only relevant logs and runbooks; place key evidence near the task.
- Tool orchestration: define strict schemas, step limits, permissions, retries, and result formats.
- Pretraining: gives broad language/code/log-pattern capability.
- SFT: improves instruction following and structured incident response behavior.
- Alignment: improves safety, escalation, refusal, and cautious recommendations under uncertainty.
- Reliability controls: trace every step, replay failed trajectories, and evaluate tool-call correctness separately from final answer quality.

---

## Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect the rendered prompt/context package and the tool trace before blaming the base model.

Why:

Long-context and tool-heavy failures usually begin in context selection, prompt assembly, tool schema, permissions, or orchestration. The model output is often only the final visible symptom.

---

## Curiosity Bridge (Mandatory Ending)

This checkpoint explains why model internals matter for system design.

Attention tells us how context is used, long-context/tool failures show where systems break, and pretraining/SFT/alignment explain why models behave differently even when they look similar from an API call.

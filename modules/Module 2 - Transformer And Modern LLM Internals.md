# Module 2 - Transformer And Modern LLM Internals

This is the evolving knowledge base for Module 2.

## Quick Topic Index

- [Topic 2.1: Text Processing, Tokens, and Context](#topic-21-text-processing-tokens-and-context)
- [Subtopic 2.1.a: Text Normalization, Segmentation, and Token Boundaries](#subtopic-21a-text-normalization-segmentation-and-token-boundaries)
- [Topic 2.2: Transformer Mechanics](#topic-22-transformer-mechanics)
- [Topic 2.3: From Pretraining to Instruction Following](#topic-23-from-pretraining-to-instruction-following)

Covered so far:

- Topic 2.1.a: Text normalization, segmentation, and token boundaries

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

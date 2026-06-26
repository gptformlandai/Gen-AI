# Tradeoff Justification Memo

## Decision

Use a retrieval-first architecture with query rewriting, reranking, citations, and guardrails before answer generation.

## Why This Choice

RAG failures are often caused before the model writes anything. If the right evidence is missing or ranked below a distractor, a better prompt cannot reliably fix the answer. The architecture therefore makes retrieval quality and guardrail decisions visible and measurable.

## Tradeoffs

| Choice | Benefit | Cost |
|---|---|---|
| Query rewriting | Recovers synonym and intent gaps | More retrieval calls and more tuning surface |
| Reranking | Improves top-1 evidence quality | Adds latency and scoring complexity |
| Guardrails before retrieval | Prevents unsafe or unauthorized answers early | Requires role and policy modeling |
| Deterministic evaluator | Easy to debug and regression test | Less realistic than noisy production traffic |
| Layer-based diagnosis | Clear remediation ownership | Requires richer traces and labeled failures |

## Alternatives

| Alternative | Why not first |
|---|---|
| Switch to a larger model | Does not fix missing evidence or unauthorized answering. |
| Prompt-only tuning | Can mask failures without improving retrieval. |
| Fine-tuning | Overkill before measuring retrieval and guardrail quality. |
| Agentic tool use everywhere | Adds orchestration complexity before the core retrieval loop is reliable. |

## Final Position

The chosen design optimizes for debuggability and trust. It is not the simplest demo, but it is the better hiring signal because the tradeoffs, failures, and metrics are visible.


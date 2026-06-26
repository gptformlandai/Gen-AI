# Interview Walkthrough

## 30-Second Summary

I built a RAG reliability case study that starts with a baseline assistant, adds advanced retrieval and guardrails, then debugs a flawed version with layer-based diagnosis. The key result is measurable improvement: Project 4 improved from 76.00% to 100.00%, and Project 9 improved from 58.33% to 100.00% while reducing retrieval failures from 5 to 0.

## System Design Walkthrough

1. Start with the user question and role.
2. Run safety and permission guardrails before retrieval.
3. Rewrite the query for retrieval intent.
4. Retrieve candidates from the corpus.
5. Rerank candidates using lexical, title, tag, and phrase signals.
6. Build an evidence packet with citations.
7. Answer only from evidence or refuse.
8. Log traces and evaluate each row.

## Debugging Walkthrough

1. Observe failed questions.
2. Classify each failure by layer: retrieval, synthesis, guardrail, model, or orchestration.
3. Notice that the expected document was often in top 3 but not rank 1.
4. Form the hypothesis that candidate ranking was the root cause.
5. Add one targeted reranking intervention.
6. Re-run the same evaluation set and compare metrics.

## Likely Deep-Dive Topics

- Why top-1 accuracy matters more than top-3 recall for this answerer.
- How permission-aware refusal changes evaluation design.
- Why prompt tuning was not the first fix.
- How to avoid overfitting reranking features.
- How this would evolve with real embeddings and production telemetry.


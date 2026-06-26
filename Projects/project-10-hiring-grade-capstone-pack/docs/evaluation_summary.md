# Evaluation Summary

## Metrics

| Evaluation | Before | After | Delta |
|---|---:|---:|---:|
| Project 4 pass rate | 76.00% | 100.00% | +24.00% |
| Project 9 pass rate | 58.33% | 100.00% | +41.67% |
| Project 9 top-1 document accuracy | 58.33% | 100.00% | +41.67% |
| Project 9 expected term coverage | 54.55% | 100.00% | +45.45% |
| Project 9 retrieval failures | 5 | 0 | -5 |

## What Improved

Project 4 fixed missed retrieval and unsafe-answer failures across 25 questions.

Project 9 isolated a retrieval-ranking root cause across 12 questions and removed the observed retrieval failures with one targeted reranking intervention.

## Before

The baseline retrieved distractor documents for synonym-heavy questions and sometimes answered requests that should have been refused.

## After

The improved system ranks the expected evidence first, answers with citations, and refuses unsafe or unauthorized requests before generation.

## Evidence Files

- `Projects/project-4-advanced-rag-reranking-guardrails/docs/baseline_vs_advanced.md`
- `Projects/project-9-rag-debugging-case-study/docs/before_after_metrics.md`
- `Projects/project-9-rag-debugging-case-study/docs/failure_cases.md`


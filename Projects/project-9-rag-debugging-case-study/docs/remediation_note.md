# Remediation Note And Remaining Risks

## Intervention

Add a retrieval reranking layer with:

- normalized tokens;
- synonym expansion for operational language;
- title and tag scoring;
- exact phrase boosts for high-signal concepts;
- top-k evidence tracking for diagnosis.

The answer synthesizer is unchanged so that the measured improvement is attributable to retrieval.

## Expected Improvement

The improved retriever should raise top-1 document accuracy and pass rate while reducing retrieval-layer failures.

## Measured Outcome

| Metric | Before | After |
|---|---:|---:|
| Pass rate | 58.33% | 100.00% |
| Top-1 document accuracy | 58.33% | 100.00% |
| Retrieval failures | 5 | 0 |

## Remaining Risks

- The synonym map is hand-authored and will not cover every user phrase.
- The corpus is small and deterministic; production needs larger, noisier evaluation sets.
- Reranking can overfit if features are tuned only to current golden questions.
- This does not address generation quality for long, multi-document synthesis.
- A production system should add trace sampling, regression tests, and periodic failure review.

# Incident Writeup: Baseline RAG Retrieval Quality Regression

## Summary

The Project 3-style baseline RAG assistant answered straightforward support questions, but failed questions that used synonyms, operational phrasing, or terms that appeared in document titles and tags rather than body text.

## Impact

Users received wrong or low-confidence answers for operational questions such as incident triage, analytics export options, webhook retry behavior, and throttling behavior.

## Failure Hypothesis

The dominant failure is in the **retrieval layer**.

The answer synthesizer is intentionally simple and extractive. When the correct document is retrieved at rank 1, it usually includes the expected terms. When it fails, the expected document is often absent from the top candidate or outranked by a lexical distractor.

## Evidence To Collect

- top-1 document accuracy;
- top-3 document recall;
- pass rate;
- missing expected answer terms;
- dominant failure layer per row.

## Observed Evidence

The generated evaluation in `docs/before_after_metrics.md` shows:

- baseline pass rate: 58.33%;
- improved pass rate: 100.00%;
- baseline top-1 document accuracy: 58.33%;
- improved top-1 document accuracy: 100.00%;
- baseline retrieval failures: 5;
- improved retrieval failures: 0.

## Remediation

Add one targeted retrieval intervention: a reranking layer that scores candidates using lexical overlap, title and tag overlap, synonym expansion, phrase boosts, and light morphology normalization.

## Success Criteria

- before-vs-after pass rate improves measurably;
- retrieval failures decrease;
- the answer synthesizer remains unchanged;
- remaining limitations are documented rather than hidden.

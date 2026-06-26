# Failure Analysis

Project 3 should not hide failures. The baseline uses a deterministic extractive synthesizer, so the most likely failures are easy to categorize.

| Failure category | Meaning | Mitigation |
|---|---|---|
| Missed retrieval | The retriever did not return a chunk from the expected topic. | Improve embeddings, chunking, metadata filters, or add hybrid search. |
| Wrong grounding | The answer says something not present in the cited evidence. | Force answer synthesis to use evidence snippets only and run citation checks. |
| Weak answer synthesis | The right evidence was retrieved but the answer omitted required details. | Improve prompt, use a stronger LLM synthesizer, or add reranking. |
| Unexpected refusal | The system refused even though useful evidence was available. | Tune minimum score and overlap thresholds. |
| Expected refusal failed | The system answered an out-of-corpus question. | Raise evidence thresholds and add domain or safety checks. |

## Baseline Limitations

- The local embedding model is lexical with a small synonym map.
- The answer synthesizer is extractive, not conversational.
- The generated corpus is useful for repeatable evaluation but simpler than real enterprise documents.
- The refusal policy depends on retrieval confidence, so broad common words can still cause false positives.

## Current Evaluation Findings

The generated evaluation run currently passes 20 of 22 questions.

Observed failures:

- `eval-009` is an unexpected refusal for report export options. The baseline retrieves weak evidence for the analytics report document, so the confidence threshold blocks the answer.
- `eval-011` is missed retrieval for incident triage. The local hashing embedding model ranks audit-trail content above incident-triage content, showing why a production embedding model or hybrid retrieval matters.

# Cost And Quality Tradeoff Note

Project 4 improves quality by spending more retrieval work per question.

| Layer | Quality gain | Cost paid |
|---|---|---|
| Multi-query retrieval | Recovers documents missed by the first query | More embedding/search calls |
| Candidate dedupe | Keeps repeated variants from flooding the answer | More bookkeeping |
| Reranking | Promotes candidates that match the actual intent | More CPU per candidate |
| Guardrails | Prevents unsafe or unauthorized answers | Extra policy logic before retrieval |

## Why This Is Worth It

The Project 3 baseline passed 20 of 22 comparable questions. The advanced system fixes the two visible baseline failures:

- report export question moves from unexpected refusal to answered;
- incident triage moves from missed retrieval to answered.

The additional cost is acceptable because Project 4 still runs locally and deterministically. In a production LLM-backed system, the same design would increase latency and token cost because each query variant may trigger another retrieval call and a larger evidence packet.

## When Not To Use This

Do not add this complexity for a tiny static FAQ where exact keyword search already works. Start with baseline retrieval, measure failures, then add query rewriting and reranking only where the evidence shows they help.

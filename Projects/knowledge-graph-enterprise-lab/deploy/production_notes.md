# Production Notes

## Ingestion

Use idempotency keys, source snapshots, validation before writes, retries with backoff, and dead-letter queues for failed records.

## Graph Storage

Create ID constraints, tune path-query indexes, use read replicas for analytics, and keep expensive algorithms out of synchronous API paths.

## GraphRAG

Require evidence citations, confidence scores, and failed-case evals. Keep vector retrieval as a fallback, not a replacement for graph retrieval.

## Governance

Allowlist query templates, enforce traversal limits, redact sensitive owner data, and route uncertain LLM extraction through human review.

## Operations

Track node and edge ingestion counts, duplicate detection counts, query latency, retrieval confidence, extraction confidence, and eval pass rate.

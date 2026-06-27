# 21 Production Checklist

## What It Is

A practical checklist for turning this lab into a production knowledge graph platform.

## Checklist

- Stable canonical IDs exist for every source.
- Ingestion is idempotent and records provenance.
- Ontology changes are versioned and reviewed.
- Graph writes use transactions, retries, and timeouts.
- Neo4j or Neptune indexes are created for IDs and key lookups.
- Query templates are allowlisted in API and CLI paths.
- Traversal depth and result-size limits are enforced before handlers run.
- Sensitive owner and incident fields are redacted.
- Entity and relationship confidence thresholds are configured.
- Human review queue handles uncertain merges.
- Vector index records embedding model version.
- GraphRAG responses include evidence, trace, and confidence.
- Golden evals run in CI.
- Backups and restore tests are scheduled.
- Operational runbooks exist for graph DB outage, stale ingestion, and bad extraction batches.

## How To Run

```bash
kg-lab run-evals
kg-lab export-graph --format json
```

## Common Mistakes

- Treating local in-memory behavior as production durability.
- Skipping ontology review.
- Launching GraphRAG without failed-case analysis.

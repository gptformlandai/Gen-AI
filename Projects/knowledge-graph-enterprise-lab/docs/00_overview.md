# 00 Overview

## What It Is

This lab is a local enterprise knowledge graph platform. It models services, APIs, databases, Kafka topics, incidents, runbooks, owners, deployments, lineage, and business capabilities.

## Why It Matters

Operational questions are usually relationship questions. A graph lets you move from "find documents about payments" to "show every service and owner impacted if payments-api fails."

## Where It Appears

- Sample data: `data/raw/`
- Graph build: `src/kg_enterprise_lab/graph/graph_builder.py`
- Query service: `src/kg_enterprise_lab/query/graph_query_service.py`
- GraphRAG: `src/kg_enterprise_lab/graphrag/graphrag_pipeline.py`

## How To Run

```bash
kg-lab ingest-sample-data
kg-lab query-graph --question "Show blast radius for payments-api."
kg-lab run-graphrag --question "Use GraphRAG to explain why provider-search-service may be slow."
```

## How To Extend

Add a new data source under `data/raw/`, map it in `graph_builder.py`, add ontology rules, then add tests.

## Common Mistakes

- Treating the graph as only visualization data.
- Skipping canonical IDs and then losing deduplication.
- Letting arbitrary graph queries bypass allowlists.

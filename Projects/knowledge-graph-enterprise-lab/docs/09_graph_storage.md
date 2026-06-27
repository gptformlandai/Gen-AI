# 09 Graph Storage

## What It Is

Graph storage persists and queries nodes and relationships. This lab uses a custom in-memory repository and includes Neo4j and RDF extension points.

## Why It Matters

Local execution should be fast and testable, while production needs transactions, indexes, retries, and access control.

## Where It Appears

- Local repository: `graph/in_memory_graph.py`
- Neo4j abstraction: `graph/neo4j_repository.py`
- RDF store: `graph/rdf_triple_store.py`

## How To Run

```bash
kg-lab build-graph
kg-lab export-graph --format ttl
```

## How To Extend

Implement the `GraphRepository` protocol for Neo4j, TigerGraph, Neptune, or PostgreSQL-backed graph-like tables.

## Common Mistakes

- No unique constraints on canonical IDs.
- No transaction boundary for batch writes.
- Forgetting retry and timeout behavior.

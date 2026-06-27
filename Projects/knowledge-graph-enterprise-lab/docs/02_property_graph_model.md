# 02 Property Graph Model

## What It Is

A property graph stores labeled nodes and typed relationships, each with properties. Neo4j is the common production example; Cypher is its query language.

## Why It Matters

Property graphs are excellent for service dependency, ownership, lineage, and impact analysis because relationships can carry properties like confidence, provenance, weight, and timestamp.

## Where It Appears

- `GraphNode` and `GraphRelationship`
- `graph/in_memory_graph.py`
- `graph/neo4j_repository.py`
- `query/cypher_templates.py`

## How To Run

```bash
kg-lab export-graph --format json
kg-lab query-graph --question "What services depend on provider-search-service?"
```

## How To Extend

Use `MERGE` semantics for idempotent writes. The local repository uses `upsert_node` and `upsert_relationship`; the Neo4j abstraction generates equivalent Cypher.

## Common Mistakes

- Using `CREATE` for batch ingestion and creating duplicates.
- Not indexing canonical IDs.
- Reversing relationship direction and making blast-radius answers wrong.

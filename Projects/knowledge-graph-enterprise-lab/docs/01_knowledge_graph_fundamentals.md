# 01 Knowledge Graph Fundamentals

## What It Is

A knowledge graph stores entities as nodes and relationships as edges. Nodes have labels like `Service` or `Incident`; edges have types like `DEPENDS_ON` or `DOCUMENTED_BY`.

## Why It Matters

Multi-hop questions need explicit relationships. "Who owns services impacted by this Kafka topic?" requires traversing topic, service, team, owner, and incident relationships.

## Where It Appears

- Node schema: `schemas/node.py`
- Relationship schema: `schemas/relationship.py`
- Repository: `graph/in_memory_graph.py`

## How To Run

```bash
kg-lab query-graph --question "Find shortest path between mobile-app and provider-db."
```

## How To Extend

Add new labels and relationship types in `ontology/ontology_models.py`, then update the graph builder and tests.

## Common Mistakes

- Modeling everything as string properties instead of relationships.
- Ignoring relationship direction.
- Allowing unlimited variable-length paths.

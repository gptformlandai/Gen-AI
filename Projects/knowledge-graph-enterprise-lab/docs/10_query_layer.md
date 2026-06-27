# 10 Query Layer

## What It Is

The query layer converts safe natural-language intents into graph operations and allowlisted templates.

## Why It Matters

Production graph systems must prevent arbitrary expensive traversals. Users need explainable answers, not opaque query strings.

## Where It Appears

- Intent classifier: `query/query_intent_classifier.py`
- Planner: `query/query_planner.py`
- Service: `query/graph_query_service.py`
- Cypher and SPARQL templates: `query/`

## How To Run

```bash
kg-lab query-graph --question "Which service has highest dependency centrality?"
```

## How To Extend

Add a new intent, add an allowlisted template, implement the service handler, and add tests.

## Common Mistakes

- Executing raw LLM-generated Cypher.
- Returning answers without paths or evidence.
- Allowing unbounded variable-length traversal.

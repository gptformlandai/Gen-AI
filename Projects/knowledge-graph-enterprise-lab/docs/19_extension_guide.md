# 19 Extension Guide

## What It Is

This guide explains how to extend the lab without breaking the graph contracts.

## Why It Matters

Knowledge graphs grow through new sources, labels, relationships, and queries. Without a repeatable path, the model becomes inconsistent.

## Where It Appears

- Ontology: `ontology/ontology_models.py`
- Source loading: `ingestion/ingestion_pipeline.py`
- Graph mapping: `graph/graph_builder.py`
- Tests: `tests/`

## How To Run

```bash
kg-lab validate-ontology
kg-lab run-evals
```

## How To Extend

Use this order: ontology change, source data, graph builder, query templates, eval cases, docs.

## Common Mistakes

- Adding query behavior before model validation.
- Forgetting RDF mapping.
- Not adding a failed-case eval.

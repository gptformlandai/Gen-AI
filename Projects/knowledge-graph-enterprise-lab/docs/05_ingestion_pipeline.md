# 05 Ingestion Pipeline

## What It Is

Ingestion loads structured JSON and Markdown architecture notes, then maps them into graph nodes and relationships.

## Why It Matters

Knowledge graphs are only useful when they can be rebuilt consistently from source systems such as service catalogs, schema registries, incident systems, deployment logs, and runbooks.

## Where It Appears

- Loaders: `ingestion/json_loader.py`, `markdown_loader.py`
- Pipeline: `ingestion/ingestion_pipeline.py`
- Mapping: `graph/graph_builder.py`
- Report schema: `schemas/ingestion.py`

## How To Run

```bash
kg-lab ingest-sample-data
kg-lab build-graph
```

`ingest-sample-data` returns source record counts, checksums, document counts, graph counts, and warnings.

## How To Extend

Add a loader for the new source, register it in `RAW_FILES` or a connector, and map records in `build_graph_from_sources`.

## Common Mistakes

- Non-idempotent ingestion.
- Ignoring source refs and provenance.
- Loading data before validation.

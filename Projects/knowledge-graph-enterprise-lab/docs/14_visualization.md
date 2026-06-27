# 14 Visualization

## What It Is

Visualization exports turn graph or subgraph data into UI-ready JSON, Mermaid diagrams, and Graphviz DOT.

## Why It Matters

Dependency, blast-radius, lineage, and incident-correlation views help engineers inspect why the graph answered the way it did.

## Where It Appears

- `visualization/visualization_service.py`
- `visualization/mermaid_exporter.py`
- `visualization/graphviz_exporter.py`
- `visualization/cytoscape_exporter.py`

## How To Run

```bash
kg-lab export-graph --format mermaid --view blast-radius --anchor payments-api
kg-lab export-graph --format dot --view lineage --anchor mobile-app
```

## How To Extend

Add filtered views for business capability, incident correlation, schema lineage, or ownership review.

## Common Mistakes

- Visualizing the entire enterprise graph by default.
- Hiding relationship types.
- Treating visualization as the product instead of an explanation tool.

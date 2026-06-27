# 11 Graph Algorithms

## What It Is

Graph algorithms compute paths, reachability, centrality, connected components, cycles, topological order, blast radius, and similarity.

## Why It Matters

Algorithms turn the graph into operational intelligence: critical services, high-risk dependencies, hidden cycles, and impacted owners.

## Where It Appears

- `algorithms/traversal.py`
- `algorithms/shortest_path.py`
- `algorithms/centrality.py`
- `algorithms/blast_radius.py`
- `algorithms/pagerank.py`
- `algorithms/similarity.py`

## How To Run

```bash
kg-lab run-algorithms
```

The CLI reports degree centrality, highest dependency centrality, PageRank-style scores, components, cycles, and topological order.

## How To Extend

Add weighted edges for latency, traffic, severity, or business criticality, then update path ranking and centrality scoring.

## Common Mistakes

- Treating all relationships as equal.
- Running global algorithms synchronously in request paths.
- Ignoring edge direction.

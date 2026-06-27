# 12 Graph Embeddings

## What It Is

Graph embeddings represent nodes and relationships as vectors so semantic retrieval can complement graph traversal.

## Why It Matters

Graph traversal is precise, but it needs known anchors. Vector retrieval helps when users describe symptoms, error messages, or partial names.

## Where It Appears

- `embeddings/embedding_service.py`
- `embeddings/vector_index.py`
- `embeddings/hybrid_similarity.py`

## How To Run

```bash
kg-lab run-graphrag --question "Which runbook helps with database timeout in provider search?"
```

## How To Extend

Replace `HashingEmbeddingService` with provider embeddings, persist vectors in a vector database, and version embedding model IDs.

## Common Mistakes

- Using vectors as a replacement for graph edges.
- Not re-embedding after ontology or source changes.
- Combining vector and graph scores without explainability.

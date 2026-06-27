# 13 GraphRAG

## What It Is

GraphRAG combines entity linking, graph retrieval, vector retrieval, subgraph context, answer generation, grounding validation, and citations.

## Why It Matters

Many enterprise questions need multi-hop reasoning. GraphRAG grounds answers in explicit relationships, not only semantically similar chunks.

## Where It Appears

- `graphrag/graphrag_pipeline.py`
- `graphrag/entity_linker.py`
- `graphrag/graph_retriever.py`
- `graphrag/vector_retriever.py`
- `graphrag/hybrid_retriever.py`
- `graphrag/grounding_validator.py`

## How To Run

```bash
kg-lab run-graphrag --question "Use GraphRAG to explain why provider-search-service may be slow."
```

## How To Extend

Swap `MockAnswerGenerator` for an LLM adapter with structured prompts, evidence citation requirements, and answer-level evaluation. Keep graph, vector, and hybrid evidence visible in the response trace.

## Common Mistakes

- Letting the LLM invent graph facts.
- Omitting entity-linking confidence.
- Returning an answer without the retrieved subgraph.

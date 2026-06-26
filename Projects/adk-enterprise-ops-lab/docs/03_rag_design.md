# RAG Design

## What It Is

Local runbook retrieval with document loading, chunking, embeddings, hybrid scoring, top-k filtering, source tracking, and grounded generation.

## Where It Appears

- `rag/document_loader.py`
- `rag/chunker.py`
- `rag/vector_store.py`
- `rag/retriever.py`
- `tools/rag_tools.py`

## Why It Matters

Incident agents should answer from runbooks before inventing remediation steps.

## Extend It

Replace `LocalVectorStore` with Vertex AI RAG Engine or Vertex AI Search in `rag/vertex_rag_extension.py`.


# Vector Store Tradeoff Memo

## Decision

Project 2 starts with an in-memory vector store plus two retrieval modes:

- exact cosine search over all filtered chunks;
- approximate search using random-hyperplane locality-sensitive hashing.

## Why This Architecture

The goal of this project is to learn retrieval mechanics, not to hide them behind a managed vector database. Keeping the index local makes these concepts visible:

- how chunks are created;
- how embeddings are normalized;
- how metadata filters affect the candidate set;
- why exact search is reliable but expensive;
- how ANN search can miss relevant results.

## Tradeoff

| Choice | Benefit | Cost |
|---|---|---|
| Exact search | Highest recall, easiest to debug | Scores every candidate, so it does not scale well |
| LSH ANN | Demonstrates approximate retrieval and candidate pruning | Lower recall and unstable behavior on small datasets |
| Local hashing embeddings | No API key, deterministic tests | Lower semantic quality than real embedding models |
| Metadata filters before ranking | More precise and safer retrieval | Bad filters can hide relevant documents |

## Production Upgrade Path

1. Replace hashing embeddings with a production embedding model.
2. Persist vectors in FAISS, Qdrant, Milvus, pgvector, Weaviate, or Chroma.
3. Add hybrid search for exact identifiers, error codes, and rare business terms.
4. Add reranking for the top 20 to 100 candidates.
5. Add tenant and permission filters before vector ranking.

## Expected Failure Modes

- Query uses a synonym that is not in the local synonym map.
- ANN bucket does not include the best exact-search neighbor.
- Metadata filter excludes the correct document.
- Chunking splits context so the useful answer spans multiple chunks.
- Repeated template language makes many documents look similarly relevant.

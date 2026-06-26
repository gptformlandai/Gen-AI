# Project 2: Semantic Search Lab

This project implements a small but non-trivial semantic search system over a generated support knowledge-base corpus.

The goal is to prove retrieval fundamentals from Modules 4 and 5:

- document ingestion
- chunking
- embedding generation
- exact vector search
- approximate nearest-neighbor search
- metadata filters
- labeled query evaluation

This is intentionally not a black-box vector database. The first version keeps the vector store local and readable so the retrieval mechanism is easy to inspect.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| Document ingestion and chunking | `corpus.py` loads JSONL documents and chunks text with overlap. |
| Embedding pipeline | `embeddings.py` implements a deterministic hashing TF-IDF embedding model. |
| Exact similarity baseline | `vector_store.py` scores every chunk with cosine similarity. |
| ANN retrieval option | `ann.py` implements a small random-hyperplane LSH index. |
| Metadata filters | CLI and search APIs accept filters like `product=finance`. |
| At least 10 labeled queries | `data/labeled_queries.json` contains 12 labeled queries. |

## Architecture

```text
documents.jsonl
    |
    v
load documents
    |
    v
chunk documents
    |
    v
fit embedding model
    |
    v
embed chunks
    |
    +--> exact search: score every filtered chunk
    |
    +--> ANN search: LSH bucket candidates, then score candidates
```

## What This Recalls From The Modules

- **Module 4: Embeddings** - embeddings convert text into vectors where related text should be close under a similarity metric.
- **Module 5: Vector search** - exact search is simple and reliable but expensive at scale; approximate search trades recall for speed.
- **Metadata filtering** - vector similarity is not enough. Production retrieval often narrows by tenant, product, time, permission, region, or document type before ranking.
- **Evaluation discipline** - retrieval quality should be measured with labeled queries, not judged by a single nice-looking demo.

## Folder Layout

```text
Projects/project-2-semantic-search-lab/
  data/
    labeled_queries.json
  docs/
    vector_store_tradeoff_memo.md
  src/semantic_search_lab/
    ann.py
    chunking.py
    cli.py
    corpus.py
    embeddings.py
    evaluation.py
    sample_data.py
    schemas.py
    vector_store.py
  tests/
    test_semantic_search.py
```

## Run Locally

```bash
cd Projects/project-2-semantic-search-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Generate the sample corpus:

```bash
semantic-search-lab build-corpus --output data/corpus.jsonl --count 360
```

Run exact search:

```bash
semantic-search-lab search \
  --corpus data/corpus.jsonl \
  --query "forgot login password reset" \
  --mode exact \
  --k 5
```

Run ANN search:

```bash
semantic-search-lab search \
  --corpus data/corpus.jsonl \
  --query "forgot login password reset" \
  --mode ann \
  --k 5
```

Run search with a metadata filter:

```bash
semantic-search-lab search \
  --corpus data/corpus.jsonl \
  --query "exception report mismatched transactions" \
  --filter product=finance \
  --mode exact
```

Evaluate exact versus ANN retrieval:

```bash
semantic-search-lab evaluate \
  --corpus data/corpus.jsonl \
  --queries data/labeled_queries.json \
  --output docs/retrieval_comparison.md
```

## Tests

```bash
cd Projects/project-2-semantic-search-lab
pytest
```

The tests use the local deterministic embedding model, so they do not need an API key.

## Design Note

The embedding model here is not meant to beat production embedding APIs. It is a learning scaffold:

- hashing gives fixed-size vectors without training;
- IDF weighting makes rare terms matter more;
- synonym expansion makes simple semantic matches possible;
- exact and approximate retrieval can be compared without external services.

For a production version, the first upgrade would be replacing `HashingTfidfEmbeddingModel` with OpenAI, Cohere, Voyage, or a local sentence-transformer embedding model while keeping the same retrieval and evaluation shape.

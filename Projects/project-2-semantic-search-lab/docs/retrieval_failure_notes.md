# Retrieval Failure Notes

The labeled set currently passes because it is intentionally friendly: each query contains several topic-specific terms and most queries include a metadata filter. That is useful for a baseline, but it is not the same as production retrieval quality.

## Failure 1: ANN Can Miss The Best Neighbor

**Observed during smoke testing:** a narrow LSH candidate set returned incident-triage chunks for `forgot login password reset` because those chunks included the word `recovery`, while the best password-reset chunks were outside the first inspected buckets.

**Why it happens:** ANN search does not score every vector. If the relevant vector is outside the inspected bucket neighborhood, it cannot be returned.

**Mitigation added:** `LSHApproximateIndex` now widens buckets when the top approximate score is very low, and falls back to the full filtered set at maximum distance.

## Failure 2: Metadata Filters Can Hide Relevant Documents

Example: a good query about CSV reconciliation with `product=support` will not return finance reconciliation documents, even if the text match is strong.

**Why it happens:** filters run before ranking. This is correct for tenant, permission, or product boundaries, but dangerous when the filter is wrong.

**Mitigation:** log filters with every query and evaluate filtered and unfiltered search separately.

## Failure 3: Template Repetition Creates Ties

The generated corpus intentionally repeats operational language across many documents. This can produce equal or near-equal scores for multiple chunks in the same topic.

**Why it happens:** repeated phrases like `traceable status` and `searchable metadata` appear everywhere, so they do not help distinguish documents.

**Mitigation:** IDF weighting reduces the impact of common terms, but a better production system should use stronger embeddings and reranking.

## Failure 4: Weak Semantic Coverage

The local embedding model only knows the synonym map in `embeddings.py`. A query such as `can't get into my profile` may not map cleanly to password reset.

**Why it happens:** hashing TF-IDF is lexical with a small semantic patch. Real embedding models learn broader paraphrase relationships.

**Mitigation:** replace the local model with a production embedding API or a sentence-transformer model, then rerun the same labeled query evaluation.

## Failure 5: Chunk Boundaries Can Split Evidence

This corpus uses short documents, so most documents produce one chunk. Longer real documents can split a question's answer across chunks.

**Why it happens:** the retriever scores chunks independently.

**Mitigation:** tune chunk size and overlap, add parent-document retrieval, or use a reranker over neighboring chunks.

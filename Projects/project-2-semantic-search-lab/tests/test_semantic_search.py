from __future__ import annotations

import json
from pathlib import Path

from semantic_search_lab.ann import LSHApproximateIndex
from semantic_search_lab.chunking import chunk_documents
from semantic_search_lab.evaluation import evaluate_queries, read_labeled_queries
from semantic_search_lab.sample_data import build_sample_documents
from semantic_search_lab.vector_store import InMemoryVectorStore


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_test_store(document_count: int = 360) -> InMemoryVectorStore:
    documents = build_sample_documents(count=document_count)
    chunks = chunk_documents(documents)
    return InMemoryVectorStore.from_chunks(chunks)


def test_generated_corpus_meets_recommended_size() -> None:
    documents = build_sample_documents(count=360)
    chunks = chunk_documents(documents)

    assert len(documents) == 360
    assert len(chunks) >= 300


def test_exact_search_finds_password_reset_topic() -> None:
    store = build_test_store()
    hits = store.search(
        "forgot login password reset account recovery",
        filters={"product": "identity"},
        k=5,
    )

    assert hits
    assert hits[0].metadata["topic"] == "password_reset"


def test_metadata_filter_controls_candidate_set() -> None:
    store = build_test_store()
    finance_hits = store.search(
        "exception report mismatched transactions",
        filters={"product": "finance"},
        k=5,
    )
    support_hits = store.search(
        "exception report mismatched transactions",
        filters={"product": "support"},
        k=5,
    )

    assert finance_hits[0].metadata["topic"] == "csv_reconciliation"
    assert all(hit.metadata["product"] == "support" for hit in support_hits)


def test_labeled_query_file_has_at_least_ten_queries() -> None:
    payload = json.loads((DATA_DIR / "labeled_queries.json").read_text(encoding="utf-8"))

    assert len(payload) >= 10


def test_evaluation_compares_exact_and_ann() -> None:
    store = build_test_store()
    ann_index = LSHApproximateIndex(store)
    queries = read_labeled_queries(DATA_DIR / "labeled_queries.json")
    summary = evaluate_queries(store, ann_index, queries, k=5)

    assert summary.total_queries >= 10
    assert summary.exact_hit_rate >= 0.8
    assert 0.0 <= summary.ann_hit_rate <= 1.0
    assert len(summary.rows) == summary.total_queries


def test_ann_search_returns_ranked_hits() -> None:
    store = build_test_store()
    ann_index = LSHApproximateIndex(store)
    hits = ann_index.search(
        "manager approve supplier onboarding tax verification",
        filters={"product": "procurement"},
        k=5,
    )

    assert hits
    assert all(hit.metadata["product"] == "procurement" for hit in hits)

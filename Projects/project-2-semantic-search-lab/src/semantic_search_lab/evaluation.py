from __future__ import annotations

import json
from pathlib import Path

from semantic_search_lab.ann import LSHApproximateIndex
from semantic_search_lab.chunking import chunk_documents
from semantic_search_lab.corpus import read_jsonl_documents
from semantic_search_lab.schemas import EvaluationRow, EvaluationSummary, LabeledQuery, SearchHit
from semantic_search_lab.vector_store import InMemoryVectorStore


def read_labeled_queries(path: Path) -> list[LabeledQuery]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [LabeledQuery.model_validate(item) for item in payload]


def is_topic_hit(hits: list[SearchHit], relevant_topics: list[str]) -> bool:
    return any(hit.metadata.get("topic") in relevant_topics for hit in hits)


def top_topic(hits: list[SearchHit]) -> str:
    if not hits:
        return "none"
    return hits[0].metadata.get("topic", "unknown")


def top_chunk_id(hits: list[SearchHit]) -> str:
    if not hits:
        return "none"
    return hits[0].chunk_id


def evaluate_queries(
    store: InMemoryVectorStore,
    ann_index: LSHApproximateIndex,
    queries: list[LabeledQuery],
    k: int = 5,
) -> EvaluationSummary:
    rows: list[EvaluationRow] = []
    for labeled_query in queries:
        exact_hits = store.search(labeled_query.query, k=k, filters=labeled_query.filters)
        ann_hits = ann_index.search(labeled_query.query, k=k, filters=labeled_query.filters)
        rows.append(
            EvaluationRow(
                query_id=labeled_query.id,
                query=labeled_query.query,
                filters=labeled_query.filters,
                exact_hit=is_topic_hit(exact_hits, labeled_query.relevant_topics),
                ann_hit=is_topic_hit(ann_hits, labeled_query.relevant_topics),
                exact_top_chunk_id=top_chunk_id(exact_hits),
                ann_top_chunk_id=top_chunk_id(ann_hits),
                exact_top_topic=top_topic(exact_hits),
                ann_top_topic=top_topic(ann_hits),
                exact_top_score=exact_hits[0].score if exact_hits else 0.0,
                ann_top_score=ann_hits[0].score if ann_hits else 0.0,
            )
        )

    total = max(len(rows), 1)
    return EvaluationSummary(
        total_queries=len(rows),
        exact_hit_rate=sum(1 for row in rows if row.exact_hit) / total,
        ann_hit_rate=sum(1 for row in rows if row.ann_hit) / total,
        rows=rows,
    )


def build_store_from_corpus(corpus_path: Path) -> InMemoryVectorStore:
    documents = read_jsonl_documents(corpus_path)
    chunks = chunk_documents(documents)
    return InMemoryVectorStore.from_chunks(chunks)


def render_markdown_summary(summary: EvaluationSummary) -> str:
    lines = [
        "# Retrieval Comparison",
        "",
        f"- Total queries: {summary.total_queries}",
        f"- Exact hit rate @5: {summary.exact_hit_rate:.2%}",
        f"- ANN hit rate @5: {summary.ann_hit_rate:.2%}",
        "",
        "| Query | Filters | Exact hit | ANN hit | Exact top topic | ANN top topic |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in summary.rows:
        filters = ", ".join(f"{key}={value}" for key, value in row.filters.items()) or "none"
        lines.append(
            f"| {row.query_id} | {filters} | {row.exact_hit} | {row.ann_hit} | "
            f"{row.exact_top_topic} | {row.ann_top_topic} |"
        )

    lines.extend(
        [
            "",
            "## Top Result Differences",
            "",
            "| Query | Exact top chunk | Exact score | ANN top chunk | ANN score | Same top chunk |",
            "|---|---|---:|---|---:|---:|",
        ]
    )
    for row in summary.rows:
        lines.append(
            f"| {row.query_id} | `{row.exact_top_chunk_id}` | {row.exact_top_score:.3f} | "
            f"`{row.ann_top_chunk_id}` | {row.ann_top_score:.3f} | "
            f"{row.exact_top_chunk_id == row.ann_top_chunk_id} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Exact search is the quality baseline because it evaluates every filtered chunk.",
            "- ANN search may return a different top topic because LSH only scores bucket candidates.",
            "- A failed filtered query can mean the filter removed the relevant document, not that embeddings failed.",
        ]
    )
    return "\n".join(lines) + "\n"

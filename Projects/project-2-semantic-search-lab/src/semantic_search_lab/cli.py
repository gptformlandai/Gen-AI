from __future__ import annotations

import argparse
import json
from pathlib import Path

from semantic_search_lab.ann import LSHApproximateIndex
from semantic_search_lab.corpus import read_jsonl_documents, write_jsonl_documents
from semantic_search_lab.evaluation import (
    build_store_from_corpus,
    evaluate_queries,
    read_labeled_queries,
    render_markdown_summary,
)
from semantic_search_lab.sample_data import build_sample_documents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 2 semantic search lab.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_corpus = subparsers.add_parser("build-corpus", help="Generate the sample support corpus.")
    build_corpus.add_argument("--output", type=Path, default=Path("data/corpus.jsonl"))
    build_corpus.add_argument("--count", type=int, default=360)

    search = subparsers.add_parser("search", help="Search the corpus.")
    search.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    search.add_argument("--query", required=True)
    search.add_argument("--mode", choices=["exact", "ann"], default="exact")
    search.add_argument("--k", type=int, default=5)
    search.add_argument(
        "--filter",
        action="append",
        default=[],
        help="Metadata filter in key=value form. Can be provided more than once.",
    )

    evaluate = subparsers.add_parser("evaluate", help="Evaluate exact vs ANN retrieval.")
    evaluate.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    evaluate.add_argument("--queries", type=Path, default=Path("data/labeled_queries.json"))
    evaluate.add_argument("--output", type=Path, default=Path("docs/retrieval_comparison.md"))
    evaluate.add_argument("--k", type=int, default=5)
    return parser


def parse_filters(raw_filters: list[str]) -> dict[str, str]:
    filters: dict[str, str] = {}
    for raw_filter in raw_filters:
        if "=" not in raw_filter:
            raise SystemExit(f"Invalid filter '{raw_filter}'. Use key=value.")
        key, value = raw_filter.split("=", 1)
        filters[key.strip()] = value.strip()
    return filters


def ensure_corpus(path: Path) -> None:
    """Generate a corpus on first use so the CLI is friendly in a fresh checkout."""

    if path.exists():
        return
    write_jsonl_documents(path, build_sample_documents())


def command_build_corpus(args: argparse.Namespace) -> None:
    documents = build_sample_documents(count=args.count)
    write_jsonl_documents(args.output, documents)
    print(f"Wrote {len(documents)} documents to {args.output}")


def command_search(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    documents = read_jsonl_documents(args.corpus)
    store = build_store_from_corpus(args.corpus)
    filters = parse_filters(args.filter)
    if args.mode == "exact":
        hits = store.search(args.query, k=args.k, filters=filters)
    else:
        hits = LSHApproximateIndex(store).search(args.query, k=args.k, filters=filters)

    print(
        json.dumps(
            {
                "documents": len(documents),
                "chunks": len(store.chunks),
                "mode": args.mode,
                "query": args.query,
                "filters": filters,
                "hits": [hit.model_dump(mode="json") for hit in hits],
            },
            indent=2,
        )
    )


def command_evaluate(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    store = build_store_from_corpus(args.corpus)
    ann_index = LSHApproximateIndex(store)
    queries = read_labeled_queries(args.queries)
    summary = evaluate_queries(store, ann_index, queries, k=args.k)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown_summary(summary), encoding="utf-8")
    print(json.dumps(summary.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "build-corpus":
        command_build_corpus(args)
    elif args.command == "search":
        command_search(args)
    elif args.command == "evaluate":
        command_evaluate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

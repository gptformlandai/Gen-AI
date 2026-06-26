from __future__ import annotations

import argparse
import json
from pathlib import Path

from advanced_rag_assistant.corpus import write_jsonl_documents
from advanced_rag_assistant.evaluation import (
    build_store_from_corpus,
    compare_systems,
    read_evaluation_questions,
    render_comparison,
)
from advanced_rag_assistant.rag import AdvancedRagAssistant, BaselineRagAssistant
from advanced_rag_assistant.sample_data import build_sample_documents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 4 advanced RAG with reranking and guardrails.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_corpus = subparsers.add_parser("build-corpus")
    build_corpus.add_argument("--output", type=Path, default=Path("data/corpus.jsonl"))
    build_corpus.add_argument("--count", type=int, default=240)

    ask = subparsers.add_parser("ask")
    ask.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    ask.add_argument("--question", required=True)
    ask.add_argument("--role", default="employee")

    compare = subparsers.add_parser("compare")
    compare.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    compare.add_argument("--questions", type=Path, default=Path("data/evaluation_questions.json"))
    compare.add_argument("--output", type=Path, default=Path("docs/baseline_vs_advanced.md"))
    return parser


def ensure_corpus(path: Path) -> None:
    if not path.exists():
        write_jsonl_documents(path, build_sample_documents())


def command_build_corpus(args: argparse.Namespace) -> None:
    documents = build_sample_documents(count=args.count)
    write_jsonl_documents(args.output, documents)
    print(f"Wrote {len(documents)} documents to {args.output}")


def command_ask(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    store = build_store_from_corpus(args.corpus)
    result = AdvancedRagAssistant(store).answer(args.question, user_role=args.role)
    print(json.dumps(result.model_dump(mode="json"), indent=2))


def command_compare(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    store = build_store_from_corpus(args.corpus)
    summary = compare_systems(
        BaselineRagAssistant(store),
        AdvancedRagAssistant(store),
        read_evaluation_questions(args.questions),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_comparison(summary), encoding="utf-8")
    print(json.dumps(summary.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "build-corpus":
        command_build_corpus(args)
    elif args.command == "ask":
        command_ask(args)
    elif args.command == "compare":
        command_compare(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

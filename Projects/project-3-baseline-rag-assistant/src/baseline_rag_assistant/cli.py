from __future__ import annotations

import argparse
import json
from pathlib import Path

from baseline_rag_assistant.corpus import write_jsonl_documents
from baseline_rag_assistant.evaluation import (
    build_assistant_from_corpus,
    evaluate_questions,
    read_evaluation_questions,
    render_citation_examples,
    render_evaluation_sheet,
)
from baseline_rag_assistant.sample_data import build_sample_documents
from baseline_rag_assistant.tracing import JsonlTraceLogger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 3 baseline RAG assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_corpus = subparsers.add_parser("build-corpus", help="Generate the sample RAG corpus.")
    build_corpus.add_argument("--output", type=Path, default=Path("data/corpus.jsonl"))
    build_corpus.add_argument("--count", type=int, default=240)

    ask = subparsers.add_parser("ask", help="Ask a grounded question.")
    ask.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    ask.add_argument("--question", required=True)
    ask.add_argument("--trace", type=Path, default=Path("docs/traces/last_run.jsonl"))

    evaluate = subparsers.add_parser("evaluate", help="Run the evaluation set.")
    evaluate.add_argument("--corpus", type=Path, default=Path("data/corpus.jsonl"))
    evaluate.add_argument("--questions", type=Path, default=Path("data/evaluation_questions.json"))
    evaluate.add_argument("--output", type=Path, default=Path("docs/evaluation_sheet.md"))
    evaluate.add_argument("--citations-output", type=Path, default=Path("docs/citation_examples.md"))
    return parser


def ensure_corpus(path: Path) -> None:
    if path.exists():
        return
    write_jsonl_documents(path, build_sample_documents())


def command_build_corpus(args: argparse.Namespace) -> None:
    documents = build_sample_documents(count=args.count)
    write_jsonl_documents(args.output, documents)
    print(f"Wrote {len(documents)} documents to {args.output}")


def command_ask(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    assistant = build_assistant_from_corpus(args.corpus)
    result = assistant.answer(args.question, trace_logger=JsonlTraceLogger(args.trace))
    print(json.dumps(result.model_dump(mode="json"), indent=2))


def command_evaluate(args: argparse.Namespace) -> None:
    ensure_corpus(args.corpus)
    assistant = build_assistant_from_corpus(args.corpus)
    questions = read_evaluation_questions(args.questions)
    answers = [assistant.answer(question.question) for question in questions]
    summary = evaluate_questions(assistant, questions)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_evaluation_sheet(summary), encoding="utf-8")
    args.citations_output.parent.mkdir(parents=True, exist_ok=True)
    args.citations_output.write_text(render_citation_examples(answers), encoding="utf-8")
    print(json.dumps(summary.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "build-corpus":
        command_build_corpus(args)
    elif args.command == "ask":
        command_ask(args)
    elif args.command == "evaluate":
        command_evaluate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

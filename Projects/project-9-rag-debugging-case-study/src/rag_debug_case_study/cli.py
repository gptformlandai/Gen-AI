from __future__ import annotations

import argparse
import json
from pathlib import Path

from rag_debug_case_study.assistant import RagDebugAssistant
from rag_debug_case_study.evaluation import compare, read_questions, render_failures, render_metrics
from rag_debug_case_study.sample_data import DOCUMENTS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 9 RAG debugging case study.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask")
    ask.add_argument("--mode", choices=["baseline", "improved"], default="improved")
    ask.add_argument("--question", required=True)

    evaluation = subparsers.add_parser("evaluate")
    evaluation.add_argument("--questions", type=Path, default=Path("data/evaluation_questions.json"))
    evaluation.add_argument("--output", type=Path, default=Path("docs/before_after_metrics.md"))
    evaluation.add_argument("--failures-output", type=Path, default=Path("docs/failure_cases.md"))
    evaluation.add_argument("--json-output", type=Path)
    return parser


def command_ask(args: argparse.Namespace) -> None:
    assistant = RagDebugAssistant(DOCUMENTS, mode=args.mode)
    answer = assistant.answer(args.question)
    print(json.dumps(answer.model_dump(mode="json"), indent=2))


def command_evaluate(args: argparse.Namespace) -> None:
    questions = read_questions(args.questions)
    comparison = compare(questions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.failures_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_metrics(comparison), encoding="utf-8")
    args.failures_output.write_text(render_failures(comparison), encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(comparison.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps(comparison.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "ask":
        command_ask(args)
    elif args.command == "evaluate":
        command_evaluate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()


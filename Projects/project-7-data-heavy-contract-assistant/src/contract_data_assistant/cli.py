from __future__ import annotations

import argparse
import json
from pathlib import Path

from contract_data_assistant.evaluation import (
    build_assistant_from_directory,
    evaluate,
    read_evaluation_questions,
    render_evaluation,
)
from contract_data_assistant.parser import load_raw_documents, parse_document
from contract_data_assistant.sample_data import SAMPLE_DOCUMENTS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 7 data-heavy contract assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_samples = subparsers.add_parser("build-samples")
    build_samples.add_argument("--output", type=Path, default=Path("data/contracts"))

    inspect = subparsers.add_parser("inspect")
    inspect.add_argument("--docs", type=Path, default=Path("data/contracts"))
    inspect.add_argument("--output", type=Path)

    ask = subparsers.add_parser("ask")
    ask.add_argument("--docs", type=Path, default=Path("data/contracts"))
    ask.add_argument("--question", required=True)

    eval_parser = subparsers.add_parser("evaluate")
    eval_parser.add_argument("--docs", type=Path, default=Path("data/contracts"))
    eval_parser.add_argument("--questions", type=Path, default=Path("data/evaluation_questions.json"))
    eval_parser.add_argument("--output", type=Path, default=Path("docs/evaluation_results.md"))
    return parser


def command_build_samples(args: argparse.Namespace) -> None:
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, text in SAMPLE_DOCUMENTS.items():
        (args.output / filename).write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Wrote {len(SAMPLE_DOCUMENTS)} sample contracts to {args.output}")


def ensure_samples(directory: Path) -> None:
    if list(directory.glob("*.md")):
        return
    command_build_samples(argparse.Namespace(output=directory))


def command_inspect(args: argparse.Namespace) -> None:
    ensure_samples(args.docs)
    parsed = [parse_document(raw) for raw in load_raw_documents(args.docs)]
    payload = [document.model_dump(mode="json") for document in parsed]
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)


def command_ask(args: argparse.Namespace) -> None:
    ensure_samples(args.docs)
    assistant = build_assistant_from_directory(args.docs)
    answer = assistant.answer(args.question)
    print(json.dumps(answer.model_dump(mode="json"), indent=2))


def command_evaluate(args: argparse.Namespace) -> None:
    ensure_samples(args.docs)
    assistant = build_assistant_from_directory(args.docs)
    questions = read_evaluation_questions(args.questions)
    summary = evaluate(assistant, questions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_evaluation(summary), encoding="utf-8")
    print(json.dumps(summary.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "build-samples":
        command_build_samples(args)
    elif args.command == "inspect":
        command_inspect(args)
    elif args.command == "ask":
        command_ask(args)
    elif args.command == "evaluate":
        command_evaluate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

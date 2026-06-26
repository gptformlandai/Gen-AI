from __future__ import annotations

import argparse
import json
from pathlib import Path

from structured_output_assistant.llm import LangChainRequirementsModel, RuleBasedRequirementsModel
from structured_output_assistant.workflow import run_requirements_assistant


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a messy feature request into a validated requirements JSON object."
    )
    parser.add_argument("--input", help="Raw stakeholder request.")
    parser.add_argument("--file", type=Path, help="Path to a text file containing the request.")
    parser.add_argument(
        "--provider",
        choices=["rule", "openai"],
        default="rule",
        help="Use the deterministic local model or a LangChain/OpenAI chat model.",
    )
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name for --provider openai.")
    parser.add_argument("--max-retries", type=int, default=1, help="Number of schema repair attempts.")
    return parser


def read_request(args: argparse.Namespace) -> str:
    if args.file:
        return args.file.read_text(encoding="utf-8")
    if args.input:
        return args.input
    raise SystemExit("Provide either --input or --file.")


def main() -> None:
    args = build_parser().parse_args()
    model = (
        LangChainRequirementsModel(model=args.model)
        if args.provider == "openai"
        else RuleBasedRequirementsModel()
    )
    result = run_requirements_assistant(
        read_request(args),
        model=model,
        max_retries=args.max_retries,
    )
    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()

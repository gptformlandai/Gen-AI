from __future__ import annotations

import argparse
from pathlib import Path

from capstone_pack_validator.validator import validate_pack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the Project 10 capstone asset pack.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--root", type=Path, default=Path("."))
    validate.add_argument("--output", type=Path)
    return parser


def command_validate(args: argparse.Namespace) -> None:
    report = validate_pack(args.root)
    markdown = report.to_markdown()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    print(markdown)
    if not report.passed:
        raise SystemExit(1)


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "validate":
        command_validate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()


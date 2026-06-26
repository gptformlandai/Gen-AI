from __future__ import annotations

import argparse
import json

from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.incident import IncidentRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enterprise Operations Intelligence Agent lab.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run")
    run.add_argument("--query", required=True)
    run.add_argument("--user-id", default="local-user")
    run.add_argument("--session-id", default="local-session")
    run.add_argument("--debug", action="store_true")

    demo = subparsers.add_parser("demo")
    demo.add_argument("--query", default="Investigate high latency in payments-api after last deployment.")
    return parser


def command_run(args: argparse.Namespace) -> None:
    response = EnterpriseOpsRunner().run(
        IncidentRequest(query=args.query, user_id=args.user_id, session_id=args.session_id, debug=args.debug)
    )
    print(json.dumps(response.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command in {"run", "demo"}:
        command_run(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()


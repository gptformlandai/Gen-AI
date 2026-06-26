from __future__ import annotations

import argparse
import json
from pathlib import Path

from mcp_change_workflow.mcp_gateway import LocalMCPGateway
from mcp_change_workflow.schemas import ChangeRequest
from mcp_change_workflow.workflow import run_change_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 6 MCP-enabled change workflow.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run")
    run.add_argument("--summary", required=True)
    run.add_argument("--environment", choices=["dev", "staging", "production"], default="staging")
    run.add_argument("--requester", default="unknown@example.com")
    run.add_argument("--approved", action="store_true")
    run.add_argument("--simulate-slow-risk-ms", type=int, default=0)
    run.add_argument("--output", type=Path)

    inspect = subparsers.add_parser("inspect")
    return parser


def command_run(args: argparse.Namespace) -> None:
    request = ChangeRequest(
        summary=args.summary,
        environment=args.environment,
        requester=args.requester,
        approved=args.approved,
    )
    result = run_change_workflow(
        request,
        gateway=LocalMCPGateway(simulate_slow_risk_ms=args.simulate_slow_risk_ms),
    )
    payload = result.model_dump(mode="json")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


def command_inspect() -> None:
    gateway = LocalMCPGateway()
    payload = {
        "resources": [resource.model_dump(mode="json") for resource in gateway.list_resources()],
        "tools": [tool.model_dump(mode="json") for tool in gateway.list_tools()],
    }
    print(json.dumps(payload, indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        command_run(args)
    elif args.command == "inspect":
        command_inspect()
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

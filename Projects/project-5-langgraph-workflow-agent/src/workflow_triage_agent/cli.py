from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_triage_agent.workflow import run_triage_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 5 LangGraph workflow triage agent.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run a workflow triage request.")
    run.add_argument("--request", required=True)
    run.add_argument("--requester", default="employee")
    run.add_argument("--decision", choices=["approved", "rejected", "pending", ""], default="")
    run.add_argument("--simulate-policy-failures", type=int, default=0)
    run.add_argument("--max-policy-retries", type=int, default=1)
    run.add_argument("--trace-output", type=Path)
    return parser


def command_run(args: argparse.Namespace) -> None:
    result = run_triage_workflow(
        request=args.request,
        requester=args.requester,
        human_decision=args.decision,
        simulate_policy_failures=args.simulate_policy_failures,
        max_policy_retries=args.max_policy_retries,
    )
    payload = result.model_dump(mode="json")
    if args.trace_output:
        args.trace_output.parent.mkdir(parents=True, exist_ok=True)
        args.trace_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        command_run(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

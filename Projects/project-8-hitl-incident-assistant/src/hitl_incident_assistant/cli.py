from __future__ import annotations

import argparse
import json
from pathlib import Path

from hitl_incident_assistant.evaluation import evaluate, read_evaluation_cases, render_evaluation
from hitl_incident_assistant.schemas import IncidentReport, IncidentState
from hitl_incident_assistant.storage import IncidentStore
from hitl_incident_assistant.workflow import IncidentWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project 8 human-in-the-loop incident assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    add_report_args(start)
    start.add_argument("--state-dir", type=Path, default=Path(".runs"))
    start.add_argument("--output", type=Path)

    approve = subparsers.add_parser("approve")
    approve.add_argument("--incident-id", required=True)
    approve.add_argument("--actor", required=True)
    approve.add_argument("--state-dir", type=Path, default=Path(".runs"))
    approve.add_argument("--output", type=Path)

    reject = subparsers.add_parser("reject")
    reject.add_argument("--incident-id", required=True)
    reject.add_argument("--actor", required=True)
    reject.add_argument("--state-dir", type=Path, default=Path(".runs"))
    reject.add_argument("--output", type=Path)

    observe = subparsers.add_parser("observe")
    observe.add_argument("--incident-id", required=True)
    observe.add_argument("--observation", required=True)
    observe.add_argument("--actor", required=True)
    observe.add_argument("--state-dir", type=Path, default=Path(".runs"))
    observe.add_argument("--output", type=Path)

    status = subparsers.add_parser("status")
    status.add_argument("--incident-id", required=True)
    status.add_argument("--state-dir", type=Path, default=Path(".runs"))

    demo = subparsers.add_parser("demo")
    demo.add_argument("--output", type=Path, default=Path("docs/demo_runthrough.md"))
    demo.add_argument("--state-dir", type=Path, default=Path("docs/demo_states"))

    evaluation = subparsers.add_parser("evaluate")
    evaluation.add_argument("--cases", type=Path, default=Path("data/evaluation_cases.json"))
    evaluation.add_argument("--output", type=Path, default=Path("docs/evaluation_results.md"))
    return parser


def add_report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--summary", required=True)
    parser.add_argument("--service", default="")
    parser.add_argument("--environment", default="production")
    parser.add_argument("--impact", default="")
    parser.add_argument("--signal", action="append", default=[])
    parser.add_argument("--requester", default="unknown@example.com")


def report_from_args(args: argparse.Namespace) -> IncidentReport:
    return IncidentReport(
        summary=args.summary,
        service=args.service,
        environment=args.environment,
        impact=args.impact,
        observed_signals=args.signal,
        requester=args.requester,
    )


def command_start(args: argparse.Namespace) -> None:
    store = IncidentStore(args.state_dir)
    state = IncidentWorkflow().start(report_from_args(args))
    store.save(state)
    emit_state(state, args.output)


def command_decide(args: argparse.Namespace, decision: str) -> None:
    store = IncidentStore(args.state_dir)
    state = store.load(args.incident_id)
    state = IncidentWorkflow().resume(state, approval_decisions={"all": decision}, actor=args.actor)
    store.save(state)
    emit_state(state, args.output)


def command_observe(args: argparse.Namespace) -> None:
    store = IncidentStore(args.state_dir)
    state = store.load(args.incident_id)
    state = IncidentWorkflow().resume(state, observation=args.observation, actor=args.actor)
    store.save(state)
    emit_state(state, args.output)


def command_status(args: argparse.Namespace) -> None:
    state = IncidentStore(args.state_dir).load(args.incident_id)
    emit_state(state, None)


def command_demo(args: argparse.Namespace) -> None:
    args.state_dir.mkdir(parents=True, exist_ok=True)
    workflow = IncidentWorkflow()
    report = IncidentReport(
        summary="Checkout is down after the latest production deploy.",
        service="checkout",
        environment="production",
        impact="Customers cannot complete purchases.",
        observed_signals=["HTTP 500 rate is 38 percent", "error budget burn is critical"],
        requester="ops@example.com",
    )
    pending = workflow.start(report, incident_id="demo-checkout-001")
    pending_snapshot = pending.model_copy(deep=True)
    (args.state_dir / "demo_pending_approval.json").write_text(pending_snapshot.model_dump_json(indent=2), encoding="utf-8")

    approved = workflow.resume(pending, approval_decisions={"all": "approved"}, actor="incident-commander@example.com")
    approved_snapshot = approved.model_copy(deep=True)
    (args.state_dir / "demo_after_approval.json").write_text(approved_snapshot.model_dump_json(indent=2), encoding="utf-8")

    resolved = workflow.resume(approved, observation="Checkout metrics are stable and the incident is resolved.", actor="incident-commander@example.com")
    resolved_snapshot = resolved.model_copy(deep=True)
    (args.state_dir / "demo_resolved.json").write_text(resolved_snapshot.model_dump_json(indent=2), encoding="utf-8")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_demo([pending_snapshot, approved_snapshot, resolved_snapshot]), encoding="utf-8")
    print(f"Wrote demo run-through to {args.output}")


def command_evaluate(args: argparse.Namespace) -> None:
    summary = evaluate(read_evaluation_cases(args.cases))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_evaluation(summary), encoding="utf-8")
    print(json.dumps(summary.model_dump(mode="json"), indent=2))


def emit_state(state: IncidentState, output: Path | None) -> None:
    text = state.model_dump_json(indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text)


def render_demo(states: list[IncidentState]) -> str:
    lines = [
        "# Demo Run-Through",
        "",
        "This run shows a long-lived incident workflow that pauses before unsafe production actions, resumes after approval, and closes after a human observation.",
        "",
        "| Step | Status | Boundary | Pending actions | Executed actions |",
        "|---|---|---|---|---|",
    ]
    for index, state in enumerate(states, start=1):
        pending = [action.name for action in state.pending_actions()]
        executed = [action.name for action in state.actions if action.executed]
        lines.append(
            f"| {index} | {state.status.value} | {state.boundary.reason} | "
            f"{', '.join(pending) or 'none'} | {', '.join(executed) or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Event Log",
            "",
        ]
    )
    for event in states[-1].events:
        lines.append(f"- `{event.event_type}`: {event.message}")
    return "\n".join(lines) + "\n"


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "start":
        command_start(args)
    elif args.command == "approve":
        command_decide(args, "approved")
    elif args.command == "reject":
        command_decide(args, "rejected")
    elif args.command == "observe":
        command_observe(args)
    elif args.command == "status":
        command_status(args)
    elif args.command == "demo":
        command_demo(args)
    elif args.command == "evaluate":
        command_evaluate(args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()

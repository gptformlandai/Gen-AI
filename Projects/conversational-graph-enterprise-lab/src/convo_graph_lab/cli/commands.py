"""CLI commands for conversational graph execution."""

from __future__ import annotations

import argparse
import json
import sys

from convo_graph_lab.config import get_settings
from convo_graph_lab.evals.runner import run_evaluations
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.file_state_store import FileStateStore
from convo_graph_lab.graph_engine.modeling import build_graph_model_report
from convo_graph_lab.graph_engine.runner import GraphRunner
from convo_graph_lab.observability.debugger import build_debug_report
from convo_graph_lab.visualization.exporters import export_graph_dot, export_graph_json, export_graph_mermaid


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="convgraph-lab")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start-conversation")
    start.add_argument("--input", required=True)
    start.add_argument("--user-id", default="local-user")
    start.add_argument("--session-id", default="local-session")
    send = sub.add_parser("send-input")
    send.add_argument("--session-id", default="local-session")
    send.add_argument("--input", required=True)
    resume = sub.add_parser("resume-conversation")
    resume.add_argument("--session-id", default="local-session")
    resume.add_argument("--approved", action="store_true")
    run = sub.add_parser("run-graph")
    run.add_argument("--input", required=True)
    viz = sub.add_parser("visualize-graph")
    viz.add_argument("--format", choices=["json", "mermaid", "dot"], default="mermaid")
    sub.add_parser("inspect-graph")
    debug = sub.add_parser("debug-conversation")
    debug.add_argument("--input", required=True)
    sub.add_parser("run-evals")
    sub.add_parser("start-api")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = get_settings()
    graph, issues = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    if any(issue.severity == "error" for issue in issues):
        print(json.dumps([issue.__dict__ for issue in issues], indent=2), file=sys.stderr)
        return 2
    runner = GraphRunner(graph, settings=settings, state_store=FileStateStore(settings.export_dir / "cli_sessions"))

    if args.command == "start-conversation":
        print(runner.start(args.input, user_id=args.user_id, session_id=args.session_id).model_dump_json(indent=2))
    elif args.command == "send-input":
        print(runner.send_input(args.session_id, args.input).model_dump_json(indent=2))
    elif args.command == "resume-conversation":
        print(runner.resume(args.session_id, {"approved": args.approved}).model_dump_json(indent=2))
    elif args.command == "run-graph":
        print(runner.start(args.input).model_dump_json(indent=2))
    elif args.command == "visualize-graph":
        output = _visualize(args.format, graph.definition)
        print(output if isinstance(output, str) else json.dumps(output, indent=2))
    elif args.command == "inspect-graph":
        print(build_graph_model_report(graph.definition).model_dump_json(indent=2))
    elif args.command == "debug-conversation":
        result = runner.start(args.input)
        debug_report = build_debug_report(result.state, result.trace, runner.state_store.get_snapshots(result.state.session_id))
        debug_report["metrics"] = runner.services.metrics.snapshot()
        print(json.dumps(debug_report, indent=2))
    elif args.command == "run-evals":
        print(run_evaluations(settings).model_dump_json(indent=2))
    elif args.command == "start-api":
        return _start_api()
    return 0


def _visualize(fmt: str, graph_definition):
    if fmt == "json":
        return export_graph_json(graph_definition)
    if fmt == "dot":
        return export_graph_dot(graph_definition)
    return export_graph_mermaid(graph_definition)


def _start_api() -> int:
    try:
        import uvicorn
    except ImportError:
        print("Install API dependencies first: python -m pip install -e '.[api]'", file=sys.stderr)
        return 2
    uvicorn.run("convo_graph_lab.api.app:app", host="127.0.0.1", port=8010, reload=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

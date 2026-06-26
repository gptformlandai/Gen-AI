from __future__ import annotations

import argparse
import json
from pathlib import Path

from enterprise_ops_lab.evals.golden_eval import run_golden_eval
from enterprise_ops_lab.evals.rag_eval import run_rag_eval
from enterprise_ops_lab.evals.trajectory_eval import run_trajectory_eval


def run_all_evaluations(root: Path) -> dict:
    reports = [
        run_golden_eval(root / "data/eval/golden_cases.json"),
        run_trajectory_eval(root / "data/eval/trajectory_cases.json"),
        run_rag_eval(root / "data/eval/rag_grounding_cases.json", root / "data/runbooks"),
    ]
    return {report.name: report.model_dump(mode="json") for report in reports}


def render_markdown(results: dict) -> str:
    lines = ["# Evaluation Report", "", "| Suite | Passed | Total | Pass rate |", "|---|---:|---:|---:|"]
    for name, report in results.items():
        lines.append(f"| {name} | {report['passed']} | {report['total']} | {report['pass_rate']:.2%} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Enterprise Ops Lab evaluations.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, default=Path("docs/evaluation_report.md"))
    parser.add_argument("--json-output", type=Path, default=Path("docs/evaluation_report.json"))
    args = parser.parse_args()
    results = run_all_evaluations(args.root)
    out = args.output if args.output.is_absolute() else args.root / args.output
    json_out = args.json_output if args.json_output.is_absolute() else args.root / args.json_output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(results), encoding="utf-8")
    json_out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()


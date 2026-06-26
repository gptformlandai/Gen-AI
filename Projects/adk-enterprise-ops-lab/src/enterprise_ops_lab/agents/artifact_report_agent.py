from __future__ import annotations

from enterprise_ops_lab.tools.artifact_tools import save_report_artifact


def build_markdown_report(response: dict) -> str:
    triage = response["triage"]
    remediation = response["recommended_remediation"]
    lines = [
        f"# Incident Report: {triage['service']}",
        "",
        f"- Severity: `{triage['severity']}`",
        f"- Intent: `{triage['intent']}`",
        f"- Likely root cause: {remediation['likely_root_cause']}",
        f"- Escalation: {response['escalation_decision']}",
        "",
        "## Recommended Actions",
    ]
    lines.extend(f"- {action}" for action in remediation["recommended_actions"])
    lines.extend(["", "## Evidence"])
    lines.extend(f"- `{item['source']}`: {item['quote'][:160]}" for item in response["evidence"])
    return "\n".join(lines) + "\n"


def run(response: dict, artifact_dir: str = ".artifacts") -> dict:
    markdown = build_markdown_report(response)
    artifact_id = f"incident_{response['request_id']}"
    return save_report_artifact(
        artifact_id=artifact_id,
        markdown=markdown,
        artifact_dir=artifact_dir,
        metadata={"service": response["triage"]["service"], "request_id": response["request_id"]},
    )


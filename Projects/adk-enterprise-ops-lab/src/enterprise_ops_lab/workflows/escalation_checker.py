from __future__ import annotations


def escalation_decision(confidence: float, severity: str, human_approval_required: bool, threshold: float = 0.72) -> str:
    if confidence < threshold:
        return "escalate: confidence below threshold"
    if severity == "sev1":
        return "escalate: sev1 requires incident commander review"
    if human_approval_required:
        return "escalate: remediation requires approval"
    return "no escalation required"


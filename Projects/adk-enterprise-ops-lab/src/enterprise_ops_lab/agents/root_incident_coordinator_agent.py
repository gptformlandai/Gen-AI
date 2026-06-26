from __future__ import annotations

from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.incident import IncidentRequest, IncidentResponse


def run(request: IncidentRequest, runner: EnterpriseOpsRunner | None = None) -> IncidentResponse:
    """Root coordinator entry point for ADK and local CLI."""
    return (runner or EnterpriseOpsRunner()).run(request)


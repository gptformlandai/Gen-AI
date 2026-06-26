from __future__ import annotations

from enterprise_ops_lab.schemas.incident import IncidentTriage
from enterprise_ops_lab.tools.incident_tools import extract_incident_fields


def run(query: str) -> IncidentTriage:
    """Specialist triage agent behavior."""
    return extract_incident_fields(query)


from __future__ import annotations

from pathlib import Path

from hitl_incident_assistant.schemas import IncidentState


class IncidentStore:
    """File-backed checkpoint store for resumable incident workflows."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, state: IncidentState) -> Path:
        path = self.path_for(state.incident_id)
        path.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        return path

    def load(self, incident_id: str) -> IncidentState:
        path = self.path_for(incident_id)
        return IncidentState.model_validate_json(path.read_text(encoding="utf-8"))

    def path_for(self, incident_id: str) -> Path:
        return self.directory / f"{incident_id}.json"


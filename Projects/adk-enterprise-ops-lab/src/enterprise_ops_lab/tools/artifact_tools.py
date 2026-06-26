from __future__ import annotations

from pathlib import Path

from enterprise_ops_lab.artifacts.artifact_service import LocalArtifactService


def save_report_artifact(artifact_id: str, markdown: str, artifact_dir: str | Path = ".artifacts", metadata: dict[str, str] | None = None) -> dict:
    root = Path(__file__).resolve().parents[3]
    directory = Path(artifact_dir)
    if not directory.is_absolute():
        directory = root / directory
    record = LocalArtifactService(directory).save_markdown(artifact_id, markdown, metadata or {})
    return record.model_dump(mode="json")


def load_report_artifact(artifact_id: str, artifact_dir: str | Path = ".artifacts", version: int | None = None) -> dict:
    root = Path(__file__).resolve().parents[3]
    directory = Path(artifact_dir)
    if not directory.is_absolute():
        directory = root / directory
    record, content = LocalArtifactService(directory).load(artifact_id, version=version)
    return {"record": record.model_dump(mode="json"), "content": content}


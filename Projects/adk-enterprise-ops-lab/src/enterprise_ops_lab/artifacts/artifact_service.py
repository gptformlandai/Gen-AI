from __future__ import annotations

from pathlib import Path
import json

from enterprise_ops_lab.schemas.artifact import ArtifactRecord


class LocalArtifactService:
    """Local artifact store that models ADK artifact persistence and versioning."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save_markdown(self, artifact_id: str, content: str, metadata: dict[str, str]) -> ArtifactRecord:
        version = self._next_version(artifact_id)
        path = self.root / f"{artifact_id}_v{version}.md"
        path.write_text(content, encoding="utf-8")
        record = ArtifactRecord(
            artifact_id=artifact_id,
            path=str(path),
            version=version,
            content_type="text/markdown",
            metadata=metadata,
        )
        (self.root / f"{artifact_id}_v{version}.json").write_text(record.model_dump_json(indent=2), encoding="utf-8")
        return record

    def load(self, artifact_id: str, version: int | None = None) -> tuple[ArtifactRecord, str]:
        version = version or max(self._versions(artifact_id))
        meta_path = self.root / f"{artifact_id}_v{version}.json"
        record = ArtifactRecord.model_validate_json(meta_path.read_text(encoding="utf-8"))
        return record, Path(record.path).read_text(encoding="utf-8")

    def list_versions(self, artifact_id: str) -> list[int]:
        return self._versions(artifact_id)

    def _next_version(self, artifact_id: str) -> int:
        versions = self._versions(artifact_id)
        return max(versions, default=0) + 1

    def _versions(self, artifact_id: str) -> list[int]:
        versions = []
        for path in self.root.glob(f"{artifact_id}_v*.json"):
            suffix = path.stem.split("_v")[-1]
            if suffix.isdigit():
                versions.append(int(suffix))
        return sorted(versions)


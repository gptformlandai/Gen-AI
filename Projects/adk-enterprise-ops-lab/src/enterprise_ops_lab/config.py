from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """Central config object with local defaults and cloud extension placeholders."""

    model: str = "gemini-2.5-flash"
    env: str = "local"
    debug: bool = True
    project_root: Path = Path(__file__).resolve().parents[2]
    artifact_dir: Path = Path(".artifacts")
    trace_dir: Path = Path(".traces")
    session_dir: Path = Path(".sessions")
    memory_dir: Path = Path(".memory")
    mcp_timeout_ms: int = 1200
    confidence_threshold: float = 0.72

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_env(cls) -> "Settings":
        root = Path(__file__).resolve().parents[2]
        return cls(
            model=os.getenv("OPS_LAB_MODEL", "gemini-2.5-flash"),
            env=os.getenv("OPS_LAB_ENV", "local"),
            debug=os.getenv("OPS_LAB_DEBUG", "true").lower() == "true",
            project_root=root,
            artifact_dir=root / os.getenv("OPS_LAB_ARTIFACT_DIR", ".artifacts"),
            trace_dir=root / os.getenv("OPS_LAB_TRACE_DIR", ".traces"),
            session_dir=root / os.getenv("OPS_LAB_SESSION_DIR", ".sessions"),
            memory_dir=root / os.getenv("OPS_LAB_MEMORY_DIR", ".memory"),
            mcp_timeout_ms=int(os.getenv("MCP_TIMEOUT_MS", "1200")),
        )


def get_settings() -> Settings:
    return Settings.from_env()


from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_name: str
    ok: bool
    data: dict = Field(default_factory=dict)
    error: str = ""
    latency_ms: int = 0
    safety: Literal["safe", "blocked", "needs_approval"] = "safe"


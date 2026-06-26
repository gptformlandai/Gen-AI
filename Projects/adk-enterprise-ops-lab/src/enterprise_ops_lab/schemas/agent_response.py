from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AgentEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_name: str
    request_id: str
    session_id: str
    status: str
    message: str
    payload: dict = Field(default_factory=dict)
    tool_calls: list[str] = Field(default_factory=list)


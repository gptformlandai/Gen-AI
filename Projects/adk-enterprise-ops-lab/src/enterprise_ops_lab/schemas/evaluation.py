from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    query: str


class EvaluationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    passed: bool
    checks: dict[str, bool]
    notes: list[str] = Field(default_factory=list)


class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    total: int
    passed: int
    pass_rate: float
    rows: list[EvaluationRow]


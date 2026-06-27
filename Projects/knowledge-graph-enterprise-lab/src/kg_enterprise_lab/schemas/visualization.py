"""Visualization export schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class VisualizationNode(BaseModel):
    id: str
    label: str
    name: str
    properties: dict[str, Any] = Field(default_factory=dict)


class VisualizationEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str
    properties: dict[str, Any] = Field(default_factory=dict)


class VisualizationGraph(BaseModel):
    nodes: list[VisualizationNode]
    edges: list[VisualizationEdge]
    view: str = "full"

"""Parse and validate graph definitions."""

from __future__ import annotations

import json
from pathlib import Path

from convo_graph_lab.graph_engine.graph import RuntimeGraph, build_runtime_graph
from convo_graph_lab.graph_engine.validator import GraphValidationIssue, validate_graph_definition
from convo_graph_lab.schema.models import GraphDefinition


def load_graph_definition(path: Path) -> GraphDefinition:
    return GraphDefinition(**json.loads(path.read_text(encoding="utf-8")))


def compile_graph(path: Path) -> tuple[RuntimeGraph, list[GraphValidationIssue]]:
    definition = load_graph_definition(path)
    issues = validate_graph_definition(definition)
    return build_runtime_graph(definition), issues

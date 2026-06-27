"""API dependency singletons."""

from __future__ import annotations

from functools import lru_cache

from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.runner import GraphRunner
from convo_graph_lab.graph_engine.state_store import InMemoryStateStore
from convo_graph_lab.observability.tracing import TraceRecorder


@lru_cache(maxsize=1)
def get_runner() -> GraphRunner:
    settings = get_settings()
    graph, issues = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        raise RuntimeError(f"Cannot start API with invalid graph: {errors}")
    return GraphRunner(graph, settings=settings, state_store=InMemoryStateStore(), trace_recorder=TraceRecorder())

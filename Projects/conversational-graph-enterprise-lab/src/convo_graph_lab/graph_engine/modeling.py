"""Graph modeling reports for design review and debugging."""

from __future__ import annotations

from collections import Counter, defaultdict

from convo_graph_lab.graph_engine.validator import _has_cycle
from convo_graph_lab.schema.models import GraphDefinition, GraphModelReport
from convo_graph_lab.workflows.sample_flows import CONVERSATIONAL_PATTERNS


def build_graph_model_report(definition: GraphDefinition) -> GraphModelReport:
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in definition.edges:
        outgoing[edge.source].append(edge.target)
    terminal_node_ids = sorted(node.id for node in definition.nodes if node.type == "EndNode" or not outgoing.get(node.id))
    branching_node_ids = sorted(node_id for node_id, targets in outgoing.items() if len(set(targets)) > 1)
    node_type_counts = Counter(node.type for node in definition.nodes)
    pattern_coverage = {
        name: all(node_id in {node.id for node in definition.nodes} for node_id in path)
        for name, path in CONVERSATIONAL_PATTERNS.items()
    }
    return GraphModelReport(
        graph_id=definition.id,
        node_count=len(definition.nodes),
        edge_count=len(definition.edges),
        start_node_id=definition.start_node_id,
        terminal_node_ids=terminal_node_ids,
        branching_node_ids=branching_node_ids,
        cycle_detected=_has_cycle(definition),
        node_type_counts=dict(sorted(node_type_counts.items())),
        pattern_coverage=pattern_coverage,
    )

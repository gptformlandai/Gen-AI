"""Extraction constants and canonical entity patterns."""

from __future__ import annotations

ENTITY_LABEL_HINTS = {
    "svc-": "Service",
    "api-": "API",
    "db": "Database",
    "table-": "Table",
    "topic-": "KafkaTopic",
    "kafka-topic-": "KafkaTopic",
    "INC-": "Incident",
    "runbook-": "Runbook",
}

RELATIONSHIP_PATTERNS = {
    "calls": "CALLS",
    "depends on": "DEPENDS_ON",
    "reads": "READS_FROM",
    "writes": "WRITES_TO",
    "publishes": "PUBLISHES_TO",
    "consumes": "CONSUMES_FROM",
    "mitigated by": "MITIGATED_BY",
    "documents": "DOCUMENTED_BY",
}

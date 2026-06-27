"""Schema-constrained mock LLM extraction adapter.

Production implementation should call an LLM with this same contract, require a
structured response, then pass candidates through ontology validation and human
review thresholds. The local adapter is deterministic so tests run offline.
"""

from __future__ import annotations

import re

from kg_enterprise_lab.schemas.extraction import ExtractedEntity, ExtractedRelationship, ExtractionBatch, SourceDocument


class LLMExtractorPlaceholder:
    provider_name = "mock-llm"

    def build_prompt(self, document: SourceDocument) -> str:
        return (
            "Extract enterprise knowledge graph entities and relationships. "
            "Return Service, API, Database, Table, KafkaTopic, Incident, Team, Owner, Runbook, Deployment, "
            "Environment, Schema, Endpoint, ErrorCode, DataEntity, and supported relationship types only.\n\n"
            f"Source: {document.id}\n{document.text}"
        )

    def extract(self, document: SourceDocument) -> ExtractionBatch:
        text = document.text
        entities: dict[str, ExtractedEntity] = {}
        for match in re.finditer(r"\b([a-z][a-z0-9]+(?:-[a-z0-9]+)+)\b", text):
            name = match.group(1)
            label = _infer_label(name)
            canonical_id = _canonical_id(name, label)
            entities[canonical_id] = ExtractedEntity(
                canonical_id=canonical_id,
                label=label,
                name=name,
                confidence=0.72,
                source_ref=document.id,
                properties={"extractor": self.provider_name, "offset": match.start()},
            )
        for match in re.finditer(r"\b(INC-\d+)\b", text):
            incident_id = match.group(1)
            entities[incident_id] = ExtractedEntity(
                canonical_id=incident_id,
                label="Incident",
                name=incident_id,
                confidence=0.9,
                source_ref=document.id,
                properties={"extractor": self.provider_name, "offset": match.start()},
            )
        relationships = _extract_relationships(text, document.id)
        return ExtractionBatch(entities=sorted(entities.values(), key=lambda item: item.canonical_id), relationships=relationships)


def _infer_label(name: str) -> str:
    if name.startswith("kafka-topic") or name.startswith("topic-"):
        return "KafkaTopic"
    if name.endswith("-api"):
        return "Service"
    if name.endswith("-db"):
        return "Database"
    if name.startswith("runbook-"):
        return "Runbook"
    if "table" in name:
        return "Table"
    return "Service"


def _canonical_id(name: str, label: str) -> str:
    if name.startswith(("svc-", "api-", "topic-", "runbook-", "table-")):
        return name
    if label == "KafkaTopic" and name.startswith("kafka-topic-"):
        return name.replace("kafka-topic-", "topic-", 1)
    if label == "Database":
        return f"svc-{name}"
    if label == "Service":
        return f"svc-{name}" if not name.startswith("svc-") else name
    return name


def _extract_relationships(text: str, source_ref: str) -> list[ExtractedRelationship]:
    patterns = [
        (r"([a-z][a-z0-9-]+)\s+calls\s+([a-z][a-z0-9-]+)", "CALLS"),
        (r"([a-z][a-z0-9-]+)\s+depends on\s+([a-z][a-z0-9-]+)", "DEPENDS_ON"),
        (r"([a-z][a-z0-9-]+)\s+reads\s+([a-z][a-z0-9-]+)", "READS_FROM"),
        (r"([a-z][a-z0-9-]+)\s+writes\s+([a-z][a-z0-9-]+)", "WRITES_TO"),
        (r"([a-z][a-z0-9-]+)\s+publishes\s+([a-z][a-z0-9-]+)", "PUBLISHES_TO"),
        (r"([a-z][a-z0-9-]+)\s+consumes\s+([a-z][a-z0-9-]+)", "CONSUMES_FROM"),
    ]
    relationships: list[ExtractedRelationship] = []
    for pattern, relationship_type in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            relationships.append(
                ExtractedRelationship(
                    source_name=match.group(1),
                    relationship_type=relationship_type,
                    target_name=match.group(2),
                    confidence=0.7,
                    source_ref=source_ref,
                    evidence=match.group(0),
                    properties={"extractor": "mock-llm"},
                )
            )
    return relationships

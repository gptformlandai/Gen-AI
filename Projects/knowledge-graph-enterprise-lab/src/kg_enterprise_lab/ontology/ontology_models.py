"""Default enterprise ontology used by local execution."""

from __future__ import annotations

from kg_enterprise_lab.schemas.ontology import CardinalityRule, OntologyDefinition, RelationshipShape


NODE_LABELS = {
    "Service",
    "API",
    "Database",
    "Table",
    "KafkaTopic",
    "Team",
    "Owner",
    "Incident",
    "Deployment",
    "Runbook",
    "BusinessCapability",
    "Environment",
    "Schema",
    "Endpoint",
    "ErrorCode",
    "DataEntity",
}

RELATIONSHIP_TYPES = {
    "DEPENDS_ON",
    "CALLS",
    "EXPOSES_API",
    "READS_FROM",
    "WRITES_TO",
    "PUBLISHES_TO",
    "CONSUMES_FROM",
    "OWNED_BY",
    "MAINTAINED_BY",
    "HAS_INCIDENT",
    "CAUSED_BY",
    "MITIGATED_BY",
    "DOCUMENTED_BY",
    "DEPLOYED_TO",
    "SUPPORTS",
    "HAS_SCHEMA",
    "HAS_ENDPOINT",
    "RETURNS_ERROR",
    "SIMILAR_TO",
    "IMPACTS",
    "HAS_LINEAGE_TO",
}

RELATIONSHIP_SHAPES = [
    RelationshipShape(relationship_type="DEPENDS_ON", source_labels={"Service"}, target_labels={"Service", "Database"}),
    RelationshipShape(relationship_type="CALLS", source_labels={"Service"}, target_labels={"Service"}),
    RelationshipShape(relationship_type="EXPOSES_API", source_labels={"Service"}, target_labels={"API"}),
    RelationshipShape(relationship_type="READS_FROM", source_labels={"Service"}, target_labels={"Table"}),
    RelationshipShape(relationship_type="WRITES_TO", source_labels={"Service"}, target_labels={"Table"}),
    RelationshipShape(relationship_type="PUBLISHES_TO", source_labels={"Service"}, target_labels={"KafkaTopic"}),
    RelationshipShape(relationship_type="CONSUMES_FROM", source_labels={"Service"}, target_labels={"KafkaTopic"}),
    RelationshipShape(relationship_type="OWNED_BY", source_labels={"Service"}, target_labels={"Team"}),
    RelationshipShape(relationship_type="MAINTAINED_BY", source_labels={"Service", "Owner"}, target_labels={"Owner", "Team"}),
    RelationshipShape(relationship_type="HAS_INCIDENT", source_labels={"Service"}, target_labels={"Incident"}),
    RelationshipShape(relationship_type="IMPACTS", source_labels={"Incident"}, target_labels={"Service", "KafkaTopic"}),
    RelationshipShape(relationship_type="DOCUMENTED_BY", source_labels={"Service", "Incident"}, target_labels={"Runbook"}),
    RelationshipShape(relationship_type="MITIGATED_BY", source_labels={"Incident"}, target_labels={"Runbook"}),
    RelationshipShape(relationship_type="DEPLOYED_TO", source_labels={"Service", "Deployment"}, target_labels={"Environment", "Deployment"}),
    RelationshipShape(relationship_type="SUPPORTS", source_labels={"Service"}, target_labels={"BusinessCapability"}),
    RelationshipShape(relationship_type="HAS_SCHEMA", source_labels={"Database", "KafkaTopic"}, target_labels={"Schema", "Table"}),
    RelationshipShape(relationship_type="HAS_ENDPOINT", source_labels={"API"}, target_labels={"Endpoint"}),
    RelationshipShape(relationship_type="RETURNS_ERROR", source_labels={"API"}, target_labels={"ErrorCode"}),
    RelationshipShape(relationship_type="HAS_LINEAGE_TO", source_labels={"Service", "KafkaTopic"}, target_labels={"Service", "Table", "DataEntity"}),
]


def default_ontology() -> OntologyDefinition:
    return OntologyDefinition(
        version="1.0.0",
        node_labels=NODE_LABELS,
        relationship_types=RELATIONSHIP_TYPES,
        required_properties={
            "Service": {"description"},
            "API": {"version"},
            "Database": {"engine"},
            "Incident": {"title", "severity"},
            "Team": {"pager"},
        },
        cardinality_rules=[
            CardinalityRule(source_label="Service", relationship_type="OWNED_BY", target_label="Team", min_count=1),
            CardinalityRule(source_label="Service", relationship_type="DEPLOYED_TO", target_label="Environment", min_count=1, severity="warning"),
            CardinalityRule(source_label="Incident", relationship_type="DOCUMENTED_BY", target_label="Runbook", min_count=1),
        ],
        relationship_shapes=RELATIONSHIP_SHAPES,
    )

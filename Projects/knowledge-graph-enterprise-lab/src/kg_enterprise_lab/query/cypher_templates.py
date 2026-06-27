"""Pre-approved Cypher templates."""

from __future__ import annotations


CYPHER_TEMPLATES: dict[str, str] = {
    "dependents": "MATCH (s:Service)-[:DEPENDS_ON|CALLS]->(target {name: $service_name}) RETURN s",
    "blast_radius": "MATCH path=(n {name: $service_name})<-[:DEPENDS_ON|CALLS*1..$depth]-(dependent) RETURN path",
    "lineage": "MATCH path=(n {name: $service_name})-[:HAS_LINEAGE_TO*1..$depth]->(downstream) RETURN path",
    "ownership": "MATCH (s:Service)-[:OWNED_BY]->(t:Team) WHERE s.name IN $service_names RETURN s,t",
    "incident_correlation": "MATCH (s:Service)-[:HAS_INCIDENT]->(i:Incident)-[:DOCUMENTED_BY]->(r:Runbook) RETURN s,i,r",
}


def get_cypher_template(name: str) -> str:
    if name not in CYPHER_TEMPLATES:
        raise ValueError(f"Cypher template is not allowlisted: {name}")
    return CYPHER_TEMPLATES[name]

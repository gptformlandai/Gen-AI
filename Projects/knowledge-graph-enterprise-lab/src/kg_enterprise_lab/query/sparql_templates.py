"""Pre-approved SPARQL templates."""

from __future__ import annotations


SPARQL_TEMPLATES: dict[str, str] = {
    "service_dependencies": """
PREFIX ent: <https://example.com/enterprise#>
SELECT ?service ?dependency WHERE {
  ?service ent:DEPENDS_ON ?dependency .
}
""".strip(),
    "service_owners": """
PREFIX ent: <https://example.com/enterprise#>
SELECT ?service ?team WHERE {
  ?service ent:OWNED_BY ?team .
}
""".strip(),
    "incident_runbooks": """
PREFIX ent: <https://example.com/enterprise#>
SELECT ?incident ?runbook WHERE {
  ?incident ent:DOCUMENTED_BY ?runbook .
}
""".strip(),
    "lineage": """
PREFIX ent: <https://example.com/enterprise#>
SELECT ?source ?target WHERE {
  ?source ent:HAS_LINEAGE_TO ?target .
}
""".strip(),
}


def get_sparql_template(name: str) -> str:
    if name not in SPARQL_TEMPLATES:
        raise ValueError(f"SPARQL template is not allowlisted: {name}")
    return SPARQL_TEMPLATES[name]

"""Build a property graph from the enterprise source catalog."""

from __future__ import annotations

from typing import Any

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.relationship import GraphRelationship


def _node(node_id: str, label: str, name: str, source: str, **properties: Any) -> GraphNode:
    aliases = list(properties.pop("aliases", []) or [])
    return GraphNode(id=node_id, label=label, name=name, properties=properties, aliases=aliases, source_refs=[source])


def _rel(source_id: str, rel_type: str, target_id: str, source: str, **properties: Any) -> GraphRelationship:
    return GraphRelationship(source_id=source_id, type=rel_type, target_id=target_id, properties=properties, source_refs=[source])


def build_graph_from_sources(sources: dict[str, Any]) -> InMemoryGraphRepository:
    graph = InMemoryGraphRepository()

    capability_by_name: dict[str, str] = {}
    for item in sources.get("business_capabilities", []):
        graph.upsert_node(_node(str(item["id"]), "BusinessCapability", str(item["name"]), "raw/business_capabilities.json", description=item.get("description", "")))
        capability_by_name[str(item["name"])] = str(item["id"])

    for item in sources.get("environments", []):
        graph.upsert_node(_node(str(item["id"]), "Environment", str(item["name"]), "raw/environments.json", region=item.get("region", ""), tier=item.get("tier", "")))

    for team in sources.get("teams", []):
        graph.upsert_node(_node(str(team["id"]), "Team", str(team["name"]), "raw/teams.json", slack=team.get("slack", ""), pager=team.get("pager", "")))

    for owner in sources.get("owners", []):
        graph.upsert_node(
            _node(str(owner["id"]), "Owner", str(owner["name"]), "raw/owners.json", email=owner.get("email", ""), role=owner.get("role", ""), team_id=owner.get("team_id", ""))
        )
        if owner.get("team_id"):
            graph.upsert_relationship(_rel(str(owner["id"]), "MAINTAINED_BY", str(owner["team_id"]), "raw/owners.json"))

    for db in sources.get("databases", []):
        db_id = str(db["id"])
        graph.upsert_node(_node(db_id, "Database", str(db["name"]), "raw/databases.json", engine=db.get("engine", "")))
        for schema_id in db.get("schema_ids", []):
            schema_name = str(schema_id).removeprefix("schema-")
            graph.upsert_node(_node(str(schema_id), "Schema", schema_name, "raw/databases.json"))
            graph.upsert_relationship(_rel(db_id, "HAS_SCHEMA", str(schema_id), "raw/databases.json"))
        for table_id in db.get("table_ids", []):
            table_name = str(table_id).removeprefix("table-").replace("-", "_")
            graph.upsert_node(_node(str(table_id), "Table", table_name, "raw/databases.json", database_id=db_id))
            graph.upsert_relationship(_rel(db_id, "HAS_SCHEMA", str(table_id), "raw/databases.json", container="table"))

    for topic in sources.get("kafka_topics", []):
        topic_id = str(topic["id"])
        graph.upsert_node(_node(topic_id, "KafkaTopic", str(topic["name"]), "raw/kafka_topics.json", schema_id=topic.get("schema_id", "")))
        if topic.get("schema_id"):
            schema_id = str(topic["schema_id"])
            graph.upsert_node(_node(schema_id, "Schema", schema_id.removeprefix("schema-"), "raw/kafka_topics.json", schema_kind="event"))
            graph.upsert_relationship(_rel(topic_id, "HAS_SCHEMA", schema_id, "raw/kafka_topics.json"))
        for entity_id in topic.get("data_entity_ids", []):
            entity_name = str(entity_id).removeprefix("entity-").replace("-", " ")
            graph.upsert_node(_node(str(entity_id), "DataEntity", entity_name, "raw/kafka_topics.json"))
            graph.upsert_relationship(_rel(topic_id, "HAS_LINEAGE_TO", str(entity_id), "raw/kafka_topics.json"))

    for api in sources.get("apis", []):
        api_id = str(api["id"])
        graph.upsert_node(_node(api_id, "API", str(api["name"]), "raw/apis.json", version=api.get("version", "")))
        for endpoint_id in api.get("endpoint_ids", []):
            endpoint_name = str(endpoint_id).removeprefix("endpoint-").replace("-", " ")
            graph.upsert_node(_node(str(endpoint_id), "Endpoint", endpoint_name, "raw/apis.json"))
            graph.upsert_relationship(_rel(api_id, "HAS_ENDPOINT", str(endpoint_id), "raw/apis.json"))
        for error_id in api.get("error_code_ids", []):
            graph.upsert_node(_node(str(error_id), "ErrorCode", str(error_id).removeprefix("err-").upper(), "raw/apis.json"))
            graph.upsert_relationship(_rel(api_id, "RETURNS_ERROR", str(error_id), "raw/apis.json"))

    for runbook in sources.get("runbooks", []):
        graph.upsert_node(
            _node(
                str(runbook["id"]),
                "Runbook",
                str(runbook["title"]),
                "raw/runbooks.json",
                keywords=runbook.get("keywords", []),
                url=runbook.get("url", ""),
                steps=runbook.get("steps", []),
            )
        )

    for service in sources.get("services", []):
        service_id = str(service["id"])
        graph.upsert_node(
            _node(
                service_id,
                "Service",
                str(service["name"]),
                "raw/services.json",
                aliases=service.get("aliases", []),
                description=service.get("description", ""),
                business_capability=service.get("business_capability", ""),
            )
        )
        if service.get("team_id"):
            graph.upsert_relationship(_rel(service_id, "OWNED_BY", str(service["team_id"]), "raw/services.json"))
        for owner_id in service.get("owner_ids", []):
            graph.upsert_relationship(_rel(service_id, "MAINTAINED_BY", str(owner_id), "raw/services.json"))
        capability_id = capability_by_name.get(str(service.get("business_capability", "")))
        if capability_id:
            graph.upsert_relationship(_rel(service_id, "SUPPORTS", capability_id, "raw/services.json"))
        for environment_id in service.get("environment_ids", []):
            graph.upsert_relationship(_rel(service_id, "DEPLOYED_TO", str(environment_id), "raw/services.json"))
        for api_id in service.get("exposes_api_ids", []):
            graph.upsert_relationship(_rel(service_id, "EXPOSES_API", str(api_id), "raw/services.json"))
        for target_id in service.get("calls", []):
            graph.upsert_relationship(_rel(service_id, "CALLS", str(target_id), "raw/services.json"))
        for target_id in service.get("depends_on", []):
            graph.upsert_relationship(_rel(service_id, "DEPENDS_ON", str(target_id), "raw/services.json"))
        for table_id in service.get("reads_from", []):
            graph.upsert_relationship(_rel(service_id, "READS_FROM", str(table_id), "raw/services.json"))
        for table_id in service.get("writes_to", []):
            graph.upsert_relationship(_rel(service_id, "WRITES_TO", str(table_id), "raw/services.json"))
        for topic_id in service.get("publishes_to", []):
            graph.upsert_relationship(_rel(service_id, "PUBLISHES_TO", str(topic_id), "raw/services.json"))
        for topic_id in service.get("consumes_from", []):
            graph.upsert_relationship(_rel(service_id, "CONSUMES_FROM", str(topic_id), "raw/services.json"))
        for runbook_id in service.get("runbook_ids", []):
            graph.upsert_relationship(_rel(service_id, "DOCUMENTED_BY", str(runbook_id), "raw/services.json"))

    for incident in sources.get("incidents", []):
        incident_id = str(incident["id"])
        graph.upsert_node(
            _node(
                incident_id,
                "Incident",
                str(incident["title"]),
                "raw/incidents.json",
                title=incident.get("title", ""),
                severity=incident.get("severity", ""),
                caused_by=incident.get("caused_by", ""),
                mitigation=incident.get("mitigation", ""),
                symptoms=incident.get("symptoms", []),
            )
        )
        for service_id in incident.get("service_ids", []):
            graph.upsert_relationship(_rel(str(service_id), "HAS_INCIDENT", incident_id, "raw/incidents.json"))
            graph.upsert_relationship(_rel(incident_id, "IMPACTS", str(service_id), "raw/incidents.json"))
        for topic_id in incident.get("topic_ids", []):
            graph.upsert_relationship(_rel(incident_id, "IMPACTS", str(topic_id), "raw/incidents.json"))
        for runbook_id in incident.get("runbook_ids", []):
            graph.upsert_relationship(_rel(incident_id, "DOCUMENTED_BY", str(runbook_id), "raw/incidents.json"))
            graph.upsert_relationship(_rel(incident_id, "MITIGATED_BY", str(runbook_id), "raw/incidents.json"))

    for deployment in sources.get("deployments", []):
        deploy_id = str(deployment["id"])
        graph.upsert_node(
            _node(
                deploy_id,
                "Deployment",
                deploy_id,
                "raw/deployments.json",
                version=deployment.get("version", ""),
                timestamp=deployment.get("timestamp", ""),
                change_summary=deployment.get("change_summary", ""),
            )
        )
        graph.upsert_relationship(_rel(str(deployment["service_id"]), "DEPLOYED_TO", deploy_id, "raw/deployments.json"))
        graph.upsert_relationship(_rel(deploy_id, "DEPLOYED_TO", str(deployment["environment_id"]), "raw/deployments.json"))

    _add_lineage_edges(graph)
    return graph


def _add_lineage_edges(graph: InMemoryGraphRepository) -> None:
    lineage_pairs = [
        ("svc-mobile-app", "svc-provider-search"),
        ("svc-provider-search", "table-providers"),
        ("svc-provider-search", "table-provider-locations"),
        ("svc-mobile-app", "svc-payments-api"),
        ("svc-payments-api", "table-payment-ledger"),
        ("svc-claims-orchestrator", "svc-eligibility-api"),
        ("svc-eligibility-api", "table-member-eligibility"),
    ]
    for source_id, target_id in lineage_pairs:
        if graph.get_node(source_id) and graph.get_node(target_id):
            graph.upsert_relationship(_rel(source_id, "HAS_LINEAGE_TO", target_id, "derived/lineage"))

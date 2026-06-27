# Neo4j Local Notes

## Start

```bash
docker compose -f deploy/docker-compose.yml up neo4j
```

## Constraints

Create uniqueness constraints for every label used in production:

```cypher
CREATE CONSTRAINT service_id IF NOT EXISTS FOR (n:Service) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT api_id IF NOT EXISTS FOR (n:API) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE;
```

## Load Pattern

Use `MERGE` for nodes and relationships. The helper functions in `graph/neo4j_repository.py` generate parameterized statements for the local graph data.

## Production Notes

Use explicit transaction batches, retry transient failures, set query timeouts, and keep graph schema migration separate from data ingestion.

# Cloud Deployment Notes

## Reference Topology

- API container on Kubernetes, Cloud Run, ECS, or App Service.
- Neo4j Aura, Amazon Neptune, TigerGraph, or managed graph DB.
- Vector database for node and document embeddings.
- Object storage for raw source snapshots and export artifacts.
- OpenTelemetry collector for traces and metrics.

## Release Flow

1. Run unit tests and golden evals.
2. Validate ontology migration.
3. Build and scan container image.
4. Deploy API behind auth.
5. Run smoke queries and GraphRAG evals.
6. Enable scheduled ingestion.

## Secrets

Store graph DB credentials, LLM keys, and vector DB credentials in the platform secret manager. Do not store secrets in `.env` or Docker images.

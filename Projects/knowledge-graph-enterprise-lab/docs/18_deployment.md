# 18 Deployment

## What It Is

Deployment moves the local lab into a production topology with API service, graph database, vector store, object storage, and observability.

## Why It Matters

Local graphs are good for learning and tests. Production needs durable storage, controlled writes, backups, and operational runbooks.

## Where It Appears

- `deploy/Dockerfile`
- `deploy/docker-compose.yml`
- `deploy/neo4j_local.md`
- `deploy/production_notes.md`

## How To Run

```bash
python -m pip install -e ".[api]"
uvicorn kg_enterprise_lab.api.app:app --reload
```

## How To Extend

Containerize the API, run Neo4j or Neptune separately, configure secrets through the platform, and run evals in CI before deployment.

## Common Mistakes

- Baking secrets into images.
- Running graph algorithms inside latency-sensitive API requests.
- Deploying without backups and restore tests.

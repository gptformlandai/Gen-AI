# Deployment

## Local CLI

```bash
ops-lab run --query "Investigate high latency in payments-api after last deployment."
```

## FastAPI

```bash
python -m pip install -e ".[api]"
uvicorn enterprise_ops_lab.api.app:app --host 0.0.0.0 --port 8000
```

## Cloud Run

Use `deploy/Dockerfile`, configure secrets through Secret Manager, and run evals before release.

## Vertex AI Agent Engine

Install `.[adk]`, replace local specs with real ADK agents, and deploy with the ADK/Agent Engine path.

## Kubernetes

Run the API image with ConfigMaps for non-secrets and Secret Manager or sealed secrets for credentials.


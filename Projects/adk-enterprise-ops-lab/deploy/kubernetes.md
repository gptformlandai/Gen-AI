# Kubernetes

Recommended components:

- Deployment for FastAPI runtime.
- ConfigMap for non-secret config.
- Secret or external secret for credentials.
- Persistent volume or GCS for artifacts.
- HorizontalPodAutoscaler based on CPU and latency.
- NetworkPolicy limiting MCP and datastore access.


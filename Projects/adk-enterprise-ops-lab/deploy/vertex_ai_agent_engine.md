# Vertex AI Agent Engine

Install ADK:

```bash
python -m pip install -e ".[adk]"
```

Replace local fallback specs in `agents/agent_factory.py` with real ADK Agent deployment objects, configure `GOOGLE_CLOUD_PROJECT`, and run the ADK deployment path for Agent Engine.

Keep local tests and evals as the deployment gate.


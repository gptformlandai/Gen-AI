from __future__ import annotations

from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.incident import IncidentRequest


def create_app():
    try:
        from fastapi import FastAPI
    except Exception as exc:  # pragma: no cover - only hit when optional extra is absent
        raise RuntimeError("Install the API extra with `pip install -e '.[api]'`.") from exc

    app = FastAPI(title="ADK Enterprise Ops Lab")
    runner = EnterpriseOpsRunner()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/incident")
    def incident(request: IncidentRequest) -> dict:
        return runner.run(request).model_dump(mode="json")

    return app


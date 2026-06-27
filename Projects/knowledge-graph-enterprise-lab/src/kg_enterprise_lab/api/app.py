"""FastAPI application factory."""

from __future__ import annotations

from kg_enterprise_lab.api.dependencies import get_graph
from kg_enterprise_lab.api.routes import register_routes


def create_app():
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError("Install API dependencies first: pip install -e '.[api]'") from exc

    app = FastAPI(title="Knowledge Graph Enterprise Lab", version="0.1.0")
    register_routes(app, get_graph)
    return app


app = create_app()

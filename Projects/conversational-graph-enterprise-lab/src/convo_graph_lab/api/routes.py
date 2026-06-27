"""API routes for conversation and graph execution."""

from __future__ import annotations

from pydantic import BaseModel

from convo_graph_lab.evals.runner import run_evaluations
from convo_graph_lab.graph_engine.modeling import build_graph_model_report
from convo_graph_lab.observability.debugger import build_debug_report
from convo_graph_lab.visualization.exporters import export_graph_json, export_graph_mermaid


class StartRequest(BaseModel):
    input: str
    user_id: str = "anonymous"
    session_id: str | None = None


class InputRequest(BaseModel):
    session_id: str
    input: str


class ResumeRequest(BaseModel):
    session_id: str
    updates: dict[str, object] = {}


def register_routes(app, runner_provider) -> None:
    from fastapi import Depends, HTTPException

    @app.post("/conversation/start")
    def start_conversation(request: StartRequest, runner=Depends(runner_provider)):
        return runner.start(request.input, user_id=request.user_id, session_id=request.session_id).model_dump()

    @app.post("/conversation/input")
    def send_input(request: InputRequest, runner=Depends(runner_provider)):
        return runner.send_input(request.session_id, request.input).model_dump()

    @app.post("/conversation/resume")
    def resume(request: ResumeRequest, runner=Depends(runner_provider)):
        return runner.resume(request.session_id, request.updates).model_dump()

    @app.get("/conversation/state")
    def state(session_id: str, runner=Depends(runner_provider)):
        state_obj = runner.state_store.get(session_id)
        if not state_obj:
            raise HTTPException(status_code=404, detail="session not found")
        return state_obj.model_dump()

    @app.get("/conversation/history")
    def history(session_id: str, runner=Depends(runner_provider)):
        state_obj = runner.state_store.get(session_id)
        if not state_obj:
            raise HTTPException(status_code=404, detail="session not found")
        return [turn.model_dump() for turn in state_obj.context.history]

    @app.get("/conversation/trace")
    def trace(session_id: str, runner=Depends(runner_provider)):
        return [event.model_dump() for event in runner.trace_recorder.get(session_id)]

    @app.get("/conversation/debug")
    def debug(session_id: str, runner=Depends(runner_provider)):
        state_obj = runner.state_store.get(session_id)
        if not state_obj:
            raise HTTPException(status_code=404, detail="session not found")
        return build_debug_report(state_obj, runner.trace_recorder.get(session_id), runner.state_store.get_snapshots(session_id))

    @app.post("/graph/execute")
    def execute(request: StartRequest, runner=Depends(runner_provider)):
        return runner.start(request.input, user_id=request.user_id, session_id=request.session_id).model_dump()

    @app.get("/graph/visualize")
    def visualize(fmt: str = "json", session_id: str | None = None, runner=Depends(runner_provider)):
        trace_events = runner.trace_recorder.get(session_id) if session_id else []
        if fmt == "mermaid":
            return {"diagram": export_graph_mermaid(runner.graph.definition, trace_events)}
        return export_graph_json(runner.graph.definition, trace_events)

    @app.get("/graph/inspect")
    def inspect_graph(runner=Depends(runner_provider)):
        return build_graph_model_report(runner.graph.definition).model_dump()

    @app.post("/eval/run")
    def eval_run():
        return run_evaluations().model_dump()

from uuid import uuid4

from fastapi import FastAPI

from trend_video_agent.config import get_settings
from trend_video_agent.schemas import (
    HealthResponse,
    ProjectCreateRequest,
    ProjectResponse,
    WorkflowDryRunRequest,
    WorkflowDryRunResponse,
)
from trend_video_agent.workflow.nodes import build_dry_run_steps

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@app.post("/projects", response_model=ProjectResponse)
def create_project(request: ProjectCreateRequest) -> ProjectResponse:
    return ProjectResponse(
        project_id=str(uuid4()),
        title=request.title,
        niche=request.niche,
        target_platforms=request.target_platforms,
        status="created",
    )


@app.post("/workflows/dry-run", response_model=WorkflowDryRunResponse)
def dry_run_workflow(request: WorkflowDryRunRequest) -> WorkflowDryRunResponse:
    return WorkflowDryRunResponse(
        video_path=request.video_path,
        target_platform=request.target_platform,
        steps=build_dry_run_steps(),
        learning_note="This is the planned agent workflow only. No video is processed in Step 01.",
    )

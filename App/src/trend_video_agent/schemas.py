from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class ProjectCreateRequest(BaseModel):
    title: str = Field(min_length=1, examples=["Podcast episode 12"])
    niche: str = Field(min_length=1, examples=["real estate education"])
    target_platforms: list[str] = Field(default_factory=lambda: ["youtube_shorts"])


class ProjectResponse(BaseModel):
    project_id: str
    title: str
    niche: str
    target_platforms: list[str]
    status: str


class WorkflowDryRunRequest(BaseModel):
    video_path: str = Field(examples=["data/raw/podcast_episode_12.mp4"])
    niche: str = Field(examples=["real estate education"])
    target_platform: str = Field(default="youtube_shorts")


class WorkflowStep(BaseModel):
    name: str
    purpose: str
    status: str = "planned"


class WorkflowDryRunResponse(BaseModel):
    video_path: str
    target_platform: str
    steps: list[WorkflowStep]
    learning_note: str

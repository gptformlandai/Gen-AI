from typing import TypedDict


class VideoWorkflowState(TypedDict, total=False):
    video_path: str
    niche: str
    target_platform: str
    transcript_path: str
    candidate_clips: list[dict[str, str]]
    style_plan: dict[str, str]
    viral_score: float
    export_path: str
    errors: list[str]

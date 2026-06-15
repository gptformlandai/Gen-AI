from trend_video_agent.schemas import WorkflowStep


def build_dry_run_steps() -> list[WorkflowStep]:
    return [
        WorkflowStep(
            name="transcription_agent",
            purpose="Convert speech into timestamped text so later steps can reason over the video.",
        ),
        WorkflowStep(
            name="scene_detection_tool",
            purpose="Find visual boundaries that help us avoid awkward clip cuts.",
        ),
        WorkflowStep(
            name="clip_selection_agent",
            purpose="Choose short moments with a strong hook, clear idea, and retention potential.",
        ),
        WorkflowStep(
            name="rag_trend_memory",
            purpose="Retrieve style examples, platform rules, and trend notes relevant to the clip.",
        ),
        WorkflowStep(
            name="edit_planning_agent",
            purpose="Plan captions, aspect ratio, pacing, and edit style before rendering.",
        ),
        WorkflowStep(
            name="viral_scoring_agent",
            purpose="Score each output using explainable criteria instead of pretending to predict virality.",
        ),
    ]

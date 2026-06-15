from trend_video_agent.workflow.nodes import build_dry_run_steps


def test_dry_run_has_core_learning_steps():
    steps = build_dry_run_steps()
    step_names = [step.name for step in steps]

    assert "transcription_agent" in step_names
    assert "scene_detection_tool" in step_names
    assert "rag_trend_memory" in step_names
    assert "viral_scoring_agent" in step_names

from trend_video_agent.workflow.state import VideoWorkflowState


def build_video_workflow():
    try:
        from langgraph.graph import END, StateGraph
    except ImportError as error:
        raise RuntimeError(
            "LangGraph is not installed yet. Install project dependencies before building the graph."
        ) from error

    workflow = StateGraph(VideoWorkflowState)
    workflow.add_node("receive_video", receive_video)
    workflow.set_entry_point("receive_video")
    workflow.add_edge("receive_video", END)
    return workflow.compile()


def receive_video(state: VideoWorkflowState) -> VideoWorkflowState:
    return {**state, "errors": state.get("errors", [])}

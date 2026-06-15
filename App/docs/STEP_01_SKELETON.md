# Step 01: Project Skeleton

## Intuition

Before we build intelligence, we need a clean map of the system.

Think of this step as building labeled empty rooms in a studio:

- API room: where users enter requests.
- Workflow room: where the agent decides the next stage.
- Tools room: where real work happens, like clipping or captioning.
- Memory room: where past examples and style knowledge will live.
- Integration rooms: where MCP and agent-to-agent communication can be added later.

## What We Are Building

We are creating a minimal FastAPI project with placeholders for:

- LangGraph workflow orchestration
- Specialist agents
- Video and trend tools
- RAG/vector memory
- MCP tool exposure
- A2A message contracts

No real video processing happens yet.

## Why This Is Useful

This prevents the common beginner problem of mixing everything into one large script.

In real projects, video processing, LLM reasoning, API routes, database code, and workflow orchestration grow quickly. If we do not separate them early, the project becomes hard to test and hard to explain.

## Alternatives

| Option | When It Is Good | Trade-off |
|---|---|---|
| Single Python script | Best for a 1-hour experiment | Becomes messy once agents/tools grow |
| Notebook first | Great for learning Whisper/FFmpeg interactively | Harder to turn into an API later |
| FastAPI skeleton | Good for a real app path | Slightly more structure upfront |
| Full frontend + backend now | Good for demos | Too much surface area for step 01 |

## Where Developers Go Wrong

- They install every library before knowing the workflow.
- They start with UI polish before proving the pipeline.
- They call everything an agent even when it is just a function.
- They do real video rendering before they can explain the workflow state.
- They skip contracts, so each step passes unclear data to the next step.

## Real-World Scenario

A creator uploads a 30-minute podcast. The production system will eventually:

1. Transcribe the full video.
2. Detect scenes and topic shifts.
3. Find strong short-form moments.
4. Compare those moments against trend/style memory.
5. Generate edit plans.
6. Render vertical clips with captions.
7. Score each clip and explain the score.

This skeleton creates the places where those responsibilities will live.

## What Comes Next

Step 02 should add the first real endpoint behavior:

> Upload or register a video file path and return a simple project/job object.

We still should not process video in Step 02. The next lesson is about API contracts and job state.

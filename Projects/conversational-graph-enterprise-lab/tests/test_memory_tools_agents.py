from convo_graph_lab.agents.agent_registry import default_agent_registry
from convo_graph_lab.memory.memory_store import MemorySystem, fill_slots_from_text
from convo_graph_lab.schema.models import ConversationContext, ToolCall
from convo_graph_lab.tools.registry import default_tool_registry


def test_slot_filling_memory_read_write_and_tools():
    context = ConversationContext(session_id="m1", user_id="user-1", latest_input="Investigate INC-1001")
    fill_slots_from_text(context, context.latest_input)
    assert context.slots["intent"] == "incident"
    assert context.slots["incident_id"] == "INC-1001"

    memory = MemorySystem()
    records = memory.write_policy(context, ["intent", "incident_id"])
    assert len(records) == 2
    assert memory.read_policy(context, "incident INC-1001")

    registry = default_tool_registry()
    result = registry.invoke(ToolCall(tool_name="incident_lookup_tool", arguments={"incident_id": "INC-1001"}))
    assert result.success
    assert result.output["owner"] == "Provider Platform"
    missing = registry.invoke(ToolCall(tool_name="incident_lookup_tool", arguments={}))
    assert not missing.success
    assert "Missing required tool args" in missing.error


def test_agent_registry_invokes_specialists():
    context = ConversationContext(session_id="a1", user_id="user-1", latest_input="debug latency")
    context.slots["intent"] = "developer"
    output, updates = default_agent_registry().invoke("developer", context)
    assert "Developer specialist" in output
    assert updates["confidence"] >= 0.8

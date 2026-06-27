from convo_graph_lab.schema.models import ConversationContext
from convo_graph_lab.transitions.conditions import evaluate_condition
from convo_graph_lab.workflows.pattern_detector import detect_patterns


def test_transition_conditions_support_compound_logic_and_contains():
    context = ConversationContext(session_id="c1")
    context.variables["confidence"] = 0.4
    context.variables["needs_human"] = True
    context.variables["latest_input"] = "please escalate this"
    assert evaluate_condition("confidence <= 0.55 and needs_human == true", context)
    assert evaluate_condition("latest_input contains 'escalate'", context)
    assert evaluate_condition("confidence > 0.9 or needs_human == true", context)
    assert not evaluate_condition("confidence > 0.9 and needs_human == true", context)


def test_pattern_detector_detects_runtime_patterns():
    path = ["input", "intent_router", "clarify", "collect_slot", "input", "intent_router", "workflow_agent", "user_profile", "memory_write", "decision", "summary", "end"]
    patterns = detect_patterns(path)
    assert patterns["clarification_loop"]
    assert patterns["multi_step_workflow"]

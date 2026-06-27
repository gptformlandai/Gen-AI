"""Concrete node types for conversational graph execution."""

from __future__ import annotations

from convo_graph_lab.agents.agent_registry import AgentRegistry
from convo_graph_lab.memory.memory_store import fill_slots_from_text
from convo_graph_lab.nodes.base import BaseNode
from convo_graph_lab.schema.models import ConversationState, NodeResult, NodeStatus, ToolCall


class InputNode(BaseNode):
    node_type = "InputNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        context = state.context
        fill_slots_from_text(context, context.latest_input)
        services.memory.session.append_turn(context, "user", context.latest_input)
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output="Input captured", updates={"latest_input": context.latest_input})


class LLMNode(BaseNode):
    node_type = "LLMNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        mode = str(self.config("mode", "summary"))
        context = state.context
        if mode == "clarify":
            required = list(self.config("required_slots", []))
            missing = [slot for slot in required if not context.slots.get(slot)]
            output = "Can you clarify the request type: support, incident, developer, or workflow?"
            context.variables["awaiting_input"] = bool(missing)
            context.outputs.append(output)
            services.memory.session.append_turn(context, "assistant", output)
            return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=output, updates={"awaiting_input": bool(missing)})
        facts = ", ".join(f"{key}={value}" for key, value in sorted(context.slots.items())) or "no slots"
        recent = services.memory.session.compress(context)
        output = f"Conversation summary with {facts}. Recent context: {recent}"
        context.outputs.append(output)
        services.memory.session.append_turn(context, "assistant", output)
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=output, updates={"confidence": max(context.get_value("confidence", 0.8), 0.8)})


class ToolNode(BaseNode):
    node_type = "ToolNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        tool_name = str(self.config("tool"))
        mapping = dict(self.config("input_mapping", {}))
        args = {target: state.context.get_value(source) for target, source in mapping.items()}
        result = services.tools.invoke(ToolCall(tool_name=tool_name, arguments=args))
        state.context.variables["last_tool_name"] = tool_name
        state.context.variables["last_tool_result"] = result.model_dump()
        state.context.variables["tool_failed"] = not result.success
        if result.success:
            output = f"{tool_name} returned {result.output}"
            state.context.outputs.append(output)
            return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=output, updates={"tool_failed": False, "confidence": 0.82})
        state.context.errors.append(result.error or "tool failed")
        return NodeResult(node_id=self.definition.id, status=NodeStatus.FAILED, error=result.error, updates={"tool_failed": True, "confidence": 0.4})


class DecisionNode(BaseNode):
    node_type = "DecisionNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        confidence = float(state.context.get_value("confidence", 0.8) or 0.0)
        needs_human = bool(state.context.get_value("needs_human", False))
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output="Decision evaluated", updates={"confidence": confidence, "needs_human": needs_human})


class RouterNode(BaseNode):
    node_type = "RouterNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        intent = state.context.slots.get("intent", "unknown")
        routes = dict(self.config("routes", {}))
        route = routes.get(str(intent), routes.get("unknown", "clarify"))
        state.context.variables["route"] = intent if route != "clarify" else "unknown"
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=f"Routed to {route}", next_node_id=route, updates={"route": state.context.variables["route"]})


class MemoryNode(BaseNode):
    node_type = "MemoryNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        operation = str(self.config("operation", "write"))
        if operation == "read":
            memories = services.memory.read_policy(state.context, state.context.latest_input)
            state.context.variables["retrieved_memories"] = [memory.model_dump() for memory in memories]
            return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=f"Read {len(memories)} memories")
        keys = [str(key) for key in self.config("keys", [])]
        records = services.memory.write_policy(state.context, keys)
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=f"Wrote {len(records)} memories")


class ValidationNode(BaseNode):
    node_type = "ValidationNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        fill_slots_from_text(state.context, state.context.latest_input)
        required = [str(slot) for slot in self.config("required_slots", [])]
        missing = [slot for slot in required if not state.context.slots.get(slot)]
        complete = not missing
        state.context.variables["slots_complete"] = complete
        state.context.variables["awaiting_input"] = not complete
        output = "Slots complete" if complete else f"Missing slots: {', '.join(missing)}"
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS if complete else NodeStatus.WAITING, output=output, updates={"slots_complete": complete, "awaiting_input": not complete})


class WorkflowNode(BaseNode):
    node_type = "WorkflowNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        workflow = str(self.config("workflow", "generic"))
        state.context.variables["workflow_started"] = workflow
        if workflow == "account_unlock" and not state.context.get_value("account_id"):
            state.context.variables["account_id"] = state.context.user_id
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=f"Workflow started: {workflow}", updates={"confidence": 0.78})


class AgentNode(BaseNode):
    node_type = "AgentNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        registry: AgentRegistry = services.agents
        output, updates = registry.invoke(str(self.config("agent", "coordinator")), state.context)
        for key, value in updates.items():
            state.context.set_value(key, value)
        state.context.outputs.append(output)
        services.memory.session.append_turn(state.context, "assistant", output)
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=output, updates=updates)


class HumanApprovalNode(BaseNode):
    node_type = "HumanApprovalNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        approval_key = str(self.config("approval_key", "approved"))
        approved = state.context.slots.get(approval_key)
        if approved is not True:
            state.context.variables["awaiting_approval"] = True
            state.interrupted_at = self.definition.id
            return NodeResult(node_id=self.definition.id, status=NodeStatus.INTERRUPTED, output="Waiting for human approval", updates={"awaiting_approval": True})
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output="Human approval granted", updates={"awaiting_approval": False})


class FallbackNode(BaseNode):
    node_type = "FallbackNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        output = str(self.config("message", "I could not complete this safely."))
        state.context.outputs.append(output)
        services.memory.session.append_turn(state.context, "assistant", output)
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=output, updates={"fallback_used": True})


class RetryNode(BaseNode):
    node_type = "RetryNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        target = str(self.config("target_node_id"))
        max_retries = int(self.config("max_retries", 2))
        count = state.retry_counts.get(target, 0)
        allowed = count < max_retries
        state.retry_counts[target] = count + 1
        state.context.variables["retry_allowed"] = allowed
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS, output=f"Retry allowed={allowed}", updates={"retry_allowed": allowed})


class EndNode(BaseNode):
    node_type = "EndNode"

    def run(self, state: ConversationState, services: object) -> NodeResult:
        return NodeResult(node_id=self.definition.id, status=NodeStatus.TERMINAL, output=state.context.outputs[-1] if state.context.outputs else "Done")

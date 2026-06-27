"""Deterministic specialist agents for local graph execution."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from convo_graph_lab.schema.models import ConversationContext


AgentHandler = Callable[[ConversationContext], tuple[str, dict[str, object]]]


@dataclass
class AgentRegistry:
    agents: dict[str, AgentHandler] = field(default_factory=dict)

    def register(self, name: str, handler: AgentHandler) -> None:
        self.agents[name] = handler

    def invoke(self, name: str, context: ConversationContext) -> tuple[str, dict[str, object]]:
        handler = self.agents.get(name)
        if not handler:
            return f"No specialist agent registered for {name}.", {"confidence": 0.2, "needs_human": True}
        return handler(context)


def default_agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register("coordinator", coordinator_agent)
    registry.register("support", support_agent)
    registry.register("incident", incident_agent)
    registry.register("developer", developer_agent)
    registry.register("routing", routing_agent)
    registry.register("clarification", clarification_agent)
    registry.register("tool", tool_agent)
    registry.register("summary", summary_agent)
    return registry


def coordinator_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    return "Coordinator delegated the turn based on intent and available slots.", {"confidence": 0.82}


def routing_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    intent = context.slots.get("intent", "unknown")
    return f"Routing decision: {intent}.", {"route": intent, "confidence": 0.8}


def clarification_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    return "Can you clarify whether this is support, incident, developer, or workflow help?", {"awaiting_input": True, "confidence": 0.7}


def support_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    return "Support specialist will load the user profile and check account eligibility.", {"confidence": 0.78}


def incident_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    incident_id = context.slots.get("incident_id")
    if incident_id:
        return f"Incident specialist will investigate {incident_id}.", {"confidence": 0.86}
    return "Incident specialist needs graph context because no incident ID was provided.", {"confidence": 0.62}


def developer_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    return "Developer specialist will search internal runbooks and debugging guidance.", {"confidence": 0.8}


def tool_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    return "Tool agent selected the next typed tool based on current slots.", {"confidence": 0.76}


def summary_agent(context: ConversationContext) -> tuple[str, dict[str, object]]:
    facts = []
    for key in ["intent", "incident_id", "account_id"]:
        value = context.get_value(key)
        if value:
            facts.append(f"{key}={value}")
    return "Summary: " + ", ".join(facts or ["conversation completed"]), {"confidence": 0.84}

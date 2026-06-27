"""Memory stores and relevance retrieval."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from convo_graph_lab.schema.models import ConversationContext, ConversationTurn, MemoryRecord


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_-]+", text.lower()))


@dataclass
class SessionMemory:
    max_turns: int = 8

    def append_turn(self, context: ConversationContext, role: str, content: str) -> None:
        context.history.append(ConversationTurn(role=role, content=content))
        if len(context.history) > self.max_turns:
            context.history = context.history[-self.max_turns :]

    def compress(self, context: ConversationContext) -> str:
        recent = context.history[-self.max_turns :]
        return " | ".join(f"{turn.role}: {turn.content}" for turn in recent)


@dataclass
class LongTermMemory:
    records: dict[str, MemoryRecord] = field(default_factory=dict)

    def write(self, user_id: str, text: str, metadata: dict[str, object] | None = None) -> MemoryRecord:
        record_id = hashlib.sha1(f"{user_id}:{text}".encode("utf-8")).hexdigest()[:16]
        record = MemoryRecord(id=record_id, user_id=user_id, text=text, metadata=metadata or {})
        self.records[record_id] = record
        return record

    def retrieve(self, user_id: str, query: str, top_k: int = 3) -> list[MemoryRecord]:
        query_tokens = token_set(query)
        scored: list[MemoryRecord] = []
        for record in self.records.values():
            if record.user_id != user_id:
                continue
            overlap = len(query_tokens & token_set(record.text))
            if overlap:
                scored.append(record.model_copy(update={"score": overlap / max(len(query_tokens), 1)}))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

    def prune(self, user_id: str, keep: int = 20) -> None:
        records = [record for record in self.records.values() if record.user_id == user_id]
        for record in sorted(records, key=lambda item: item.timestamp, reverse=True)[keep:]:
            self.records.pop(record.id, None)


@dataclass
class MemorySystem:
    session: SessionMemory = field(default_factory=SessionMemory)
    long_term: LongTermMemory = field(default_factory=LongTermMemory)

    def write_policy(self, context: ConversationContext, keys: list[str]) -> list[MemoryRecord]:
        records: list[MemoryRecord] = []
        for key in keys:
            value = context.get_value(key)
            if value:
                records.append(self.long_term.write(context.user_id, f"{key}: {value}", {"session_id": context.session_id, "key": key}))
        context.long_term_memory_refs = sorted({*context.long_term_memory_refs, *(record.id for record in records)})
        return records

    def read_policy(self, context: ConversationContext, query: str, top_k: int = 3) -> list[MemoryRecord]:
        return self.long_term.retrieve(context.user_id, query, top_k=top_k)


def fill_slots_from_text(context: ConversationContext, text: str) -> None:
    lowered = text.lower()
    if any(term in lowered for term in ["incident", "inc-", "sev", "outage", "latency"]):
        context.slots["intent"] = "incident"
    elif any(term in lowered for term in ["unlock", "workflow", "automate", "approval"]):
        context.slots["intent"] = "workflow"
    elif any(term in lowered for term in ["debug", "search", "docs", "code", "developer"]):
        context.slots["intent"] = "developer"
    elif any(term in lowered for term in ["refund", "billing", "support", "customer", "profile"]):
        context.slots["intent"] = "support"
    if any(term in lowered for term in ["human", "handoff", "escalate", "approval"]):
        context.variables["needs_human"] = True
    match = re.search(r"\bINC-\d+\b", text.upper())
    if match:
        context.slots["incident_id"] = match.group(0)
    account_match = re.search(r"\b(?:account|user)[-\s:]*(\d{3,})\b", lowered)
    if account_match:
        context.slots["account_id"] = account_match.group(1)

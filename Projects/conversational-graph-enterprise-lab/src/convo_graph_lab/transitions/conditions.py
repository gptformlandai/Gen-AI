"""Small safe condition evaluator for graph edges."""

from __future__ import annotations

import operator
from typing import Any

from convo_graph_lab.schema.models import ConversationContext


OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
}


def evaluate_condition(condition: str, context: ConversationContext) -> bool:
    condition = condition.strip()
    if condition in {"always", "default"}:
        return True
    if " or " in condition:
        return any(evaluate_condition(part, context) for part in condition.split(" or "))
    if " and " in condition:
        return all(evaluate_condition(part, context) for part in condition.split(" and "))
    if " contains " in condition:
        left, right = [part.strip() for part in condition.split(" contains ", 1)]
        value = context.get_value(left)
        expected = _parse_value(right)
        if isinstance(value, str):
            return str(expected).lower() in value.lower()
        if isinstance(value, (list, tuple, set)):
            return expected in value
        return False
    for op_text, op_func in OPS.items():
        if op_text in condition:
            left, right = [part.strip() for part in condition.split(op_text, 1)]
            try:
                return op_func(context.get_value(left), _parse_value(right))
            except TypeError:
                return False
    if condition.endswith(" is set"):
        key = condition.removesuffix(" is set").strip()
        return context.get_value(key) is not None
    return bool(context.get_value(condition))


def _parse_value(value: str) -> Any:
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value.strip("'\"")

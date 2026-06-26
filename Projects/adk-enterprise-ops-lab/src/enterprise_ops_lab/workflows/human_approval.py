from __future__ import annotations


def require_human_approval(action: str, approved: bool = False) -> dict:
    if action in {"rollback_deployment", "cancel_database_query", "scale_production"} and not approved:
        return {"allowed": False, "reason": f"{action} requires incident commander approval"}
    return {"allowed": True, "reason": "approved or safe action"}


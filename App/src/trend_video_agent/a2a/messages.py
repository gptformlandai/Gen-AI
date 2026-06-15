from pydantic import BaseModel


class AgentMessage(BaseModel):
    sender: str
    receiver: str
    intent: str
    payload: dict[str, str]

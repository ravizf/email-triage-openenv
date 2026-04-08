from pydantic import BaseModel
from typing import Optional

class Email(BaseModel):
    subject: str
    body: str

class Observation(BaseModel):
    email: Email
    step: int
    history: Optional[str] = ""

class Action(BaseModel):
    action_type: str  # reply, ignore, mark_urgent
    response: Optional[str] = ""
    reason: Optional[str] = ""
    confidence: Optional[float] = 0.0

class Reward(BaseModel):
    score: float

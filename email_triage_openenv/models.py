from pydantic import BaseModel
from typing import Optional


class Email(BaseModel):
    subject: str
    body: str


class Observation(BaseModel):
    email: Email
    step: int


class Action(BaseModel):
    action_type: str
    response: Optional[str] = ""
    reason: Optional[str] = ""
    confidence: Optional[float] = 0.0

from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high", "critical"]

class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    due: Optional[str] = None
    priority: Priority = "medium"
    rationale: Optional[str] = None

class Decision(BaseModel):
    statement: str
    made_by: Optional[str] = None

class MeetingSummary(BaseModel):
    title: Optional[str] = None
    participants: List[str] = Field(default_factory=list)
    summary: str
    decisions: List[Decision] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)

class AgentOutput(BaseModel):
    summary: MeetingSummary
    word_count: int
    processing_seconds: float
    llm_provider: str
    llm_model: str

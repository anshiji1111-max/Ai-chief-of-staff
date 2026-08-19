"""
Structured output models for every specialist agent.

Every agent in this system returns one of these Pydantic models instead of
free text, so the Executive Planner (and the Report Generator) can reliably
combine outputs without re-parsing prose.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class EmailTriageItem(BaseModel):
    thread_id: str
    sender: str
    subject: str
    urgency: Literal["low", "medium", "high"]
    summary: str
    draft_reply: Optional[str] = None
    requires_approval: bool = False


class EmailTriageResult(BaseModel):
    triaged: List[EmailTriageItem]


class MeetingBrief(BaseModel):
    meeting_title: str
    start_time: str
    attendees: List[str]
    background_summary: str
    talking_points: List[str]
    related_docs: List[str]


class ResearchSummary(BaseModel):
    question: str
    key_findings: List[str]
    sources: List[str]
    confidence: Literal["low", "medium", "high"]


class GoalStatus(BaseModel):
    goal_name: str
    owner: str
    status: Literal["on_track", "at_risk", "stalled"]
    reason: str
    recommended_action: str


class StrategyReport(BaseModel):
    goals: List[GoalStatus]


class ExecutiveDigest(BaseModel):
    date: str
    headline_summary: str
    meeting_briefs: List[MeetingBrief]
    email_highlights: List[EmailTriageItem]
    goal_health: List[GoalStatus]
    pending_approvals: List[str]


class ApprovalRequest(BaseModel):
    action_type: Literal["send_email", "update_goal", "schedule_external"]
    description: str
    payload: dict


class ApprovalDecision(BaseModel):
    approved: bool
    edited_payload: Optional[dict] = None
    note: Optional[str] = None

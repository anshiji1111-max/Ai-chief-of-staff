"""
Shared context object passed through every agent run.

The Agents SDK lets you pass a typed `context` object into `Runner.run(...)`
that every tool function can access via `RunContextWrapper[AppContext]`.
We use it for:
  1. Read access to the day's mock data (calendar/email/goals/docs), standing
     in for real Calendar/Gmail/Docs/CRM APIs.
  2. A running log of pending approvals, so the Planner can report on them
     even across multiple tool calls / handoffs in the same session.
  3. Lightweight cross-session persistence (loaded/saved to disk).
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "mock_data.json")
SESSION_STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "session_store.json")


@dataclass
class AppContext:
    user_name: str = "CEO"
    today: str = "2026-08-19"
    mock_data: Dict[str, Any] = field(default_factory=dict)
    pending_approvals: List[Dict[str, Any]] = field(default_factory=list)
    standing_preferences: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, user_name: str = "CEO") -> "AppContext":
        with open(DATA_PATH, "r") as f:
            mock_data = json.load(f)

        standing_preferences: List[str] = []
        if os.path.exists(SESSION_STORE_PATH):
            with open(SESSION_STORE_PATH, "r") as f:
                stored = json.load(f)
                standing_preferences = stored.get("standing_preferences", [])

        return cls(user_name=user_name, mock_data=mock_data, standing_preferences=standing_preferences)

    def save_session(self) -> None:
        """Persist anything that should survive across runs (advanced feature: session persistence)."""
        with open(SESSION_STORE_PATH, "w") as f:
            json.dump({"standing_preferences": self.standing_preferences}, f, indent=2)

    def add_pending_approval(self, action_type: str, description: str, payload: dict) -> str:
        approval_id = f"appr_{len(self.pending_approvals) + 1:03d}"
        self.pending_approvals.append(
            {
                "approval_id": approval_id,
                "action_type": action_type,
                "description": description,
                "payload": payload,
                "status": "pending",
            }
        )
        return approval_id

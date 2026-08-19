"""
AI Chief of Staff — demo entry point.

Run:
    python main.py

Walks through a "morning brief" cycle: meeting prep + goal health + email
triage, then pauses on any item that needs human approval (e.g. sending a
reply) before showing the final digest.
"""

import asyncio
from agents import Runner
from context import AppContext
from cos_agents.planner import executive_planner_agent
from tools.email_tools import send_email_impl


async def run_human_approval_loop(ctx: AppContext) -> None:
    """
    Walk any pending approvals and ask the human (CLI here — swap for a
    real UI) to approve, reject, or edit before executing the action.
    """
    for approval in list(ctx.pending_approvals):
        if approval["status"] != "pending":
            continue

        print("\n--- HUMAN APPROVAL NEEDED ---")
        print(f"Action: {approval['action_type']}")
        print(f"Description: {approval['description']}")
        print(f"Payload: {approval['payload']}")
        decision = input("Approve? [y/n]: ").strip().lower()

        if decision == "y":
            approval["status"] = "approved"
            if approval["action_type"] == "send_email":
                payload = approval["payload"]
                result = send_email_impl(
                    thread_id=payload.get("thread_id", ""),
                    body=payload.get("body", ""),
                )
                print(result)
        else:
            approval["status"] = "rejected"
            print("Rejected — no action taken.")


async def main():
    ctx = AppContext.load(user_name="CEO")

    print("Requesting morning brief...\n")
    result = await Runner.run(
        executive_planner_agent,
        input=(
            "Give me my morning brief: today's meetings, how our goals are "
            "tracking, and triage my inbox. Compile it all into a digest."
        ),
        context=ctx,
    )

    print("=== EXECUTIVE PLANNER OUTPUT ===")
    print(result.final_output)

    # NOTE: In a full run, request_human_approval tool calls made during
    # the agent run above will have populated ctx.pending_approvals.
    # We resolve those here, outside the agent loop, since approval is a
    # human-in-the-loop step, not something an agent should decide for itself.
    await run_human_approval_loop(ctx)

    ctx.save_session()
    print("\nSession saved.")


if __name__ == "__main__":
    asyncio.run(main())

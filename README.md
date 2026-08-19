# AI Chief of Staff

A multi-agent executive assistant built on the OpenAI Agents SDK. See
`AI_Chief_of_Staff_Project_Doc.md` for the full problem analysis and
architecture writeup.

## Important: mocked integrations

Calendar, Email, Docs, and Goal/OKR data are **mocked** via
`data/mock_data.json` rather than wired to live Google/Microsoft/CRM APIs.
This is intentional for the capstone — it keeps the project runnable
without OAuth/API keys while demonstrating the exact same tool-calling
pattern you'd use with real APIs. Swapping in a real integration means
replacing the body of a function in `tools/*.py` — the agent-facing
interface doesn't change.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...    # required by the Agents SDK
```

## Run the demo

```bash
python main.py
```

This runs a full "morning brief" cycle:
1. Executive Planner hands off to Meeting Preparation, Strategy Tracker,
   and Email Manager.
2. Email Manager drafts a reply and registers it for approval instead of
   sending it.
3. Report Generator compiles everything into one `ExecutiveDigest`.
4. You'll be prompted in the terminal to approve/reject the pending
   email send — approving actually invokes the (mocked) send.

## Project layoutmain.py entry point + human approval loop
context.py shared AppContext (mock data, pending approvals, session persistence)
models.py Pydantic structured outputs for every agent
cos_agents/
planner.py Executive Planner (orchestrator, owns handoffs)
email_manager.py
meeting_prep.py
research_analyst.py
strategy_tracker.py
report_generator.py
tools/
calendar_tools.py
email_tools.py
docs_tools.py
search_tools.py
goal_tools.py
approval_tools.py
data/
mock_data.json seed data standing in for live APIs
session_store.json created at runtime for persisted preferences


Note: the local package is named `cos_agents/` (not `agents/`) specifically
to avoid shadowing the installed `agents` package from the OpenAI Agents
SDK — a common gotcha if you rename things.

## Extending

- Swap `tools/search_tools.py`'s mock for the SDK's hosted web search tool.
- Add RAG by giving Meeting Preparation / Research Analyst a vector store
  of real internal docs instead of `docs_tools.py`'s flat lookup.
- Parallelize meeting prep across multiple events with `asyncio.gather`.

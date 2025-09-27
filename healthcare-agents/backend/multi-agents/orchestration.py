# agents/orchestrator.py
from google.adk.agents import SequentialAgent, ParallelAgent
from .agent_task_intake import task_loop
from .agent_coach import coach
from .agent_report import reporter
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Optional: Skin triage as remote A2A
skin_agent = RemoteA2aAgent(
    name="skin_agent",
    description="Non-diagnostic skin triage from images",
    agent_card="https://skin-agent.example.com/.well-known/a2a/agent-card.json"
)

# Run coach + skin triage in parallel
parallel = ParallelAgent(
    name="coach_plus_skin",
    sub_agents=[coach, skin_agent]
)

# Full workflow: Task intake loop -> Parallel agents -> Reporter
root_agent = SequentialAgent(
    name="orchestrator",
    sub_agents=[task_loop, parallel, reporter]
)

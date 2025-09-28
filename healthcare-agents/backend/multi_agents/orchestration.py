# agents/orchestrator.py
from google.adk.agents import SequentialAgent, ParallelAgent
from .intake_agent import task_loop
from .coach_agent import coach
from .report_agent import reporter
# from google.adk.agents.remote_a2a_agent import RemoteA2aAgent  # Commented out until a2a module is available
import vertexai
import os
from vertexai.generative_models import GenerativeModel

# Optional: Skin triage as remote A2A (commented out until a2a dependency is resolved)
# skin_agent = RemoteA2aAgent(
#     name="skin_agent",
#     description="Non-diagnostic skin triage from images",
#     agent_card="https://skin-agent.example.com/.well-known/a2a/agent-card.json"
# )

# Run coach in parallel (removed skin_agent for now)
parallel = ParallelAgent(
    name="coach_parallel",
    sub_agents=[coach]
)

# Full workflow: Task intake loop -> Parallel agents -> Reporter
root_agent = SequentialAgent(
    name="orchestrator",
    sub_agents=[task_loop, parallel, reporter]
)

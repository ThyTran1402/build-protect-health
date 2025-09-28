# from google.adk.agents import LlmAgent

# GEMINI_TEXT = "gemini-2.0-flash"

# coach = LlmAgent(
#     name="previsit_coach",
#     model=GEMINI_TEXT,
#     instruction=(
#         "You are a pre-visit coach. Given a condition and appointment type, "
#         "output JSON with {checklist, cautions, questions_for_doctor}. "
#         "Be non-diagnostic and encourage confirming with a doctor."
#     ),
#     output_key="coach_json"
# )


# import json
# from google.adk.agents import LlmAgent
# from .mcp.client import MCPToolClient
# from .common.schema import CoachOutput


# GEMINI_TEXT = "gemini-2.0-flash"
# _mcp_coach = MCPToolClient(["python", "-m", "multi_agents.mcp.coach_mcp"])

# def _coach(condition: str, visit_type: str) -> dict:
#     return _mcp_coach.call("coach_for_visit", condition=condition, visit_type=visit_type)

# coach = LlmAgent(
#     name="previsit_coach",
#     model=GEMINI_TEXT,
#     instruction=("Return strict JSON {checklist:[], cautions:[], questions_for_doctor:[]}"),
#     output_key="coach_json",
#     on_output=lambda s: CoachOutput.parse_obj(s["coach_json"])  # validate
# )

# # optional helper used by orchestrator (tool-like)
# def coach_json(condition: str, visit_type: str) -> dict:
#     data = _coach(condition, visit_type)
#     CoachOutput.parse_obj(data)
#     return data



import json
from google.adk.agents import LlmAgent
from .mcp.client import MCPToolClient
from .common.schemas import CoachOutput   
GEMINI_TEXT = "gemini-2.0-flash"
_mcp_coach = MCPToolClient(["python", "-m", "multi_agents.mcp.coach_mcp"])

# Helper: run MCP coach tool
def _coach(condition: str, visit_type: str) -> dict:
    return _mcp_coach.call("coach_for_visit", condition=condition, visit_type=visit_type)

# Create LLM agent
coach = LlmAgent(
    name="previsit_coach",
    model=GEMINI_TEXT,
    instruction="Return strict JSON {checklist:[], cautions:[], questions_for_doctor:[]}",
    output_key="coach_json",
)

# Note: Output validation removed - LlmAgent API has changed
# Validation can be handled in the helper functions instead

# Optional helper for orchestrator (like a tool)
def coach_json(condition: str, visit_type: str) -> dict:
    data = _coach(condition, visit_type)
    CoachOutput.parse_obj(data)  # validate once more
    return data

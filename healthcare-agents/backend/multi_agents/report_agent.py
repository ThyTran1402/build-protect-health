# agents/agent_report.py
# from google.adk.agents import LlmAgent

# GEMINI_TEXT = "gemini-2.0-flash"

# reporter = LlmAgent(
#     name="reporter",
#     model=GEMINI_TEXT,
#     instruction=(
#         "Compare the current patient metrics (from session state) with prior "
#         "records. Identify trends, improvements, or concerns. "
#         "Output a structured summary in Markdown with sections: "
#         "Summary, Trends, and What to discuss next. "
#         "Avoid diagnosis; phrase recommendations as questions for the doctor."
#     ),
#     output_key="report_markdown"
# )



from google.adk.agents import LlmAgent
from .mcp.client import MCPToolClient

GEMINI_TEXT = "gemini-1.5-pro"
_mcp_report = MCPToolClient(["python", "-m", "multi_agents.mcp.report_mcp"])

reporter = LlmAgent(
    name="reporter",
    model=GEMINI_TEXT,
    instruction=(
      "Compare current inputs to prior_metrics. Produce Markdown with sections: "
      "Summary, Trends, What to discuss next. Avoid diagnosis."
    ),
    output_key="report_markdown"
)

def fetch_prior_metrics(patient_id: str) -> dict:
    return _mcp_report.call("prior_metrics", patient_id=patient_id)

def publish_report(patient_id: str, markdown_text: str) -> dict:
    return _mcp_report.call("publish_report", patient_id=patient_id, markdown_text=markdown_text)

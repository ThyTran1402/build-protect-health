# agents/agent_report.py
from google.adk.agents import LlmAgent

GEMINI_TEXT = "gemini-2.0-flash"

reporter = LlmAgent(
    name="reporter",
    model=GEMINI_TEXT,
    instruction=(
        "Compare the current patient metrics (from session state) with prior "
        "records. Identify trends, improvements, or concerns. "
        "Output a structured summary in Markdown with sections: "
        "Summary, Trends, and What to discuss next. "
        "Avoid diagnosis; phrase recommendations as questions for the doctor."
    ),
    output_key="report_markdown"
)

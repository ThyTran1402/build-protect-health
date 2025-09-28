# agents/agent_task_intake.py
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext

GEMINI_TEXT = "gemini-2.0-flash"

# Single-step agent: extract tasks from transcript snippets
task_extractor = LlmAgent(
    name="task_extractor",
    model=GEMINI_TEXT,
    instruction=(
        "From the transcript snippet, extract concrete patient tasks "
        "(appointments, labs, medications, insurance paperwork). "
        "De-duplicate by title+due_date. "
        "Return JSON list with keys: title, due_date (optional), "
        "source, and confidence."
    ),
    output_key="task_delta"
)

# Loop until there are no new tasks OR max iterations reached
def should_stop(ctx: InvocationContext) -> bool:
    last_delta = ctx.state.get("task_delta")
    return not last_delta  # stop if no new tasks were extracted

task_loop = LoopAgent(
    name="task_loop",
    sub_agents=[task_extractor],
    max_iterations=5,
    stop_condition=should_stop
)

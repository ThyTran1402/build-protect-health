# agents/agent_coach.py
from google.adk.agents import LlmAgent

GEMINI_TEXT = "gemini-2.0-flash"

coach = LlmAgent(
    name="previsit_coach",
    model=GEMINI_TEXT,
    instruction=(
        "You are a helpful pre-visit coach. "
        "Given the patient's condition and type of visit, provide general, "
        "non-diagnostic guidance: what to eat/avoid, what to bring, "
        "and what questions to ask the doctor. "
        "Always encourage confirming with their clinician. "
        "Output JSON with keys: checklist, cautions, questions_for_doctor."
    ),
    output_key="coach_json"
)

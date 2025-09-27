# backend/main.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from google.adk.runners import InMemoryRunner
from agents.orchestrator import root_agent

app = FastAPI(title="MedAgents API")

runner = InMemoryRunner(app_name="medagents", root_agent=root_agent)

@app.post("/api/ingest/transcript")
async def ingest_transcript(snippet: str = Form(...), session_id: str = Form(...)):
    # push transcript chunk into state then run one loop iteration
    ctx = {"transcript_snippet": snippet}
    result = await runner.run_async(user_id="user-123", session_id=session_id, inputs=ctx)
    return {"state": result.state, "events": result.events}

@app.post("/api/skin/analyze")
async def skin_analyze(image: UploadFile = File(...), session_id: str = Form("skin")):
    content = await image.read()
    # store image in GCS (omitted for brevity); pass URL or base64 to the skin agent
    result = await runner.run_async(user_id="user-123", session_id=session_id,
                                    inputs={"skin_image_bytes": content})
    return {"skin": result.state.get("skin_agent_result")}

@app.post("/api/coach")
async def coach_reco(condition: str = Form(...), visit_type: str = Form(...), session_id: str = Form("coach")):
    result = await runner.run_async(user_id="user-123", session_id=session_id,
                                    inputs={"condition": condition, "visit_type": visit_type})
    return result.state.get("coach_json")

@app.get("/api/report/{session_id}")
async def get_report(session_id: str):
    result = await runner.run_async(user_id="user-123", session_id=session_id, inputs={})
    return {"report_markdown": result.state.get("report_markdown")}

# backend/main.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import InMemoryRunner
from multi_agents.orchestration import root_agent

app = FastAPI(title="MedAgents API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = InMemoryRunner(app_name="medagents", root_agent=root_agent)

@app.get("/")
async def root():
    return {"message": "Healthcare AI Agents API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "healthcare-agents-api"}

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

@app.post("/api/agents/process")
async def process_agents(data: dict):
    """
    Process healthcare data through the multi-agent system
    Expected data format:
    {
        "transcript": "doctor visit transcript",
        "condition": "patient condition",
        "visit_type": "visit type",
        "current_metrics": {...},
        "prior_metrics": {...}
    }
    """
    session_id = "process_session"
    
    # Process transcript if provided
    if data.get("transcript"):
        transcript_result = await runner.run_async(
            user_id="user-123", 
            session_id=session_id, 
            inputs={"transcript_snippet": data["transcript"]}
        )
    
    # Get coaching recommendations if condition and visit_type provided
    coach_result = None
    if data.get("condition") and data.get("visit_type"):
        coach_result = await runner.run_async(
            user_id="user-123", 
            session_id=session_id,
            inputs={
                "condition": data["condition"], 
                "visit_type": data["visit_type"]
            }
        )
    
    # Get final report
    report_result = await runner.run_async(
        user_id="user-123", 
        session_id=session_id, 
        inputs={}
    )
    
    # Format response to match frontend expectations
    return {
        "tasks": [
            {
                "title": "Follow up on medication changes",
                "due_date": "2024-01-15",
                "source": "Doctor's recommendation",
                "confidence": 0.95
            },
            {
                "title": "Schedule blood work",
                "due_date": "2024-01-20",
                "source": "Lab results needed",
                "confidence": 0.88
            }
        ],
        "guidance": {
            "checklist": [
                "Bring current medication list",
                "Prepare questions about symptoms",
                "Bring recent lab results"
            ],
            "cautions": [
                "Monitor blood sugar levels closely",
                "Watch for any new symptoms"
            ],
            "questions_for_doctor": [
                "How often should I check my blood sugar?",
                "Are there any side effects I should watch for?",
                "When should I schedule my next appointment?"
            ]
        },
        "report": report_result.state.get("report_markdown", "Health report generated successfully.")
    }

from mcp.server.fastmcp import FastMCP
from ..common.schemas import CoachOutput
from mcp.client import MCPToolClient


# mcp = FastMCP("coach-agent")

# @mcp.tool()
# def coach_for_visit(condition: str, visit_type: str) -> str:
#     # TODO: replace stub with Gemini Flash call with JSON schema
#     data = {
#       "checklist": ["Bring ID", "Bring insurance card", "List your meds"],
#       "cautions": ["Avoid heavy meals if fasting required"],
#       "questions_for_doctor": ["Any interactions with current meds?"]
#     }
#     CoachOutput.parse_obj(data)  # validate
#     return json.dumps(data)

# if __name__ == "__main__":
#     asyncio.run(mcp.run_stdio())
    
    
    
import asyncio, json, os
import vertexai
from vertexai.generative_models import GenerativeModel
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Init Vertex AI
PROJECT_ID = os.getenv("GCP_PROJECT", "build-protect-health")
LOCATION = os.getenv("GCP_REGION", "us-east1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Choose Gemini model
model = GenerativeModel("gemini-2.0-flash")

server = Server("coach-agent")

@server.tool()
async def coach_for_visit(condition: str, visit_type: str) -> str:
    """
    Generate pre-visit recommendations for patients.
    """
    prompt = f"""
    You are a pre-visit coach for a patient with {condition} coming for {visit_type}.
    Output **strict JSON** with fields:
      - checklist: list of things to bring/do
      - cautions: list of things to avoid
      - questions_for_doctor: list of suggested questions
    """
    response = model.generate_content(prompt)
    return response.text  # LLM should output JSON

if __name__ == "__main__":
    asyncio.run(stdio_server(server))


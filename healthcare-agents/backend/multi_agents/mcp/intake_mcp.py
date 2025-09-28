import asyncio, json
from mcp.server.fastmcp import FastMCP
from mcp.client import MCPToolClient
from ..common.schemas import Task
from ..tools.firestore import save_tasks

mcp = FastMCP("intake-agent")

@mcp.tool()
def extract_tasks_from_transcript(transcript: str) -> str:
    """
    Tool contract: returns JSON array of Task.
    In real use, call Gemini here. For demo, stub a deterministic result.
    """
    # TODO: replace stub with Gemini call
    tasks = [{"title": "Schedule fasting blood test", "due_date": None, "source":"doctor", "confidence":0.88}]
    return json.dumps(tasks)

@mcp.tool()
def persist_tasks(patient_id: str, tasks_json: str) -> str:
    arr = json.loads(tasks_json)
    parsed = [Task.parse_obj(t) for t in arr]
    res = save_tasks(patient_id, parsed)
    return json.dumps(res)

if __name__ == "__main__":
    asyncio.run(mcp.run_stdio())

# from google.adk.agents import LlmAgent, LoopAgent
# from google.adk.agents.invocation_context import InvocationContext

# GEMINI_TEXT = "gemini-2.0-flash"

# task_extractor = LlmAgent(
#     name="task_extractor",
#     model=GEMINI_TEXT,
#     instruction=(
#         "From the transcript snippet, extract concrete patient tasks "
#         "(appointments, labs, meds, paperwork). "
#         "Return JSON list {title, due_date?, source, confidence}."
#     ),
#     output_key="task_delta"
# )

# def stop_condition(ctx: InvocationContext) -> bool:
#     if ctx.state.get("iter", 0) >= 5:
#         return True
#     return not ctx.state.get("task_delta")

# task_loop = LoopAgent(
#     name="task_loop",
#     sub_agents=[task_extractor],
#     max_iterations=5,
#     stop_condition=stop_condition
# )


import json, asyncio
from typing import List, Tuple
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from .mcp.client import MCPToolClient
from .common.schemas import Task


GEMINI_TEXT = "gemini-2.0-flash"
_mcp_intake = MCPToolClient(["python", "-m", "multi_agents.mcp.intake_mcp"])

task_extractor = LlmAgent(
    name="task_extractor",
    model=GEMINI_TEXT,
    instruction=(
      "Extract concrete patient tasks from {transcript_snippet}. "
      "Return strict JSON array with objects: "
      "{title, due_date?, source, confidence}. No prose."
    ),
    output_key="task_delta"
)

def _dedupe_and_filter(arr: List[dict], seen: set) -> Tuple[List[Task], set]:
    kept = []
    for d in arr:
        try:
            t = Task.parse_obj(d)
            key = (t.title.lower(), t.due_date.isoformat() if t.due_date else "")
            if key not in seen and t.confidence >= 0.7:
                kept.append(t); seen.add(key)
        except Exception:
            continue
    return kept, seen

async def _persist(patient_id: str, tasks: List[Task]):
    payload = json.dumps([t.dict() for t in tasks])
    return _mcp_intake.call("persist_tasks", patient_id=patient_id, tasks_json=payload)

def stop_condition(ctx: InvocationContext) -> bool:
    # stop if: 2 empties, or >=5 iters, or no new tasks
    if ctx.state.get("iter", 0) >= 5: return True
    if ctx.state.get("empty_count", 0) >= 2: return True
    last = ctx.state.get("task_delta") or []
    return len(last) == 0

async def loop_step(ctx: InvocationContext):
    # 1) ask MCP to extract (or use LLM directly). We’ll demo MCP path:
    transcript = ctx.inputs.get("transcript_snippet", "")
    extracted = _mcp_intake.call("extract_tasks_from_transcript", transcript=transcript)

    # 2) dedupe + filter
    seen = set(ctx.state.get("seen_hashes", []))
    kept, seen = _dedupe_and_filter(extracted, seen)

    if kept:
        await _persist(ctx.inputs.get("patient_id", "demo-patient"), kept)
        ctx.state["task_delta"] = [t.dict() for t in kept]
        ctx.state["seen_hashes"] = list(seen)
        ctx.state["empty_count"] = 0
    else:
        ctx.state["task_delta"] = []
        ctx.state["empty_count"] = ctx.state.get("empty_count", 0) + 1
    ctx.state["iter"] = ctx.state.get("iter", 0) + 1


task_loop = LoopAgent(
    name="task_loop",
    sub_agents=[task_extractor],
    max_iterations=5,
)

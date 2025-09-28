import asyncio, json
from mcp.server.fastmcp import FastMCP
from ..tools.firestore import get_prior_metrics, save_report
from ..tools.pdf_render import render_pdf_from_markdown

mcp = FastMCP("report-agent")

@mcp.tool()
def prior_metrics(patient_id: str) -> str:
    return json.dumps(get_prior_metrics(patient_id))

@mcp.tool()
def publish_report(patient_id: str, markdown_text: str) -> str:
    url = render_pdf_from_markdown(markdown_text, f"reports/{patient_id}.html")
    rid = save_report(patient_id, markdown_text, url)
    return json.dumps({"report_id": rid, "url": url})

if __name__ == "__main__":
    asyncio.run(mcp.run_stdio())

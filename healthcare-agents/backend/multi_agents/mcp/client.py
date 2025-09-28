import json, asyncio
import asyncio, json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPToolClient:
    def __init__(self, cmd: list[str]):
        self.cmd = cmd

    async def _open(self):
        # Create stdio client with subprocess command
        client = await stdio_client(StdioServerParameters(command=self.cmd))
        return client

    def call(self, tool_name: str, **kwargs):
        return asyncio.run(self._call(tool_name, **kwargs))

    async def _call(self, tool_name: str, **kwargs):
        client = await self._open()
        try:
            result = await client.call_tool(tool_name, **kwargs)
            # convert JSON strings to dicts if needed
            if isinstance(result, str):
                return json.loads(result)
            return result
        finally:
            await client.close()

import sys
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("demo-mcp-server")

def log(msg: str):
    print(f"[demo-mcp-server] {msg}", file=sys.stderr)

init_opts = {}
@server.list_tools()
async def list_tools():
    log("Client requested tool list")
    return [
        Tool(
            name="echo",
            description="Echo back the input text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            },
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    log(f"Tool called: {name} with args: {arguments}")
    if name == "echo":
        return [
            TextContent(
                type="text",
                text=f"echo: {arguments['text']}"
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    log("Starting MCP server…")
    async with stdio_server() as (read, write):
        log("stdio transport established; server is now running")
        await server.run(read, write,init_opts)
    log("Server shut down")

if __name__ == "__main__":
    asyncio.run(main())

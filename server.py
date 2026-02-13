import sys
import asyncio
from mcp.server import (
    Server,
)

from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult
from tools.echo import echo_tool
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions

server = Server("demo-mcp-server")
TOOLS = {
    "echo": {
    "handler": echo_tool,
    "schema": {
        "type": "object",
        "properties":{"text": {"type":"string"}},
        "required":["text"]
    },
    "description": "Echo back the input text",
    "output_schema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"]
    }
    }
}

def log(msg: str):
    print(f"[demo-mcp-server] {msg}", file=sys.stderr)

@server.list_tools()
async def list_tools()-> ListToolsResult:
    return ListToolsResult(
        tools =[
            Tool(
                name = name,
                description= meta["description"],
                inputSchema= meta["schema"],
                outputSchema=meta["output_schema"],
            )
        for name, meta in TOOLS.items()
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    log(f"Tool called: {name} with args: {arguments}")
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    try:
        handler = TOOLS[name]["handler"]
        result = await handler(**arguments)
    except Exception as e:
        log(f"Error in tool {name}: {e}")
        raise
    return result


async def main():
    log("Starting demo-mcp-server... waiting for MCP client connection")

    try:
        async with stdio_server() as (read_stream, write_stream):
            log("demo-mcp-server connected. Running event loop.")

            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="my-mcp-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    except asyncio.CancelledError:
        log("Received cancellation. Shutting down gracefully.")
        raise

    except Exception as e:
        log(f"Unexpected error: {e}")

    finally:
        log("demo-mcp-server has shut down cleanly.")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(
        ["python", "server.py"]
    ) as client:

        tools = await client.list_tools()
        print("TOOLS:", tools)

        result = await client.call_tool(
            "echo",
            {"text": "hello mcp"}
        )
        print("RESULT:", result)

asyncio.run(main())

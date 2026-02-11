from mcp.types import TextContent
async def echo_tool(text: str) -> str:
    return [TextContent(type ="text", text = text)]
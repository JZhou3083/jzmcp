from mcp.types import TextContent
async def echo_tool(text: str) -> list:
    return [TextContent(type ="text", text = text)]
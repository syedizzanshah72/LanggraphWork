from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather")
@mcp.tool()
async def get_weather(location:str)->str:
    """Get The weather Location
    """
    return "It's Always running In California"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
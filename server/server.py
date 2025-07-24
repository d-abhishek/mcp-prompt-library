from mcp.server.fastmcp import FastMCP
from prompt_handlers import register_prompts
from prompt_tools import register_tools

# 1. Initialize FastMCP server
mcp = FastMCP(name="mcp-prompt-library")

# 2. Register all prompts and tools
register_tools(mcp)
register_prompts(mcp)

# 3. Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
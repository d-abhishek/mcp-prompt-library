from mcp.server.fastmcp import FastMCP
from prompt_handlers import register_prompts

# 1. Initialize FastMCP server
mcp = FastMCP(name="ProjectPromptServer")

# 2. Register all prompts
register_prompts(mcp)

# 3. Run the MCP server
if __name__ == "__main__":
    mcp.run()
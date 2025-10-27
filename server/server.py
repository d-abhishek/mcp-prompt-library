import os
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from prompt_handlers import register_prompts
from prompt_tools import register_tools
from fastmcp.server.auth.providers.descope import DescopeProvider

# Load environment variables from .env file (if it exists)
# In production/CI, environment variables should be set directly in the pipeline
# env_path = Path(__file__).parent.parent / '.env'
# if env_path.exists():
#     load_dotenv(dotenv_path=env_path)

# 1. Initialize FastMCP server
# auth_provider = DescopeProvider(
#     project_id=os.environ["DESCOPE_PROJECT_ID"],        # Your Descope Project ID
#     base_url=os.environ["SERVER_URL"],                  # Your server's public URL
#     descope_base_url=os.environ["DESCOPE_BASE_URL"],    # Descope API base URL
# )
# mcp = FastMCP(name="mcp-prompt-library", auth=auth_provider) # Localhost testing only

mcp = FastMCP(name="mcp-prompt-library")

# 2. Register all prompts and tools
register_tools(mcp)
register_prompts(mcp)
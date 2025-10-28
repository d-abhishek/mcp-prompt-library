# server/server.py
import os
from pathlib import Path
from dotenv import load_dotenv

from fastmcp import FastMCP
from .prompt_handlers import register_prompts
from .prompt_tools import register_tools

from fastmcp.server.auth.providers.descope import DescopeProvider

# Load .env from repo root (optional)
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

auth_provider = DescopeProvider(
    project_id=os.environ["DESCOPE_PROJECT_ID"],        # Your Descope Project ID
    base_url=os.environ["SERVER_URL"],                  # Your server's public URL
    descope_base_url=os.environ["DESCOPE_BASE_URL"],    # Descope API base URL
)
mcp = FastMCP(name="mcp-prompt-library", auth=auth_provider)

register_tools(mcp)
register_prompts(mcp)

# Expose ASGI app at /mcp
app = mcp.http_app()

# Health endpoint for checks
from starlette.responses import JSONResponse  # noqa: E402
@mcp.custom_route("/health", methods=["GET"])
async def health(_):
    return JSONResponse({"status": "healthy"})

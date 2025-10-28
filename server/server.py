# server/server.py
import os
from pathlib import Path
from dotenv import load_dotenv

from fastmcp import FastMCP
from prompt_handlers import register_prompts
from prompt_tools import register_tools

# Load .env from repo root (optional)
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

mcp = FastMCP(name="mcp-prompt-library")

register_tools(mcp)
register_prompts(mcp)

# Expose ASGI app at /mcp
app = mcp.http_app()

# Health endpoint for checks
from starlette.responses import JSONResponse  # noqa: E402
@mcp.custom_route("/health", methods=["GET"])
async def health(_):
    return JSONResponse({"status": "healthy"})

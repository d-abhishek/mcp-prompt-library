# in server/server.py
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from .prompt_handlers import register_prompts
from .prompt_tools import register_tools

import logging
import sys

print("✅ server/server.py loaded", file=sys.stderr)
logging.basicConfig(level=logging.INFO)

# Create the MCP server
mcp = FastMCP(name="mcp-prompt-library")
register_tools(mcp)
register_prompts(mcp)

# Create the main MCP HTTP app
mcp_app = mcp.http_app()

# Create a simple health check endpoint
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-prompt-library"})

# Create a simple ASGI app that routes health to our function and everything else to MCP
async def asgi_app(scope, receive, send):

    if scope["type"] == "http":
        path = scope.get("path", "/")
        if path == "/health":
            # Handle health check directly
            response = JSONResponse({"status": "healthy", "service": "mcp-prompt-library"})
            await response(scope, receive, send)
            return
    
    # For all other requests, delegate to the MCP app
    await mcp_app(scope, receive, send)

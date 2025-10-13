#!/usr/bin/env python3
"""
Entry point for running the MCP server as a module.
This allows: python -m server
"""

from .server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
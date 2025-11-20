"""
Simple runner script for the MCP server.
This avoids relative import issues when using fastmcp.

Use - fastmcp run run_server.py --transport http --port 8000
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the server module
from server.server import mcp, app

# Expose the app for fastmcp to find
__all__ = ['mcp', 'app']

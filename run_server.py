"""
Simple runner script for the MCP server.
This avoids relative import issues when using fastmcp.
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

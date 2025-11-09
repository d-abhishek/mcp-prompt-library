"""
Base class for all MCP tools.

This module provides a simple base class that all tool classes can inherit from.
It provides common functionality and a consistent interface.
"""

from typing import Any


class BaseTool:
    """Base class for all MCP tools.
    
    This class provides a foundation for building MCP tools with shared
    functionality and consistent patterns.
    """
    
    def __init__(self):
        """Initialize the base tool."""
        pass
    
    def __repr__(self) -> str:
        """Return a string representation of the tool."""
        return f"<{self.__class__.__name__}>"

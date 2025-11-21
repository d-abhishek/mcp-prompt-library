"""
Resource registry for MCP server.

This module registers static resources like guidelines, documentation,
and configuration files that can be accessed by MCP clients.
"""

import pathlib
from typing import Optional

from .config import SOURCE_GITHUB_DIR


def register_resources(mcp):
    """Register all MCP resources for guidelines and documentation"""
    
    @mcp.resource(
        uri="resource://guidelines/commit-messages",
        meta={"version": "1.0"}
    )
    def get_commit_message_guidelines() -> str:
        """
        Git & GitHub Standards - Commit Message Format and Best Practices
        
        Provides comprehensive guidelines for:
        - Conventional commit format
        - Branch naming conventions
        - Pull request standards
        - Development workflow best practices
        
        Returns the complete commit message and GitHub workflow guidelines.
        """
        file_path = SOURCE_GITHUB_DIR / "copilot-commit-message-instructions.md"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return "❌ Error: Commit message guidelines file not found"
        except Exception as e:
            return f"❌ Error reading commit message guidelines: {str(e)}"
    
    @mcp.resource(
        uri="resource://guidelines/coding-standards",
        meta={"version": "1.0"}
    )
    def get_coding_standards() -> str:
        """
        Company Guidelines for GitHub Copilot - Code Quality & Development Standards
        
        Provides comprehensive guidelines for:
        - Code readability and consistency
        - Documentation standards
        - Architecture & design principles
        - Security & compliance
        - Performance & efficiency
        - Error handling & robustness
        - Testing & quality assurance
        - Code review focus areas
        - Language-specific guidelines
        
        Returns the complete code quality and development standards guidelines.
        """
        file_path = SOURCE_GITHUB_DIR / "copilot-instructions.md"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return "❌ Error: Code quality guidelines file not found"
        except Exception as e:
            return f"❌ Error reading code quality guidelines: {str(e)}"

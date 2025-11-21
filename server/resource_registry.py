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
        name="Git & GitHub Standards",
        description="Provides comprehensive guidelines for conventional commit format, branch naming conventions, pull request standards, and development workflow best practices",
        enabled=True,
        tags={"guidelines", "git", "commits"},
        meta={"version": "1.0", "permissions": ["admin", "team-a", "team-b"]}
    )
    def get_commit_message_guidelines() -> str:
        """
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
        name="Code Quality & Development Standards",
        description="Provides comprehensive guidelines for code readability and consistency, documentation standards, architecture & design principles, security & compliance, performance & efficiency, error handling & robustness, testing & quality assurance, code review focus areas, and language-specific guidelines",
        enabled=True,
        tags={"guidelines", "code-quality", "standards"},
        meta={"version": "1.0", "permissions": ["admin", "team-a", "team-b"]}
    )
    def get_coding_standards() -> str:
        """
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

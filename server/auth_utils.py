"""
Authentication and Authorization Utilities for MCP Prompt Library.

This module provides helper functions for checking user permissions
based on AWS Cognito user groups with configurable role-based access control.
"""

from typing import List, Set, Dict
from fastmcp.server.dependencies import get_access_token


class InsufficientPermissionsError(Exception):
    """Raised when a user lacks required permissions for an operation."""
    pass


# ==================== ROLE-BASED ACCESS CONTROL CONFIGURATION ====================

# Define which tools each group can access
# Easy to extend - just add new groups and their allowed tools here
TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        # Admins can access ALL tools
        "create_prompt",
        "update_prompt",
        "delete_prompt",
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
    ],
    "team-a": [
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
    ],
    "team-b": [
        "list_prompts",
        "setup_work_environment",
    ],
    # Add more teams here as needed:
    # "team-c": [
    #     "list_prompts",
    #     "setup_work_environment",
    # ],
}

# Define which prompts each group can access
# Easy to extend - just add new groups and their allowed prompts here
PROMPT_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        # Admins can access ALL prompts
        "create_api",
        "code_review",
        "code_correctness_review",
        "performance_bottleneck_analysis",
        "security_vulnerability_analysis",
        "code_simplification_deduplication",
        "error_handling_and_logging",
        "bug_analysis_and_resolution",
        "code_refactoring",
        "generate_project_documentation",
        "generate_test_scenarios",
    ],
    "team-a": [
        "create_api",
        "code_review",
        "code_correctness_review",
        "performance_bottleneck_analysis",
        "security_vulnerability_analysis",
        "code_simplification_deduplication",
        "error_handling_and_logging",
        "bug_analysis_and_resolution",
        "code_refactoring",
        "generate_project_documentation",
        "generate_test_scenarios",
    ],
    "team-b": [
        "code_review",
        "code_correctness_review",
        "bug_analysis_and_resolution",
    ],
    # Add more teams here as needed:
    # "team-c": [
    #     "code_review",
    #     "bug_analysis_and_resolution",
    # ],
}


def get_allowed_tools_for_groups(groups: List[str]) -> Set[str]:
    """Get the combined set of allowed tools for the given groups.
    
    Args:
        groups: List of group names the user belongs to
        
    Returns:
        Set of tool names the user can access based on all their group memberships
    """
    allowed_tools = set()
    for group in groups:
        if group in TOOL_PERMISSIONS:
            allowed_tools.update(TOOL_PERMISSIONS[group])
    return allowed_tools


def get_allowed_prompts_for_groups(groups: List[str]) -> Set[str]:
    """Get the combined set of allowed prompts for the given groups.
    
    Args:
        groups: List of group names the user belongs to
        
    Returns:
        Set of prompt names the user can access based on all their group memberships
    """
    allowed_prompts = set()
    for group in groups:
        if group in PROMPT_PERMISSIONS:
            allowed_prompts.update(PROMPT_PERMISSIONS[group])
    return allowed_prompts


def get_user_groups() -> List[str]:
    """Get the list of Cognito groups the current user belongs to.
    
    Returns:
        List of group names the user is a member of.
        Returns empty list if no groups are assigned.
    
    Raises:
        RuntimeError: If called outside of an authenticated request context.
    """
    try:
        token = get_access_token()
        groups = token.claims.get("cognito:groups", []) # type: ignore
        return groups if groups else []
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve user groups: {str(e)}")


def require_tool_access(tool_name: str) -> None:
    """Require that the user has access to a specific tool.
    
    Checks if any of the user's groups grant access to the specified tool.
    
    Args:
        tool_name: Name of the tool to check access for
        
    Raises:
        InsufficientPermissionsError: If the user doesn't have access to the tool
    """
    user_groups = get_user_groups()
    allowed_tools = get_allowed_tools_for_groups(user_groups)
    token = get_access_token()
    username = token.claims.get("username", "unknown") # type: ignore
    
    if tool_name not in allowed_tools:
        # Find which groups have access to this tool for the error message
        groups_with_access = [
            group for group, tools in TOOL_PERMISSIONS.items() 
            if tool_name in tools
        ]
        
        raise InsufficientPermissionsError(
            f"Access denied. User '{username}' does not have permission to use '{tool_name}'. "
            f"Required group membership: {', '.join(groups_with_access)}. "
            f"Current groups: {', '.join(user_groups) if user_groups else 'none'}"
        )


def require_prompt_access(prompt_name: str) -> None:
    """Require that the user has access to a specific prompt.
    
    Checks if any of the user's groups grant access to the specified prompt.
    
    Args:
        prompt_name: Name of the prompt to check access for
        
    Raises:
        InsufficientPermissionsError: If the user doesn't have access to the prompt
    """
    user_groups = get_user_groups()
    allowed_prompts = get_allowed_prompts_for_groups(user_groups)
    token = get_access_token()
    username = token.claims.get("username", "unknown") # type: ignore
    
    if prompt_name not in allowed_prompts:
        # Find which groups have access to this prompt for the error message
        groups_with_access = [
            group for group, prompts in PROMPT_PERMISSIONS.items() 
            if prompt_name in prompts
        ]
        
        raise InsufficientPermissionsError(
            f"Access denied. User '{username}' does not have permission to use prompt '{prompt_name}'. "
            f"Required group membership: {', '.join(groups_with_access)}. "
            f"Current groups: {', '.join(user_groups) if user_groups else 'none'}"
        )

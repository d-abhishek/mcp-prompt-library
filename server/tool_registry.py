"""
MCP Prompt Tools - Slim orchestrator for tool registration.

This module serves as the entry point for registering all MCP tools.
The actual tool implementations are organized in the tools/ package.
"""

from typing import List, Dict, Any, Optional

from .tools import (
    PromptManagementTool,
    EnvironmentSetupTool,
    FlutterSetupTool
)
from .auth_utils import require_tool_access, InsufficientPermissionsError


def register_tools(mcp):
    """Register all MCP tools for prompt management.
    
    This function instantiates all tool classes and registers their methods
    as MCP tools using the provided mcp instance.
    
    Args:
        mcp: The MCP server instance to register tools with
    """
    # Instantiate tool classes
    prompt_tool = PromptManagementTool()
    env_tool = EnvironmentSetupTool()
    flutter_tool = FlutterSetupTool()
    
    # ==================== PROMPT MANAGEMENT TOOLS ====================
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def create_prompt(
        Name: str,
        Description: str,
        Content: str,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Create a new MCP prompt file with frontmatter metadata.
        
        **ADMIN ONLY**: This tool requires admin group membership.
        
        Args:
            name: The name/identifier for the prompt
            description: Description of what the prompt does
            content: The prompt content (must use Jinja2 template syntax - see template guidelines below)
            arguments: Optional list of argument definitions with 'name', 'description', and 'required' fields
        
        Template Syntax Guidelines:
            This system uses Jinja2 templating engine. Please follow these syntax rules:
            
            ✅ CORRECT Jinja2 Syntax:
            - Variables: {{ variable_name }}
            - Conditionals: {% if condition %} ... {% endif %}
            - Equality: {% if var == "value" %} ... {% endif %}
            - Nested conditions: {% if outer %} {% if inner %} ... {% endif %} {% endif %}
            - Comments: {# This is a comment #}
            
            ❌ INCORRECT (Handlebars/Mustache syntax - will cause errors):
            - {{#if condition}} ... {{/if}}
            - {{#eq var "value"}} ... {{/eq}}
            - {{#unless condition}} ... {{/unless}}
            
            📝 Template Variables:
            - Reference argument values using: {{ argument_name }}
            - Use conditionals to show content based on arguments: {% if argument_name %} ... {% endif %}
            - Check argument values: {% if argument_name == "specific_value" %} ... {% endif %}
            
            📚 Examples:
            {% if user_input %}
            You provided: {{ user_input }}
            {% endif %}
            
            {% if mode == "detailed" %}
            ## Detailed Analysis
            {{ detailed_content }}
            {% else %}
            ## Quick Summary
            {{ summary_content }}
            {% endif %}
        """
        # Check tool access permissions
        try:
            require_tool_access("create_prompt")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return prompt_tool.create_prompt(Name, Description, Content, Arguments)
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def update_prompt(
        Name: str,
        Description: Optional[str] = None,
        Content: Optional[str] = None,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Update an existing MCP prompt file.
        
        **ADMIN ONLY**: This tool requires admin group membership.
        
        Args:
            name: The name/identifier of the prompt to update
            description: New description (optional)
            content: New prompt content (optional - must use Jinja2 template syntax if provided)
            arguments: New argument definitions (optional)
        
        Note: Content must follow Jinja2 template syntax guidelines. Use {% if %} instead of {{#if}}.
        """
        # Check tool access permissions
        try:
            require_tool_access("update_prompt")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return prompt_tool.update_prompt(Name, Description, Content, Arguments)
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def delete_prompt(Name: str) -> str:
        """Delete an MCP prompt file.
        
        **ADMIN ONLY**: This tool requires admin group membership.
        
        Args:
            name: The name/identifier of the prompt to delete
        """
        # Check tool access permissions
        try:
            require_tool_access("delete_prompt")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return prompt_tool.delete_prompt(Name)
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def list_prompts(include_content: bool = False, query: Optional[str] = None) -> str:
        """List all available MCP prompts or suggest the best matching prompts for a query.
        
        Args:
            include_content: Whether to include the full content of each prompt
            query: Optional search query to filter and rank prompts by relevance
        """
        # Check tool access permissions
        try:
            require_tool_access("list_prompts")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return prompt_tool.list_prompts(include_content, query)
    
    # ==================== ENVIRONMENT SETUP TOOLS ====================
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def setup_work_environment(
        target_directory: str,
        update_vscode_settings: bool = True,
        update_gitignore: bool = True,
        gitignore_entries: Optional[List[str]] = None
    ) -> str:
        """Setup work environment by copying GitHub Copilot instruction files to target directory.
        
        EXACTLY what this tool does:
        1. Creates .github folder in target directory
        2. Copies copilot-instructions.md (code quality guidelines)
        3. Copies copilot-commit-message-instructions.md (Git standards)
        4. Optionally updates VS Code user settings for commit message generation
        5. Optionally updates .gitignore to exclude .github/ folder and other entries
        
        Args:
            target_directory: The root directory where .github folder should be created
            update_vscode_settings: Whether to update VS Code settings (default: True)
            update_gitignore: Whether to update .gitignore file (default: True)
            gitignore_entries: Custom entries to add to .gitignore (default: [".github/"])
        """
        # Check tool access permissions
        try:
            require_tool_access("setup_work_environment")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return env_tool.setup_work_environment(
            target_directory,
            update_vscode_settings,
            update_gitignore,
            gitignore_entries
        )
    
    # ==================== FLUTTER SETUP TOOLS ====================
    
    @mcp.tool(
        meta={"version": "1.0"}
    )
    def setup_flutter_developer_environment(
        target_directory: str,
        flutter_version: str = "latest",
        codecommit_repo_url: Optional[str] = None,
        aws_profile: Optional[str] = None,
        install_git: bool = True,
        install_aws_cli: bool = True,
        install_flutter: bool = True,
        install_vscode_extensions: bool = True
    ) -> str:
        """Setup a complete Flutter development environment for a new developer.
        
        This tool automates the onboarding process by:
        1. Installing Flutter SDK (latest stable version)
        2. Installing AWS CLI
        3. Installing Git
        4. Cloning project from AWS CodeCommit
        5. Installing VS Code Flutter/Dart extensions (if VS Code is detected)
        6. Running flutter doctor to verify setup
        
        Args:
            target_directory: Directory where the project should be cloned
            flutter_version: Flutter SDK version to install (default: "latest" for latest stable)
            codecommit_repo_url: AWS CodeCommit repository URL to clone
            aws_profile: AWS CLI profile to use for CodeCommit access
            install_git: Whether to install Git (default: True)
            install_aws_cli: Whether to install AWS CLI (default: True)
            install_flutter: Whether to install Flutter SDK (default: True)
            install_vscode_extensions: Whether to install VS Code extensions (default: True)
        """
        # Check tool access permissions
        try:
            require_tool_access("setup_flutter_developer_environment")
        except InsufficientPermissionsError as e:
            return f"❌ {str(e)}"
        
        return flutter_tool.setup_flutter_developer_environment(
            target_directory,
            flutter_version,
            codecommit_repo_url,
            aws_profile,
            install_git,
            install_aws_cli,
            install_flutter,
            install_vscode_extensions
        )

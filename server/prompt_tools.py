import frontmatter
import pathlib
import os
import shutil
import json
import platform
from typing import List, Dict, Any, Optional

# Get the prompts directory
prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"
# Get the source .github directory with instruction files
source_github_dir = pathlib.Path(__file__).parent.parent / "data/setup_work_environment"

def validate_prompt_metadata(metadata: Dict[str, Any]) -> bool:
    """Validate that prompt metadata has required fields"""
    required_fields = ['name', 'description']
    return all(field in metadata for field in required_fields)

def sanitize_filename(name: str) -> str:
    """Sanitize a name to be used as a filename"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()

def validate_jinja2_syntax(content: str) -> tuple[bool, List[str]]:
    """Validate that content uses Jinja2 syntax, not Handlebars/Mustache
    
    Returns:
        tuple: (is_valid, list_of_warnings)
    """
    warnings = []
    
    # Check for common Handlebars patterns
    handlebars_patterns = [
        ('{{#if', 'Use {% if condition %} instead of {{#if condition}}'),
        ('{{#eq', 'Use {% if var == "value" %} instead of {{#eq var "value"}}'),
        ('{{#unless', 'Use {% if not condition %} instead of {{#unless condition}}'),
        ('{{#each', 'Use {% for item in items %} instead of {{#each items}}'),
        ('{{/if}}', 'Use {% endif %} instead of {{/if}}'),
        ('{{/eq}}', 'Use {% endif %} instead of {{/eq}}'),
        ('{{/unless}}', 'Use {% endif %} instead of {{/unless}}'),
        ('{{/each}}', 'Use {% endfor %} instead of {{/each}}')
    ]
    
    for pattern, message in handlebars_patterns:
        if pattern in content:
            warnings.append(f"⚠️  Found '{pattern}': {message}")
    
    is_valid = len(warnings) == 0
    return is_valid, warnings

def get_vscode_user_settings_path() -> pathlib.Path:
    """Get the VS Code user settings.json path for the current operating system"""
    system = platform.system()
    
    if system == "Windows":
        # Windows: %APPDATA%\Code\User\settings.json
        appdata = os.environ.get('APPDATA')
        if appdata:
            return pathlib.Path(appdata) / "Code" / "User" / "settings.json"
    elif system == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/Code/User/settings.json
        home = pathlib.Path.home()
        return home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    elif system == "Linux":
        # Linux: ~/.config/Code/User/settings.json
        home = pathlib.Path.home()
        return home / ".config" / "Code" / "User" / "settings.json"
    
    # Fallback - try Windows path as default
    appdata = os.environ.get('APPDATA', '')
    if appdata:
        return pathlib.Path(appdata) / "Code" / "User" / "settings.json"
    
    # Last resort fallback
    home = pathlib.Path.home()
    return home / ".vscode" / "settings.json"


def update_vscode_user_settings(target_directory: str) -> tuple[bool, str]:
    """Update VS Code user settings.json to include commit message instructions
    
    Safely preserves all existing settings while adding only the commit message instruction.
    
    Args:
        target_directory: The directory containing the .github folder
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        settings_path = get_vscode_user_settings_path()
        
        # Create the settings directory if it doesn't exist
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing settings or create empty dict
        settings = {}
        original_content = ""
        
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                    
                # Try to parse the JSON
                if original_content.strip():
                    settings = json.loads(original_content)
                    
            except json.JSONDecodeError as e:
                # If settings file has JSON errors, create a backup and start fresh
                backup_path = settings_path.with_suffix(f'.json.backup.{pathlib.Path().name}')
                try:
                    shutil.copy2(settings_path, backup_path)
                    return False, f"Settings file has JSON errors. Created backup at {backup_path}. Please fix the JSON and retry."
                except Exception:
                    return False, f"Settings file has JSON errors and couldn't create backup: {str(e)}"
            except Exception as e:
                return False, f"Could not read settings file: {str(e)}"
        
        # Ensure settings is a dictionary
        if not isinstance(settings, dict):
            settings = {}
        
        # Define our target setting
        commit_instructions_key = "github.copilot.chat.commitMessageGeneration.instructions"
        target_instruction = {
            "file": ".github/copilot-commit-message-instructions.md"
        }
        
        # Get current instructions or initialize empty list
        current_instructions = settings.get(commit_instructions_key, [])
        
        # Ensure it's a list
        if not isinstance(current_instructions, list):
            current_instructions = []
        
        # Check if our instruction already exists (exact match)
        instruction_exists = any(
            isinstance(instr, dict) and instr.get("file") == target_instruction["file"] 
            for instr in current_instructions
        )
        
        if not instruction_exists:
            # Add our instruction to the list
            current_instructions.append(target_instruction)
            settings[commit_instructions_key] = current_instructions
            
            # Write back to settings file with proper formatting
            try:
                with open(settings_path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False, sort_keys=False)
                
                return True, f"Added commit message instructions to VS Code settings"
                
            except Exception as e:
                # If write fails, restore the original content
                if original_content:
                    try:
                        with open(settings_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    except Exception:
                        pass  # Best effort to restore
                        
                return False, f"Failed to write settings file: {str(e)}"
        else:
            return True, f"Commit message instructions already exist in VS Code settings"
            
    except Exception as e:
        return False, f"Failed to update VS Code settings: {str(e)}"


def register_tools(mcp):
    """Register all MCP tools for prompt management"""
    
    @mcp.tool()
    def create_prompt(
        Name: str,
        Description: str,
        Content: str,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Create a new MCP prompt file with frontmatter metadata.
        
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
        try:
            # Validate Jinja2 syntax
            is_valid, warnings = validate_jinja2_syntax(Content)
            
            # Sanitize the filename
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
            # Check if file already exists
            if file_path.exists():
                return f"Error: Prompt '{Name}' already exists. Use update_prompt to modify it."
            
            # If there are syntax warnings, include them in the response but still create the prompt
            warning_message = ""
            if not is_valid:
                warning_message = "\n\n⚠️  TEMPLATE SYNTAX WARNINGS:\n" + "\n".join(warnings) + "\n\nThe prompt was created but may not render correctly. Please fix the syntax issues above.\n"
            
            # Prepare metadata
            metadata = {
                'name': Name,
                'description': Description
            }
            
            if Arguments:
                metadata['arguments'] = Arguments # type: ignore
            
            # Create the frontmatter post
            post = frontmatter.Post(Content)
            post.metadata.update(metadata)
            
            # Ensure prompts directory exists
            prompts_dir.mkdir(exist_ok=True)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            return f"Successfully created prompt '{Name}' at {file_path}{warning_message}"
            
        except Exception as e:
            return f"Error creating prompt: {str(e)}"
    
    @mcp.tool()
    def update_prompt(
        Name: str,
        Description: Optional[str] = None,
        Content: Optional[str] = None,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Update an existing MCP prompt file.
        
        Args:
            name: The name/identifier of the prompt to update
            description: New description (optional)
            content: New prompt content (optional - must use Jinja2 template syntax if provided)
            arguments: New argument definitions (optional)
        
        Note: Content must follow Jinja2 template syntax guidelines. Use {% if %} instead of {{#if}}.
        """
        try:
            # Validate Jinja2 syntax if content is being updated
            warning_message = ""
            if Content is not None:
                is_valid, warnings = validate_jinja2_syntax(Content)
                if not is_valid:
                    warning_message = "\n\n⚠️  TEMPLATE SYNTAX WARNINGS:\n" + "\n".join(warnings) + "\n\nThe prompt was updated but may not render correctly. Please fix the syntax issues above.\n"
            
            # Find the file
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
            if not file_path.exists():
                return f"Error: Prompt '{Name}' does not exist. Use create_prompt to create it."
            
            # Load existing prompt
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Update metadata
            if Description is not None:
                post.metadata['description'] = Description
            
            if Arguments is not None:
                post.metadata['arguments'] = Arguments
            
            # Update content
            if Content is not None:
                post.content = Content
            
            # Write back the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            return f"Successfully updated prompt '{Name}'{warning_message}"
            
        except Exception as e:
            return f"Error updating prompt: {str(e)}"
    
    @mcp.tool()
    def delete_prompt(Name: str) -> str:
        """Delete an MCP prompt file.
        
        Args:
            name: The name/identifier of the prompt to delete
        """
        try:
            # Find the file
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
            if not file_path.exists():
                return f"Error: Prompt '{Name}' does not exist."
            
            # Delete the file
            file_path.unlink()
            
            return f"Successfully deleted prompt '{Name}'"
            
        except Exception as e:
            return f"Error deleting prompt: {str(e)}"
    
    @mcp.tool()
    def list_prompts(include_content: bool = False, query: Optional[str] = None) -> str:
        """List all available MCP prompts or suggest the best matching prompts for a query.
        
        Args:
            include_content: Whether to include the full content of each prompt
            query: Optional search query to filter and rank prompts by relevance
        """
        try:
            if not prompts_dir.exists():
                return "No prompts directory found."
            
            prompt_files = list(prompts_dir.glob("*.md"))
            
            if not prompt_files:
                return "No prompts found."
            
            # Load all prompts and their metadata
            prompts_info = []
            for file_path in prompt_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    prompt_info = {
                        'name': post.metadata.get('name', file_path.stem),
                        'description': post.metadata.get('description', 'No description'),
                        'file': file_path.name,
                        'arguments': post.metadata.get('arguments', []),
                        'keywords': post.metadata.get('keywords', []),
                        'triggers': post.metadata.get('triggers', []),
                        'content_preview': post.content[:200] + "..." if len(post.content) > 200 else post.content
                    }
                    
                    if include_content:
                        prompt_info['content'] = post.content
                    
                    prompts_info.append(prompt_info)
                    
                except Exception as e:
                    prompts_info.append({
                        'name': file_path.stem,
                        'description': f'Error reading file: {str(e)}',
                        'file': file_path.name,
                        'arguments': [],
                        'keywords': [],
                        'triggers': [],
                        'content_preview': ''
                    })
            
            # If query is provided, filter and rank by relevance
            if query:
                query_lower = query.lower()
                scored_prompts = []
                
                for prompt in prompts_info:
                    score = 0
                    
                    # Score based on name matches
                    if any(word in prompt['name'].lower() for word in query_lower.split()):
                        score += 10
                    
                    # Score based on description matches
                    desc_words = prompt['description'].lower().split()
                    query_words = query_lower.split()
                    common_words = set(desc_words) & set(query_words)
                    score += len(common_words) * 5
                    
                    # Score based on keywords (if present)
                    keywords = prompt.get('keywords', [])
                    for keyword in keywords:
                        if keyword.lower() in query_lower:
                            score += 8
                    
                    # Score based on triggers (if present)
                    triggers = prompt.get('triggers', [])
                    for trigger in triggers:
                        if trigger.lower() in query_lower:
                            score += 15  # High score for trigger phrases
                    
                    # Specific keyword scoring for known patterns
                    if 'api' in query_lower and 'api' in prompt['name'].lower():
                        score += 15
                    if 'review' in query_lower and 'review' in prompt['name'].lower():
                        score += 15
                    if any(word in query_lower for word in ['create', 'build', 'generate']) and 'create' in prompt['name'].lower():
                        score += 10
                    
                    # Score based on content matches
                    content_words = prompt['content_preview'].lower().split()
                    common_content_words = set(content_words) & set(query_words)
                    score += len(common_content_words) * 2
                    
                    if score > 0:
                        scored_prompts.append((prompt, score))
                
                # Sort by score and filter to only relevant prompts
                scored_prompts.sort(key=lambda x: x[1], reverse=True)
                
                if not scored_prompts:
                    return f"No matching prompts found for query: '{query}'\n\nAll available prompts:\n" + "\n".join([f"- {p['name']}: {p['description']}" for p in prompts_info])
                
                # Format response for query results
                result = f"🎯 **Search results for**: '{query}'\n\n"
                
                best_match = scored_prompts[0]
                prompt_info = best_match[0]
                
                result += f"**Best match**: `{prompt_info['name']}` (score: {best_match[1]})\n"
                result += f"Description: {prompt_info['description']}\n\n"
                
                if prompt_info['arguments']:
                    result += "**Required arguments**:\n"
                    for arg in prompt_info['arguments']:
                        if arg.get('required', False):
                            result += f"- `{arg.get('name')}`: {arg.get('description', 'No description')}\n"
                    
                    result += "\n**Optional arguments**:\n"
                    for arg in prompt_info['arguments']:
                        if not arg.get('required', False):
                            result += f"- `{arg.get('name')}`: {arg.get('description', 'No description')}\n"
                
                result += f"\n**Usage**: Call the prompt `{prompt_info['name']}` with the appropriate arguments.\n"
                
                # Show other matches if any
                if len(scored_prompts) > 1:
                    result += f"\n**Other matches** ({len(scored_prompts)-1} found):\n"
                    for prompt_data, score in scored_prompts[1:4]:  # Show top 3 alternatives
                        result += f"- `{prompt_data['name']}` (score: {score}): {prompt_data['description']}\n"
                
                return result
            
            else:
                # No query provided - show all prompts (original behavior)
                result = f"📚 **All available prompts** ({len(prompts_info)} found):\n\n"
                
                for i, prompt in enumerate(prompts_info, 1):
                    result += f"{i}. **{prompt['name']}**\n"
                    result += f"   Description: {prompt['description']}\n"
                    result += f"   File: {prompt['file']}\n"
                    
                    if prompt['arguments']:
                        result += "   Arguments:\n"
                        for arg in prompt['arguments']:
                            req_text = " (required)" if arg.get('required', False) else " (optional)"
                            result += f"     - {arg.get('name', 'unnamed')}{req_text}: {arg.get('description', 'No description')}\n"
                    
                    if include_content:
                        result += f"   Content:\n{prompt['content']}\n"
                    
                    result += "\n"
                
                result += "\n💡 **Tip**: Use `list_prompts(query='your search terms')` to find specific prompts.\n"
                return result
            
        except Exception as e:
            return f"Error listing prompts: {str(e)}"

    @mcp.tool()
    def smart_prompt_executor(query: str, auto_execute: bool = False) -> str:
        """Automatically detect and execute the most appropriate prompt for a user query.
        
        Args:
            query: The user's natural language query or request
            auto_execute: If True, automatically execute the best matching prompt
        """
        try:
            # First, get the suggestion using list_prompts with query
            suggestion_result = list_prompts(include_content=False, query=query)
            
            if not auto_execute:
                return suggestion_result + "\n\n💡 **Tip**: Use `smart_prompt_executor` with `auto_execute=True` to automatically run the suggested prompt."
            
            # Extract parameters from query for auto-execution
            query_lower = query.lower()
            
            # For create_api prompt specifically
            if 'api' in query_lower and ('create' in query_lower or 'build' in query_lower or 'generate' in query_lower):
                # Try to extract purpose and parameters from the query
                api_purpose = ""
                expected_parameters = ""
                
                # Extract what comes after "api for"
                if 'api for' in query_lower:
                    start_idx = query_lower.find('api for') + 7
                    api_purpose_part = query[start_idx:].split('.')[0].split(',')[0].strip()
                    api_purpose = api_purpose_part if api_purpose_part else "data management"
                elif 'student' in query_lower:
                    api_purpose = "student information management"
                elif 'user' in query_lower:
                    api_purpose = "user management"
                else:
                    api_purpose = "data management"
                
                # Extract parameters if mentioned
                if 'parameters' in query_lower or 'fields' in query_lower:
                    # Try to extract parameter list
                    param_keywords = ['name', 'class', 'contact', 'address', 'email', 'phone', 'age', 'id']
                    found_params = [param for param in param_keywords if param in query_lower]
                    if found_params:
                        expected_parameters = ", ".join(found_params)
                
                # Import and execute the create_api prompt
                from prompt_handlers import load_template
                import jinja2
                
                template = load_template("create_api")
                result = template.render(
                    api_purpose=api_purpose,
                    expected_parameters=expected_parameters if expected_parameters else None,
                    custom_api_reference=None
                )
                
                return f"🚀 **Auto-executed**: `create_api` prompt\n\n**Detected Parameters**:\n- API Purpose: {api_purpose}\n- Expected Parameters: {expected_parameters or 'None specified'}\n\n**Generated Result**:\n\n{result}"
            
            else:
                return suggestion_result + "\n\n⚠️ **Auto-execution not implemented** for this prompt type yet. Please use the suggested prompt manually."
                
        except Exception as e:
            return f"Error in auto-execution: {str(e)}"

    @mcp.tool()
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
        try:
            # Validate and resolve target directory
            target_path = pathlib.Path(target_directory).resolve()
            
            if not target_path.exists():
                return f"Error: Target directory '{target_directory}' does not exist."
            
            if not target_path.is_dir():
                return f"Error: '{target_directory}' is not a directory."
            
            # Create .github directory in target location
            github_target_dir = target_path / ".github"
            github_target_dir.mkdir(exist_ok=True)
            
            # Define source files to copy
            files_to_copy = [
                "copilot-instructions.md",
                "copilot-commit-message-instructions.md"
            ]
            
            copied_files = []
            errors = []
            
            for filename in files_to_copy:
                source_file = source_github_dir / filename
                target_file = github_target_dir / filename
                
                if not source_file.exists():
                    errors.append(f"Source file '{filename}' not found in {source_github_dir}")
                    continue
                
                try:
                    # Copy the file
                    shutil.copy2(source_file, target_file)
                    copied_files.append(filename)
                except Exception as e:
                    errors.append(f"Failed to copy '{filename}': {str(e)}")
            
            # Update .gitignore if requested
            gitignore_success = False
            gitignore_message = ""
            if update_gitignore:
                try:
                    gitignore_path = target_path / ".gitignore"
                    
                    # Default entries if none specified
                    if gitignore_entries is None:
                        gitignore_entries = [".github/"]
                    
                    # Read existing content if file exists
                    existing_content = ""
                    if gitignore_path.exists():
                        with open(gitignore_path, 'r', encoding='utf-8') as f:
                            existing_content = f.read()
                    
                    # Check which entries need to be added
                    new_entries = []
                    for entry in gitignore_entries:
                        entry = entry.strip()
                        if entry and entry not in existing_content:
                            new_entries.append(entry)
                    
                    if new_entries:
                        # Append new entries
                        with open(gitignore_path, 'a', encoding='utf-8') as f:
                            if existing_content and not existing_content.endswith('\n'):
                                f.write('\n')
                            for entry in new_entries:
                                f.write(f"{entry}\n")
                        
                        gitignore_success = True
                        gitignore_message = f"Added {len(new_entries)} entries to .gitignore: {', '.join(new_entries)}"
                    else:
                        gitignore_success = True
                        gitignore_message = "All specified entries already exist in .gitignore"
                        
                except Exception as e:
                    gitignore_success = False
                    gitignore_message = f"Failed to update .gitignore: {str(e)}"
            
            # Update VS Code settings if requested
            vscode_success = False
            vscode_message = ""
            if update_vscode_settings:
                vscode_success, vscode_message = update_vscode_user_settings(target_directory)
            
            # Prepare result message
            result = f"🚀 **Work Environment Setup Complete**\n\n"
            result += f"**Target Directory**: {target_path}\n"
            result += f"**GitHub Directory**: {github_target_dir}\n\n"
            
            if copied_files:
                result += f"✅ **Successfully copied {len(copied_files)} file(s)**:\n"
                for filename in copied_files:
                    result += f"   - {filename}\n"
            
            if update_gitignore:
                if gitignore_success:
                    result += f"\n✅ **.gitignore**: {gitignore_message}\n"
                else:
                    result += f"\n⚠️ **.gitignore**: {gitignore_message}\n"
            
            if update_vscode_settings:
                if vscode_success:
                    result += f"\n✅ **VS Code Settings**: {vscode_message}\n"
                    result += f"   - Settings file: {get_vscode_user_settings_path()}\n"
                else:
                    result += f"\n⚠️ **VS Code Settings**: {vscode_message}\n"
            
            if errors:
                result += f"\n⚠️ **Encountered {len(errors)} error(s)**:\n"
                for error in errors:
                    result += f"   - {error}\n"
            
            result += f"\n📋 **Files provide**:\n"
            result += f"   - **copilot-instructions.md**: Comprehensive code quality guidelines, standards, and best practices\n"
            result += f"   - **copilot-commit-message-instructions.md**: Git commit message format, branch naming, and PR standards\n"
            
            if update_vscode_settings and vscode_success:
                result += f"\n� **VS Code Integration**:\n"
                result += f"   - GitHub Copilot will now use your commit message guidelines\n"
                result += f"   - Commit message suggestions will follow your standards\n"
                result += f"   - Setting: github.copilot.chat.commitMessageGeneration.instructions\n"
            
            result += f"\n�💡 **Next Steps**:\n"
            result += f"   1. Review and customize the guidelines for your team\n"
            result += f"   2. Restart VS Code to apply the new settings\n"
            result += f"   3. Set up pre-commit hooks for automated compliance\n"
            result += f"   4. Share with your development team\n"
            result += f"   5. Test GitHub Copilot commit message generation\n"
            
            return result
            
        except Exception as e:
            return f"Error setting up work environment: {str(e)}"

def get_tool_definitions() -> List[Dict[str, Any]]:
    """Get all tool definitions for MCP tools/list response"""
    return [
        {
            "name": "create_prompt",
            "description": "Create a new MCP prompt file with frontmatter metadata.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name/identifier for the prompt"
                    },
                    "description": {
                        "type": "string", 
                        "description": "Description of what the prompt does"
                    },
                    "content": {
                        "type": "string",
                        "description": "The prompt content (must use Jinja2 template syntax)"
                    },
                    "arguments": {
                        "type": "array",
                        "description": "Optional list of argument definitions",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "required": {"type": "boolean"}
                            }
                        }
                    }
                },
                "required": ["name", "description", "content"]
            }
        },
        {
            "name": "delete_prompt",
            "description": "Delete an MCP prompt file.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name/identifier of the prompt to delete"
                    }
                },
                "required": ["name"]
            }
        },
        {
            "name": "list_prompts",
            "description": "List all available MCP prompts or suggest the best matching prompts for a query.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "include_content": {
                        "type": "boolean",
                        "description": "Whether to include the full content of each prompt",
                        "default": False
                    },
                    "query": {
                        "type": "string",
                        "description": "Optional search query to filter and rank prompts by relevance"
                    }
                },
                "required": []
            }
        },
        {
            "name": "smart_prompt_executor",
            "description": "Automatically detect and execute the most appropriate prompt for a user query.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's natural language query or request"
                    },
                    "auto_execute": {
                        "type": "boolean",
                        "description": "If True, automatically execute the best matching prompt",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "setup_work_environment",
            "description": "Setup work environment by copying GitHub Copilot instruction files to target directory.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "target_directory": {
                        "type": "string",
                        "description": "The root directory where .github folder should be created"
                    },
                    "update_vscode_settings": {
                        "type": "boolean",
                        "description": "Whether to update VS Code settings",
                        "default": True
                    },
                    "update_gitignore": {
                        "type": "boolean", 
                        "description": "Whether to update .gitignore file",
                        "default": True
                    },
                    "gitignore_entries": {
                        "type": "array",
                        "description": "Custom entries to add to .gitignore",
                        "items": {"type": "string"},
                        "default": [".github/"]
                    }
                },
                "required": ["target_directory"]
            }
        },
        {
            "name": "update_prompt",
            "description": "Update an existing MCP prompt file.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name/identifier of the prompt to update"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)"
                    },
                    "content": {
                        "type": "string",
                        "description": "New prompt content (optional - must use Jinja2 template syntax if provided)"
                    },
                    "arguments": {
                        "type": "array",
                        "description": "New argument definitions (optional)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "required": {"type": "boolean"}
                            }
                        }
                    }
                },
                "required": ["name"]
            }
        }
    ]

def execute_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """Execute a tool by name with given arguments"""
    if tool_name == "create_prompt":
        return create_prompt_impl(
            args.get("name") or "",
            args.get("description") or "",
            args.get("content") or "",
            args.get("arguments")
        )
    elif tool_name == "delete_prompt":
        return delete_prompt_impl(args.get("name") or "")
    elif tool_name == "list_prompts":
        return list_prompts_impl(
            args.get("include_content", False),
            args.get("query")
        )
    elif tool_name == "smart_prompt_executor":
                return smart_prompt_executor_impl(
            args.get("query") or "",
            args.get("auto_execute", False)
        )
    elif tool_name == "setup_work_environment":
        return setup_work_environment_impl(
            args.get("target_directory") or "",
            args.get("update_vscode_settings", True),
            args.get("update_gitignore", True),
            args.get("gitignore_entries", [".github/"])
        )
    elif tool_name == "update_prompt":
                return update_prompt_impl(
            args.get("name") or "",
            args.get("description"),
            args.get("content"),
            args.get("arguments")
        )
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

# Implementation functions that map to the @mcp.tool decorated functions
def create_prompt_impl(name: str, description: str, content: str, arguments: Optional[List[Dict[str, Any]]] = None) -> str:
    """Implementation of create_prompt tool"""
    # This would call the actual implementation from the @mcp.tool function
    # For now, return a placeholder
    return f"Tool create_prompt called with name='{name}', description='{description}'"

def delete_prompt_impl(name: str) -> str:
    """Implementation of delete_prompt tool"""
    return f"Tool delete_prompt called with name='{name}'"

def list_prompts_impl(include_content: bool = False, query: Optional[str] = None) -> str:
    """Implementation of list_prompts tool"""
    return f"Tool list_prompts called with include_content={include_content}, query='{query}'"

def smart_prompt_executor_impl(query: str, auto_execute: bool = False) -> str:
    """Implementation of smart_prompt_executor tool"""
    return f"Tool smart_prompt_executor called with query='{query}', auto_execute={auto_execute}"

def setup_work_environment_impl(target_directory: str, update_vscode_settings: bool = True, update_gitignore: bool = True, gitignore_entries: Optional[List[str]] = None) -> str:
    """Implementation of setup_work_environment tool"""
    # Call the actual function that's already implemented
    gitignore_entries = gitignore_entries or [".github/"]
    return setup_work_environment(target_directory, update_vscode_settings, update_gitignore, gitignore_entries)

def update_prompt_impl(name: str, description: Optional[str] = None, content: Optional[str] = None, arguments: Optional[List[Dict[str, Any]]] = None) -> str:
    """Implementation of update_prompt tool"""
    return f"Tool update_prompt called with name='{name}'"

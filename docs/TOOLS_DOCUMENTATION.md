# MCP Prompt Management Tools

This MCP server provides tools for managing prompt files with frontmatter metadata. Each tool allows you to perform CRUD operations on prompt files stored in the `prompts/` directory.

## Available Tools

### Prompt Management Tools

#### 1. `create_prompt`
Creates a new MCP prompt file with frontmatter metadata.

**Access Required:** Admin only

**Parameters:**
- `name` (required): The name/identifier for the prompt
- `description` (required): Description of what the prompt does  
- `content` (required): The prompt content (can include Jinja2 template variables like `{{variable}}`)
- `arguments` (optional): List of argument definitions with `name`, `description`, and `required` fields

**Example:**
```json
{
  "name": "generate_function",
  "description": "Generate a function in a specific programming language",
  "content": "Please create a {{language}} function named **{{function_name}}** that {{description}}. Include:\n- Proper type hints/annotations\n- Error handling\n- Documentation/comments",
  "arguments": [
    {"name": "language", "description": "Programming language", "required": true},
    {"name": "function_name", "description": "Name of the function", "required": true},
    {"name": "description", "description": "What the function should do", "required": true}
  ]
}
```

#### 2. `update_prompt`
Updates an existing MCP prompt file.

**Access Required:** Admin only

**Parameters:**
- `name` (required): The name/identifier of the prompt to update
- `description` (optional): New description
- `content` (optional): New prompt content
- `arguments` (optional): New argument definitions

**Example:**
```json
{
  "name": "generate_function",
  "description": "Generate a well-documented function in a specific programming language",
  "content": "Please create a {{language}} function named **{{function_name}}** that {{description}}. Include:\n- Proper type hints/annotations\n- Comprehensive error handling\n- Detailed documentation/comments\n- Unit test examples"
}
```

#### 3. `delete_prompt`
Deletes an MCP prompt file.

**Access Required:** Admin only

**Parameters:**
- `name` (required): The name/identifier of the prompt to delete

**Example:**
```json
{
  "name": "generate_function"
}
```

#### 4. `list_prompts`
Lists all available MCP prompts with smart search capability.

**Access Required:** All users

**Parameters:**
- `query` (optional): Natural language search query to find specific prompts. Returns ranked results when provided.
- `include_content` (optional, default: false): Whether to include the full content of each prompt

**Example:**
```json
{
  "include_content": true
}
```

### Environment Setup Tools

#### 5. `setup_work_environment`
Sets up a work environment by copying GitHub Copilot instruction files to a target directory and optionally configuring VS Code settings and .gitignore.

**Access Required:** All users

**Scope - EXACTLY what it does:**
- Creates `.github` directory in target location
- Copies `copilot-instructions.md` (comprehensive coding guidelines)
- Copies `copilot-commit-message-instructions.md` (Git workflow standards)
- Updates VS Code user settings.json for commit message instructions (if enabled)
- Updates .gitignore with common development entries (if enabled)

**Scope - What it does NOT do:**
- Create .env files
- Install dependencies
- Modify package.json or project files
- Make git commits
- Perform any actions outside the specified parameters

**Parameters:**
- `target_directory` (required): The root directory where `.github` folder should be created
- `update_vscode_settings` (optional, default: true): Whether to update VS Code user settings for commit message generation
- `update_gitignore` (optional, default: true): Whether to update .gitignore file
- `gitignore_entries` (optional): Custom list of entries to add to .gitignore (default: [".github/"])

**Default .gitignore entries:**
```
# Development
.env
.env.local
.env.*.local
*.log

# OS
.DS_Store
Thumbs.db

# Editors
.vscode/settings.json
.idea/

# Dependencies
node_modules/
__pycache__/
*.pyc

# Build
dist/
build/
*.egg-info/
```

**Examples:**
```json
{
  "target_directory": "/path/to/your/project",
  "update_vscode_settings": true,
  "update_gitignore": true
}
```

```json
{
  "target_directory": "/path/to/your/project",
  "update_vscode_settings": false,
  "update_gitignore": true,
  "gitignore_entries": ["*.tmp", "temp/", "logs/"]
}
```

**VS Code Integration:**
When `update_vscode_settings` is true, the tool safely updates your VS Code user settings while preserving all existing configurations:

- **Preserves all existing settings**: Your current VS Code configuration remains completely intact
- **Smart duplicate detection**: Won't add duplicate entries if the setting already exists
- **Safe JSON handling**: Creates backups and recovers gracefully from corrupted settings files
- **Proper formatting**: Maintains clean JSON structure with 4-space indentation
- **Error recovery**: Automatically restores original content if any write operation fails

The tool adds this setting to your VS Code user settings:
```json
{
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "file": ".github/copilot-commit-message-instructions.md"
    }
  ]
}
```

This ensures GitHub Copilot uses your custom commit message guidelines when generating commit messages.

**Use Cases:**
- Setting up new development projects with standardized coding guidelines
- Onboarding new team members with consistent development standards
- Implementing company-wide coding practices across multiple repositories
- Establishing GitHub Copilot best practices for your organization
- Automatically configuring VS Code to use your commit message standards

## Prompt File Format

Each prompt file is stored as a Markdown file with YAML frontmatter:

```markdown
---
name: prompt_name
description: "Description of what the prompt does"
arguments:
  - name: variable_name
    description: "Description of the variable"
    required: true
---

Your prompt content here with {{variable_name}} placeholders.
```

## Usage Examples

### Creating a Code Review Prompt
```json
{
  "name": "code_review",
  "description": "Perform a comprehensive code review",
  "content": "Please review the following {{language}} code and provide feedback on:\n\n```{{language}}\n{{code}}\n```\n\nFocus on:\n- Code quality and best practices\n- Performance implications\n- Security considerations\n- Maintainability\n- Documentation",
  "arguments": [
    {"name": "language", "description": "Programming language of the code", "required": true},
    {"name": "code", "description": "Code to review", "required": true}
  ]
}
```

### Creating a Documentation Prompt
```json
{
  "name": "generate_docs",
  "description": "Generate documentation for code",
  "content": "Generate comprehensive documentation for the following {{type}}:\n\n{{code}}\n\nInclude:\n- Purpose and functionality\n- Parameters and return values\n- Usage examples\n- Error conditions",
  "arguments": [
    {"name": "type", "description": "Type of code (function, class, module, etc.)", "required": true},
    {"name": "code", "description": "Code to document", "required": true}
  ]
}
```

### Creating a Code Correctness Review Prompt
```json
{
  "name": "code_correctness_review",
  "description": "Review code for correctness, functional requirements, and potential bugs or issues",
  "content": "You are an expert {{language}} code reviewer specializing in correctness and functional requirements...",
  "arguments": [
    {"name": "code_reference", "description": "The code to review, file name, or function/method name to analyze for correctness and functionality", "required": true},
    {"name": "language", "description": "Programming language of the code (e.g., python, javascript, java)", "required": true},
    {"name": "functional_requirements", "description": "Functional requirements or specifications the code should meet", "required": true},
    {"name": "test_cases", "description": "Specific test cases or scenarios to verify against", "required": false}
  ]
}
```

### Setting Up Work Environment
```json
{
  "target_directory": "C:\\Users\\username\\Projects\\my-new-project",
  "update_vscode_settings": true
}
```

This will create a `.github` directory with:
- **copilot-instructions.md**: Comprehensive coding standards and best practices
- **copilot-commit-message-instructions.md**: Git workflow and commit message standards

And automatically configure VS Code by adding:
```json
{
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "file": ".github/copilot-commit-message-instructions.md"
    }
  ]
}
```

The files provide guidelines for:
- Code quality and consistency standards
- Security and compliance requirements
- Testing and documentation practices
- Git commit message formatting
- Branch naming conventions
- Pull request standards

**VS Code Benefits:**
- GitHub Copilot will automatically use your commit message guidelines
- Consistent commit message generation across your team
- No manual configuration required
- Works across all projects that include the `.github` folder

### Flutter Development Tools

#### 6. `install_flutter_sdk`
Downloads and installs a specific Flutter SDK version.

**Access Required:** Admin, Team A

**Parameters:**
- `version` (required): Flutter SDK version to install (e.g., "3.24.0")
- `channel` (required): Release channel - "stable", "beta", or "dev"
- `installation_path` (required): Directory path where Flutter SDK will be installed

**Example:**
```json
{
  "version": "3.24.0",
  "channel": "stable",
  "installation_path": "/opt/flutter"
}
```

#### 7. `list_flutter_releases`
Lists available Flutter SDK releases from a specific channel.

**Access Required:** Admin, Team A

**Parameters:**
- `channel` (required): Release channel - "stable", "beta", or "dev"
- `limit` (optional, default: 10): Maximum number of releases to return

**Example:**
```json
{
  "channel": "stable",
  "limit": 5
}
```

## Jinja2 Template Syntax Guidelines

When creating prompts, use **Jinja2** syntax for template variables (not Handlebars/Mustache):

### ✅ Correct Jinja2 Syntax

**Variables:**
```
{{ variable_name }}
```

**Conditionals:**
```
{% if condition %}
  Content when true
{% endif %}
```

**Equality checks:**
```
{% if var == "value" %}
  Content
{% endif %}
```

**Nested conditions:**
```
{% if outer %}
  {% if inner %}
    Content
  {% endif %}
{% endif %}
```

**Comments:**
```
{# This is a comment #}
```

### ❌ Incorrect Handlebars Syntax (Will Cause Errors)

```
{{#if condition}} ... {{/if}}
{{#eq var "value"}} ... {{/eq}}
{{#unless condition}} ... {{/unless}}
```

The `create_prompt` tool validates Jinja2 syntax and will warn about common mistakes.

## Running the Server

### Using FastMCP (Recommended)
```bash
fastmcp run run_server.py --transport http --port 8000
```

### Using Uvicorn
```bash
uvicorn server.server:app --host 0.0.0.0 --port 8000
```

### Health Check
```bash
curl http://localhost:8000/health
```

## File Structure

```
mcp-prompt-library/
├── prompts/                     # Directory containing prompt .md files
│   ├── create_api.md
│   ├── code_review.md
│   ├── code_correctness_review.md
│   ├── security_vulnerability_analysis.md
│   ├── performance_bottleneck_analysis.md
│   ├── code_refactoring.md
│   ├── code_simplification_deduplication.md
│   ├── bug_analysis_and_resolution.md
│   ├── error_handling_and_logging.md
│   ├── generate_test_scenarios.md
│   └── generate_project_documentation.md
├── server/                      # MCP server implementation
│   ├── server.py                # Main server with authentication
│   ├── prompt_registry.py       # Prompt function registration
│   ├── tool_registry.py         # Tool registration
│   ├── resource_registry.py     # Resource registration
│   ├── auth_utils.py            # Access control configuration
│   ├── config.py                # Path configuration
│   └── tools/                   # Tool implementations
│       ├── prompt_management.py
│       ├── environment_setup.py
│       ├── flutter_setup.py
│       ├── validation_utils.py
│       └── system_utils.py
├── resources/                   # Resource files
│   └── setup_work_environment/
│       ├── copilot-instructions.md
│       └── copilot-commit-message-instructions.md
├── docs/                        # Documentation
├── run_server.py                # Server startup script
└── README.md
```

## Access Control

All tools implement role-based access control through AWS Cognito user groups:
- **Admin**: Full access to all tools
- **Team Members**: Configured access based on team assignment
- **Local Testing Mode**: Bypass authentication for development

See [Access Control Guide](ACCESS_CONTROL.md) for details on:
- Configuring team permissions
- Adding new teams
- Local testing mode setup
- Production deployment with Cognito

## Additional Resources

- [README.md](../README.md) - Project overview and quick start
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Practical usage examples
- [ACCESS_CONTROL.md](ACCESS_CONTROL.md) - Authentication and authorization
- [PROMPT_DISCOVERY.md](PROMPT_DISCOVERY.md) - Smart prompt discovery features
- [RESOURCES_DOCUMENTATION.md](RESOURCES_DOCUMENTATION.md) - MCP resources (guidelines)
- [WORK_ENVIRONMENT_SETUP.md](WORK_ENVIRONMENT_SETUP.md) - Environment setup details

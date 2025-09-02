# MCP Prompt Management Tools

This MCP server provides tools for managing prompt files with frontmatter metadata. Each tool allows you to perform CRUD operations on prompt files stored in the `prompts/` directory.

## Available Tools

### 1. `create_prompt`
Creates a new MCP prompt file with frontmatter metadata.

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

### 2. `update_prompt`
Updates an existing MCP prompt file.

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

### 3. `delete_prompt`
Deletes an MCP prompt file.

**Parameters:**
- `name` (required): The name/identifier of the prompt to delete

**Example:**
```json
{
  "name": "generate_function"
}
```

### 4. `list_prompts`
Lists all available MCP prompts.

**Parameters:**
- `include_content` (optional, default: false): Whether to include the full content of each prompt

**Example:**
```json
{
  "include_content": true
}
```

### 5. `setup_work_environment`
Sets up a work environment by copying GitHub Copilot instruction files to a target directory and optionally configuring VS Code settings and .gitignore.

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
- `update_vscode_settings` (optional, default: true): Whether to update VS Code user settings
- `update_gitignore` (optional, default: true): Whether to update .gitignore file
- `gitignore_entries` (optional): List of entries to add to .gitignore. If not specified, uses default common entries

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

## Running the Server

To start the MCP server:

```bash
cd server
python server.py
```

The server will register all tools and be available for MCP clients to use.

## File Structure

```
mcp-prompt-library/
├── prompts/                     # Directory containing prompt .md files
│   ├── create_api.md           # API creation prompt
│   ├── code_review.md          # Code review prompt  
│   └── code_correctness_review.md # Code correctness and functional review prompt
│   └── ...           # Your custom prompts
├── server/           # MCP server code
│   ├── server.py     # Main server entry point
│   ├── prompt_handlers.py  # Prompt functions and registration
│   ├── tools.py      # MCP tools implementation (CRUD operations)
│   └── pyproject.toml
└── README.md
```

## Code Organization

- **`tools.py`**: Contains all MCP tool implementations for prompt management (create, update, delete, list)
- **`prompt_handlers.py`**: Contains prompt template functions and registers both prompts and tools
- **`server.py`**: Main entry point that starts the MCP server

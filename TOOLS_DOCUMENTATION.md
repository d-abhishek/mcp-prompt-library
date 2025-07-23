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
├── prompts/           # Directory containing prompt .md files
│   ├── create_api.md  # Example prompt file
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

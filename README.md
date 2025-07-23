# MCP Prompt Library

A Model Context Protocol (MCP) server for managing and using reusable prompts with Jinja2 templating support.

## Features

- 🛠️ **CRUD Operations**: Create, read, update, and delete prompt files through MCP tools
- 📝 **Frontmatter Support**: Prompts with YAML metadata for better organization
- 🔄 **Template Variables**: Jinja2 template support for dynamic prompts
- 📋 **Argument Validation**: Define required and optional arguments for prompts
- 🔍 **Easy Discovery**: List and search through available prompts

## Quick Start

1. **Install Dependencies**
   ```bash
   cd server
   uv install
   ```

2. **Run the MCP Server**
   ```bash
   python server.py
   ```

3. **Use the Tools**
   The server provides 4 main tools:
   - `create_prompt`: Create new prompt files
   - `update_prompt`: Update existing prompts
   - `delete_prompt`: Delete prompt files
   - `list_prompts`: List all available prompts

## Example Usage

### Creating a New Prompt
```json
{
  "name": "generate_test",
  "description": "Generate unit tests for functions",
  "content": "Create unit tests for **{{function_name}}** in **{{language}}**:\n- Test edge cases\n- Include error handling\n- Add assertions",
  "arguments": [
    {"name": "function_name", "description": "Function to test", "required": true},
    {"name": "language", "description": "Programming language", "required": true}
  ]
}
```

### Using a Prompt Template
Once created, prompts become available as MCP prompt functions that can be called with the defined arguments.

## Documentation

- [Tools Documentation](TOOLS_DOCUMENTATION.md) - Detailed guide for all MCP tools
- [Server Documentation](server/README.md) - Server setup and configuration

## File Structure

```
mcp-prompt-library/
├── prompts/                 # Prompt files directory
│   └── create_api.md       # Example prompt
├── server/                 # MCP server
│   ├── server.py          # Main server entry point
│   ├── prompt_handlers.py # Prompt functions and registration
│   ├── tools.py           # MCP tools for prompt management
│   └── pyproject.toml     # Dependencies
└── README.md
```

## Contributing

1. Fork the repository
2. Create prompts using the `create_prompt` tool
3. Test your prompts with the MCP client
4. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.
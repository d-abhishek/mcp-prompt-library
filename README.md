# MCP Prompt Library

A Model Conte   **Basic Tools:**
   - `create_prompt`: Create new prompt files
   - `update_prompt`: Update existing prompts
   - `delete_prompt`: Delete prompt files
   - `list_prompts`: List all prompts OR search with smart ranking
   
   **Smart Discovery Tools:**
   - `smart_prompt_executor`: Auto-execute prompts based on natural languageol (MCP) server for managing and using reusable prompts with Jinja2 templating support and smart auto-discovery.

## ✨ New Features

- 🧠 **Smart Prompt Discovery**: Automatically suggests the right prompt based on natural language queries
- 🚀 **Auto-Execution**: Automatically executes prompts with extracted parameters from user queries
- 🏷️ **Enhanced Metadata**: Keywords and triggers for better prompt matching
- � **Intelligent Suggestions**: Context-aware prompt recommendations

## Features

- �🛠️ **CRUD Operations**: Create, read, update, and delete prompt files through MCP tools
- 📝 **Frontmatter Support**: Prompts with YAML metadata for better organization
- 🔄 **Template Variables**: Jinja2 template support for dynamic prompts
- 📋 **Argument Validation**: Define required and optional arguments for prompts
- 🔍 **Easy Discovery**: List and search through available prompts
- 🎯 **Smart Matching**: Automatically find the right prompt for your task
- ⚡ **Auto-Execution**: Run prompts directly from natural language descriptions

## Quick Start

1. **Install Dependencies**
   ```bash
   cd server
   uv install
   ```

2. **Configure Environment**
   ```bash
   # Copy the example configuration
   cp .env.example .env
   
   # For local testing (authentication disabled):
   # Edit .env and set LOCAL_TESTING=true
   
   # For production (Cognito authentication enabled):
   # Edit .env and set LOCAL_TESTING=false
   # Then configure AWS Cognito credentials
   ```

3. **Run the MCP Server**
   ```bash
   python server.py
   ```

4. **Use the Tools**
   The server provides these main tools:
   
   **Basic Tools:**
   - `create_prompt`: Create new prompt files
   - `update_prompt`: Update existing prompts
   - `delete_prompt`: Delete prompt files
   - `list_prompts`: List all available prompts
   
   **Smart Discovery Tools:**
   - `suggest_prompt`: Analyze queries and suggest the best prompt
   - `smart_prompt_executor`: Auto-execute prompts based on natural language

## 🚀 Smart Usage Examples

### Automatic Prompt Discovery
Instead of remembering prompt names, just describe what you want:

```
Query: list_prompts(query="create api for storing student information")
→ Returns ranked search results with create_api as the top match
```

```
Query: smart_prompt_executor("create api for student data", auto_execute=True)
→ Automatically executes the create_api prompt with extracted parameters
```

### Traditional Usage (Still Supported)

#### Creating a New Prompt
```json
{
  "name": "generate_test",
  "description": "Generate unit tests for functions",
  "content": "Create unit tests for **{{function_name}}** in **{{language}}**:\n- Test edge cases\n- Include error handling\n- Add assertions",
  "arguments": [
    {"name": "function_name", "description": "Function to test", "required": true},
    {"name": "language", "description": "Programming language", "required": true}
  ],
  "keywords": ["test", "unit", "testing", "qa"],
  "triggers": ["create tests", "generate tests", "unit tests for"]
}
```

### Using a Prompt Template
Once created, prompts become available as MCP prompt functions that can be called with the defined arguments.

## 📚 Documentation

- **[Access Control Guide](docs/ACCESS_CONTROL.md)** - Complete guide to authentication, authorization, and team management
- **[Prompt Discovery Guide](docs/PROMPT_DISCOVERY.md)** - Smart prompt discovery and auto-execution
- [Tools Documentation](docs/TOOLS_DOCUMENTATION.md) - Detailed guide for all MCP tools
- [Usage Examples](docs/USAGE_EXAMPLES.md) - Example queries and use cases
- [Work Environment Setup](docs/WORK_ENVIRONMENT_SETUP.md) - Setup development environment
- [Server Documentation](server/README.md) - Server setup and configuration

## 🔐 Security & Access Control

The MCP Prompt Library uses AWS Cognito for authentication and implements configuration-driven role-based access control (RBAC):

- **Admin Users**: Full access including prompt management (create/update/delete)
- **Team Users**: Configurable access to specific tools
- **Easy Setup**: Add new teams by editing one configuration dictionary

### Local Testing Mode

For local development and testing, you can disable authentication:

1. Set `LOCAL_TESTING=true` in your `.env` file
2. Restart the server
3. All authentication and authorization checks will be bypassed
4. All tools and prompts will be accessible without Cognito login

**⚠️ Important**: Never use `LOCAL_TESTING=true` in production deployments!

See the [Access Control Guide](docs/ACCESS_CONTROL.md) for complete setup, configuration, and usage instructions.

## 💡 How Smart Discovery Solves Your Problem

**Before:**
```
User: "create api for storing student information"
System: "I don't know what you want. Try calling create_api with proper parameters."
```

**After:**
```
User: "create api for storing student information. The parameters should be name, class, contact, address"
System: 🚀 Auto-executed create_api prompt with detected parameters:
- API Purpose: student information management  
- Expected Parameters: name, class, contact, address
[Generated FastAPI code follows...]
```

## File Structure

```
mcp-prompt-library/
├── prompts/                     # Prompt files directory
│   ├── create_api.md           # Enhanced API creation prompt
│   ├── code_review.md          # Enhanced code review prompt
│   └── code_correctness_review.md # Code correctness and functional requirements review
├── server/                     # MCP server
│   ├── server.py              # Main server entry point
│   ├── prompt_handlers.py     # Prompt functions and registration
│   ├── prompt_tools.py        # MCP tools with smart discovery
│   └── pyproject.toml         # Dependencies
├── PROMPT_DISCOVERY.md        # Smart discovery documentation
└── README.md
```

## Contributing

1. Fork the repository
2. Create prompts using the `create_prompt` tool
3. Test your prompts with the MCP client
4. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.
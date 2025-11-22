# MCP Prompt Library

A Model Context Protocol (MCP) server providing reusable prompts, development tools, and coding guidelines with smart discovery and Jinja2 templating support.

## ✨ Features

### 🎯 Smart Prompt System
- **11 Production-Ready Prompts**: API creation, code review, security analysis, refactoring, and more
- **Smart Discovery**: Find prompts using natural language queries
- **Jinja2 Templates**: Dynamic prompts with variable substitution
- **YAML Frontmatter**: Metadata with keywords, triggers, and argument definitions

### 🛠️ Development Tools
- **Prompt Management**: Create, update, delete, and list prompts with validation
- **Environment Setup**: Configure workspace with Copilot instructions and Git standards
- **Flutter SDK Manager**: Install and manage Flutter SDK versions

### 📚 MCP Resources
- **Coding Guidelines**: Comprehensive code quality and development standards
- **Git Standards**: Commit message format and GitHub workflow best practices

### 🔐 Security & Access Control
- **AWS Cognito Authentication**: Enterprise-ready user management
- **Role-Based Access Control**: Configure tool and prompt access by team
- **Local Testing Mode**: Bypass authentication for development

## 🚀 Quick Start

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd mcp-prompt-library
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   # or with uv
   uv pip install -e .
   ```

3. **Configure Environment**
   ```bash
   # Copy example configuration
   cp .env.example .env
   
   # For local development (no authentication):
   # Edit .env and set: LOCAL_TESTING=true
   
   # For production (AWS Cognito required):
   # Edit .env and configure Cognito credentials
   ```

### Running the Server

**Option 1: FastMCP (Recommended)**
```bash
fastmcp run run_server.py --transport http --port 8000
```

**Option 2: Uvicorn**
```bash
uvicorn server.server:app --host 0.0.0.0 --port 8000
```

**Health Check**
```bash
curl http://localhost:8000/health
```

### MCP Client Configuration

Add to your MCP client settings (e.g., Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "prompt-library": {
      "command": "fastmcp",
      "args": ["run", "/path/to/mcp-prompt-library/run_server.py"]
    }
  }
}
```

For HTTP transport:
```json
{
  "mcpServers": {
    "prompt-library": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 📋 Available Prompts

The library includes 11 production-ready prompts:

| Prompt | Description | Use Cases |
|--------|-------------|-----------|
| `create_api` | FastAPI application generator with CRUD endpoints | REST APIs, backend services, data management |
| `code_review` | Comprehensive code quality analysis | Code reviews, refactoring preparation, quality audits |
| `code_correctness_review` | Functional correctness verification | Bug detection, requirement validation, logic errors |
| `security_vulnerability_analysis` | Security weakness detection (OWASP Top 10) | Security audits, penetration testing prep |
| `performance_bottleneck_analysis` | Performance optimization guidance | Slow code analysis, optimization planning |
| `code_refactoring` | Refactoring recommendations | Code modernization, technical debt reduction |
| `code_simplification_deduplication` | Complexity reduction strategies | Code cleanup, DRY principle application |
| `bug_analysis_and_resolution` | Root cause analysis and fixes | Debugging, error resolution |
| `error_handling_and_logging` | Robust error handling patterns | Production readiness, observability |
| `generate_test_scenarios` | Comprehensive test case generation | Test planning, QA preparation |
| `generate_project_documentation` | Automated documentation creation | README files, API docs, onboarding guides |

**Using Prompts:**
```python
# Call prompts through MCP client
result = mcp.call_prompt("create_api", {
    "api_purpose": "user management",
    "expected_parameters": "name, email, role, created_at"
})
```

## 🛠️ Available Tools

### Prompt Management Tools (Admin Only)
- **`create_prompt`**: Create new prompt templates with Jinja2 syntax validation
- **`update_prompt`**: Modify existing prompts (content, description, arguments)
- **`delete_prompt`**: Remove prompt files
- **`list_prompts`**: List all prompts or search with smart ranking

### Environment Setup Tools
- **`setup_coding_guidelines`**: Configure workspace with Copilot instructions
  - Copies coding guidelines to `.github/copilot-instructions.md`
  - Copies Git standards to `.github/copilot-commit-message-instructions.md`
  - Updates VS Code settings for commit message generation
  - Configures `.gitignore` entries

### Flutter Development Tools
- **`install_flutter_sdk`**: Download and install specific Flutter SDK versions
- **`list_flutter_releases`**: Browse available Flutter stable/beta/dev releases

## 📚 MCP Resources

Access read-only guidelines and standards:

- **`resource://guidelines/coding-guidelines`** - Code quality and development standards
  - Code readability and consistency
  - Documentation standards
  - Security & compliance (OWASP, GDPR, HIPAA)
  - Performance & error handling
  - Testing & code review guidelines

- **`resource://guidelines/commit-messages`** - Git and GitHub workflow standards
  - Conventional commit format
  - Branch naming conventions
  - Pull request standards
  - Pre-merge requirements

## 💡 Usage Examples

### Smart Prompt Discovery

Find prompts using natural language:
```bash
# Search for API creation
list_prompts(query="create api for student management")
# Returns: create_api (score: 0.95)

# Search for security analysis
list_prompts(query="check code for vulnerabilities")
# Returns: security_vulnerability_analysis (score: 0.89)
```

### Creating a Custom Prompt

```json
{
  "Name": "generate_dockerfile",
  "Description": "Generate optimized Dockerfiles for applications",
  "Content": "Create a production-ready Dockerfile for {{language}} application:\n\n{% if framework %}Using framework: {{framework}}{% endif %}\n\nRequirements:\n- Multi-stage build\n- Minimal image size\n- Security best practices",
  "Arguments": [
    {"name": "language", "description": "Programming language", "required": true},
    {"name": "framework", "description": "Framework name", "required": false}
  ]
}
```

### Setting Up a Development Environment

```python
# Configure workspace with Copilot instructions
setup_coding_guidelines(
    target_directory="/path/to/project",
    update_vscode_settings=True,
    update_gitignore=True,
    gitignore_entries=[".github/", "*.env"]
)
```

### Using Resources in Context

```python
# Load coding guidelines for code generation
guidelines = get_resource("resource://guidelines/coding-guidelines")

# Use with create_api prompt
create_api(
    api_purpose="user authentication",
    custom_api_reference=guidelines.content
)
```

## 🔐 Authentication & Access Control

### Local Testing Mode (Development)

Disable authentication for local development:

```bash
# .env file
LOCAL_TESTING=true
```

⚠️ **Warning**: Never use `LOCAL_TESTING=true` in production!

### Production Mode (AWS Cognito)

Configure Cognito authentication:

```bash
# .env file
LOCAL_TESTING=false
USER_POOL_ID=your-user-pool-id
AWS_REGION=us-east-1
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
BASE_URL=https://your-domain.com
```

### Role-Based Access Control

Configure access in `server/auth_utils.py`:

```python
TEAM_TOOL_ACCESS = {
    "team-a": ["create_prompt", "update_prompt", "list_prompts"],
    "team-b": ["list_prompts", "setup_coding_guidelines"],
}

TEAM_PROMPT_ACCESS = {
    "team-a": ["create_api", "code_review"],
    "team-b": ["code_review", "generate_test_scenarios"],
}
```

**Access Levels:**
- **Admin**: Full access to all tools and prompts
- **Team Members**: Configured access based on team assignment
- **Unauthenticated**: Blocked in production mode

See [Access Control Documentation](docs/ACCESS_CONTROL.md) for details.

## 📚 Documentation

Comprehensive guides for all features:

- **[Access Control Guide](docs/ACCESS_CONTROL.md)** - Authentication, authorization, and team management
- **[Prompt Discovery Guide](docs/PROMPT_DISCOVERY.md)** - Smart prompt matching and search
- **[Tools Documentation](docs/TOOLS_DOCUMENTATION.md)** - Detailed tool reference
- **[Resources Documentation](docs/RESOURCES_DOCUMENTATION.md)** - Guidelines and standards access
- **[Usage Examples](docs/USAGE_EXAMPLES.md)** - Practical examples and use cases
- **[Work Environment Setup](docs/WORK_ENVIRONMENT_SETUP.md)** - Development environment configuration

## 🏗️ Project Structure

```
mcp-prompt-library/
├── prompts/                           # Prompt template files
│   ├── create_api.md                 # FastAPI generator
│   ├── code_review.md                # Code quality analysis
│   ├── security_vulnerability_analysis.md
│   └── ... (11 prompts total)
├── server/                           # MCP server implementation
│   ├── server.py                     # Main server with auth config
│   ├── prompt_registry.py            # Prompt function registration
│   ├── tool_registry.py              # Tool registration
│   ├── resource_registry.py          # Resource registration
│   ├── auth_utils.py                 # Authentication & authorization
│   ├── config.py                     # Path configuration
│   └── tools/                        # Tool implementations
│       ├── prompt_management.py      # Prompt CRUD operations
│       ├── environment_setup.py      # Workspace configuration
│       ├── flutter_setup.py          # Flutter SDK manager
│       ├── validation_utils.py       # Jinja2 and syntax validation
│       └── system_utils.py           # File system utilities
├── resources/                        # Resource files
│   └── setup_work_environment/
│       ├── copilot-instructions.md
│       └── copilot-commit-message-instructions.md
├── docs/                             # Documentation
├── infrastructure/                   # AWS CDK deployment (optional)
├── run_server.py                     # Server startup script
├── pyproject.toml                    # Dependencies
└── README.md
```

## 🚢 Deployment

### Local Development
```bash
# Run with FastMCP
fastmcp run run_server.py --transport http --port 8000

# Or with Uvicorn
uvicorn server.server:app --reload --port 8000
```

### Production Deployment

**Option 1: AWS with CDK (Included)**

The repository includes AWS CDK infrastructure for deployment to:
- AWS Lambda with Function URL
- API Gateway
- Cognito User Pool integration

```bash
cd infrastructure
pip install -r requirements.txt
cdk deploy
```

**Option 2: Docker**

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["fastmcp", "run", "run_server.py", "--transport", "http", "--port", "8000"]
```

**Option 3: Traditional Server**

Deploy to any cloud provider supporting Python:
- AWS EC2 / Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- DigitalOcean App Platform

## 🤝 Contributing

Contributions are welcome! Here's how:

### Adding New Prompts

1. Create a new `.md` file in `prompts/` directory
2. Include YAML frontmatter with metadata:
   ```yaml
   ---
   name: your_prompt_name
   description: Clear description
   keywords: [relevant, search, terms]
   triggers: ["phrases that", "should match"]
   arguments:
     - name: param_name
       description: What it does
       required: true
   ---
   ```
3. Write prompt content using Jinja2 syntax: `{{variable_name}}`
4. Test with `list_prompts(query="your test query")`

### Improving Tools

1. Tools are in `server/tools/` directory
2. Extend `BaseTool` class
3. Add validation and error handling
4. Register in `tool_registry.py`
5. Update documentation

### Development Setup

```bash
# Clone and install
git clone <repo-url>
cd mcp-prompt-library
pip install -e ".[dev]"

# Enable local testing
echo "LOCAL_TESTING=true" > .env

# Run tests
pytest

# Run server
fastmcp run run_server.py
```

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 🆘 Support & Resources

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io)
- **FastMCP**: [FastMCP Framework](https://github.com/jlowin/fastmcp)

---

**Built with [FastMCP](https://github.com/jlowin/fastmcp)** - A Python framework for Model Context Protocol servers
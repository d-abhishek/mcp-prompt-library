# Usage Examples for MCP Prompt Library

Practical examples demonstrating how to use prompts, tools, and resources in the MCP Prompt Library.

## Table of Contents

1. [Prompt Usage Examples](#prompt-usage-examples)
2. [Tool Usage Examples](#tool-usage-examples)
3. [Resource Usage Examples](#resource-usage-examples)
4. [Smart Discovery Examples](#smart-discovery-examples)
5. [Advanced Integration Examples](#advanced-integration-examples)
6. [MCP Client Integration](#mcp-client-integration-examples)
7. [Common Use Cases](#common-use-cases)
8. [Best Practices](#best-practices)

---

## Prompt Usage Examples

### Using the create_api Prompt

Generate a complete FastAPI application:

```python
# Call the create_api prompt
result = mcp.call_prompt("create_api", {
    "api_purpose": "student information management",
    "expected_parameters": "name, class, contact, address, enrollment_date",
    "include_tests": "yes"
})
```

**Output**: Complete FastAPI application with:
- Pydantic models
- CRUD endpoints
- Database abstraction
- Validation
- Test cases

### Using the code_review Prompt

Comprehensive code quality analysis:

```python
result = mcp.call_prompt("code_review", {
    "code_reference": """
    def process_user_data(data):
        user = data['user']
        return user.upper()
    """,
    "language": "python",
    "specific_concerns": "error handling, input validation"
})
```

**Output**: Detailed review covering:
- Code quality issues
- Security concerns
- Best practices violations
- Suggested improvements

### Using the security_vulnerability_analysis Prompt

Identify security weaknesses:

```python
result = mcp.call_prompt("security_vulnerability_analysis", {
    "code_reference": "app.py",
    "programming_language": "python",
    "security_context": "web application with user authentication"
})
```

**Output**: OWASP Top 10 analysis with:
- Identified vulnerabilities
- Risk severity ratings
- Remediation steps
- Secure code examples

---

## Tool Usage Examples

### Prompt Management Tools

#### Creating a New Prompt

```python
# Create a custom prompt for generating Dockerfiles
result = mcp.call_tool("create_prompt", {
    "Name": "generate_dockerfile",
    "Description": "Generate optimized Dockerfiles for various applications",
    "Content": """Create a production-ready Dockerfile for {{language}} application:

{% if framework %}
Using framework: {{framework}}
{% endif %}

Requirements:
- Multi-stage build for smaller image size
- Security best practices (non-root user, minimal base image)
- Efficient layer caching
- Health checks

{% if additional_requirements %}
Additional requirements:
{{additional_requirements}}
{% endif %}

Generate the complete Dockerfile with comments explaining each section.""",
    "Arguments": [
        {
            "name": "language",
            "description": "Programming language (e.g., python, node, go, java)",
            "required": True
        },
        {
            "name": "framework",
            "description": "Framework name if applicable (e.g., fastapi, express, spring)",
            "required": False
        },
        {
            "name": "additional_requirements",
            "description": "Any additional requirements or constraints",
            "required": False
        }
    ]
})
```

**Output**: `✅ Prompt 'generate_dockerfile' created successfully`

#### Updating an Existing Prompt

```python
# Update the dockerfile prompt to add more features
result = mcp.call_tool("update_prompt", {
    "Name": "generate_dockerfile",
    "Description": "Generate optimized, multi-stage Dockerfiles with security scanning",
    "Content": """[Updated content with additional features]"""
})
```

#### Listing and Searching Prompts

```python
# List all available prompts
all_prompts = mcp.call_tool("list_prompts", {})

# Search for specific prompts
api_prompts = mcp.call_tool("list_prompts", {
    "query": "create api backend service"
})
# Returns ranked results with relevance scores

# Search for security-related prompts
security_prompts = mcp.call_tool("list_prompts", {
    "query": "security vulnerabilities"
})
```

#### Deleting a Prompt

```python
# Remove a prompt (admin only)
result = mcp.call_tool("delete_prompt", {
    "Name": "generate_dockerfile"
})
```

### Environment Setup Tools

#### Setting Up a Development Workspace

```python
# Configure a new project with Copilot instructions
result = mcp.call_tool("setup_work_environment", {
    "target_directory": "/home/user/projects/my-new-app",
    "update_vscode_settings": True,
    "update_gitignore": True,
    "gitignore_entries": [".github/", "*.env", ".env.local", "secrets/"]
})
```

**What this does:**
1. Creates `.github/` directory in target
2. Copies `copilot-instructions.md` (coding guidelines)
3. Copies `copilot-commit-message-instructions.md` (Git standards)
4. Updates VS Code user settings for commit message generation
5. Adds entries to `.gitignore`

**Output**:
```
✅ Work Environment Setup Complete

📁 Created Directory: /home/user/projects/my-new-app/.github

📄 Files Copied:
  ✓ copilot-instructions.md
  ✓ copilot-commit-message-instructions.md

⚙️ VS Code Settings Updated:
  ✓ GitHub Copilot commit message authoring enabled

📝 .gitignore Updated:
  ✓ Added .github/
  ✓ Added *.env
  ✓ Added .env.local
  ✓ Added secrets/
```

### Flutter Development Tools

#### Installing Flutter SDK

```python
# Install a specific Flutter version
result = mcp.call_tool("install_flutter_sdk", {
    "version": "3.24.0",
    "channel": "stable",
    "installation_path": "/opt/flutter"
})
```

#### Listing Available Flutter Releases

```python
# Get all stable releases
stable_releases = mcp.call_tool("list_flutter_releases", {
    "channel": "stable",
    "limit": 10
})

# Get beta releases
beta_releases = mcp.call_tool("list_flutter_releases", {
    "channel": "beta"
})
```

---

## Resource Usage Examples

### Accessing Coding Guidelines

```python
# Get comprehensive code quality standards
guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")

# Use in code generation context
prompt = f"""
Generate a Python class for user management.

Follow these coding standards:
{guidelines.content}
"""
```

**Resource includes:**
- Code readability and consistency rules
- Documentation standards
- Security & compliance requirements (OWASP, GDPR, HIPAA)
- Performance guidelines
- Error handling patterns
- Testing standards
- Language-specific guidelines

### Accessing Git Standards

```python
# Get commit message and GitHub workflow standards
git_standards = mcp.get_resource("resource://guidelines/commit-messages")

# Use for commit message generation
commit_message = f"""
Create a commit message for these changes:
- Added user authentication
- Implemented JWT tokens
- Added login/logout endpoints

Follow these standards:
{git_standards.content}
"""
```

**Resource includes:**
- Conventional commit format
- Branch naming conventions
- Pull request standards
- Pre-merge requirements
- Development workflow best practices

### Using Resources in Code Review

```python
# Combine resources with code review prompt
coding_guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")

review_result = mcp.call_prompt("code_review", {
    "code_reference": "path/to/code.py",
    "language": "python",
    "company_guidelines": coding_guidelines.content
})
```

---

## Smart Discovery Examples

### Finding the Right Prompt

```python
# Natural language search
results = mcp.call_tool("list_prompts", {
    "query": "I need to create a REST API for managing products"
})

# Returns:
# 1. create_api (score: 0.92)
# 2. generate_project_documentation (score: 0.45)
```

**How it works:**
- Matches keywords: "create", "api", "managing"
- Checks triggers: "create api", "build api"
- Analyzes description similarity
- Returns ranked results with scores

### Query Patterns for Best Results

**API Development:**
```python
list_prompts(query="create api for user management")
list_prompts(query="build rest backend for products")
list_prompts(query="generate fastapi application")
```

**Code Quality:**
```python
list_prompts(query="review python code for best practices")
list_prompts(query="check security vulnerabilities")
list_prompts(query="find performance bottlenecks")
```

**Testing:**
```python
list_prompts(query="generate test cases")
list_prompts(query="create unit tests for authentication")
```

**Documentation:**
```python
list_prompts(query="write readme for project")
list_prompts(query="generate api documentation")
```

---

## Advanced Integration Examples

### Complete Workflow: Creating a New API

```python
# Step 1: Search for the right prompt
search_results = mcp.call_tool("list_prompts", {
    "query": "create rest api for blog posts"
})

# Step 2: Get coding guidelines
guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")

# Step 3: Generate the API
api_code = mcp.call_prompt("create_api", {
    "api_purpose": "blog post management (CRUD operations)",
    "expected_parameters": "title, content, author, tags, published_date, status",
    "custom_api_reference": guidelines.content,
    "include_tests": "yes"
})

# Step 4: Review the generated code
review = mcp.call_prompt("code_review", {
    "code_reference": api_code,
    "language": "python",
    "company_guidelines": guidelines.content
})

# Step 5: Run security analysis
security_check = mcp.call_prompt("security_vulnerability_analysis", {
    "code_reference": api_code,
    "programming_language": "python",
    "security_context": "public-facing REST API with database"
})
```

### Automating Code Quality Checks

```python
# Automated review pipeline
def review_code_complete(code_path, language):
    guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")
    
    # 1. General code review
    general_review = mcp.call_prompt("code_review", {
        "code_reference": code_path,
        "language": language,
        "company_guidelines": guidelines.content
    })
    
    # 2. Correctness check
    correctness = mcp.call_prompt("code_correctness_review", {
        "code_reference": code_path,
        "language": language
    })
    
    # 3. Security analysis
    security = mcp.call_prompt("security_vulnerability_analysis", {
        "code_reference": code_path,
        "programming_language": language
    })
    
    # 4. Performance analysis
    performance = mcp.call_prompt("performance_bottleneck_analysis", {
        "code_reference": code_path,
        "language": language
    })
    
    return {
        "general_review": general_review,
        "correctness": correctness,
        "security": security,
        "performance": performance
    }
```

### Setting Up Multiple Projects

```python
# Batch setup for team projects
projects = [
    "/home/user/projects/api-service",
    "/home/user/projects/web-frontend",
    "/home/user/projects/data-pipeline"
]

for project_path in projects:
    result = mcp.call_tool("setup_work_environment", {
        "target_directory": project_path,
        "update_vscode_settings": True,
        "update_gitignore": True,
        "gitignore_entries": [".github/", "*.env", "secrets/", ".vscode/"]
    })
    print(f"✅ Configured: {project_path}")
```

---

## MCP Client Integration Examples

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent:

```json
{
  "mcpServers": {
    "prompt-library": {
      "command": "fastmcp",
      "args": ["run", "/path/to/mcp-prompt-library/run_server.py"],
      "env": {
        "LOCAL_TESTING": "true"
      }
    }
  }
}
```

### VS Code MCP Extension Configuration

```json
{
  "mcp.servers": [
    {
      "name": "prompt-library",
      "command": "fastmcp",
      "args": ["run", "/path/to/mcp-prompt-library/run_server.py"],
      "transport": "stdio"
    }
  ]
}
```

### HTTP Transport Example

Start server:
```bash
fastmcp run run_server.py --transport http --port 8000
```

Client configuration:
```json
{
  "mcpServers": {
    "prompt-library": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

---

## Common Use Cases

### Use Case 1: New Project Setup

**Scenario:** Starting a new Python FastAPI project with best practices

```python
# 1. Setup workspace
setup_work_environment(
    target_directory="/projects/new-api",
    update_vscode_settings=True,
    update_gitignore=True
)

# 2. Generate API skeleton
api_code = create_api(
    api_purpose="product catalog management",
    expected_parameters="name, description, price, category, stock",
    include_tests="yes"
)

# 3. Review generated code
review = code_review(
    code_reference=api_code,
    language="python"
)

# 4. Generate documentation
docs = generate_project_documentation(
    project_name="Product Catalog API",
    project_type="FastAPI REST API"
)
```

### Use Case 2: Code Quality Audit

**Scenario:** Comprehensive review of existing codebase

```python
# Load standards
guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")

# Run multiple analyses
results = {
    "quality": code_review(
        code_reference="src/",
        language="python",
        company_guidelines=guidelines.content
    ),
    "security": security_vulnerability_analysis(
        code_reference="src/",
        programming_language="python"
    ),
    "performance": performance_bottleneck_analysis(
        code_reference="src/",
        language="python"
    ),
    "correctness": code_correctness_review(
        code_reference="src/",
        language="python"
    )
}
```

### Use Case 3: Refactoring Legacy Code

**Scenario:** Modernizing old codebase

```python
# 1. Analyze current issues
bugs = bug_analysis_and_resolution(
    code_reference="legacy/user_module.py",
    programming_language="python"
)

# 2. Get refactoring suggestions
refactoring = code_refactoring(
    code_snippet="legacy/user_module.py",
    language="python"
)

# 3. Simplify complex sections
simplification = code_simplification_deduplication(
    code_snippet="legacy/user_module.py",
    language="python"
)

# 4. Improve error handling
error_handling = error_handling_and_logging(
    code_reference="legacy/user_module.py",
    programming_language="python"
)
```

### Use Case 4: Team Onboarding

**Scenario:** Setting up new developer's environment

```python
# 1. Provide guidelines
coding_guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")
git_standards = mcp.get_resource("resource://guidelines/commit-messages")

# 2. Setup their projects
team_projects = [
    "/home/newdev/api-service",
    "/home/newdev/frontend-app",
    "/home/newdev/shared-library"
]

for project in team_projects:
    setup_work_environment(
        target_directory=project,
        update_vscode_settings=True,
        update_gitignore=True
    )

# 3. Generate onboarding documentation
docs = generate_project_documentation(
    project_name="Team Development Standards",
    custom_sections=f"{coding_guidelines.content}\n\n{git_standards.content}"
)
```

---

## Tips for Effective Usage

### 1. Search Strategy

**Be Specific:**
```python
# ❌ Too vague
list_prompts(query="code")

# ✅ Specific and descriptive
list_prompts(query="create rest api with database operations")
```

**Use Domain Terms:**
```python
# Include relevant keywords
list_prompts(query="security analysis OWASP vulnerabilities")
list_prompts(query="performance optimization bottlenecks")
```

### 2. Prompt Customization

**Leverage Optional Parameters:**
```python
# Basic call
create_api(api_purpose="user management")

# Enhanced with optional parameters
create_api(
    api_purpose="user management with roles",
    expected_parameters="name, email, password, role, permissions",
    custom_api_reference=guidelines.content,
    include_tests="yes"
)
```

### 3. Resource Integration

**Always Use Guidelines:**
```python
# Load guidelines once
coding_guidelines = mcp.get_resource("resource://guidelines/coding-guidelines")
git_standards = mcp.get_resource("resource://guidelines/commit-messages")

# Reuse in multiple calls
review1 = code_review(..., company_guidelines=coding_guidelines.content)
review2 = code_review(..., company_guidelines=coding_guidelines.content)
```

### 4. Error Handling

**Check Tool Access:**
```python
try:
    result = mcp.call_tool("create_prompt", {...})
except PermissionError as e:
    print(f"Access denied: {e}")
    # Request admin access or use alternative approach
```

### 5. Batch Operations

**Process Multiple Files:**
```python
code_files = ["module1.py", "module2.py", "module3.py"]

for file_path in code_files:
    review = mcp.call_prompt("code_review", {
        "code_reference": file_path,
        "language": "python"
    })
    # Save or process review
```

---

## Troubleshooting

### Issue: Prompt Not Found

```python
# Check if prompt exists
all_prompts = list_prompts()
print(all_prompts)

# Search for similar prompts
similar = list_prompts(query="api creation")
```

### Issue: Permission Denied

```python
# Check your access level
# Admin users: Full access
# Team members: Check TEAM_TOOL_ACCESS configuration
# Solution: Contact admin or use local testing mode
```

### Issue: Template Syntax Error

```python
# Validate Jinja2 syntax before creating
content = "{{variable_name}}"  # ✅ Correct
content = "{{#variable_name}}"  # ❌ Wrong (Handlebars syntax)

# The create_prompt tool validates automatically
```

### Issue: Resource Not Loading

```python
# Verify resource URI
# ✅ Correct
get_resource("resource://guidelines/coding-guidelines")
get_resource("resource://guidelines/commit-messages")

# ❌ Wrong (old scheme)
get_resource("copilot://guidelines/code-quality")
```

---

## Best Practices

1. **Always use resources for consistency** - Load guidelines once, reuse everywhere
2. **Search before creating** - Check if a similar prompt already exists
3. **Be descriptive** - Use clear, specific prompts and parameters
4. **Validate syntax** - Test Jinja2 templates before deployment
5. **Document custom prompts** - Add clear descriptions and examples
6. **Use version control** - Track changes to prompt templates
7. **Test thoroughly** - Verify prompts work with various inputs
8. **Follow naming conventions** - Use snake_case for prompt names
9. **Leverage permissions** - Configure team access appropriately
10. **Monitor usage** - Review logs to understand prompt effectiveness

---

## Additional Resources

- [Prompt Discovery Guide](PROMPT_DISCOVERY.md) - Advanced search techniques
- [Tools Documentation](TOOLS_DOCUMENTATION.md) - Complete tool reference
- [Resources Documentation](RESOURCES_DOCUMENTATION.md) - Guidelines details
- [Access Control Guide](ACCESS_CONTROL.md) - Authentication setup
- [Work Environment Setup](WORK_ENVIRONMENT_SETUP.md) - Development configuration
- [MCP Documentation](https://modelcontextprotocol.io) - Official MCP docs
- [FastMCP Framework](https://github.com/jlowin/fastmcp) - Server framework docs

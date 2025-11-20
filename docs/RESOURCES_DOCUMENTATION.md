# MCP Resources Documentation

## Overview

MCP Resources provide read-only access to static content like guidelines, documentation, and configuration files. Unlike tools (which perform actions) and prompts (which generate dynamic content), resources serve as a knowledge base that can be referenced by MCP clients.

## Available Resources

### 1. `resource://guidelines/commit-messages`

**Description**: Git & GitHub Standards - Commit Message Format and Best Practices

**Content Includes**:
- Conventional commit format (`<type>(<scope>): <subject>`)
- Valid commit types (feat, fix, docs, style, refactor, perf, test, chore)
- Scope and subject rules
- Submessages with hyphens for clarity
- Branch naming conventions
- Pull request standards
- Pre-merge requirements
- Development workflow best practices
- Automation & tooling integration recommendations

**Use When**:
- Creating commit messages
- Setting up branch naming
- Preparing pull requests
- Configuring pre-commit hooks
- Establishing team workflows

**Example Usage**:
```python
# Access the resource through your MCP client
resource = client.get_resource("resource://guidelines/commit-messages")
print(resource.content)
```

---

### 2. `resource://guidelines/coding-guidelines`

**Description**: Company Guidelines for GitHub Copilot - Code Quality & Development Standards

**Content Includes**:
- Code readability and consistency rules
- Documentation standards (docstrings, comments)
- Architecture & design principles (SOLID, DRY, separation of concerns)
- Security & compliance requirements (OWASP, GDPR, HIPAA)
- Performance & efficiency guidelines
- Error handling & robustness patterns
- Testing & quality assurance standards
- Code review focus areas with severity levels
- Language-specific guidelines (Python, JavaScript/TypeScript, Java, Go, C#)

**Use When**:
- Writing new code
- Performing code reviews
- Refactoring existing code
- Setting up project standards
- Training team members
- Creating development guidelines

**Example Usage**:
```python
# Access the resource through your MCP client
resource = client.get_resource("resource://guidelines/coding-guidelines")
print(resource.content)
```

---

## Resource URI Scheme

All resources use the custom URI scheme: `resource://guidelines/<resource-name>`

**Available Paths**:
- `/commit-messages` - Git & GitHub workflow standards
- `/coding-guidelines` - Code quality and development standards

---

## Integration with VS Code

When using the MCP server with VS Code, these resources can be:

1. **Referenced in prompts**: Include guideline content in your prompts
2. **Used for validation**: Check code against standards
3. **Integrated with Copilot**: Provide context for code generation
4. **Embedded in documentation**: Reference in your project docs

**Example MCP Client Configuration**:
```json
{
  "mcpServers": {
    "prompt-library": {
      "command": "fastmcp",
      "args": ["run", "path/to/run_server.py"]
    }
  }
}
```

---

## Technical Implementation

Resources are implemented in `server/resource_registry.py` using the `@mcp.resource()` decorator:

```python
@mcp.resource("resource://guidelines/commit-messages")
def get_commit_message_guidelines() -> str:
    """Git & GitHub Standards documentation"""
    file_path = SOURCE_GITHUB_DIR / "copilot-commit-message-instructions.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**Key Features**:
- Read-only access
- Files loaded from `resources/setup_work_environment/` directory
- Error handling with meaningful messages
- UTF-8 encoding support

---

## Error Handling

All resources include comprehensive error handling:

- **File Not Found**: Returns `❌ Error: <filename> file not found`
- **Read Errors**: Returns `❌ Error reading <resource>: <error details>`
- **Encoding Issues**: Handled with UTF-8 encoding specification

---

## Best Practices

1. **Reference Before Creating**: Check guidelines before writing code
2. **Use Specific Resources**: Request only the resource you need based on your task
3. **Cache Locally**: If using frequently, cache the content in your application
4. **Keep Updated**: Resources reflect the latest files in the repository
5. **Combine with Prompts**: Use resources as context for prompt execution
6. **Access via MCP Clients**: Use Claude Desktop, VS Code, or other MCP-compatible clients

---

## Future Enhancements

Potential additions to the resource registry:

- API documentation resources
- Architecture diagrams and patterns
- Testing strategy guidelines
- Deployment procedures
- Security policies
- Performance benchmarks
- Team-specific resources with access control

---

## Related Documentation

- [Tools Documentation](TOOLS_DOCUMENTATION.md) - MCP tools for CRUD operations
- [Prompt Discovery](PROMPT_DISCOVERY.md) - Smart prompt suggestions
- [Usage Examples](USAGE_EXAMPLES.md) - Practical examples
- [Access Control](ACCESS_CONTROL.md) - Permission system

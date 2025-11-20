# Access Control Guide

## Overview

The MCP Prompt Library uses AWS Cognito for authentication and implements **configuration-driven** role-based access control (RBAC) through Cognito user groups. All permissions are defined in configuration dictionaries, making it easy to add teams and manage permissions without code changes.

Access control is enforced for both **tools** and **prompts** with separate permission configurations.

## Quick Reference

### User Groups

| Group | Description | Access Level |
|-------|-------------|--------------|
| `admin` | Administrators | Full access to all tools and prompts |
| `team-a` | Team A members | Most tools and prompts |
| `team-b` | Team B members | Limited tools and prompts |

### Tool Access Matrix

| Tool | Admin | Team A | Team B |
|------|-------|--------|--------|
| `create_prompt` | ✅ | ❌ | ❌ |
| `update_prompt` | ✅ | ❌ | ❌ |
| `delete_prompt` | ✅ | ❌ | ❌ |
| `list_prompts` | ✅ | ✅ | ✅ |
| `setup_work_environment` | ✅ | ✅ | ✅ |
| `setup_flutter_developer_environment` | ✅ | ✅ | ❌ |

### Prompt Access Matrix

| Prompt | Admin | Team A | Team B |
|--------|-------|--------|--------|
| `create_api` | ✅ | ✅ | ❌ |
| `code_review` | ✅ | ✅ | ✅ |
| `code_correctness_review` | ✅ | ✅ | ✅ |
| `performance_bottleneck_analysis` | ✅ | ✅ | ❌ |
| `security_vulnerability_analysis` | ✅ | ✅ | ❌ |
| `code_simplification_deduplication` | ✅ | ✅ | ❌ |
| `error_handling_and_logging` | ✅ | ✅ | ❌ |
| `bug_analysis_and_resolution` | ✅ | ✅ | ✅ |
| `code_refactoring` | ✅ | ✅ | ❌ |
| `generate_project_documentation` | ✅ | ✅ | ❌ |
| `generate_test_scenarios` | ✅ | ✅ | ❌ |

## Configuration

### Location

All permissions are configured in: **`server/auth_utils.py`**
- **`TOOL_PERMISSIONS`** dictionary - Controls tool access
- **`PROMPT_PERMISSIONS`** dictionary - Controls prompt access

### Current Configuration

#### Tool Permissions

```python
TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        # Admins can access ALL tools
        "create_prompt",
        "update_prompt",
        "delete_prompt",
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
    ],
    "team-a": [
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
    ],
    "team-b": [
        "list_prompts",
        "setup_work_environment",
    ],
}
```

#### Prompt Permissions

```python
PROMPT_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        # Admins can access ALL prompts
        "create_api",
        "code_review",
        "code_correctness_review",
        "performance_bottleneck_analysis",
        "security_vulnerability_analysis",
        "code_simplification_deduplication",
        "error_handling_and_logging",
        "bug_analysis_and_resolution",
        "code_refactoring",
        "generate_project_documentation",
        "generate_test_scenarios",
    ],
    "team-a": [
        "create_api",
        "code_review",
        "code_correctness_review",
        "performance_bottleneck_analysis",
        "security_vulnerability_analysis",
        "code_simplification_deduplication",
        "error_handling_and_logging",
        "bug_analysis_and_resolution",
        "code_refactoring",
        "generate_project_documentation",
        "generate_test_scenarios",
    ],
    "team-b": [
        "code_review",
        "code_correctness_review",
        "bug_analysis_and_resolution",
    ],
}
```

## Adding a New Team

### Step 1: Create Group in AWS Cognito

1. Go to **AWS Cognito Console**
2. Select your User Pool
3. Navigate to **Users and groups** → **Groups**
4. Click **Create group**
5. Enter group name (e.g., `team-c`)
6. Save

### Step 2: Add to Configuration

Edit `server/auth_utils.py` and add the new team to both `TOOL_PERMISSIONS` and `PROMPT_PERMISSIONS`:

#### Tool Permissions

```python
TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [...],
    "team-a": [...],
    "team-b": [...],
    "team-c": [  # <-- NEW TEAM
        "list_prompts",
        "setup_work_environment",
        # Add any tools this team should access
    ],
}
```

#### Prompt Permissions

```python
PROMPT_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [...],
    "team-a": [...],
    "team-b": [...],
    "team-c": [  # <-- NEW TEAM
        "code_review",
        "bug_analysis_and_resolution",
        # Add any prompts this team should access
    ],
}
```

### Step 3: Restart the Server

```bash
# Restart to pick up configuration changes
systemctl restart mcp-prompt-library
# OR for manual/dev environments
# Stop and restart your server process
```

### Step 4: Assign Users to Group

1. Go to **AWS Cognito Console** → **Users**
2. Select a user
3. Click **Add user to group**
4. Select the new group (e.g., `team-c`)

**Done!** No code changes needed.

## Adding a New Tool

### Step 1: Register the Tool

In `server/tool_registry.py`, add your new tool:

```python
@mcp.tool()
def my_new_tool(param1: str) -> str:
    """My new tool description."""
    try:
        require_tool_access("my_new_tool")
    except InsufficientPermissionsError as e:
        return f"❌ {str(e)}"
    
    # Tool implementation
    return "Success!"
```

### Step 2: Add to Permissions Configuration

Edit `server/auth_utils.py`:

```python
TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        "create_prompt",
        "update_prompt",
        "delete_prompt",
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
        "my_new_tool",  # <-- ADD HERE
    ],
    "team-a": [
        "list_prompts",
        "setup_work_environment",
        "setup_flutter_developer_environment",
        "my_new_tool",  # <-- ADD TO TEAMS THAT NEED IT
    ],
}
```

### Step 3: Restart Server

```bash
systemctl restart mcp-prompt-library
```

## Adding a New Prompt

### Step 1: Register the Prompt

In `server/prompt_registry.py`, add your new prompt:

```python
@mcp.prompt()
def my_new_prompt(param1: str, param2: Optional[str] = None) -> str:
    """My new prompt description.
    
    🔒 **PERMISSION REQUIRED**: admin, team-a
    ⚠️  Team B users will receive "Access Denied"
    """
    # Check prompt access permissions
    try:
        require_prompt_access("my_new_prompt")
    except InsufficientPermissionsError as e:
        return f"❌ {str(e)}"
    
    template = load_template("my_new_prompt")
    return template.render(param1=param1, param2=param2)
```

### Step 2: Add to Permissions Configuration

Edit `server/auth_utils.py`:

```python
PROMPT_PERMISSIONS: Dict[str, List[str]] = {
    "admin": [
        "create_api",
        "code_review",
        # ... other prompts
        "my_new_prompt",  # <-- ADD HERE
    ],
    "team-a": [
        "create_api",
        "code_review",
        # ... other prompts
        "my_new_prompt",  # <-- ADD TO TEAMS THAT NEED IT
    ],
}
```

### Step 3: Restart Server

```bash
systemctl restart mcp-prompt-library
```

## Setup Guide for New Users

### Prerequisites

- AWS Cognito User Pool configured
- User account created in Cognito
- User assigned to at least one group

### AWS Cognito Configuration

#### 1. Create User Pool (if not exists)

```bash
# Using AWS CLI
aws cognito-idp create-user-pool \
  --pool-name mcp-prompt-library \
  --auto-verified-attributes email
```

#### 2. Create User Groups

```bash
# Create admin group
aws cognito-idp create-group \
  --user-pool-id <pool-id> \
  --group-name admin \
  --description "Administrators with full access"

# Create team-a group
aws cognito-idp create-group \
  --user-pool-id <pool-id> \
  --group-name team-a \
  --description "Team A members"

# Create team-b group
aws cognito-idp create-group \
  --user-pool-id <pool-id> \
  --group-name team-b \
  --description "Team B members"
```

#### 3. Create Users

```bash
# Via AWS Console or CLI
aws cognito-idp admin-create-user \
  --user-pool-id <pool-id> \
  --username john.doe \
  --user-attributes Name=email,Value=john.doe@example.com
```

#### 4. Add Users to Groups

```bash
aws cognito-idp admin-add-user-to-group \
  --user-pool-id <pool-id> \
  --username john.doe \
  --group-name team-a
```

### Server Configuration

Ensure your server is configured with Cognito credentials in `server/server.py`:

```python
cognito_provider = CognitoAuthProvider(
    user_pool_id="your-user-pool-id",
    client_id="your-client-id",
    region="your-region"
)

mcp = FastMCP(
    "MCP Prompt Library",
    auth_provider=cognito_provider
)
```

## Architecture

### Components

```
server/
├── auth_utils.py              # Authentication & authorization
│   ├── TOOL_PERMISSIONS       # Tool access configuration
│   ├── PROMPT_PERMISSIONS     # Prompt access configuration
│   ├── get_user_groups()      # Extract user groups from token
│   ├── require_tool_access()  # Enforce tool permissions
│   ├── require_prompt_access() # Enforce prompt permissions
│   └── InsufficientPermissionsError # Custom exception
├── tool_registry.py           # Tool registration with access controls
├── prompt_registry.py         # Prompt registration with access controls
└── server.py                  # FastMCP server with Cognito provider
```

### Flow Diagram

```
User Request → Cognito Auth → Extract Groups → Check Permissions → Execute Tool/Prompt
                    ↓              ↓                  ↓                    ↓
                JWT Token    cognito:groups    TOOL/PROMPT_PERMISSIONS   Success/Error
```

### How It Works

1. **Authentication**: AWS Cognito validates user credentials
2. **Token Generation**: Cognito issues JWT with `cognito:groups` claim
3. **Group Extraction**: `get_user_groups()` reads groups from token
4. **Permission Check**: `require_tool_access()` or `require_prompt_access()` validates against configurations
5. **Execution**: If authorized, tool/prompt executes; otherwise, returns error

### Key Functions

```python
# Get user's groups from token
def get_user_groups() -> List[str]:
    """Returns list of Cognito groups user belongs to."""
    
# Get allowed tools for groups
def get_allowed_tools_for_groups(groups: List[str]) -> Set[str]:
    """Returns set of tools user can access."""

# Get allowed prompts for groups
def get_allowed_prompts_for_groups(groups: List[str]) -> Set[str]:
    """Returns set of prompts user can access."""
    
# Enforce tool access
def require_tool_access(tool_name: str) -> None:
    """Raises InsufficientPermissionsError if user lacks access."""

# Enforce prompt access
def require_prompt_access(prompt_name: str) -> None:
    """Raises InsufficientPermissionsError if user lacks access."""
```

## Testing Access Control

### Test Script

Use the interactive test script:

```bash
python tests/test_access_control.py
```

Options:
- Test admin user access to tools and prompts
- Test team user access to tools and prompts
- Verify specific permissions
- Get user info

### Manual Testing

#### Testing Tool Access

```python
# Test getting user groups
from server.auth_utils import get_user_groups
print(get_user_groups())  # ['admin']

# Test checking tool access
from server.auth_utils import require_tool_access
try:
    require_tool_access("create_prompt")
    print("✅ Access granted")
except InsufficientPermissionsError as e:
    print(f"❌ {e}")
```

#### Testing Prompt Access

```python
# Test checking prompt access
from server.auth_utils import require_prompt_access
try:
    require_prompt_access("create_api")
    print("✅ Access granted")
except InsufficientPermissionsError as e:
    print(f"❌ {e}")
```

### MCP Client Testing

#### Testing Tools

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_prompt",
    "arguments": {
      "name": "test",
      "description": "Test prompt",
      "content": "Test content"
    }
  }
}
```

**Expected Results:**
- **Admin user**: Creates prompt successfully
- **Team user**: Returns permission error

#### Testing Prompts

```json
{
  "method": "prompts/get",
  "params": {
    "name": "create_api",
    "arguments": {
      "api_purpose": "Test API",
      "framework": "FastAPI"
    }
  }
}
```

**Expected Results:**
- **Admin/Team-A user**: Returns prompt content
- **Team-B user**: Returns permission error

## Error Messages

### Common Errors

#### Insufficient Permissions for Tools

```
❌ You do not have permission to use the 'create_prompt' tool. 
Required group membership: admin. 
Your current groups: team-a
```

**Solution**: Add user to required group or grant group access to tool

#### Insufficient Permissions for Prompts

```
❌ You do not have permission to use the 'create_api' prompt. 
Required group membership: admin, team-a. 
Your current groups: team-b
```

**Solution**: Add user to required group or grant group access to prompt

#### No Groups Assigned

```
❌ You do not have permission to use the 'list_prompts' tool. 
Required group membership: admin, team-a, team-b. 
Your current groups: none
```

**Solution**: Assign user to at least one group in Cognito

#### Missing Group in Configuration for Tools

User is in group `team-c` but it's not in `TOOL_PERMISSIONS`:

```
❌ You do not have permission to use the 'list_prompts' tool. 
Required group membership: admin, team-a, team-b. 
Your current groups: team-c
```

**Solution**: Add `team-c` to `TOOL_PERMISSIONS` in `server/auth_utils.py`

#### Missing Group in Configuration for Prompts

User is in group `team-c` but it's not in `PROMPT_PERMISSIONS`:

```
❌ You do not have permission to use the 'code_review' prompt. 
Required group membership: admin, team-a, team-b. 
Your current groups: team-c
```

**Solution**: Add `team-c` to `PROMPT_PERMISSIONS` in `server/auth_utils.py`

## Security Best Practices

### Do's ✅

- **Always** use `require_tool_access()` and `require_prompt_access()` for protected operations
- **Keep** sensitive operations admin-only
- **Review** permissions regularly
- **Use** principle of least privilege
- **Log** access denials for auditing
- **Test** access controls after changes
- **Document** permission requirements in docstrings

### Don'ts ❌

- **Don't** hardcode permissions in tool/prompt code
- **Don't** skip authorization checks
- **Don't** store credentials in code
- **Don't** give excessive permissions
- **Don't** ignore permission errors
- **Don't** bypass access controls for "convenience"

## Troubleshooting

### Users Can't Access Any Tools or Prompts

**Check:**
1. User exists in Cognito User Pool
2. User is assigned to at least one group
3. Group name matches exactly (case-sensitive)
4. Server has been restarted after config changes

### New Team Not Working

**Check:**
1. Group created in AWS Cognito
2. Group added to both `TOOL_PERMISSIONS` and `PROMPT_PERMISSIONS` in `auth_utils.py`
3. Server restarted
4. Users assigned to the group
5. No typos in group name (case-sensitive)

### Tool or Prompt Shows Permission Error for Admin

**Check:**
1. User is actually in `admin` group (not just username "admin")
2. `admin` group includes the tool/prompt in `TOOL_PERMISSIONS`/`PROMPT_PERMISSIONS`
3. Tool/prompt uses `require_tool_access()`/`require_prompt_access()` correctly
4. Server has latest configuration

### Debug Mode

Enable verbose logging to troubleshoot:

```python
# In server/auth_utils.py - for tools
def require_tool_access(tool_name: str) -> None:
    user_groups = get_user_groups()
    allowed_tools = get_allowed_tools_for_groups(user_groups)
    
    # DEBUG: Print current state
    print(f"User groups: {user_groups}")
    print(f"Allowed tools: {allowed_tools}")
    print(f"Requested tool: {tool_name}")
    
    if tool_name not in allowed_tools:
        # ... error handling

# In server/auth_utils.py - for prompts
def require_prompt_access(prompt_name: str) -> None:
    user_groups = get_user_groups()
    allowed_prompts = get_allowed_prompts_for_groups(user_groups)
    
    # DEBUG: Print current state
    print(f"User groups: {user_groups}")
    print(f"Allowed prompts: {allowed_prompts}")
    print(f"Requested prompt: {prompt_name}")
    
    if prompt_name not in allowed_prompts:
        # ... error handling
```

## Migration Guide

### From Admin-Only to Team-Based

If you previously had admin-only checks:

**Before (Tools):**
```python
@mcp.tool()
def create_prompt(...):
    require_admin()
    # ...
```

**After (Tools):**
```python
@mcp.tool()
def create_prompt(...):
    require_tool_access("create_prompt")
    # Configuration handles which groups can access
```

**Before (Prompts):**
```python
@mcp.prompt()
def create_api(...):
    require_admin()
    # ...
```

**After (Prompts):**
```python
@mcp.prompt()
def create_api(...):
    require_prompt_access("create_api")
    # Configuration handles which groups can access
```

**Update Configuration:**
```python
# Tools
TOOL_PERMISSIONS = {
    "admin": ["create_prompt", ...],
    # Other teams as needed
}

# Prompts
PROMPT_PERMISSIONS = {
    "admin": ["create_api", ...],
    # Other teams as needed
}
```

## FAQ

### Can a user belong to multiple groups?

**Yes!** Users get combined permissions from all their groups. If a user is in both `team-a` and `team-b`, they can access tools from both groups.

### How do I make a tool available to everyone?

Add it to all groups in `TOOL_PERMISSIONS`, or create a `public` group and assign all users to it.

### Can I have group hierarchies?

Not directly in this implementation. However, you can manually include lower-level permissions in higher-level groups (e.g., `admin` includes all `team-a` tools).

### Do I need to restart after adding users to groups?

**No**, only server configuration changes require restart. User-to-group assignments in Cognito take effect immediately.

### How do I audit who accessed what?

Implement logging in `require_tool_access()` to track access attempts, approvals, and denials.

### Can I use this with non-Cognito authentication?

The architecture supports it, but you'd need to modify `get_user_groups()` to extract groups from your auth system's tokens.

## Related Documentation

- [Tools Documentation](TOOLS_DOCUMENTATION.md) - Available tools and usage
- [Usage Examples](USAGE_EXAMPLES.md) - Prompt discovery examples
- [Work Environment Setup](WORK_ENVIRONMENT_SETUP.md) - Development environment tools

## Support

For issues or questions:
1. Check error messages for specific guidance
2. Review this documentation
3. Test with the included test scripts
4. Check AWS Cognito console for user/group configuration
5. Verify server logs for detailed error information

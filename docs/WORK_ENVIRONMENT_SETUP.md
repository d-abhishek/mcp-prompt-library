# Work Environment Setup Tool

## Overview

The `setup_work_environment` MCP tool configures development environments with coding guidelines and Git standards, including automatic VS Code integration.

## Features

### 📁 File Management
- Creates `.github/` folder in target directory
- Copies `copilot-instructions.md` (comprehensive coding guidelines)
- Copies `copilot-commit-message-instructions.md` (Git workflow standards)

### ⚙️ VS Code Integration
- Automatically updates VS Code user `settings.json`
- Configures GitHub Copilot commit message generation
- Preserves all existing settings
- Cross-platform support (Windows, macOS, Linux)

### 📝 .gitignore Management
- Optionally updates `.gitignore` with development entries
- Prevents committing sensitive or generated files
- Customizable entry list

## Tool Parameters

```python
setup_work_environment(
    target_directory: str,          # Required: Root directory for .github folder
    update_vscode_settings: bool,   # Optional: Update VS Code settings (default: True)
    update_gitignore: bool,         # Optional: Update .gitignore (default: True)
    gitignore_entries: List[str]    # Optional: Custom .gitignore entries
)
```

### Parameter Details

**`target_directory`** (required)
- Absolute path to project root
- `.github/` folder will be created here
- Example: `/home/user/projects/my-app`

**`update_vscode_settings`** (optional, default: `True`)
- `True`: Updates VS Code settings for commit message generation
- `False`: Skips VS Code configuration

**`update_gitignore`** (optional, default: `True`)
- `True`: Adds entries to `.gitignore`
- `False`: Skips .gitignore modification

**`gitignore_entries`** (optional)
- Custom list of patterns to add
- Default: `[".github/"]`
- Example: `[".github/", "*.env", ".vscode/", "secrets/"]`

## Usage Examples

### Full Setup with Defaults

```json
{
  "target_directory": "/home/user/projects/my-app"
}
```

**What happens:**
1. Creates `/home/user/projects/my-app/.github/`
2. Copies both guideline files
3. Updates VS Code settings
4. Adds `.github/` to `.gitignore`

### Custom .gitignore Entries

```json
{
  "target_directory": "/home/user/projects/my-app",
  "gitignore_entries": [
    ".github/",
    "*.env",
    ".env.local",
    "secrets/",
    ".vscode/",
    "*.log"
  ]
}
```

### Files Only (No VS Code or .gitignore)

```json
{
  "target_directory": "/home/user/projects/my-app",
  "update_vscode_settings": false,
  "update_gitignore": false
}
```

### Skip VS Code, Update .gitignore

```json
{
  "target_directory": "/home/user/projects/my-app",
  "update_vscode_settings": false,
  "update_gitignore": true,
  "gitignore_entries": [".github/", "temp/"]
}
```

## Output Example

```
✅ Work Environment Setup Complete

📁 Created Directory: /home/user/projects/my-app/.github

📄 Files Copied:
  ✓ copilot-instructions.md
  ✓ copilot-commit-message-instructions.md

⚙️ VS Code Settings Updated:
  ✓ GitHub Copilot commit message authoring enabled

📝 .gitignore Updated:
  ✓ Added .github/
  ✓ Added *.env
  ✓ Added secrets/

💡 Next Steps:
  1. Review and customize guidelines for your team
  2. Restart VS Code to apply new settings
  3. Commit and share .github/ folder with team (optional)
```

## What Gets Configured

### Coding Guidelines (`copilot-instructions.md`)

Comprehensive standards covering:
- Code readability and consistency
- Documentation requirements
- Architecture principles (SOLID, DRY)
- Security & compliance (OWASP, GDPR, HIPAA)
- Performance optimization
- Error handling patterns
- Testing standards
- Code review criteria
- Language-specific guidelines

### Git Standards (`copilot-commit-message-instructions.md`)

Git workflow best practices:
- Conventional commit format: `<type>(<scope>): <subject>`
- Valid commit types (feat, fix, docs, etc.)
- Branch naming conventions
- Pull request requirements
- Pre-merge checklist
- Development workflow

### VS Code Configuration

Adds this setting to `settings.json`:
```json
{
  "github.copilot.chat.commitMessageGeneration.instructions": [
    {
      "file": ".github/copilot-commit-message-instructions.md"
    }
  ]
}
```

**VS Code Settings Paths:**
- Windows: `%APPDATA%\Code\User\settings.json`
- macOS: `~/Library/Application Support/Code/User/settings.json`
- Linux: `~/.config/Code/User/settings.json`

**Safety Features:**
- Preserves all existing settings
- Prevents duplicate entries
- Creates backups for corrupted files
- Maintains JSON formatting
- Graceful error handling

## Use Cases

### 1. New Project Setup

Configure a fresh project with best practices:
```python
setup_work_environment(
    target_directory="/path/to/new-project"
)
```

### 2. Team Onboarding

Set up multiple projects for new team members:
```python
projects = [
    "/home/newdev/project-a",
    "/home/newdev/project-b",
    "/home/newdev/project-c"
]

for project in projects:
    setup_work_environment(target_directory=project)
```

### 3. Standardize Existing Projects

Apply guidelines to existing codebases:
```python
setup_work_environment(
    target_directory="/path/to/legacy-project",
    gitignore_entries=[".github/", "*.log", "temp/", ".env"]
)
```

### 4. CI/CD Integration

Automate environment setup in build pipelines:
```bash
# In your CI/CD script
python -c "
import mcp_client
client.call_tool('setup_work_environment', {
    'target_directory': os.getcwd(),
    'update_vscode_settings': False
})
"
```

## Benefits

### For Individual Developers
- ✅ Consistent coding standards across projects
- ✅ Automated commit message generation
- ✅ No manual configuration needed
- ✅ Best practices out of the box

### For Teams
- ✅ Standardized development environment
- ✅ Uniform code quality across team
- ✅ Simplified onboarding process
- ✅ Automated compliance enforcement

### For Organizations
- ✅ Scalable standards deployment
- ✅ Reduced configuration errors
- ✅ Enterprise-ready guidelines
- ✅ Audit trail for compliance

## Technical Details

### File Operations
1. Validates target directory exists (creates if needed)
2. Creates `.github/` subdirectory
3. Copies files from `resources/setup_work_environment/`
4. Sets appropriate file permissions

### VS Code Integration
1. Detects OS-specific VS Code settings path
2. Reads existing `settings.json` (creates if missing)
3. Parses JSON safely with error recovery
4. Merges new settings without duplicates
5. Writes formatted JSON (4-space indent)
6. Creates backup on corruption

### .gitignore Updates
1. Reads existing `.gitignore` (creates if missing)
2. Checks for duplicate entries
3. Appends new entries with comments
4. Preserves existing content and formatting

## Troubleshooting

### Issue: VS Code Settings Not Updated

**Possible Causes:**
- VS Code not installed
- Non-standard settings location
- File permission issues

**Solution:**
- Check VS Code installation
- Verify settings path exists
- Run with appropriate permissions
- Or use `update_vscode_settings=False`

### Issue: Files Not Copied

**Possible Causes:**
- Target directory doesn't exist
- Permission denied
- Source files missing

**Solution:**
- Verify target directory path
- Check file permissions
- Ensure source files exist in `resources/`

### Issue: .gitignore Not Updated

**Possible Causes:**
- .gitignore is read-only
- Directory doesn't exist

**Solution:**
- Check file permissions
- Create directory first
- Use custom `gitignore_entries`

## Related Documentation

- [TOOLS_DOCUMENTATION.md](TOOLS_DOCUMENTATION.md) - Complete tool reference
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Practical examples
- [README.md](../README.md) - Project overview
- [ACCESS_CONTROL.md](ACCESS_CONTROL.md) - Permission configuration

"""
Environment setup tool for MCP.

This module provides tools for setting up work environments, including
copying GitHub Copilot instruction files and configuring VS Code settings.
"""

import pathlib
import shutil
from typing import List, Optional

from .base_tool import BaseTool
from .system_utils import SystemUtils
from ..config import SOURCE_GITHUB_DIR


class EnvironmentSetupTool(BaseTool):
    """Tool for setting up development environments."""
    
    def __init__(self):
        """Initialize the environment setup tool."""
        super().__init__()
        self.source_github_dir = SOURCE_GITHUB_DIR
    
    def setup_work_environment(
        self,
        target_directory: str,
        update_vscode_settings: bool = True,
        update_gitignore: bool = True,
        gitignore_entries: Optional[List[str]] = None
    ) -> str:
        """Setup work environment by copying GitHub Copilot instruction files to target directory.
        
        EXACTLY what this tool does:
        1. Creates .github folder in target directory
        2. Copies copilot-instructions.md (code quality guidelines)
        3. Copies copilot-commit-message-instructions.md (Git standards)
        4. Optionally updates VS Code user settings for commit message generation
        5. Optionally updates .gitignore to exclude .github/ folder and other entries
        
        Args:
            target_directory: The root directory where .github folder should be created
            update_vscode_settings: Whether to update VS Code settings (default: True)
            update_gitignore: Whether to update .gitignore file (default: True)
            gitignore_entries: Custom entries to add to .gitignore (default: [".github/"])
            
        Returns:
            str: Formatted setup report
        """
        try:
            # Validate and resolve target directory
            target_path = pathlib.Path(target_directory).resolve()
            
            if not target_path.exists():
                return f"Error: Target directory '{target_directory}' does not exist."
            
            if not target_path.is_dir():
                return f"Error: '{target_directory}' is not a directory."
            
            # Create .github directory in target location
            github_target_dir = target_path / ".github"
            github_target_dir.mkdir(exist_ok=True)
            
            # Define source files to copy
            files_to_copy = [
                "copilot-instructions.md",
                "copilot-commit-message-instructions.md"
            ]
            
            copied_files = []
            errors = []
            
            for filename in files_to_copy:
                source_file = self.source_github_dir / filename
                target_file = github_target_dir / filename
                
                if not source_file.exists():
                    errors.append(f"Source file '{filename}' not found in {self.source_github_dir}")
                    continue
                
                try:
                    # Copy the file
                    shutil.copy2(source_file, target_file)
                    copied_files.append(filename)
                except Exception as e:
                    errors.append(f"Failed to copy '{filename}': {str(e)}")
            
            # Update .gitignore if requested
            gitignore_success = False
            gitignore_message = ""
            if update_gitignore:
                try:
                    gitignore_path = target_path / ".gitignore"
                    
                    # Default entries if none specified
                    if gitignore_entries is None:
                        gitignore_entries = [".github/"]
                    
                    # Read existing content if file exists
                    existing_content = ""
                    if gitignore_path.exists():
                        with open(gitignore_path, 'r', encoding='utf-8') as f:
                            existing_content = f.read()
                    
                    # Check which entries need to be added
                    new_entries = []
                    for entry in gitignore_entries:
                        entry = entry.strip()
                        if entry and entry not in existing_content:
                            new_entries.append(entry)
                    
                    if new_entries:
                        # Append new entries
                        with open(gitignore_path, 'a', encoding='utf-8') as f:
                            if existing_content and not existing_content.endswith('\n'):
                                f.write('\n')
                            for entry in new_entries:
                                f.write(f"{entry}\n")
                        
                        gitignore_success = True
                        gitignore_message = f"Added {len(new_entries)} entries to .gitignore: {', '.join(new_entries)}"
                    else:
                        gitignore_success = True
                        gitignore_message = "All specified entries already exist in .gitignore"
                        
                except Exception as e:
                    gitignore_success = False
                    gitignore_message = f"Failed to update .gitignore: {str(e)}"
            
            # Update VS Code settings if requested
            vscode_success = False
            vscode_message = ""
            if update_vscode_settings:
                vscode_success, vscode_message = SystemUtils.update_vscode_user_settings(target_directory)
            
            # Prepare result message
            result = f"🚀 **Work Environment Setup Complete**\n\n"
            result += f"**Target Directory**: {target_path}\n"
            result += f"**GitHub Directory**: {github_target_dir}\n\n"
            
            if copied_files:
                result += f"✅ **Successfully copied {len(copied_files)} file(s)**:\n"
                for filename in copied_files:
                    result += f"   - {filename}\n"
            
            if update_gitignore:
                if gitignore_success:
                    result += f"\n✅ **.gitignore**: {gitignore_message}\n"
                else:
                    result += f"\n⚠️ **.gitignore**: {gitignore_message}\n"
            
            if update_vscode_settings:
                if vscode_success:
                    result += f"\n✅ **VS Code Settings**: {vscode_message}\n"
                    result += f"   - Settings file: {SystemUtils.get_vscode_user_settings_path()}\n"
                else:
                    result += f"\n⚠️ **VS Code Settings**: {vscode_message}\n"
            
            if errors:
                result += f"\n⚠️ **Encountered {len(errors)} error(s)**:\n"
                for error in errors:
                    result += f"   - {error}\n"
            
            result += f"\n📋 **Files provide**:\n"
            result += f"   - **copilot-instructions.md**: Comprehensive code quality guidelines, standards, and best practices\n"
            result += f"   - **copilot-commit-message-instructions.md**: Git commit message format, branch naming, and PR standards\n"
            
            if update_vscode_settings and vscode_success:
                result += f"\n💻 **VS Code Integration**:\n"
                result += f"   - GitHub Copilot will now use your commit message guidelines\n"
                result += f"   - Commit message suggestions will follow your standards\n"
                result += f"   - Setting: github.copilot.chat.commitMessageGeneration.instructions\n"
            
            result += f"\n💡 **Next Steps**:\n"
            result += f"   1. Review and customize the guidelines for your team\n"
            result += f"   2. Restart VS Code to apply the new settings\n"
            result += f"   3. Set up pre-commit hooks for automated compliance\n"
            result += f"   4. Share with your development team\n"
            result += f"   5. Test GitHub Copilot commit message generation\n"
            
            return result
            
        except Exception as e:
            return f"Error setting up work environment: {str(e)}"

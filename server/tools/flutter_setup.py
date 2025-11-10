"""
Flutter development environment setup tool for MCP.

This module generates PowerShell commands for setting up Flutter development environments
on the LOCAL machine (not on the MCP server). It generates structured commands that
GitHub Copilot can execute locally via run_in_terminal.

The tool generates commands for:
- Installing Flutter SDK, Git, AWS CLI
- Cloning repositories
- Installing VS Code extensions
- Running flutter doctor
"""

import pathlib
import json
import urllib.request
import traceback
from typing import Optional, Dict

from .base_tool import BaseTool


class FlutterSetupTool(BaseTool):
    """Tool for setting up Flutter development environments."""
    
    def __init__(self):
        """Initialize the Flutter setup tool."""
        super().__init__()
    
    def get_latest_flutter_release(self, platform_name: str = "windows") -> Optional[Dict[str, str]]:
        """Get the latest stable Flutter release information from Google's API.
        
        Args:
            platform_name: Platform to get release for ("windows", "macos", "linux")
            
        Returns:
            Dict with 'version', 'archive', 'sha256' keys, or None if failed
        """
        try:
            releases_url = f"https://storage.googleapis.com/flutter_infra_release/releases/releases_{platform_name}.json"
            with urllib.request.urlopen(releases_url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            # Find the first stable release
            for release in data.get('releases', []):
                if release.get('channel') == 'stable':
                    return {
                        'version': release.get('version'),
                        'archive': release.get('archive'),
                        'sha256': release.get('sha256'),
                        'dart_version': release.get('dart_sdk_version')
                    }
            return None
        except Exception:
            return None
    
    def setup_flutter_developer_environment(
        self,
        target_directory: str,
        flutter_version: str = "latest",
        codecommit_repo_url: Optional[str] = "https://github.com/d-abhishek/Thesis-Test-Project",
        aws_profile: Optional[str] = None,
        install_git: bool = True,
        install_aws_cli: bool = True,
        install_flutter: bool = True,
        install_vscode_extensions: bool = True
    ) -> str:
        """Setup a complete Flutter development environment for a new developer.
        
        This tool generates PowerShell commands to be executed on the LOCAL machine by GitHub Copilot.
        It does NOT execute commands on the MCP server (EC2).
        
        This tool automates the onboarding process by generating commands for:
        1. Installing Flutter SDK (latest stable version)
        2. Installing AWS CLI
        3. Installing Git
        4. Cloning project from Git repository (GitHub, AWS CodeCommit, etc.)
        5. Installing VS Code Flutter/Dart extensions (if VS Code is detected)
        6. Running flutter doctor to verify setup
        
        Args:
            target_directory: Directory where the project should be cloned
            flutter_version: Flutter SDK version to install (default: "latest" for latest stable)
            codecommit_repo_url: Git repository URL to clone (default: "https://github.com/d-abhishek/Thesis-Test-Project")
            aws_profile: AWS CLI profile to use for CodeCommit access (only needed for AWS CodeCommit repos)
            install_git: Whether to install Git (default: True)
            install_aws_cli: Whether to install AWS CLI (default: True)
            install_flutter: Whether to install Flutter SDK (default: True)
            install_vscode_extensions: Whether to install VS Code extensions (default: True)
            
        Returns:
            str: JSON-formatted commands to be executed locally by GitHub Copilot
        """
        try:
            target_path = pathlib.Path(target_directory).resolve()
            
            # Generate commands structure
            commands = {
                "target_directory": str(target_path),
                "platform": "windows",  # Assume Windows for now, can be parameterized
                "steps": []
            }
            
            # ==================== GIT CHECK & INSTALLATION ====================
            if install_git:
                commands["steps"].append({
                    "name": "Check Git Installation",
                    "check_command": "git --version",
                    "install_command": "winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements",
                    "required": True,
                    "description": "Git is required for cloning repositories"
                })
            
            # ==================== AWS CLI CHECK & INSTALLATION ====================
            if install_aws_cli:
                commands["steps"].append({
                    "name": "Check AWS CLI Installation",
                    "check_command": "aws --version",
                    "install_command": "winget install --id Amazon.AWSCLI -e --source winget --accept-package-agreements --accept-source-agreements",
                    "required": False,
                    "description": "AWS CLI is needed for AWS CodeCommit repositories"
                })
            
            # ==================== FLUTTER CHECK & INSTALLATION ====================
            if install_flutter:
                flutter_install_dir = str(pathlib.Path.home() / "flutter")
                flutter_bin = str(pathlib.Path.home() / "flutter" / "bin")
                
                commands["steps"].append({
                    "name": "Check Flutter Installation",
                    "check_command": "flutter --version",
                    "install_commands": [
                        {
                            "description": "Clone Flutter SDK from GitHub (stable branch - much faster than zip download)",
                            "command": f"git clone https://github.com/flutter/flutter.git -b stable --depth 1 '{flutter_install_dir}'",
                            "skip_if_exists": flutter_install_dir
                        },
                        {
                            "description": "Add Flutter to PATH (User)",
                            "command": f"$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($currentPath -notlike '*{flutter_bin}*') {{ [Environment]::SetEnvironmentVariable('Path', $currentPath + ';{flutter_bin}', 'User') }}"
                        },
                        {
                            "description": "Add Flutter to current session PATH",
                            "command": f"if ($env:Path -notlike '*{flutter_bin}*') {{ $env:Path += ';{flutter_bin}' }}"
                        }
                    ],
                    "required": True,
                    "description": "Flutter SDK is required for Flutter development (installed via Git clone). Note: First run will download Dart SDK automatically.",
                    "flutter_install_dir": flutter_install_dir
                })
            
            # ==================== VS CODE EXTENSIONS ====================
            if install_vscode_extensions:
                commands["steps"].append({
                    "name": "Install VS Code Extensions",
                    "check_command": "code --version",
                    "install_commands": [
                        {
                            "description": "Install Dart extension",
                            "command": "code --install-extension Dart-Code.dart-code --force"
                        },
                        {
                            "description": "Install Flutter extension",
                            "command": "code --install-extension Dart-Code.flutter --force"
                        }
                    ],
                    "required": False,
                    "description": "VS Code extensions for Flutter development"
                })
            
            # ==================== CLONE REPOSITORY ====================
            if codecommit_repo_url:
                repo_name = codecommit_repo_url.rstrip('/').split('/')[-1]
                if repo_name.endswith('.git'):
                    repo_name = repo_name[:-4]
                
                clone_dir = str(target_path / repo_name)
                
                commands["steps"].append({
                    "name": "Clone Repository",
                    "check_command": f"Test-Path '{clone_dir}\\.git'",
                    "install_command": f"git clone {codecommit_repo_url} '{clone_dir}'",
                    "required": False,
                    "description": f"Clone project repository to {clone_dir}",
                    "repo_url": codecommit_repo_url,
                    "clone_directory": clone_dir
                })
            
            # ==================== FLUTTER DOCTOR ====================
            commands["steps"].append({
                "name": "Run Flutter Doctor",
                "check_command": "flutter --version",
                "install_command": "flutter doctor -v",
                "required": True,
                "description": "Verify Flutter installation and dependencies. NOTE: If this is the first time running Flutter, it will download Dart SDK and build tools (5-10 minutes). Please be patient - do not cancel!"
            })
            
            # ==================== POST-SETUP INSTRUCTIONS ====================
            commands["post_setup"] = {
                "git_config": [
                    "git config --global user.name 'Your Name'",
                    "git config --global user.email 'your.email@example.com'"
                ],
                "aws_config": ["aws configure"] if install_aws_cli else [],
                "flutter_licenses": ["flutter doctor --android-licenses"],
                "flutter_dependencies": [f"cd '{clone_dir}' && flutter pub get"] if codecommit_repo_url else []
            }
            
            # Return JSON for GitHub Copilot to parse and execute
            return json.dumps(commands, indent=2)
            
        except Exception as e:
            error_response = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            return json.dumps(error_response, indent=2)

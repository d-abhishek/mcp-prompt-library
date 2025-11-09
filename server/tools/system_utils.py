"""
System utilities for MCP tools.

This module provides static utility methods for system operations like
running commands, checking installed software, downloading files, etc.
"""

import subprocess
import urllib.request
import zipfile
import tarfile
import pathlib
import os
import platform
import json
import shutil
from typing import Tuple, Optional, List


class SystemUtils:
    """Utility class for system operations."""
    
    @staticmethod
    def run_command(command: List[str], check: bool = True, timeout: Optional[int] = None) -> Tuple[bool, str, str]:
        """Run a shell command and return success status, stdout, and stderr.
        
        Args:
            command: List of command arguments
            check: Whether to raise exception on non-zero exit code
            timeout: Command timeout in seconds (None for no timeout)
            
        Returns:
            tuple: (success: bool, stdout: str, stderr: str)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check,
                timeout=timeout
            )
            return True, result.stdout, result.stderr
        except subprocess.TimeoutExpired as e:
            return False, e.stdout.decode() if e.stdout else "", f"Command timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)
    
    @staticmethod
    def check_command_exists(command: str) -> Tuple[bool, str]:
        """Check if a command exists in PATH.
        
        Args:
            command: Command name to check
            
        Returns:
            tuple: (exists: bool, version: str)
        """
        try:
            # Try running with --version
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True, result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            try:
                # Try with -v
                result = subprocess.run(
                    [command, "-v"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return True, result.stdout.strip()
            except:
                return False, ""
    
    @staticmethod
    def download_file(url: str, destination: pathlib.Path, description: str = "file") -> Tuple[bool, str]:
        """Download a file from URL to destination.
        
        Args:
            url: URL to download from
            destination: Path where file should be saved
            description: Description of what's being downloaded (for messages)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Download with progress (simplified for now)
            urllib.request.urlretrieve(url, destination)
            
            return True, f"Successfully downloaded {description}"
        except Exception as e:
            return False, f"Failed to download {description}: {str(e)}"
    
    @staticmethod
    def extract_archive(archive_path: pathlib.Path, extract_to: pathlib.Path) -> Tuple[bool, str]:
        """Extract a zip or tar archive.
        
        Args:
            archive_path: Path to the archive file
            extract_to: Directory to extract to
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            extract_to.mkdir(parents=True, exist_ok=True)
            
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix in ['.tar', '.gz', '.xz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                return False, f"Unsupported archive format: {archive_path.suffix}"
            
            return True, f"Successfully extracted to {extract_to}"
        except Exception as e:
            return False, f"Failed to extract archive: {str(e)}"
    
    @staticmethod
    def add_to_windows_path(path: pathlib.Path) -> Tuple[bool, str]:
        """Add a directory to Windows user PATH environment variable.
        
        Args:
            path: Path to add to PATH
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            import winreg
            import ctypes
            
            # Open user environment variables key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )
            
            try:
                # Get current PATH
                current_path, _ = winreg.QueryValueEx(key, 'Path')
            except FileNotFoundError:
                current_path = ''
            
            # Check if path already in PATH
            path_str = str(path)
            if path_str.lower() in current_path.lower():
                winreg.CloseKey(key)
                return True, f"{path} already in PATH"
            
            # Add to PATH
            new_path = f"{current_path};{path_str}" if current_path else path_str
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            
            # Broadcast WM_SETTINGCHANGE to notify system of environment change
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment',
                SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
            )
            
            return True, f"Added {path} to PATH. Please restart your terminal."
            
        except Exception as e:
            return False, f"Failed to add to PATH: {str(e)}"
    
    @staticmethod
    def get_vscode_user_settings_path() -> pathlib.Path:
        """Get the VS Code user settings.json path for the current operating system.
        
        Returns:
            pathlib.Path: Path to VS Code user settings.json
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows: %APPDATA%\Code\User\settings.json
            appdata = os.environ.get('APPDATA')
            if appdata:
                return pathlib.Path(appdata) / "Code" / "User" / "settings.json"
        elif system == "Darwin":  # macOS
            # macOS: ~/Library/Application Support/Code/User/settings.json
            home = pathlib.Path.home()
            return home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        elif system == "Linux":
            # Linux: ~/.config/Code/User/settings.json
            home = pathlib.Path.home()
            return home / ".config" / "Code" / "User" / "settings.json"
        
        # Fallback - try Windows path as default
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            return pathlib.Path(appdata) / "Code" / "User" / "settings.json"
        
        # Last resort fallback
        home = pathlib.Path.home()
        return home / ".vscode" / "settings.json"
    
    @staticmethod
    def update_vscode_user_settings(target_directory: str) -> tuple[bool, str]:
        """Update VS Code user settings.json to include commit message instructions.
        
        Safely preserves all existing settings while adding only the commit message instruction.
        
        Args:
            target_directory: The directory containing the .github folder
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            settings_path = SystemUtils.get_vscode_user_settings_path()
            
            # Create the settings directory if it doesn't exist
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing settings or create empty dict
            settings = {}
            original_content = ""
            
            if settings_path.exists():
                try:
                    with open(settings_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                        
                    # Try to parse the JSON
                    if original_content.strip():
                        settings = json.loads(original_content)
                        
                except json.JSONDecodeError as e:
                    # If settings file has JSON errors, create a backup and start fresh
                    backup_path = settings_path.with_suffix(f'.json.backup.{pathlib.Path().name}')
                    try:
                        shutil.copy2(settings_path, backup_path)
                        return False, f"Settings file has JSON errors. Created backup at {backup_path}. Please fix the JSON and retry."
                    except Exception:
                        return False, f"Settings file has JSON errors and couldn't create backup: {str(e)}"
                except Exception as e:
                    return False, f"Could not read settings file: {str(e)}"
            
            # Ensure settings is a dictionary
            if not isinstance(settings, dict):
                settings = {}
            
            # Define our target setting
            commit_instructions_key = "github.copilot.chat.commitMessageGeneration.instructions"
            target_instruction = {
                "file": ".github/copilot-commit-message-instructions.md"
            }
            
            # Get current instructions or initialize empty list
            current_instructions = settings.get(commit_instructions_key, [])
            
            # Ensure it's a list
            if not isinstance(current_instructions, list):
                current_instructions = []
            
            # Check if our instruction already exists (exact match)
            instruction_exists = any(
                isinstance(instr, dict) and instr.get("file") == target_instruction["file"] 
                for instr in current_instructions
            )
            
            if not instruction_exists:
                # Add our instruction to the list
                current_instructions.append(target_instruction)
                settings[commit_instructions_key] = current_instructions
                
                # Write back to settings file with proper formatting
                try:
                    with open(settings_path, 'w', encoding='utf-8') as f:
                        json.dump(settings, f, indent=4, ensure_ascii=False, sort_keys=False)
                    
                    return True, f"Added commit message instructions to VS Code settings"
                    
                except Exception as e:
                    # If write fails, restore the original content
                    if original_content:
                        try:
                            with open(settings_path, 'w', encoding='utf-8') as f:
                                f.write(original_content)
                        except Exception:
                            pass  # Best effort to restore
                            
                    return False, f"Failed to write settings file: {str(e)}"
            else:
                return True, f"Commit message instructions already exist in VS Code settings"
                
        except Exception as e:
            return False, f"Failed to update VS Code settings: {str(e)}"

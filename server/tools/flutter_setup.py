"""
Flutter development environment setup tool for MCP.

This module provides tools for setting up complete Flutter development environments,
including Flutter SDK installation, Git, AWS CLI, and VS Code extensions.
"""

import pathlib
import platform
import os
import json
import urllib.request
import urllib.error
import zipfile
import time
import tempfile
import subprocess
import traceback
from typing import Optional, Dict, Tuple

from .base_tool import BaseTool
from .system_utils import SystemUtils


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
        except Exception as e:
            return None
    
    def download_and_extract_flutter(self, archive_path: str, install_dir: pathlib.Path) -> Tuple[bool, str]:
        """Download and extract Flutter SDK.
        
        Args:
            archive_path: Path to the archive on Google's storage (e.g., "stable/windows/flutter_windows_3.35.7-stable.zip")
            install_dir: Directory to install Flutter to (e.g., C:/flutter)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            base_url = "https://storage.googleapis.com/flutter_infra_release/releases"
            download_url = f"{base_url}/{archive_path}"
            
            # Check if Flutter is already installed
            if install_dir.exists() and (install_dir / "bin" / "flutter").exists():
                return True, f"Flutter already exists at {install_dir}. Skipping download."
            
            # Use system temp directory for download (user-accessible, no admin needed)
            temp_dir = pathlib.Path(tempfile.gettempdir())
            temp_zip = temp_dir / "flutter_download_temp.zip"
            
            print(f"📥 Downloading Flutter SDK from {download_url}...")
            print("⏳ This may take several minutes (200-300 MB download)...")
            
            start_time = time.time()
            
            # Download with progress callback
            def reporthook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(100, downloaded * 100 / total_size)
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    if block_num % 100 == 0:  # Print every 100 blocks to avoid spam
                        print(f"   Downloaded: {mb_downloaded:.1f} MB / {mb_total:.1f} MB ({percent:.1f}%)")
            
            urllib.request.urlretrieve(download_url, temp_zip, reporthook)
            download_time = time.time() - start_time
            
            print(f"✅ Download completed in {download_time:.1f} seconds")
            
            # Verify the downloaded file
            if not temp_zip.exists() or temp_zip.stat().st_size < 1024 * 1024:  # Less than 1 MB is suspicious
                return False, f"Downloaded file is too small or doesn't exist. Download may have failed."
            
            # Create the parent directory if it doesn't exist (with proper permissions)
            install_dir.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"📦 Extracting Flutter SDK to {install_dir.parent}...")
            extract_start = time.time()
            
            # Extract the archive
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                # Extract to parent directory (zip contains 'flutter' folder)
                zip_ref.extractall(install_dir.parent)
            
            extract_time = time.time() - extract_start
            print(f"✅ Extraction completed in {extract_time:.1f} seconds")
            
            # Clean up temp file
            temp_zip.unlink()
            print("🧹 Cleaned up temporary files")
            
            # Verify installation
            flutter_bin = install_dir / "bin" / "flutter"
            if not flutter_bin.exists() and not (install_dir / "bin" / "flutter.bat").exists():
                return False, f"Flutter binary not found after extraction. Installation may be incomplete."
            
            return True, f"Flutter SDK downloaded and extracted to {install_dir}"
            
        except urllib.error.URLError as e:
            return False, f"Network error downloading Flutter: {str(e)}. Please check your internet connection."
        except zipfile.BadZipFile as e:
            return False, f"Downloaded file is corrupted: {str(e)}. Please try again."
        except PermissionError as e:
            return False, f"Permission denied: {str(e)}. Try running as administrator or choose a different install directory."
        except Exception as e:
            error_details = traceback.format_exc()
            return False, f"Failed to download/extract Flutter: {str(e)}\n\nDetails:\n{error_details}"
    
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
        
        This tool automates the onboarding process by:
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
            str: Formatted setup report
        """
        try:
            system = platform.system()
            target_path = pathlib.Path(target_directory).resolve()
            
            # Create target directory if it doesn't exist
            target_path.mkdir(parents=True, exist_ok=True)
            
            results = {
                'git': {'status': 'skipped', 'message': ''},
                'aws_cli': {'status': 'skipped', 'message': ''},
                'flutter': {'status': 'skipped', 'message': ''},
                'vscode_extensions': {'status': 'skipped', 'message': ''},
                'project_clone': {'status': 'skipped', 'message': ''},
                'flutter_doctor': {'status': 'skipped', 'message': ''}
            }
            
            # ==================== GIT INSTALLATION ====================
            if install_git:
                git_exists, git_version = SystemUtils.check_command_exists('git')
                
                if git_exists:
                    results['git'] = {
                        'status': 'already_installed',
                        'message': f'Git already installed: {git_version.split()[0] if git_version else "unknown version"}'
                    }
                else:
                    if system == "Windows":
                        # Try to install via winget (available on Windows 10/11)
                        winget_exists, _ = SystemUtils.check_command_exists('winget')
                        if winget_exists:
                            success, stdout, stderr = SystemUtils.run_command(['winget', 'install', '--id', 'Git.Git', '-e', '--source', 'winget', '--accept-package-agreements', '--accept-source-agreements'], check=False)
                            if success:
                                results['git'] = {
                                    'status': 'installed',
                                    'message': 'Git installed via winget. Please restart your terminal or add Git to PATH manually.'
                                }
                            else:
                                results['git'] = {
                                    'status': 'failed',
                                    'message': f'Winget install failed: {stderr}. Please download from: https://git-scm.com/download/windows'
                                }
                        else:
                            results['git'] = {
                                'status': 'manual_required',
                                'message': 'Winget not found. Please install winget (Windows Package Manager) or download Git from: https://git-scm.com/download/windows'
                            }
                    elif system == "Darwin":  # macOS
                        # Try to install via Homebrew
                        brew_exists, _ = SystemUtils.check_command_exists('brew')
                        if brew_exists:
                            success, stdout, stderr = SystemUtils.run_command(['brew', 'install', 'git'], check=False)
                            if success:
                                results['git'] = {'status': 'installed', 'message': 'Git installed via Homebrew'}
                            else:
                                results['git'] = {'status': 'failed', 'message': f'Homebrew install failed: {stderr}'}
                        else:
                            results['git'] = {
                                'status': 'manual_required',
                                'message': 'Please install Homebrew first or download Git from: https://git-scm.com/download/mac'
                            }
            
            # ==================== AWS CLI INSTALLATION ====================
            if install_aws_cli:
                aws_exists, aws_version = SystemUtils.check_command_exists('aws')
                
                if aws_exists:
                    results['aws_cli'] = {
                        'status': 'already_installed',
                        'message': f'AWS CLI already installed: {aws_version.split()[0] if aws_version else "unknown version"}'
                    }
                else:
                    if system == "Windows":
                        # Try to install via winget
                        winget_exists, _ = SystemUtils.check_command_exists('winget')
                        if winget_exists:
                            success, stdout, stderr = SystemUtils.run_command(['winget', 'install', '--id', 'Amazon.AWSCLI', '-e', '--source', 'winget', '--accept-package-agreements', '--accept-source-agreements'], check=False)
                            if success:
                                results['aws_cli'] = {
                                    'status': 'installed',
                                    'message': 'AWS CLI installed via winget. Please restart your terminal or add AWS CLI to PATH manually.'
                                }
                            else:
                                results['aws_cli'] = {
                                    'status': 'failed',
                                    'message': f'Winget install failed: {stderr}. Please download from: https://awscli.amazonaws.com/AWSCLIV2.msi'
                                }
                        else:
                            results['aws_cli'] = {
                                'status': 'manual_required',
                                'message': 'Winget not found. Please install winget or download AWS CLI from: https://awscli.amazonaws.com/AWSCLIV2.msi'
                            }
                    elif system == "Darwin":  # macOS
                        # Try to install via Homebrew
                        brew_exists, _ = SystemUtils.check_command_exists('brew')
                        if brew_exists:
                            success, stdout, stderr = SystemUtils.run_command(['brew', 'install', 'awscli'], check=False)
                            if success:
                                results['aws_cli'] = {'status': 'installed', 'message': 'AWS CLI installed via Homebrew'}
                            else:
                                results['aws_cli'] = {'status': 'failed', 'message': f'Homebrew install failed: {stderr}'}
                        else:
                            results['aws_cli'] = {
                                'status': 'manual_required',
                                'message': 'Please install Homebrew first or download AWS CLI from: https://awscli.amazonaws.com/AWSCLIV2.pkg'
                            }
            
            # ==================== FLUTTER INSTALLATION ====================
            if install_flutter:
                # Always check first, _install_flutter also checks but this provides better UX
                flutter_exists, flutter_ver = SystemUtils.check_command_exists('flutter')
                
                if flutter_exists:
                    results['flutter'] = {
                        'status': 'already_installed',
                        'message': f'Flutter already installed: {flutter_ver.split()[0] if flutter_ver else "unknown version"}'
                    }
                else:
                    # _install_flutter will double-check before attempting download
                    results['flutter'] = self._install_flutter(system)
            
            # ==================== VS CODE EXTENSIONS ====================
            if install_vscode_extensions:
                results['vscode_extensions'] = self._install_vscode_extensions()
            
            # ==================== CLONE PROJECT FROM CODECOMMIT ====================
            if codecommit_repo_url:
                results['project_clone'] = self._clone_codecommit_project(codecommit_repo_url, target_path, aws_profile)
            
            # ==================== RUN FLUTTER DOCTOR ====================
            results['flutter_doctor'] = self._get_flutter_doctor_instructions(results['flutter'])
            
            # ==================== GENERATE REPORT ====================
            return self._generate_setup_report(results, target_path, system, flutter_version, codecommit_repo_url)
            
        except Exception as e:
            return f"Error setting up Flutter developer environment: {str(e)}"
    
    def _install_flutter(self, system: str) -> Dict[str, str]:
        """Internal method to install Flutter SDK."""
        # First check if Flutter is already installed and in PATH
        flutter_exists, flutter_ver = SystemUtils.check_command_exists('flutter')
        
        if flutter_exists:
            return {
                'status': 'already_installed',
                'message': f'Flutter already installed and available in PATH: {flutter_ver.split()[0] if flutter_ver else "unknown version"}'
            }
        
        if system == "Windows":
            # Use user's home directory to avoid permission issues (no admin needed)
            flutter_install_dir = pathlib.Path.home() / "flutter"
            flutter_bin_path = flutter_install_dir / "bin"
            
            print("🔍 Fetching Flutter release information...")
            
            # Get latest Flutter release info
            release_info = self.get_latest_flutter_release("windows")
            
            if release_info and release_info.get('archive'):
                print(f"📌 Found Flutter {release_info['version']} (Dart {release_info.get('dart_version', 'unknown')})")
                
                # Attempt automatic download and installation
                success, message = self.download_and_extract_flutter(
                    release_info['archive'],
                    flutter_install_dir
                )
                
                if success:
                    print("🔧 Adding Flutter to Windows PATH...")
                    # Add to PATH
                    path_success, path_message = SystemUtils.add_to_windows_path(flutter_bin_path)
                    
                    if path_success:
                        return {
                            'status': 'installed',
                            'message': (
                                f"✅ Flutter {release_info['version']} installed successfully!\n\n"
                                f"📂 Location: {flutter_install_dir}\n"
                                f"🔗 {path_message}\n\n"
                                f"⚡ Next steps:\n"
                                f"1. Restart your terminal (close and reopen)\n"
                                f"2. Run 'flutter doctor' to verify installation\n"
                                f"3. Accept Android licenses: 'flutter doctor --android-licenses'\n"
                                f"4. You may need to install Android Studio or VS Code extensions"
                            )
                        }
                    else:
                        return {
                            'status': 'partial_success',
                            'message': (
                                f"⚠️ Flutter {release_info['version']} downloaded but PATH update failed.\n\n"
                                f"📂 Location: {flutter_install_dir}\n"
                                f"❌ PATH issue: {path_message}\n\n"
                                f"🔧 Manual PATH setup required:\n"
                                f"1. Add to System Environment Variables:\n"
                                f"   {flutter_bin_path}\n"
                                f"2. Restart your terminal\n"
                                f"3. Run 'flutter doctor' to verify"
                            )
                        }
                else:
                    # Download failed, provide manual instructions
                    return {
                        'status': 'failed',
                        'message': (
                            f"❌ Automatic installation failed:\n{message}\n\n"
                            f"🔄 Alternative installation methods:\n\n"
                            f"1. Manual download:\n"
                            f"   - Download: https://storage.googleapis.com/flutter_infra_release/releases/{release_info['archive']}\n"
                            f"   - Extract to: {flutter_install_dir}\n"
                            f"   - Add {flutter_bin_path} to your PATH\n\n"
                            f"2. VS Code method:\n"
                            f"   - Install Flutter extension\n"
                            f"   - Ctrl+Shift+P → 'Flutter: New Project' → 'Download SDK'\n\n"
                            f"3. Package manager:\n"
                            f"   - Chocolatey: choco install flutter\n"
                            f"   - Scoop: scoop install flutter"
                        )
                    }
            else:
                # Couldn't get release info, provide manual instructions
                return {
                    'status': 'manual_required',
                    'message': (
                        f'❌ Could not fetch Flutter release information.\n\n'
                        f'Please install manually using one of these methods:\n\n'
                        f'1. VS Code method (EASIEST):\n'
                        f'   - Install Flutter extension\n'
                        f'   - Ctrl+Shift+P → "Flutter: New Project" → "Download SDK"\n\n'
                        f'2. Package managers:\n'
                        f'   - Chocolatey: choco install flutter\n'
                        f'   - Scoop: scoop install flutter\n\n'
                        f'3. Direct download:\n'
                        f'   - https://docs.flutter.dev/get-started/install/windows'
                    )
                }
        elif system == "Darwin":  # macOS
            # Truncated for brevity - similar logic for macOS
            return {
                'status': 'manual_required',
                'message': 'Please install Flutter manually on macOS. See: https://docs.flutter.dev/get-started/install/macos'
            }
        else:
            return {
                'status': 'failed',
                'message': f'Unsupported operating system: {system}. Please install Flutter manually.'
            }
    
    def _install_vscode_extensions(self) -> Dict[str, str]:
        """Internal method to install VS Code extensions."""
        code_exists, _ = SystemUtils.check_command_exists('code')
        
        if not code_exists:
            return {
                'status': 'manual_required',
                'message': 'VS Code not detected. Please install VS Code and the Flutter/Dart extensions manually.'
            }
        
        extensions_to_install = [
            'Dart-Code.dart-code',
            'Dart-Code.flutter'
        ]
        
        # First, check which extensions are already installed
        # Use subprocess directly with shell=True for Windows compatibility
        try:
            result = subprocess.run(
                ['code', '--list-extensions'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=30
            )
            installed_ext_list = []
            if result.returncode == 0 and result.stdout:
                installed_ext_list = [ext.strip().lower() for ext in result.stdout.strip().split('\n')]
        except Exception:
            installed_ext_list = []
        
        already_installed = []
        newly_installed = []
        failed_extensions = []
        
        for ext in extensions_to_install:
            ext_lower = ext.lower()
            
            # Check if already installed
            if ext_lower in installed_ext_list:
                already_installed.append(ext)
                continue
            
            # Try to install
            try:
                result = subprocess.run(
                    ['code', '--install-extension', ext, '--force'],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=60
                )
                
                # Check output for "already installed" message
                if result.returncode == 0 or (result.stdout and 'already installed' in result.stdout.lower()):
                    if 'already installed' in result.stdout.lower():
                        already_installed.append(ext)
                    else:
                        newly_installed.append(ext)
                else:
                    failed_extensions.append(ext)
            except Exception:
                failed_extensions.append(ext)
        
        # Generate appropriate response
        total_working = len(already_installed) + len(newly_installed)
        
        if total_working == len(extensions_to_install):
            # All extensions are working
            parts = []
            if newly_installed:
                parts.append(f"Installed: {', '.join(newly_installed)}")
            if already_installed:
                parts.append(f"Already installed: {', '.join(already_installed)}")
            
            return {
                'status': 'success',
                'message': '. '.join(parts)
            }
        elif total_working > 0:
            # Some working, some failed
            parts = []
            if newly_installed:
                parts.append(f"Installed: {', '.join(newly_installed)}")
            if already_installed:
                parts.append(f"Already installed: {', '.join(already_installed)}")
            if failed_extensions:
                parts.append(f"Failed: {', '.join(failed_extensions)}")
            
            return {
                'status': 'partial',
                'message': '. '.join(parts) + '. Please install failed extensions manually from VS Code marketplace.'
            }
        else:
            # All failed
            return {
                'status': 'failed',
                'message': f'Failed to install extensions. Please install manually from VS Code: {", ".join(extensions_to_install)}'
            }
    
    def _clone_codecommit_project(self, repo_url: str, target_path: pathlib.Path, aws_profile: Optional[str]) -> Dict[str, str]:
        """Internal method to clone project from any Git repository (GitHub, GitLab, AWS CodeCommit, etc.)."""
        git_exists, _ = SystemUtils.check_command_exists('git')
        
        if not git_exists:
            return {
                'status': 'failed',
                'message': 'Git is not installed. Cannot clone repository.'
            }
        
        # Extract repository name for the clone directory
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        clone_dir = target_path / repo_name
        
        # Check if directory already exists
        if clone_dir.exists():
            # Check if it's a valid Git repository
            git_dir = clone_dir / ".git"
            if git_dir.exists():
                # It's a valid Git repo, try to pull latest changes
                try:
                    result = subprocess.run(
                        ['git', 'pull'],
                        cwd=clone_dir,
                        capture_output=True,
                        text=True,
                        shell=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        return {
                            'status': 'updated',
                            'message': f'Repository already exists at {clone_dir}. Updated to latest version.'
                        }
                    else:
                        return {
                            'status': 'exists',
                            'message': f'Repository exists at {clone_dir} but could not update: {result.stderr}. You may need to manually pull changes.'
                        }
                except Exception as e:
                    return {
                        'status': 'exists',
                        'message': f'Repository exists at {clone_dir} but could not update: {str(e)}. You may need to manually pull changes.'
                    }
            else:
                # Directory exists but is not a Git repo
                return {
                    'status': 'failed',
                    'message': f'Directory {clone_dir} exists but is not a Git repository. Please remove or rename it and try again.'
                }
        
        # Clone the repository
        clone_command = ['git', 'clone', repo_url]
        
        # Determine if this is an AWS CodeCommit URL
        is_codecommit = 'codecommit' in repo_url.lower()
        
        if aws_profile and is_codecommit:
            # Set AWS profile for CodeCommit
            env = os.environ.copy()
            env['AWS_PROFILE'] = aws_profile
            try:
                result = subprocess.run(
                    clone_command,
                    cwd=target_path,
                    capture_output=True,
                    text=True,
                    env=env,
                    check=False
                )
                if result.returncode == 0:
                    return {
                        'status': 'success',
                        'message': f'Successfully cloned {repo_name} to {clone_dir}'
                    }
                else:
                    return {
                        'status': 'failed',
                        'message': f'Failed to clone: {result.stderr}'
                    }
            except Exception as e:
                return {
                    'status': 'failed',
                    'message': f'Clone error: {str(e)}'
                }
        else:
            # Standard Git clone (works for GitHub, GitLab, etc.)
            try:
                result = subprocess.run(
                    clone_command,
                    cwd=target_path,
                    capture_output=True,
                    text=True,
                    check=False,
                    shell=True  # Use shell for better Windows compatibility
                )
                if result.returncode == 0:
                    return {
                        'status': 'success',
                        'message': f'Successfully cloned {repo_name} to {clone_dir}'
                    }
                else:
                    return {
                        'status': 'failed',
                        'message': f'Failed to clone: {result.stderr if result.stderr else "Unknown error"}'
                    }
            except Exception as e:
                return {
                    'status': 'failed',
                    'message': f'Clone error: {str(e)}'
                }
    
    def _get_flutter_doctor_instructions(self, flutter_result: Dict[str, str]) -> Dict[str, str]:
        """Internal method to generate flutter doctor instructions."""
        flutter_exists, _ = SystemUtils.check_command_exists('flutter')
        
        if flutter_result.get('status') == 'installed':
            # Flutter was just installed
            flutter_install_dir = pathlib.Path.home() / "flutter"
            
            return {
                'status': 'manual_recommended',
                'message': (
                    f'✅ Flutter installed successfully at {flutter_install_dir}\n\n'
                    f'🔧 IMPORTANT: Complete the setup by running these commands in a NEW terminal:\n\n'
                    f'1. Close and reopen your terminal (to refresh PATH)\n'
                    f'2. Run: flutter doctor -v\n'
                    f'3. Follow any instructions from flutter doctor\n'
                    f'4. Accept Android licenses: flutter doctor --android-licenses\n\n'
                    f'💡 TIP: The first flutter command may take 2-3 minutes to complete\n'
                    f'as it downloads dependencies and sets up the environment.'
                )
            }
        elif flutter_exists:
            return {
                'status': 'recommended',
                'message': (
                    '✅ Flutter is available in PATH\n\n'
                    '🔧 Run these commands to verify your setup:\n'
                    '1. flutter doctor -v\n'
                    '2. flutter doctor --android-licenses'
                )
            }
        else:
            return {
                'status': 'skipped',
                'message': 'Flutter not installed. Install Flutter first, then run "flutter doctor -v" to verify.'
            }
    
    def _generate_setup_report(
        self,
        results: Dict[str, Dict[str, str]],
        target_path: pathlib.Path,
        system: str,
        flutter_version: str,
        codecommit_repo_url: Optional[str]
    ) -> str:
        """Internal method to generate the setup report."""
        report = "🚀 **Flutter Developer Environment Setup Report**\n\n"
        report += f"**Target Directory**: {target_path}\n"
        report += f"**Operating System**: {system}\n"
        report += f"**Flutter Version**: {flutter_version}\n\n"
        
        # Status icons
        status_icons = {
            'success': '✅',
            'installed': '✅',
            'already_installed': '✅',
            'updated': '✅',
            'exists': '💡',
            'partial_success': '⚠️',
            'partial': '⚠️',
            'failed': '❌',
            'manual_required': '📋',
            'manual_recommended': '💡',
            'recommended': '💡',
            'skipped': '⏭️'
        }
        
        report += "## Installation Summary\n\n"
        
        for component, result in results.items():
            icon = status_icons.get(result['status'], '❓')
            component_name = component.replace('_', ' ').title()
            report += f"{icon} **{component_name}**: {result['status']}\n"
            if result['message']:
                report += f"   {result['message']}\n\n"
        
        # Next steps
        report += "\n## 📋 Next Steps\n\n"
        
        manual_steps = []
        if results['git']['status'] == 'manual_required':
            manual_steps.append("1. Install Git as instructed above")
        if results['aws_cli']['status'] == 'manual_required':
            manual_steps.append("2. Install AWS CLI as instructed above")
        if results['flutter']['status'] == 'manual_required':
            manual_steps.append("3. Install Flutter SDK as instructed above")
        if results['vscode_extensions']['status'] in ['manual_required', 'failed', 'partial']:
            manual_steps.append("4. Install VS Code Flutter and Dart extensions")
        
        if manual_steps:
            report += "**Manual Actions Required**:\n"
            for step in manual_steps:
                report += f"   {step}\n"
            report += "\n"
        
        report += "**Configuration Steps**:\n"
        report += "   1. Configure Git: `git config --global user.name 'Your Name'`\n"
        report += "   2. Configure Git: `git config --global user.email 'your.email@example.com'`\n"
        report += "   3. Configure AWS CLI: `aws configure` (set up your credentials)\n"
        report += "   4. Run `flutter doctor` to verify all dependencies\n"
        report += "   5. Accept Android licenses: `flutter doctor --android-licenses`\n"
        
        if codecommit_repo_url:
            report += f"   6. Navigate to project: `cd {target_path}`\n"
            report += "   7. Run `flutter pub get` to install dependencies\n"
            report += "   8. Open in VS Code: `code .`\n"
        
        report += "\n## 🎯 IDEs\n\n"
        report += "**Android Studio**: Download from https://developer.android.com/studio\n"
        report += "   - After installation, install Flutter and Dart plugins\n"
        report += "   - Configure Android SDK\n\n"
        report += "**VS Code**: Download from https://code.visualstudio.com/\n"
        if results['vscode_extensions']['status'] == 'installed':
            report += "   - Flutter and Dart extensions already installed ✅\n"
        else:
            report += "   - Install Flutter and Dart extensions from the marketplace\n"
        
        return report

"""
Configuration module for MCP Prompt Library server.

This module provides centralized configuration for paths and shared constants
used across different tools and components.
"""

import pathlib

# Base directories
SERVER_DIR = pathlib.Path(__file__).parent
PROJECT_ROOT = SERVER_DIR.parent

# Prompts directory - where all prompt templates are stored
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Source directory for work environment setup files
SOURCE_GITHUB_DIR = PROJECT_ROOT / "data" / "setup_work_environment"

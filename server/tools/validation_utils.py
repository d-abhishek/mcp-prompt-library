"""
Validation utilities for MCP tools.

This module provides static validation methods used across different tools
for validating data, syntax, and file names.
"""

from typing import Dict, Any, List


class ValidationUtils:
    """Utility class for validation operations."""
    
    @staticmethod
    def validate_prompt_metadata(metadata: Dict[str, Any]) -> bool:
        """Validate that prompt metadata has required fields.
        
        Args:
            metadata: Dictionary containing prompt metadata
            
        Returns:
            bool: True if metadata is valid, False otherwise
        """
        required_fields = ['name', 'description']
        return all(field in metadata for field in required_fields)
    
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a name to be used as a filename.
        
        Removes or replaces invalid characters that cannot be used in filenames.
        
        Args:
            name: The name to sanitize
            
        Returns:
            str: Sanitized filename-safe string
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
    
    @staticmethod
    def validate_jinja2_syntax(content: str) -> tuple[bool, List[str]]:
        """Validate that content uses Jinja2 syntax, not Handlebars/Mustache.
        
        Checks for common Handlebars/Mustache patterns and suggests Jinja2 alternatives.
        
        Args:
            content: The template content to validate
            
        Returns:
            tuple: (is_valid: bool, warnings: List[str])
        """
        warnings = []
        
        # Check for common Handlebars patterns
        handlebars_patterns = [
            ('{{#if', 'Use {% if condition %} instead of {{#if condition}}'),
            ('{{#eq', 'Use {% if var == "value" %} instead of {{#eq var "value"}}'),
            ('{{#unless', 'Use {% if not condition %} instead of {{#unless condition}}'),
            ('{{#each', 'Use {% for item in items %} instead of {{#each items}}'),
            ('{{/if}}', 'Use {% endif %} instead of {{/if}}'),
            ('{{/eq}}', 'Use {% endif %} instead of {{/eq}}'),
            ('{{/unless}}', 'Use {% endif %} instead of {{/unless}}'),
            ('{{/each}}', 'Use {% endfor %} instead of {{/each}}')
        ]
        
        for pattern, message in handlebars_patterns:
            if pattern in content:
                warnings.append(f"⚠️  Found '{pattern}': {message}")
        
        is_valid = len(warnings) == 0
        return is_valid, warnings

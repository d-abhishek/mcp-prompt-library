"""
Prompt management tool for MCP.

This module provides tools for creating, updating, deleting, and managing
prompt templates.
"""

import frontmatter
import pathlib
from typing import List, Dict, Any, Optional

from .base_tool import BaseTool
from .validation_utils import ValidationUtils
from ..config import PROMPTS_DIR


class PromptManagementTool(BaseTool):
    """Tool for managing prompt templates."""
    
    def __init__(self):
        """Initialize the prompt management tool."""
        super().__init__()
        self.prompts_dir = PROMPTS_DIR
    
    def create_prompt(
        self,
        Name: str,
        Description: str,
        Content: str,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Create a new MCP prompt file with frontmatter metadata.
        
        Args:
            Name: The name/identifier for the prompt
            Description: Description of what the prompt does
            Content: The prompt content (must use Jinja2 template syntax)
            Arguments: Optional list of argument definitions with 'name', 'description', and 'required' fields
            
        Returns:
            str: Success or error message
        """
        try:
            # Validate Jinja2 syntax
            is_valid, warnings = ValidationUtils.validate_jinja2_syntax(Content)
            
            # Sanitize the filename
            filename = ValidationUtils.sanitize_filename(Name)
            file_path = self.prompts_dir / f"{filename}.md"
            
            # Check if file already exists
            if file_path.exists():
                return f"Error: Prompt '{Name}' already exists. Use update_prompt to modify it."
            
            # If there are syntax warnings, include them in the response but still create the prompt
            warning_message = ""
            if not is_valid:
                warning_message = "\n\n⚠️  TEMPLATE SYNTAX WARNINGS:\n" + "\n".join(warnings) + "\n\nThe prompt was created but may not render correctly. Please fix the syntax issues above.\n"
            
            # Prepare metadata
            metadata = {
                'name': Name,
                'description': Description
            }
            
            if Arguments:
                metadata['arguments'] = Arguments  # type: ignore
            
            # Create the frontmatter post
            post = frontmatter.Post(Content)
            post.metadata.update(metadata)
            
            # Ensure prompts directory exists
            self.prompts_dir.mkdir(exist_ok=True)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            return f"Successfully created prompt '{Name}' at {file_path}{warning_message}"
            
        except Exception as e:
            return f"Error creating prompt: {str(e)}"
    
    def update_prompt(
        self,
        Name: str,
        Description: Optional[str] = None,
        Content: Optional[str] = None,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Update an existing MCP prompt file.
        
        Args:
            Name: The name/identifier of the prompt to update
            Description: New description (optional)
            Content: New prompt content (optional - must use Jinja2 template syntax if provided)
            Arguments: New argument definitions (optional)
            
        Returns:
            str: Success or error message
        """
        try:
            # Validate Jinja2 syntax if content is being updated
            warning_message = ""
            if Content is not None:
                is_valid, warnings = ValidationUtils.validate_jinja2_syntax(Content)
                if not is_valid:
                    warning_message = "\n\n⚠️  TEMPLATE SYNTAX WARNINGS:\n" + "\n".join(warnings) + "\n\nThe prompt was updated but may not render correctly. Please fix the syntax issues above.\n"
            
            # Find the file
            filename = ValidationUtils.sanitize_filename(Name)
            file_path = self.prompts_dir / f"{filename}.md"
            
            if not file_path.exists():
                return f"Error: Prompt '{Name}' does not exist. Use create_prompt to create it."
            
            # Load existing prompt
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Update metadata
            if Description is not None:
                post.metadata['description'] = Description
            
            if Arguments is not None:
                post.metadata['arguments'] = Arguments
            
            # Update content
            if Content is not None:
                post.content = Content
            
            # Write back the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            return f"Successfully updated prompt '{Name}'{warning_message}"
            
        except Exception as e:
            return f"Error updating prompt: {str(e)}"
    
    def delete_prompt(self, Name: str) -> str:
        """Delete an MCP prompt file.
        
        Args:
            Name: The name/identifier of the prompt to delete
            
        Returns:
            str: Success or error message
        """
        try:
            # Find the file
            filename = ValidationUtils.sanitize_filename(Name)
            file_path = self.prompts_dir / f"{filename}.md"
            
            if not file_path.exists():
                return f"Error: Prompt '{Name}' does not exist."
            
            # Delete the file
            file_path.unlink()
            
            return f"Successfully deleted prompt '{Name}'"
            
        except Exception as e:
            return f"Error deleting prompt: {str(e)}"
    
    def list_prompts(self, include_content: bool = False, query: Optional[str] = None) -> str:
        """List all available MCP prompts or suggest the best matching prompts for a query.
        
        Args:
            include_content: Whether to include the full content of each prompt
            query: Optional search query to filter and rank prompts by relevance
            
        Returns:
            str: Formatted list of prompts or search results
        """
        try:
            if not self.prompts_dir.exists():
                return "No prompts directory found."
            
            prompt_files = list(self.prompts_dir.glob("*.md"))
            
            if not prompt_files:
                return "No prompts found."
            
            # Load all prompts and their metadata
            prompts_info = []
            for file_path in prompt_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    prompt_info = {
                        'name': post.metadata.get('name', file_path.stem),
                        'description': post.metadata.get('description', 'No description'),
                        'file': file_path.name,
                        'arguments': post.metadata.get('arguments', []),
                        'keywords': post.metadata.get('keywords', []),
                        'triggers': post.metadata.get('triggers', []),
                        'content_preview': post.content[:200] + "..." if len(post.content) > 200 else post.content
                    }
                    
                    if include_content:
                        prompt_info['content'] = post.content
                    
                    prompts_info.append(prompt_info)
                    
                except Exception as e:
                    prompts_info.append({
                        'name': file_path.stem,
                        'description': f'Error reading file: {str(e)}',
                        'file': file_path.name,
                        'arguments': [],
                        'keywords': [],
                        'triggers': [],
                        'content_preview': ''
                    })
            
            # If query is provided, filter and rank by relevance
            if query:
                query_lower = query.lower()
                scored_prompts = []
                
                for prompt in prompts_info:
                    score = 0
                    
                    # Score based on name matches
                    if any(word in prompt['name'].lower() for word in query_lower.split()):
                        score += 10
                    
                    # Score based on description matches
                    desc_words = prompt['description'].lower().split()
                    query_words = query_lower.split()
                    common_words = set(desc_words) & set(query_words)
                    score += len(common_words) * 5
                    
                    # Score based on keywords (if present)
                    keywords = prompt.get('keywords', [])
                    for keyword in keywords:
                        if keyword.lower() in query_lower:
                            score += 8
                    
                    # Score based on triggers (if present)
                    triggers = prompt.get('triggers', [])
                    for trigger in triggers:
                        if trigger.lower() in query_lower:
                            score += 15  # High score for trigger phrases
                    
                    # Specific keyword scoring for known patterns
                    if 'api' in query_lower and 'api' in prompt['name'].lower():
                        score += 15
                    if 'review' in query_lower and 'review' in prompt['name'].lower():
                        score += 15
                    if any(word in query_lower for word in ['create', 'build', 'generate']) and 'create' in prompt['name'].lower():
                        score += 10
                    
                    # Score based on content matches
                    content_words = prompt['content_preview'].lower().split()
                    common_content_words = set(content_words) & set(query_words)
                    score += len(common_content_words) * 2
                    
                    if score > 0:
                        scored_prompts.append((prompt, score))
                
                # Sort by score and filter to only relevant prompts
                scored_prompts.sort(key=lambda x: x[1], reverse=True)
                
                if not scored_prompts:
                    return f"No matching prompts found for query: '{query}'\n\nAll available prompts:\n" + "\n".join([f"- {p['name']}: {p['description']}" for p in prompts_info])
                
                # Format response for query results
                result = f"🎯 **Search results for**: '{query}'\n\n"
                
                best_match = scored_prompts[0]
                prompt_info = best_match[0]
                
                result += f"**Best match**: `{prompt_info['name']}` (score: {best_match[1]})\n"
                result += f"Description: {prompt_info['description']}\n\n"
                
                if prompt_info['arguments']:
                    result += "**Required arguments**:\n"
                    for arg in prompt_info['arguments']:
                        if arg.get('required', False):
                            result += f"- `{arg.get('name')}`: {arg.get('description', 'No description')}\n"
                    
                    result += "\n**Optional arguments**:\n"
                    for arg in prompt_info['arguments']:
                        if not arg.get('required', False):
                            result += f"- `{arg.get('name')}`: {arg.get('description', 'No description')}\n"
                
                result += f"\n**Usage**: Call the prompt `{prompt_info['name']}` with the appropriate arguments.\n"
                
                # Show other matches if any
                if len(scored_prompts) > 1:
                    result += f"\n**Other matches** ({len(scored_prompts)-1} found):\n"
                    for prompt_data, score in scored_prompts[1:4]:  # Show top 3 alternatives
                        result += f"- `{prompt_data['name']}` (score: {score}): {prompt_data['description']}\n"
                
                return result
            
            else:
                # No query provided - show all prompts (original behavior)
                result = f"📚 **All available prompts** ({len(prompts_info)} found):\n\n"
                
                for i, prompt in enumerate(prompts_info, 1):
                    result += f"{i}. **{prompt['name']}**\n"
                    result += f"   Description: {prompt['description']}\n"
                    result += f"   File: {prompt['file']}\n"
                    
                    if prompt['arguments']:
                        result += "   Arguments:\n"
                        for arg in prompt['arguments']:
                            req_text = " (required)" if arg.get('required', False) else " (optional)"
                            result += f"     - {arg.get('name', 'unnamed')}{req_text}: {arg.get('description', 'No description')}\n"
                    
                    if include_content:
                        result += f"   Content:\n{prompt['content']}\n"
                    
                    result += "\n"
                
                result += "\n💡 **Tip**: Use `list_prompts(query='your search terms')` to find specific prompts.\n"
                return result
            
        except Exception as e:
            return f"Error listing prompts: {str(e)}"

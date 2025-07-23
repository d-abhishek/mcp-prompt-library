import frontmatter
import pathlib
from typing import List, Dict, Any, Optional

# Get the prompts directory
prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"

def validate_prompt_metadata(metadata: Dict[str, Any]) -> bool:
    """Validate that prompt metadata has required fields"""
    required_fields = ['name', 'description']
    return all(field in metadata for field in required_fields)

def sanitize_filename(name: str) -> str:
    """Sanitize a name to be used as a filename"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()

def register_tools(mcp):
    """Register all MCP tools for prompt management"""
    
    @mcp.tool()
    def create_prompt(
        Name: str,
        Description: str,
        Content: str,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Create a new MCP prompt file with frontmatter metadata.
        
        Args:
            name: The name/identifier for the prompt
            description: Description of what the prompt does
            content: The prompt content (can include Jinja2 template variables like {{variable}})
            arguments: Optional list of argument definitions with 'name', 'description', and 'required' fields
        """
        try:
            # Sanitize the filename
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
            # Check if file already exists
            if file_path.exists():
                return f"Error: Prompt '{Name}' already exists. Use update_prompt to modify it."
            
            # Prepare metadata
            metadata = {
                'name': Name,
                'description': Description
            }
            
            if Arguments:
                metadata['arguments'] = Arguments # type: ignore
            
            # Create the frontmatter post
            post = frontmatter.Post(Content)
            post.metadata.update(metadata)
            
            # Ensure prompts directory exists
            prompts_dir.mkdir(exist_ok=True)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            return f"Successfully created prompt '{Name}' at {file_path}"
            
        except Exception as e:
            return f"Error creating prompt: {str(e)}"
    
    @mcp.tool()
    def update_prompt(
        Name: str,
        Description: Optional[str] = None,
        Content: Optional[str] = None,
        Arguments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Update an existing MCP prompt file.
        
        Args:
            name: The name/identifier of the prompt to update
            description: New description (optional)
            content: New prompt content (optional)
            arguments: New argument definitions (optional)
        """
        try:
            # Find the file
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
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
            
            return f"Successfully updated prompt '{Name}'"
            
        except Exception as e:
            return f"Error updating prompt: {str(e)}"
    
    @mcp.tool()
    def delete_prompt(Name: str) -> str:
        """Delete an MCP prompt file.
        
        Args:
            name: The name/identifier of the prompt to delete
        """
        try:
            # Find the file
            filename = sanitize_filename(Name)
            file_path = prompts_dir / f"{filename}.md"
            
            if not file_path.exists():
                return f"Error: Prompt '{Name}' does not exist."
            
            # Delete the file
            file_path.unlink()
            
            return f"Successfully deleted prompt '{Name}'"
            
        except Exception as e:
            return f"Error deleting prompt: {str(e)}"
    
    @mcp.tool()
    def list_prompts(include_content: bool = False) -> str:
        """List all available MCP prompts.
        
        Args:
            include_content: Whether to include the full content of each prompt
        """
        try:
            if not prompts_dir.exists():
                return "No prompts directory found."
            
            prompt_files = list(prompts_dir.glob("*.md"))
            
            if not prompt_files:
                return "No prompts found."
            
            prompts_info = []
            
            for file_path in prompt_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    prompt_info = {
                        'name': post.metadata.get('name', file_path.stem),
                        'description': post.metadata.get('description', 'No description'),
                        'file': file_path.name,
                        'arguments': post.metadata.get('arguments', [])
                    }
                    
                    if include_content:
                        prompt_info['content'] = post.content
                    
                    prompts_info.append(prompt_info)
                    
                except Exception as e:
                    prompts_info.append({
                        'name': file_path.stem,
                        'description': f'Error reading file: {str(e)}',
                        'file': file_path.name,
                        'arguments': []
                    })
            
            # Format the output
            result = f"Found {len(prompts_info)} prompt(s):\n\n"
            
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
            
            return result
            
        except Exception as e:
            return f"Error listing prompts: {str(e)}"

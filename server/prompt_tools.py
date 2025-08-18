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
    def list_prompts(include_content: bool = False, query: Optional[str] = None) -> str:
        """List all available MCP prompts or suggest the best matching prompts for a query.
        
        Args:
            include_content: Whether to include the full content of each prompt
            query: Optional search query to filter and rank prompts by relevance
        """
        try:
            if not prompts_dir.exists():
                return "No prompts directory found."
            
            prompt_files = list(prompts_dir.glob("*.md"))
            
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

    @mcp.tool()
    def smart_prompt_executor(query: str, auto_execute: bool = False) -> str:
        """Automatically detect and execute the most appropriate prompt for a user query.
        
        Args:
            query: The user's natural language query or request
            auto_execute: If True, automatically execute the best matching prompt
        """
        try:
            # First, get the suggestion using list_prompts with query
            suggestion_result = list_prompts(include_content=False, query=query)
            
            if not auto_execute:
                return suggestion_result + "\n\n💡 **Tip**: Use `smart_prompt_executor` with `auto_execute=True` to automatically run the suggested prompt."
            
            # Extract parameters from query for auto-execution
            query_lower = query.lower()
            
            # For create_api prompt specifically
            if 'api' in query_lower and ('create' in query_lower or 'build' in query_lower or 'generate' in query_lower):
                # Try to extract purpose and parameters from the query
                api_purpose = ""
                expected_parameters = ""
                
                # Extract what comes after "api for"
                if 'api for' in query_lower:
                    start_idx = query_lower.find('api for') + 7
                    api_purpose_part = query[start_idx:].split('.')[0].split(',')[0].strip()
                    api_purpose = api_purpose_part if api_purpose_part else "data management"
                elif 'student' in query_lower:
                    api_purpose = "student information management"
                elif 'user' in query_lower:
                    api_purpose = "user management"
                else:
                    api_purpose = "data management"
                
                # Extract parameters if mentioned
                if 'parameters' in query_lower or 'fields' in query_lower:
                    # Try to extract parameter list
                    param_keywords = ['name', 'class', 'contact', 'address', 'email', 'phone', 'age', 'id']
                    found_params = [param for param in param_keywords if param in query_lower]
                    if found_params:
                        expected_parameters = ", ".join(found_params)
                
                # Import and execute the create_api prompt
                from prompt_handlers import load_template
                import jinja2
                
                template = load_template("create_api")
                result = template.render(
                    api_purpose=api_purpose,
                    expected_parameters=expected_parameters if expected_parameters else None,
                    custom_api_reference=None
                )
                
                return f"🚀 **Auto-executed**: `create_api` prompt\n\n**Detected Parameters**:\n- API Purpose: {api_purpose}\n- Expected Parameters: {expected_parameters or 'None specified'}\n\n**Generated Result**:\n\n{result}"
            
            else:
                return suggestion_result + "\n\n⚠️ **Auto-execution not implemented** for this prompt type yet. Please use the suggested prompt manually."
                
        except Exception as e:
            return f"Error in auto-execution: {str(e)}"

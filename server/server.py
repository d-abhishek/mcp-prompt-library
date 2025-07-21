from mcp.server.fastmcp import FastMCP
import frontmatter                                # parses Markdown front matter
import jinja2                                     # templating engine
import pathlib

# 1. Initialize FastMCP server
mcp = FastMCP(name="ProjectPromptServer")

# 2. Auto-discover and load all prompt templates
prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"

def load_all_prompts():
    """Load all markdown prompt templates from the prompts directory"""
    prompt_templates = {}
    
    # Find all .md files in the prompts directory
    for md_file in prompts_dir.glob("*.md"):
        # Load the markdown file with front matter
        post = frontmatter.load(str(md_file))
        meta = post.metadata
        body = post.content
        
        # Get the prompt name from metadata or use filename
        prompt_name = meta.get('name', md_file.stem)
        
        # Store the template and metadata
        prompt_templates[prompt_name] = {
            'template': jinja2.Template(body),
            'metadata': meta,
            'description': meta.get('description', f'Prompt from {md_file.name}')
        }
    
    return prompt_templates

def create_prompt_function(name, template_data):
    """Dynamically create a prompt function based on template metadata"""
    template = template_data['template']
    metadata = template_data['metadata']
    description = template_data['description']
    
    # Extract argument information from metadata
    arguments = metadata.get('arguments', [])
    
    # Get parameter names
    param_names = [arg['name'] for arg in arguments]
    
    # Create a closure function that captures the template
    def create_func():
        # Build the function signature dynamically using exec
        param_list = ', '.join([f"{param}: str" for param in param_names])
        param_dict = ', '.join([f"'{param}': {param}" for param in param_names])
        
        func_code = f"""
def {name}({param_list}) -> str:
    '''
    {description}
    '''
    return captured_template.render({{{param_dict}}})
"""
        
        # Execute with the captured template
        namespace = {'captured_template': template}
        exec(func_code, namespace)
        return namespace[name]
    
    return create_func()

# 3. Load all prompts and register them
prompt_templates = load_all_prompts()

# 4. Dynamically register all prompt functions
for prompt_name, template_data in prompt_templates.items():
    prompt_func = create_prompt_function(prompt_name, template_data)
    
    # Register the function as an MCP prompt
    mcp.prompt()(prompt_func)

# 5. Run the MCP server
if __name__ == "__main__":
    mcp.run()
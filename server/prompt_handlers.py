import frontmatter
import jinja2
import pathlib

# Get the prompts directory
prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"

def load_template(filename: str) -> jinja2.Template:
    """Load a specific template file"""
    template_path = prompts_dir / f"{filename}.md"
    post = frontmatter.load(str(template_path))
    return jinja2.Template(post.content)

def register_prompts(mcp):
    """Register all prompt functions with the MCP server"""
    
    @mcp.prompt()
    def create_api(resource: str, methods: str) -> str:
        """Generate a REST API endpoint"""
        template = load_template("create_api")
        return template.render(resource=resource, methods=methods)
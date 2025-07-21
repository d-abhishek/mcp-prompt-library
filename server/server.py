from mcp.server.fastmcp import FastMCP
import frontmatter                                # parses Markdown front matter
import jinja2                                     # templating engine
import pathlib

# 1. Initialize FastMCP server
mcp = FastMCP(name="ProjectPromptServer")

# 2. Load template helper
prompts_dir = pathlib.Path(__file__).parent.parent / "prompts"

def load_template(filename: str) -> jinja2.Template:
    """Load a specific template file"""
    template_path = prompts_dir / f"{filename}.md"
    post = frontmatter.load(str(template_path))
    return jinja2.Template(post.content)

# 3. Define each prompt as a separate function

@mcp.prompt()
def create_api(resource: str, methods: str) -> str:
    """Generate a REST API endpoint"""
    template = load_template("create_api")
    return template.render(resource=resource, methods=methods)

# 4. Run the MCP server
if __name__ == "__main__":
    mcp.run()
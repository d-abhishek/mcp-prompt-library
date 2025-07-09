from mcp.server.fastmcp import FastMCP
import frontmatter                                # parses Markdown front matter :contentReference[oaicite:4]{index=4}
import jinja2                                     # templating engine :contentReference[oaicite:5]{index=5}
import pathlib

# 1. Initialize FastMCP server
mcp = FastMCP(name="ProjectPromptServer")

# 2. Load prompt template
tpl_path = pathlib.Path(__file__).parent.parent/"prompts/create_api.md"
post = frontmatter.load(str(tpl_path))
meta = post.metadata
body = post.content

# 3. Prepare Jinja2 template
jinja = jinja2.Template(body)

# 4. Dynamically define MCP prompt using function signature
#    Argument names and types must match front matter keys
#    @mcp.prompt will reflectively infer argument schema
@mcp.prompt()
def create_api(resource: str, methods: str) -> str:
    """
    Generates a REST API endpoint for the specified resource using given methods.
    """
    return jinja.render(resource=resource, methods=methods)

# 5. Run the MCP server
if __name__ == "__main__":
    mcp.run()

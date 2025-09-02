import frontmatter
import jinja2
import pathlib
from typing import Optional

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
    def create_api(api_purpose: str, expected_parameters: Optional[str] = None, custom_api_reference: Optional[str] = None, include_tests: Optional[str] = None) -> str:
        """Assists developers in creating a FastAPI-based API following best practices with Pydantic models, database abstraction, and CRUD endpoints"""
        template = load_template("create_api")
        return template.render(
            api_purpose=api_purpose,
            expected_parameters=expected_parameters,
            custom_api_reference=custom_api_reference,
            include_tests=include_tests
        )
    
    @mcp.prompt()
    def code_review(code: Optional[str], language: Optional[str] = None, framework: Optional[str] = None, specific_concerns: Optional[str] = None) -> str:
        """Perform a comprehensive code review with feedback on quality, security, and best practices"""
        template = load_template("code_review")
        return template.render(
            code=code,
            language=language,
            framework=framework,
            specific_concerns=specific_concerns
        )
    
    @mcp.prompt()
    def code_correctness_review(code_reference: str, language: str, functional_requirements: str, test_cases: Optional[str] = None) -> str:
        """Review code for correctness against functional requirements and test cases"""
        template = load_template("code_correctness_review")
        return template.render(
            code_reference=code_reference,
            language=language,
            functional_requirements=functional_requirements,
            test_cases=test_cases
        )
    
    @mcp.prompt()
    def coding_standards_check(code: Optional[str], language: Optional[str] = None, framework: Optional[str] = None, style_guide: Optional[str] = None, company_standards: Optional[str] = None) -> str:
        """Check code against established coding standards and best practices"""
        template = load_template("coding_standards_check")
        return template.render(
            code=code,
            language=language,
            framework=framework,
            style_guide=style_guide,
            company_standards=company_standards
        )
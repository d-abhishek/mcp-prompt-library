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
    def code_review(code_reference: str, language: str, specific_concerns: Optional[str] = None, company_guidelines: Optional[str] = None) -> str:
        """Perform a comprehensive code review with feedback on quality, architecture, and best practices"""
        template = load_template("code_review")
        return template.render(
            code_reference=code_reference,
            language=language,
            specific_concerns=specific_concerns,
            company_guidelines=company_guidelines
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
    def performance_bottleneck_analysis(code_reference: str, language: str, specific_performance_areas: Optional[str] = None, number_of_users: Optional[str] = None) -> str:
        """Identify performance bottlenecks, algorithmic inefficiencies, and scalability issues in code with detailed optimization recommendations"""
        template = load_template("performance_bottleneck_analysis")
        return template.render(
            code_reference=code_reference,
            language=language,
            specific_performance_areas=specific_performance_areas,
            number_of_users=number_of_users
        )
    
    @mcp.prompt()
    def security_vulnerability_analysis(code_reference: str, language: str, security_focus: Optional[str] = None, compliance_requirements: Optional[str] = None) -> str:
        """Identify security vulnerabilities, weaknesses, and attack vectors in code with comprehensive remediation strategies and compliance guidance"""
        template = load_template("security_vulnerability_analysis")
        return template.render(
            code_reference=code_reference,
            language=language,
            security_focus=security_focus,
            compliance_requirements=compliance_requirements
        )
    
    @mcp.prompt()
    def code_simplification_deduplication(code_reference: str, language: Optional[str] = None, focus_area: Optional[str] = None) -> str:
        """Analyzes code for simplification opportunities and identifies duplicate code patterns that can be refactored into reusable components"""
        template = load_template("code_simplification_deduplication")
        return template.render(
            code_reference=code_reference,
            language=language,
            focus_area=focus_area
        )
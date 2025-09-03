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
    
    @mcp.prompt()
    def error_handling_and_logging(code_reference: str, language: Optional[str] = None) -> str:
        """A comprehensive prompt to guide developers in implementing proper error handling and logging mechanisms in their code, including best practices for exception handling, logging levels, structured logging, and monitoring"""
        template = load_template("error_handling_and_logging")
        return template.render(
            code_reference=code_reference,
            language=language
        )
    
    @mcp.prompt()
    def bug_analysis_and_resolution(bug_description: str, code_reference: Optional[str] = None, language: Optional[str] = None, error_logs: Optional[str] = None, steps_to_reproduce: Optional[str] = None, environment_details: Optional[str] = None) -> str:
        """A comprehensive prompt to guide developers in analyzing bugs, understanding root causes, and implementing effective solutions with proper testing and documentation."""
        template = load_template("bug_analysis_and_resolution")
        return template.render(
            bug_description=bug_description,
            code_reference=code_reference,
            language=language,
            error_logs=error_logs,
            steps_to_reproduce=steps_to_reproduce,
            environment_details=environment_details
        )
    
    @mcp.prompt()
    def generate_project_documentation(project_name: str, project_type: str, primary_language: str, project_description: Optional[str] = None, target_audience: Optional[str] = None, include_api_docs: Optional[str] = None, include_architecture: Optional[str] = None, deployment_platforms: Optional[str] = None) -> str:
        """Generate comprehensive project documentation including README, architecture overview, setup instructions, and API documentation. Creates or updates markdown files in the documentation directory."""
        template = load_template("generate_project_documentation")
        return template.render(
            project_name=project_name,
            project_type=project_type,
            primary_language=primary_language,
            project_description=project_description,
            target_audience=target_audience,
            include_api_docs=include_api_docs,
            include_architecture=include_architecture,
            deployment_platforms=deployment_platforms
        )
    
    @mcp.prompt()
    def generate_test_scenarios(code_reference: str, programming_language: str, test_types: Optional[str] = None, business_context: Optional[str] = None) -> str:
        """Generate comprehensive test cases covering scenarios from basic functionality to complex edge cases, organized by difficulty and risk levels"""
        template = load_template("generate_test_scenarios")
        return template.render(
            code_reference=code_reference,
            programming_language=programming_language,
            test_types=test_types,
            business_context=business_context
        )
    
    @mcp.prompt()
    def code_refactoring(code_reference: str, language: Optional[str] = None, refactoring_goals: Optional[str] = None, current_issues: Optional[str] = None) -> str:
        """A comprehensive prompt to guide developers through systematic code refactoring, including structural improvements, design pattern implementation, legacy code modernization, and safety-first refactoring practices"""
        template = load_template("code_refactoring")
        return template.render(
            code_reference=code_reference,
            language=language,
            refactoring_goals=refactoring_goals,
            current_issues=current_issues
        )
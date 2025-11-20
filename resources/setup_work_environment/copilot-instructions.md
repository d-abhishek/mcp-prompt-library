# Company Guidelines for GitHub Copilot

These instructions provide comprehensive guidelines for code generation, commit messages, branch naming, and pull request standards. Follow these guidelines when assisting with development tasks.

## Code Quality & Development Standards

### Code Readability and Consistency
- Use 4 spaces for indentation (never tabs)
- Keep line length between 80-120 characters maximum
- Use proper blank line separation for logical sections
- Follow language-specific naming conventions:
  - Variables/Functions: `snake_case` (Python) or `camelCase` (JavaScript/TypeScript)
  - Classes/Types: `PascalCase`
  - Constants: `ALL_CAPS_WITH_UNDERSCORES`
  - Files/Directories: lowercase with hyphens or underscores
- Organize code logically with related modules grouped together
- Prefer clear, self-explanatory code over clever solutions

### Documentation Standards
- Write comments that explain "why" not "what"
- Include complete docstrings for all public functions, classes, and modules with:
  - Purpose and behavior description
  - Input parameters and types
  - Return values and types
  - Potential exceptions
- Keep external documentation updated alongside code changes
- Write self-documenting code when possible

### Architecture & Design Principles
- Apply Single Responsibility Principle - each function/class has one purpose
- Follow DRY principle - avoid code duplication
- Maintain proper separation of concerns
- Use appropriate design patterns
- Structure code into logical modules/components
- Keep functions and classes focused and cohesive

### Security & Compliance
- Validate and sanitize all external inputs
- Never hardcode credentials or sensitive data
- Follow OWASP and CERT security standards
- Consider regulatory compliance (GDPR, HIPAA) requirements
- Implement proper authentication and authorization
- Use structured error handling without exposing sensitive information
- Protect against SQL injection, XSS, and other common vulnerabilities

### Performance & Efficiency
- Use efficient algorithms and data structures
- Optimize database queries and operations
- Implement appropriate caching strategies
- Manage memory usage efficiently
- Properly allocate and release resources
- Consider performance implications of code changes

### Error Handling & Robustness
- Use native exception mechanisms (try-catch, try-except)
- Provide meaningful error messages without exposing sensitive data
- Handle edge cases and boundary conditions
- Validate all external inputs with appropriate error responses
- Implement graceful degradation for system failures
- Log errors appropriately for debugging

### Testing & Quality Assurance
- Write testable code with clear interfaces
- Include unit, integration, and regression tests
- Focus on meaningful tests, not just coverage metrics
- Test edge cases and error scenarios
- Keep tests clear, focused, and maintainable
- Ensure tests cover business logic and critical paths

## Code Review Focus Areas

When reviewing code, prioritize these areas:

**Severity Levels:**
- **Critical**: Security vulnerabilities, data loss risks, system crashes
- **High**: Performance issues, major design flaws, compliance violations
- **Medium**: Code quality issues, maintainability concerns, minor security issues
- **Low**: Style inconsistencies, documentation gaps, minor optimizations

**Review Checklist:**
- Code readability and consistency
- Architecture and design principles compliance
- Security vulnerabilities and compliance issues
- Performance and efficiency concerns
- Error handling and robustness
- Testing coverage and quality
- Documentation completeness
- Standards and best practices adherence

## Language-Specific Guidelines

Apply these general principles while respecting language-specific idioms and conventions:

- **Python**: Follow PEP 8, use type hints, leverage built-in functions
- **JavaScript/TypeScript**: Use modern ES6+ features, prefer const/let over var
- **Java**: Follow Oracle conventions, use appropriate access modifiers
- **Go**: Follow effective Go guidelines, use gofmt
- **C#**: Follow Microsoft conventions, use proper naming

Remember: These guidelines ensure code quality, maintainability, security, and team collaboration. When generating code or providing suggestions, always consider these standards and explain the reasoning behind recommendations.
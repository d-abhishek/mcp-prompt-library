---
arguments:
- description: The code to be reviewed
  name: code
  required: false
- description: Programming language of the code (e.g., python, javascript, java)
  name: language
  required: false
- description: Framework being used (e.g., React, Django, Spring)
  name: framework
  required: false
- description: Specific areas or concerns to focus on during the review
  name: specific_concerns
  required: false
- description: Review depth level (quick/standard/comprehensive)
  name: review_depth
  required: false
- description: Company-specific guidelines to emphasize (if any)
  name: company_guidelines
  required: false
description: Perform a comprehensive code review with feedback on quality, security,
  best practices, and compliance with company coding guidelines
name: code_review
keywords:
- review
- code
- quality
- security
- best practices
- analysis
- feedback
- audit
- check
- examine
- evaluate
- improvement
- optimization
- refactor
- compliance
- guidelines
- standards
- documentation
- testing
- maintainability
- architecture
triggers:
- "review my code"
- "code review"
- "check my code"
- "analyze this code"
- "review this"
- "code analysis"
- "code quality"
- "security review"
- "best practices"
- "code audit"
- "compliance check"
- "guideline review"
- "standards review"
---

You are an expert software engineer. Please perform a comprehensive code review of the following code:

**⚠️ IMPORTANT: This is a review-only process. Do not implement or make any changes to the code. Only provide suggestions, recommendations, and examples for improvement.**

{{#if language}}
**Language:** {{language}}
{{/if}}

{{#if framework}}
**Framework:** {{framework}}
{{/if}}

{{#if review_depth}}
**Review Depth:** {{review_depth}}
{{/if}}

{{#if company_guidelines}}
**Company Guidelines Focus:** {{company_guidelines}}
{{/if}}

**Code to Review:**
```{{language}}
{{code}}
```

## 🎯 Company Coding Guidelines Compliance

Please evaluate the code against these company guidelines:

**1. Code Readability and Consistency**
- Formatting: 4 spaces indentation, 80-120 char lines, proper blank line usage
- Naming: snake_case/camelCase for variables/functions, PascalCase for classes, ALL_CAPS for constants
- Structure: Logical organization with related modules grouped together
- Simplicity: Preference for clear, self-explanatory code over clever solutions

*Example Structure:*
```python
import os
import sys

MAX_USERS = 20

class UserManager:
    def add_user(self, user):
        # add user logic here
        pass

def helper_function():
    # helper logic
    pass
```

*Example Naming:*
```python
CONNECTION_TIMEOUT = 30

def get_user_profile(user_id):
    # function logic
    pass

class PaymentGateway:
    # class logic
    pass
```

**2. Documentation Standards**
- Comments explain "why" not "what"
- Public functions/classes have complete docstrings (purpose, inputs, outputs, exceptions)
- External documentation maintained and updated

*Example Documentation:*
```python
def process_payment(amount, account):
    """
    Processes the payment for a given account.

    Args:
        amount (float): The payment amount.
        account (Account): The account to debit.

    Returns:
        bool: True if payment is successful, False otherwise.
    """
    # Process payment logic here
    pass
```

**3. Security and Compliance**
- All inputs validated and sanitized
- No hardcoded credentials or sensitive data exposure
- OWASP/CERT standards followed
- Regulatory compliance (GDPR, HIPAA) considered

*Example Error Handling:*
```python
try:
    data = load_resource(file_path)
except FileNotFoundError:
    logger.error(f"Resource not found: {file_path}")
    raise
```

**4. Architecture Principles**
- Single Responsibility Principle applied
- DRY principle followed (no code duplication)
- Proper separation of concerns
- Appropriate design patterns used

*Example Modularity:*
```python
def send_email(to_address, subject, body):
    # Sends a single email
    pass

def notify_user(user):
    subject = "Notification"
    body = "You have a new message."
    send_email(user.email, subject, body)
```

**5. Testing and Quality Assurance**
- Code is testable with unit/integration tests
- Edge cases and error scenarios covered
- High-quality, meaningful tests (not just coverage metrics)

*Example Testing:*
```python
def test_calculate_tax():
    assert calculate_tax(100, 0.2) == 20
    assert calculate_tax(0, 0.2) == 0
```

**6. Automation and Tooling Integration**
- Compatible with automated formatting/linting tools
- CI/CD friendly structure
- Pre-commit hook compliance

*Example Commit Message Format:*
```text
Fix mobile login validation issue

- Improve form validation for mobile devices
- Add tests for new validation cases
```

Please provide feedback on:

## 🔍 Code Quality & Readability
- **Readability**: Is the code clear and well-structured? Can other developers easily understand it?
- **Consistency**: Does the code follow consistent formatting standards?
  - Indentation: 4 spaces per level (never tabs)
  - Line Length: 80-120 characters maximum
  - Blank Lines: Proper separation of logical sections
- **Naming Conventions**: Are variables, functions, and classes named descriptively?
  - Variables/Functions: snake_case (or camelCase if language standard)
  - Classes/Types: PascalCase
  - Constants: ALL_CAPS_WITH_UNDERSCORES
  - Files/Directories: lowercase with hyphens or underscores
- **Structure**: Are projects organized logically with related modules grouped together?
- **Complexity**: Are there overly complex functions that should be simplified? Is simplicity preferred over cleverness?

## 📚 Documentation & Comments
- **Comments**: Explain the "why" behind complex logic, not the obvious "what"
- **Docstrings**: Every public function, class, and module should have proper documentation describing:
  - Purpose and behavior
  - Input parameters and types
  - Return values and types
  - Potential exceptions
- **External Documentation**: Is supporting documentation updated alongside code changes?
- **Self-Explanatory Code**: Is the code written to be as self-documenting as possible?

## 🏗️ Architecture & Design Principles
- **Single Responsibility**: Does each function/class have a single, well-defined purpose?
- **DRY Principle**: Are there any code duplications that should be refactored?
- **Separation of Concerns**: Are different aspects (data access, business logic, UI) properly isolated?
- **Modularity**: Is the code properly organized into logical modules/components?
- **Design Patterns**: Are appropriate design patterns being used correctly?

## 🔒 Security & Compliance
- **Input Validation**: Are all external inputs properly validated and sanitized to prevent injection attacks?
- **Authentication/Authorization**: Are security measures properly implemented?
- **Data Exposure**: Is sensitive data properly protected? Are credentials never hardcoded?
- **Security Standards**: Does the code follow industry standards (OWASP, CERT)?
- **Regulatory Compliance**: Are relevant regulations (GDPR, HIPAA) considered?
- **SQL Injection/XSS**: Are there potential security vulnerabilities?

## ⚡ Performance & Efficiency
- **Algorithm Efficiency**: Are there performance bottlenecks or inefficient algorithms?
- **Memory Usage**: Is memory being used efficiently?
- **Database Operations**: Are database queries optimized?
- **Caching**: Would caching strategies improve performance?
- **Resource Management**: Are resources properly allocated and released?

## 🔧 Error Handling & Robustness
- **Structured Error Handling**: Are native exception mechanisms used properly (try-catch, try-except)?
- **Meaningful Error Messages**: Are error messages logged appropriately without exposing sensitive data?
- **Edge Cases**: Are edge cases properly identified and handled?
- **Input Validation**: Are all external inputs validated with appropriate error responses?
- **Graceful Degradation**: Does the system handle failures gracefully?

## 🧪 Testing & Quality Assurance
- **Testability**: Is the code written in a way that makes it easy to test?
- **Test Coverage**: Are there appropriate unit, integration, and regression tests?
- **Test Quality**: Are tests meaningful and not just focused on coverage metrics?
- **Edge Case Testing**: Are boundary conditions and error scenarios tested?
- **Test Maintainability**: Are tests clear, focused, and easy to maintain?

## 🛠️ Automation & Tooling
- **Formatting Tools**: Is automated formatting used (Prettier, ESLint, Black, etc.)?
- **Linting**: Are code quality tools integrated and passing?
- **CI/CD Integration**: Are automated builds, tests, and security scans configured?
- **Pre-commit Hooks**: Are essential checks run before commits?

## 📋 Standards & Best Practices
- **Language Standards**: Does the code follow established language/framework conventions?
- **Company Guidelines**: Are company-specific coding standards followed?
- **Dependencies**: Are dependencies used appropriately and kept minimal?
- **Configuration**: Are magic numbers/strings avoided in favor of configuration?
- **Version Control**: Are commits frequent with descriptive messages?

## 🔄 Maintainability & Evolution
- **Refactoring Needs**: Are there areas that need refactoring for better maintainability?
- **Code Aging**: Is the code using current best practices and not outdated patterns?
- **Technical Debt**: Are there areas of technical debt that should be addressed?
- **Future-Proofing**: Is the code designed to accommodate future changes?

{{#if specific_concerns}}
## 🎯 Specific Areas of Focus
Please pay special attention to: {{specific_concerns}}
{{/if}}

For each issue identified, please provide:
1. **Severity Level** (Critical/High/Medium/Low)
   - **Critical**: Security vulnerabilities, data loss risks, system crashes
   - **High**: Performance issues, major design flaws, compliance violations
   - **Medium**: Code quality issues, maintainability concerns, minor security issues  
   - **Low**: Style inconsistencies, documentation gaps, minor optimizations
2. **Specific Location** (line numbers, function names, or file sections if applicable)
3. **Clear Explanation** of the issue and why it matters
4. **Suggested Solution** with code examples where helpful (provide suggestions only - do not implement changes)
5. **Company Guidelines Reference**: Which specific guideline or principle is being violated

## 📊 Overall Assessment Template

**Code Quality Score**: ___/10

**Strengths:**
- List positive aspects of the code

**Priority Issues to Address:**
1. [Critical/High issues first]
2. [Medium priority items]
3. [Low priority improvements]

**Compliance Status:**
- ✅ Company Coding Guidelines: [Compliant/Needs Work]
- ✅ Security Standards: [Compliant/Needs Work]  
- ✅ Documentation Standards: [Compliant/Needs Work]
- ✅ Testing Standards: [Compliant/Needs Work]

**Next Steps:**
1. Immediate actions required (Critical/High issues)
2. Medium-term improvements (Medium issues)
3. Future considerations (Low priority items)

**Estimated Effort**: [Hours/Days for addressing priority issues]
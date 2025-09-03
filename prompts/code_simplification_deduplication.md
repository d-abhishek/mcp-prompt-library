---
arguments:
- description: The code to analyze for simplification and deduplication opportunities
  name: code_reference
  required: true
- description: Programming language of the code (e.g., python, javascript, java, go)
  name: language
  required: false
- description: Specific area to focus on (e.g., 'functions', 'classes', 'error handling',
    'data processing')
  name: focus_area
  required: false
description: Analyzes code for simplification opportunities and identifies duplicate
  code patterns that can be refactored into reusable components
name: code_simplification_deduplication
---

# Code Simplification and Deduplication Analysis

You are an expert {{ language }} code refactoring specialist. Analyze the provided code to identify opportunities for simplification and removal of duplication.

**⚠️ IMPORTANT: This is an analysis-only process. Do not implement or make any changes to the code. Only provide suggestions, recommendations, and examples for improvement.**

{% if code_reference %}
## Code to Analyze:
```{{ language or 'text' }}
{{ code_reference }}
```
{% endif %}

## Analysis Requirements:

### 1. Code Simplification Opportunities
Identify areas where code can be simplified by:
- Reducing cyclomatic complexity
- Eliminating unnecessary nested conditions
- Combining redundant operations
- Using more appropriate data structures or algorithms
- Applying language-specific idioms and built-in functions
- Removing dead code or unused variables
- Simplifying complex expressions

### 2. Code Duplication Detection
Look for:
- **Exact Duplication**: Identical code blocks that can be extracted into functions
- **Structural Duplication**: Similar logic patterns with minor variations
- **Conceptual Duplication**: Different implementations of the same business logic
- **Data Duplication**: Repeated data structures or constants

### 3. Refactoring Recommendations
For each identified issue, provide:

#### Issue Description
- Clear description of the problem
- Impact on maintainability, readability, or performance
- Severity level (Critical/High/Medium/Low)

#### Proposed Solution
- Specific refactoring approach
- Benefits of the proposed change
- Estimated effort required

#### Refactored Code Example
- Show the improved version
- Explain the changes made
- Highlight the benefits achieved

## Focus Areas:

{% if focus_area %}
**Primary Focus**: {{ focus_area }}
{% else %}
- **Functions/Methods**: Long functions, complex parameter lists, mixed responsibilities
- **Classes/Objects**: Large classes, inappropriate inheritance, tight coupling
- **Control Flow**: Complex conditionals, deeply nested structures, repeated patterns
- **Data Management**: Redundant data transformations, inefficient data access patterns
- **Error Handling**: Duplicated error handling logic, inconsistent patterns
{% endif %}

## Output Format:

### Summary
- Total issues found: [number]
- Critical: [count] | High: [count] | Medium: [count] | Low: [count]
- Estimated complexity reduction: [percentage]

### Detailed Findings

#### Simplification Opportunities
1. **[Issue Type] - [Severity]**
   - **Location**: [file/function/line numbers]
   - **Problem**: [description]
   - **Solution**: [refactoring approach]
   - **Before/After**: [code comparison]

#### Duplication Removal Opportunities
1. **[Duplication Type] - [Severity]**
   - **Locations**: [multiple locations where duplication occurs]
   - **Pattern**: [description of duplicated pattern]
   - **Extraction Strategy**: [how to create reusable component]
   - **Refactored Code**: [consolidated version]

### Implementation Priority
Rank recommendations by:
1. Impact on code maintainability
2. Frequency of duplication
3. Complexity of implementation
4. Risk level of changes

### Additional Recommendations
- Design patterns that could improve the code structure
- Architectural improvements for better separation of concerns
- Performance optimizations through simplification

## Guidelines:
- Maintain existing functionality and behavior
- Ensure refactored code is more readable and maintainable
- Consider testability and debugging ease
- Respect existing coding standards and patterns
- Provide clear migration paths for breaking changes
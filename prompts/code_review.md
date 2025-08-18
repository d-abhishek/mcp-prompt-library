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
description: Perform a comprehensive code review with feedback on quality, security,
  and best practices
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
---

Please perform a comprehensive code review of the following code:

{{#if language}}
**Language:** {{language}}
{{/if}}

{{#if framework}}
**Framework:** {{framework}}
{{/if}}

**Code to Review:**
```{{language}}
{{code}}
```

Please provide feedback on:

## 🔍 Code Quality
- **Readability**: Is the code clear and well-structured?
- **Naming**: Are variables, functions, and classes named descriptively?
- **Comments**: Is the code appropriately documented?
- **Complexity**: Are there overly complex functions that should be simplified?

## 🏗️ Architecture & Design
- **Single Responsibility**: Does each function/class have a single, well-defined purpose?
- **DRY Principle**: Are there any code duplications that should be refactored?
- **Modularity**: Is the code properly organized into logical modules/components?
- **Design Patterns**: Are appropriate design patterns being used?

## 🔒 Security
- **Input Validation**: Are all inputs properly validated and sanitized?
- **Authentication/Authorization**: Are security measures properly implemented?
- **Data Exposure**: Is sensitive data properly protected?
- **SQL Injection/XSS**: Are there potential security vulnerabilities?

## ⚡ Performance
- **Efficiency**: Are there performance bottlenecks or inefficient algorithms?
- **Memory Usage**: Is memory being used efficiently?
- **Database Queries**: Are database operations optimized?
- **Caching**: Would caching improve performance?

## 🧪 Testing
- **Testability**: Is the code written in a way that makes it easy to test?
- **Edge Cases**: Are edge cases properly handled?
- **Error Handling**: Is error handling comprehensive and appropriate?

## 📋 Best Practices
- **Code Standards**: Does the code follow language/framework conventions?
- **Dependencies**: Are dependencies used appropriately and kept minimal?
- **Configuration**: Are magic numbers/strings avoided in favor of configuration?

{{#if specific_concerns}}
## 🎯 Specific Areas of Focus
Please pay special attention to: {{specific_concerns}}
{{/if}}

For each issue identified, please provide:
1. **Severity Level** (Critical/High/Medium/Low)
2. **Specific Location** (line numbers if applicable)
3. **Clear Explanation** of the issue
4. **Suggested Solution** with code examples where helpful

End with an overall assessment and priority recommendations for improvement.
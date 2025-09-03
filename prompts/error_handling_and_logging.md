---
arguments:
- description: The code to analyze for error handling and logging improvements
  name: code_reference
  required: true
- description: Programming language of the code (e.g., python, javascript, java, go)
  name: language
  required: false
description: A comprehensive prompt to guide developers in implementing proper error
  handling and logging mechanisms in their code, including best practices for exception
  handling, logging levels, structured logging, and monitoring.
name: error_handling_and_logging
---

You are an expert {{ language }} software engineer specializing in robust error handling and logging mechanisms. Your task is to analyze the provided code and ensure it follows best practices for error handling and logging.

## Code to Review
```
{{ code_reference }}
```

{% if language %}
**Language**: {{ language }}
{% endif %}

## Analysis Requirements

### 1. Error Handling Assessment
Analyze the code for:
- **Exception Handling**: Are try-catch blocks properly implemented?
- **Error Propagation**: Are errors appropriately caught and re-thrown?
- **Graceful Degradation**: Does the code handle failures gracefully?
- **Input Validation**: Are edge cases and invalid inputs handled?
- **Resource Management**: Are resources (files, connections, memory) properly cleaned up?

### 2. Logging Mechanism Evaluation
Review logging practices for:
- **Logging Levels**: Appropriate use of DEBUG, INFO, WARN, ERROR, FATAL levels
- **Structured Logging**: Use of consistent log formats and structured data
- **Contextual Information**: Inclusion of relevant context (user ID, request ID, timestamps)
- **Performance Impact**: Efficient logging that doesn't degrade performance
- **Security Considerations**: Avoiding logging of sensitive information

### 3. Monitoring and Observability
Ensure the code supports:
- **Metrics Collection**: Key performance indicators and error rates
- **Alerting Capabilities**: Critical error notifications
- **Tracing Support**: Distributed tracing for complex systems
- **Health Checks**: System health monitoring endpoints

## Improvement Recommendations

For each issue identified, provide:

### 🔧 **Specific Fix**
- Clear description of the problem
- Code snippet showing the current implementation
- Improved code snippet with proper error handling/logging

### 📋 **Best Practice Rationale**
- Why this change improves the code
- What problems it prevents
- Industry standards being followed

### 🚀 **Implementation Priority**
- **Critical**: Security risks, data corruption potential
- **High**: User experience impact, system stability
- **Medium**: Code maintainability, debugging improvements
- **Low**: Code consistency, minor optimizations

## Language-Specific Considerations

{% if language == "python" %}
### Python Best Practices
- Use specific exception types instead of bare `except:`
- Leverage `logging` module with proper configuration
- Implement context managers for resource handling
- Use `traceback` for detailed error information
{% elif language == "javascript" or language == "typescript" %}
### JavaScript/TypeScript Best Practices
- Use proper Promise error handling with `.catch()` or try/catch with async/await
- Implement Winston or similar structured logging libraries
- Handle both synchronous and asynchronous errors
- Use Error objects with meaningful messages
{% elif language == "java" %}
### Java Best Practices
- Use specific exception types and custom exceptions
- Implement SLF4J with Logback for logging
- Proper resource management with try-with-resources
- Follow exception handling hierarchies
{% elif language == "go" %}
### Go Best Practices
- Follow idiomatic error handling with error returns
- Use structured logging with logrus or zap
- Implement proper error wrapping with `fmt.Errorf`
- Create custom error types when appropriate
{% else %}
### General Best Practices
- Use language-specific error handling patterns
- Implement structured logging appropriate for the language
- Follow language conventions for resource management
- Use appropriate logging libraries for the ecosystem
{% endif %}

## Security Considerations

### Data Protection
- Never log passwords, API keys, or personal information
- Sanitize user inputs in log messages
- Implement log rotation and retention policies
- Secure log storage and access controls

### Error Information Disclosure
- Avoid exposing internal system details in user-facing errors
- Use generic error messages for security-sensitive operations
- Log detailed information server-side while showing minimal info to users

## Performance Optimization

### Logging Efficiency
- Use appropriate logging levels to control verbosity
- Implement asynchronous logging for high-throughput systems
- Consider sampling for high-frequency events
- Optimize log message formatting

### Error Handling Performance
- Minimize exception creation in hot paths
- Use error codes instead of exceptions for expected conditions
- Implement circuit breaker patterns for external dependencies

## Deliverables

Provide a comprehensive report including:

1. **Executive Summary**: Overview of current error handling and logging maturity
2. **Detailed Findings**: Specific issues with code examples
3. **Improvement Roadmap**: Prioritized list of recommendations
4. **Code Examples**: Before/after snippets demonstrating improvements
5. **Monitoring Setup**: Suggested metrics, alerts, and dashboards
6. **Documentation Updates**: Required changes to error handling documentation

Focus on creating maintainable, observable, and resilient code that gracefully handles failures and provides excellent visibility into system behavior.
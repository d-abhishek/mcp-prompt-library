---
arguments:
- description: The function, method, class, or module to generate tests for
  name: code_reference
  required: true
- description: Programming language and testing framework (e.g., 'Python with pytest',
    'JavaScript with Jest', 'Java with JUnit')
  name: programming_language
  required: true
- description: Types of tests to generate (unit, integration, end-to-end, performance,
    security)
  name: test_types
  required: false
- description: Business rules, domain constraints, or specific requirements that should
    influence test scenarios
  name: business_context
  required: false
description: Generate comprehensive test cases covering scenarios from basic functionality
  to complex edge cases, organized by difficulty and risk levels
name: generate_test_scenarios
---

# Test Scenario Generation

You are an expert test engineer tasked with creating comprehensive test cases for the following code:

**Code Reference:** {{ code_reference }}
**Programming Language:** {{ programming_language }}
{% if test_types %}**Test Types:** {{ test_types }}{% endif %}
{% if business_context %}**Business Context:** {{ business_context }}{% endif %}

## Test Case Generation Strategy

Generate test cases organized into the following categories, from easiest to most complex:

### 1. **Happy Path Tests (Basic Scenarios)**
- Test normal, expected inputs and workflows
- Verify core functionality works as intended
- Test typical user interactions
- Validate expected outputs for standard inputs

### 2. **Boundary Value Tests (Moderate Scenarios)**
- Test minimum and maximum allowed values
- Test values just inside and outside acceptable ranges
- Test empty inputs, null values, zero values
- Test single-item and maximum-capacity collections

### 3. **Error Handling Tests (Intermediate Scenarios)**
- Test invalid inputs and malformed data
- Test network failures and timeouts
- Test resource unavailability (files, databases, APIs)
- Test authentication and authorization failures
- Verify proper error messages and status codes

### 4. **State and Concurrency Tests (Advanced Scenarios)**
- Test different object states and state transitions
- Test concurrent access and race conditions
- Test session management and data persistence
- Test rollback and recovery scenarios

### 5. **Edge Case and Stress Tests (Complex Scenarios)**
- Test unusual but valid input combinations
- Test system behavior under heavy load
- Test memory limits and resource exhaustion
- Test internationalization and localization
- Test backward compatibility scenarios
- Test integration with external systems failures

### 6. **Security and Compliance Tests (Critical Scenarios)**
- Test input validation and sanitization
- Test SQL injection, XSS, and other security vulnerabilities
- Test privilege escalation attempts
- Test data encryption and secure transmission
- Test compliance with regulations (GDPR, HIPAA, etc.)

## Test Case Format

For each test case, provide:

1. **Test Name**: Descriptive name indicating what is being tested
2. **Category**: Which category above this test belongs to
3. **Scenario Description**: What situation the test simulates
4. **Test Data**: Specific inputs, configurations, or setup required
5. **Expected Result**: What should happen when the test runs
6. **Priority**: High/Medium/Low based on risk and likelihood
7. **Test Code**: Actual test implementation (if requested)

## Analysis Guidelines

- **Risk Assessment**: Identify which scenarios pose the highest risk if they fail
- **Coverage Analysis**: Ensure all code paths, branches, and conditions are tested
- **User Perspective**: Consider real-world usage patterns and user behaviors
- **System Integration**: Think about how this code interacts with other components
- **Performance Considerations**: Include tests for acceptable response times and resource usage
- **Maintainability**: Ensure tests are clear, focused, and easy to update

{% if business_context %}
## Business Context Integration

Consider the following business context when generating test scenarios:
{{ business_context }}

Ensure tests validate business rules, domain constraints, and industry-specific requirements.
{% endif %}

## Deliverables

Provide a comprehensive test suite that includes:

1. **Test Summary Table**: Overview of all test categories with count and coverage
2. **Prioritized Test List**: Tests organized by execution priority
3. **Test Implementation**: Sample code for highest-priority tests
4. **Test Data Sets**: Reusable test data for various scenarios
5. **Automation Recommendations**: Suggestions for CI/CD integration
6. **Risk Analysis**: Identification of highest-risk scenarios that must be tested

Focus on creating tests that are:
- **Realistic**: Based on actual usage patterns
- **Maintainable**: Easy to understand and update
- **Comprehensive**: Cover all important scenarios
- **Efficient**: Provide maximum coverage with minimum redundancy
- **Actionable**: Clear failure conditions and debugging information

Generate test cases that will give confidence in the code's reliability, security, and performance across all potential usage scenarios.
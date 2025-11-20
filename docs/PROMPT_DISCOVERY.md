# Smart Prompt Discovery

This document explains how the MCP Prompt Library implements smart prompt discovery using natural language queries.

## Overview

Instead of requiring users to know exact prompt names, the library provides intelligent search and discovery through the `list_prompts` tool with optional query parameter.

## Features

### 1. Enhanced Prompt Metadata

Prompts include searchable metadata in YAML frontmatter:

```yaml
---
name: create_api
description: Assists developers in creating a FastAPI-based API following best practices
keywords:
  - api
  - fastapi
  - rest
  - crud
  - endpoints
  - create
  - build
  - backend
triggers:
  - "create api"
  - "build api"
  - "api for storing"
  - "student information"
arguments:
  - name: api_purpose
    description: What the API is for
    required: true
---
```

**Metadata Fields:**
- **keywords**: Individual search terms that match user queries
- **triggers**: Specific phrases that strongly indicate this prompt
- **description**: Detailed explanation used for semantic matching
- **arguments**: Parameter definitions for the prompt

### 2. Smart Search with `list_prompts`

The `list_prompts` tool serves dual purposes:

**Without query** (List all prompts):
```python
list_prompts()
```
Returns all available prompts with their descriptions and arguments.

**With query** (Smart search):
```python
list_prompts(query="create api for student management")
```
Analyzes the query and returns ranked results with relevance scores.

### Scoring Algorithm

The search uses a weighted scoring system:

- **Exact trigger phrase match**: 15 points
- **Keyword match**: 8 points each
- **Name word match**: 10 points each  
- **Description word match**: 5 points each
- **Content word match**: 2 points each (if content included)

**Example Search Result:**
```
🎯 Search results for: 'create api for student information'

Best match: create_api (score: 42)
Description: Assists developers in creating a FastAPI-based API...

Required arguments:
- api_purpose: What the API is for
- expected_parameters: Optional description of expected parameters/fields

Usage: Call the prompt create_api with the appropriate arguments.

Other matches (2 found):
- code_review (score: 8)
- generate_project_documentation (score: 6)
```

## Usage Patterns

### Discovery Workflow

**Step 1: Explore Available Prompts**
```python
# List all prompts
all_prompts = list_prompts()
```

**Step 2: Search for Specific Tasks**
```python
# Find prompts for API development
api_prompts = list_prompts(query="create rest api backend")

# Find prompts for security
security_prompts = list_prompts(query="security vulnerabilities OWASP")

# Find prompts for testing
test_prompts = list_prompts(query="generate test cases")
```

**Step 3: Call the Recommended Prompt**
```python
# Based on search results, call the appropriate prompt
result = call_prompt("create_api", {
    "api_purpose": "student management",
    "expected_parameters": "name, email, class, enrollment_date"
})
```

## Creating Discoverable Prompts

### Step 1: Add Rich Metadata

Include comprehensive keywords and triggers in your prompt frontmatter:

```yaml
---
name: generate_dockerfile
description: Generate optimized Dockerfiles for various applications
keywords:
  - docker
  - dockerfile
  - container
  - image
  - deployment
  - build
  - containerize
triggers:
  - "create dockerfile"
  - "generate dockerfile"
  - "containerize application"
  - "docker image"
arguments:
  - name: language
    description: Programming language
    required: true
  - name: framework
    description: Framework name if applicable
    required: false
---
```

### Step 2: Choose Effective Keywords

**Good Keywords:**
- Technical terms: `api`, `rest`, `crud`, `docker`
- Action words: `create`, `build`, `generate`, `review`
- Domain terms: `security`, `performance`, `testing`
- Synonyms: `analyse`/`analyze`, `optimize`/`optimise`

**Avoid:**
- Overly generic terms: `code`, `help`, `work`
- Stop words: `the`, `and`, `or`, `but`

### Step 3: Write Clear Triggers

**Good Triggers:**
- Complete user phrases: "create api", "review code for security"
- Domain-specific requests: "student information", "user management"
- Task descriptions: "generate test cases", "analyze performance"

**Pattern Examples:**
```yaml
triggers:
  - "create [type]"      # create api, create dockerfile
  - "[action] for [purpose]"  # api for student management
  - "[domain] [task]"    # security analysis, performance review
```

## Search Query Best Practices

### Be Specific

❌ **Too vague:**
```python
list_prompts(query="code")
```

✅ **Specific and descriptive:**
```python
list_prompts(query="create rest api with database operations")
list_prompts(query="review python code for security vulnerabilities")
```

### Include Domain Terms

```python
# API development
list_prompts(query="fastapi backend crud endpoints")

# Security
list_prompts(query="OWASP security analysis")

# Performance
list_prompts(query="optimize slow code bottlenecks")

# Testing
list_prompts(query="unit test generation")
```

### Use Natural Language

The system understands natural queries:
```python
list_prompts(query="I need to create an API for managing products")
list_prompts(query="help me find performance problems in my code")
list_prompts(query="generate documentation for my project")
```

## Example Search Scenarios

### Scenario 1: API Development

**Query:** `"create api for product catalog"`

**Expected Results:**
1. `create_api` (high score) - Main API creation prompt
2. `generate_project_documentation` (medium score) - For API docs

### Scenario 2: Code Quality

**Query:** `"review code for best practices and security"`

**Expected Results:**
1. `code_review` (high score) - General code review
2. `security_vulnerability_analysis` (high score) - Security focus
3. `code_correctness_review` (medium score) - Correctness check

### Scenario 3: Performance

**Query:** `"find slow code and optimization opportunities"`

**Expected Results:**
1. `performance_bottleneck_analysis` (high score) - Performance focus
2. `code_refactoring` (medium score) - Refactoring suggestions

### Scenario 4: Testing

**Query:** `"generate test cases for authentication module"`

**Expected Results:**
1. `generate_test_scenarios` (high score) - Test generation
2. `bug_analysis_and_resolution` (low score) - Related testing

## Integration Examples

### In VS Code with MCP Extension

```typescript
// Search for prompts
const results = await mcp.callTool("list_prompts", {
  query: "create rest api"
});

// Call the recommended prompt
const apiCode = await mcp.callPrompt(results.best_match.name, {
  api_purpose: "user management",
  expected_parameters: "name, email, password"
});
```

### In Claude Desktop

Simply ask:
- "Search for prompts about creating APIs"
- "Find prompts for code review"
- "What prompts help with security analysis?"

The MCP server will use `list_prompts` to find relevant matches.

## Troubleshooting

### Low Match Scores

**Problem:** Search returns results with low scores (< 10)

**Solutions:**
1. Add more keywords to the prompt
2. Include common trigger phrases
3. Improve description text
4. Use more specific search terms

### No Results Found

**Problem:** Query returns "No prompts found"

**Solutions:**
1. Verify prompts have metadata (keywords, triggers)
2. Try broader search terms
3. List all prompts to see what's available
4. Check prompt file format and frontmatter

### Wrong Prompt Suggested

**Problem:** Search suggests unrelated prompt

**Solutions:**
1. Be more specific in query
2. Review prompt keywords for conflicts
3. Adjust trigger phrases to be more precise
4. Use negative keywords if needed (future feature)

## Best Practices Summary

1. **Add comprehensive metadata** to all prompts
2. **Use natural language** queries for better matches
3. **Be specific** in search terms when possible
4. **Include synonyms** in keywords
5. **Test queries** with various phrasings
6. **Review scores** to understand matching quality
7. **Iterate on metadata** based on search results
8. **Document patterns** that work well for your team

## Related Documentation

- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Practical usage examples
- [TOOLS_DOCUMENTATION.md](TOOLS_DOCUMENTATION.md) - Complete tool reference
- [README.md](../README.md) - Project overview
- [ACCESS_CONTROL.md](ACCESS_CONTROL.md) - Permission configuration

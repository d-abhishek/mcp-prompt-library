# Usage Examples for Smart Prompt Discovery

## Quick Examples

Here are some example queries you can try with your enhanced MCP prompt library:

### API Creation Examples

**Query:** "create api for storing student information. The parameters should be name, class, contact, address"
- **Tool:** `smart_prompt_executor` with `auto_execute=True`
- **Result:** Automatically generates a complete FastAPI application for student management

**Query:** "I need to build a REST API for user management"
- **Tool:** `list_prompts` with query
- **Result:** Returns ranked search results with `create_api` as the top match

**Query:** "generate backend service for product catalog"
- **Tool:** `list_prompts(query="generate backend service for product catalog")`
- **Result:** Shows scored matches with `create_api` recommended for the task

### Code Review Examples

**Query:** "review my code for security issues"
- **Tool:** `list_prompts(query="review my code for security issues")`
- **Result:** Returns `code_review` prompt as the best match with security focus

**Query:** "check this Python code for best practices"
- **Tool:** `smart_prompt_executor` with extracted language parameter
- **Result:** Sets up code review with Python-specific guidelines

**Query:** "analyze my React component for optimization"
- **Tool:** `list_prompts(query="analyze my React component for optimization")` 
- **Result:** Recommends `code_review` with React framework context

### Code Correctness Review Examples

**Query:** "check if my function works correctly"
- **Tool:** `list_prompts(query="check if my function works correctly")`
- **Result:** Returns `code_correctness_review` as the top match for functional verification

**Query:** "verify this Python code meets the requirements"
- **Tool:** `smart_prompt_executor` with code and requirements
- **Result:** Automatically runs correctness review with Python expertise

**Query:** "test this JavaScript function for bugs and edge cases"
- **Tool:** `code_correctness_review` with language="javascript"
- **Result:** Specialized JavaScript correctness analysis with bug detection

**Query:** "review calculateTotal() function in utils.py"
- **Tool:** `code_correctness_review` with code_reference="calculateTotal()"
- **Result:** Targeted analysis of specific function for correctness issues

### General Discovery

**Query:** "what can you help me with?"
- **Tool:** `list_prompts`
- **Result:** Shows all available prompts with descriptions

**Query:** "something related to testing"
- **Tool:** `suggest_prompt`
- **Result:** Would suggest test-related prompts if any exist

## Test Commands

You can test these with your MCP client:

```json
// Test smart search
{
  "method": "tools/call",
  "params": {
    "name": "list_prompts",
    "arguments": {
      "query": "create api for storing student information"
    }
  }
}

// Test auto-execution
{
  "method": "tools/call", 
  "params": {
    "name": "smart_prompt_executor",
    "arguments": {
      "query": "create api for storing student information. The parameters should be name, class, contact, address",
      "auto_execute": true
    }
  }
}
```

## Tips for Users

1. **Be specific**: The more details you provide, the better the parameter extraction
2. **Use natural language**: Don't worry about exact syntax, describe what you want
3. **Include context**: Mention the domain, technology, or specific requirements
4. **Try variations**: If one phrasing doesn't work, try rephrasing your request

## For Developers: Adding New Prompts

To make your prompts discoverable:

1. **Add keywords** that users might search for
2. **Include trigger phrases** that should strongly indicate your prompt
3. **Write clear descriptions** that explain the prompt's purpose
4. **Test with various phrasings** to ensure good coverage

Example prompt structure:
```yaml
---
name: my_awesome_prompt
description: Does something really useful
keywords:
  - useful
  - awesome
  - helpful
  - specific_domain
triggers:
  - "do something useful"
  - "help me with X"
  - "create something awesome"
arguments:
  - name: main_param
    description: What this parameter does
    required: true
---
```

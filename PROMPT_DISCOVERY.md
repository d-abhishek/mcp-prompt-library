# MCP Prompt Discovery & Auto-Execution

This document explains how to make your MCP prompts automatically discoverable and executable based on natural language queries.

## Problem Statement

By default, MCP servers require users to explicitly call prompt functions by name. This means users need to know:
1. The exact prompt name
2. The required parameters
3. When to use which prompt

This creates a poor user experience where users might not discover or use your custom prompts.

## Solution Overview

We've implemented two complementary solutions:

### 1. Enhanced Prompt Metadata
Added `keywords` and `triggers` to prompt frontmatter for better discoverability.

### 2. Enhanced List Prompts (`list_prompts`)
A unified tool that can both list all prompts and provide smart suggestions based on queries.

### 3. Automatic Execution (`smart_prompt_executor`)
A tool that can automatically execute the best matching prompt with extracted parameters.

## How It Works

### Enhanced Prompt Metadata

Your prompts now support additional metadata fields:

```yaml
---
name: create_api
description: Creates FastAPI applications with best practices
keywords:
  - api
  - fastapi
  - rest
  - crud
  - create
  - build
  - generate
triggers:
  - "create api"
  - "build api"
  - "api for storing"
  - "student information"
---
```

- **keywords**: Individual words that match user queries
- **triggers**: Specific phrases that strongly indicate this prompt should be used

### Enhanced List Prompts

The `list_prompts` tool now serves dual purposes:

**Without query** (traditional listing):
```
list_prompts(include_content=False)
```
Shows all available prompts in a numbered list.

**With query** (smart search):
```
list_prompts(query="create api for student information")
```
Analyzes the query using the same scoring algorithm and returns ranked results.

**Scoring Factors:**
- Exact trigger phrase matches (15 points)
- Keyword matches (8 points each)
- Name matches (10 points each)
- Description word matches (5 points each)
- Content matches (2 points each)

**Example output with query:**
```
🎯 Search results for: 'create api for student information'

Best match: create_api (score: 42)
Description: Assists developers in creating a FastAPI-based API...

Required arguments:
- api_purpose: What the API is for

Usage: Call the prompt create_api with the appropriate arguments.

Other matches (1 found):
- code_review (score: 8): Perform a comprehensive code review...
```

### Automatic Execution

The `smart_prompt_executor` tool goes one step further by:
1. Analyzing the query to suggest the best prompt
2. Extracting parameters from the natural language query
3. Automatically executing the prompt with those parameters

**Usage:**
```
Tool: smart_prompt_executor(
  query="create api for storing student information. The parameters should be name, class, contact, address",
  auto_execute=true
)
```

**Parameter Extraction Logic:**
- **API Purpose**: Extracted from phrases like "api for X" or detected domain keywords
- **Expected Parameters**: Extracted from lists after "parameters should be" or "fields"
- **Framework/Language**: Detected from context

## Implementation Guide

### Step 1: Update Your Prompts

Add keywords and triggers to your prompt frontmatter:

```yaml
---
name: your_prompt_name
description: What your prompt does
keywords:
  - relevant
  - keywords
  - for
  - matching
triggers:
  - "exact phrases"
  - "that should trigger"
  - "this prompt"
arguments:
  # ... existing arguments
---
```

### Step 2: Use the Discovery Tools

**Option A: Browse All Prompts**
```
list_prompts()
```

**Option B: Smart Search**
```
list_prompts(query="user's natural language request")
```

**Option C: Auto-Execute**
```
smart_prompt_executor(query="user's request", auto_execute=true)
```

### Step 3: Extend Auto-Execution

To add auto-execution support for your custom prompts, modify the `smart_prompt_executor` function in `prompt_tools.py`:

```python
# Add your prompt's auto-execution logic
elif 'your_keyword' in query_lower and 'trigger_word' in query_lower:
    # Extract parameters from query
    param1 = extract_param1(query)
    param2 = extract_param2(query)
    
    # Execute your prompt
    from prompt_handlers import load_template
    template = load_template("your_prompt_name")
    result = template.render(param1=param1, param2=param2)
    
    return f"🚀 Auto-executed: your_prompt_name\\n\\n{result}"
```

## Best Practices

### Writing Good Keywords
- Include synonyms and related terms
- Think about how users might describe the task
- Include both technical and common language terms

### Writing Good Triggers
- Use complete phrases users might type
- Include variations and common phrasings
- Be specific enough to avoid false matches

### Parameter Extraction
- Look for common patterns in how users specify requirements
- Handle both explicit lists and implicit mentions
- Provide sensible defaults when parameters aren't specified

## When to Use Each Tool

**Use `list_prompts()` (no query) when:**
- You want to see all available prompts
- You're exploring what's available in the library
- You want to browse the complete catalog
- You're learning what prompts exist

**Use `list_prompts(query='...')` when:**
- You want to find prompts for a specific task
- You need smart recommendations with scoring
- You want to see ranked results
- You want to understand what parameters are required

**Use `smart_prompt_executor` when:**
- You want a "one-click" solution
- You're confident the parameter extraction will work well
- You want to quickly get results without manual prompt calling
- You trust the system to interpret your natural language correctly

## Example Usage Scenarios

### Scenario 1: API Creation
**User Query:** "create api for storing student information. The parameters should be name, class, contact, address"

**Result:** Automatically detects `create_api` prompt, extracts:
- `api_purpose`: "student information management"
- `expected_parameters`: "name, class, contact, address"

### Scenario 2: Code Review
**User Query:** "review my code for security issues"

**Result:** Suggests `code_review` prompt with focus on security

### Scenario 3: Ambiguous Query
**User Query:** "help me with my project"

**Result:** Lists all available prompts since no specific match found

## Troubleshooting

### Prompt Not Being Suggested
1. Check your keywords and triggers are relevant
2. Verify the prompt file has valid frontmatter
3. Use `list_prompts` to see all available prompts

### Auto-Execution Not Working
1. Ensure auto-execution logic exists for your prompt type
2. Check parameter extraction is working correctly
3. Verify the prompt template renders without errors

### Poor Matching Quality
1. Add more specific keywords and triggers
2. Improve the scoring algorithm weights
3. Add domain-specific matching logic

## Advanced Customization

### Custom Scoring Algorithm
Modify the scoring logic in `suggest_prompt` to better match your domain:

```python
# Custom scoring for your domain
if 'domain_specific_word' in query_lower:
    score += 20
```

### Context-Aware Execution
Enhance parameter extraction to consider project context:

```python
# Check project files for context
if project_has_database():
    add_database_params()
```

### Machine Learning Integration
Consider integrating ML-based query understanding for better matching accuracy.

## Contributing

To add new auto-execution patterns:
1. Update the keywords/triggers in relevant prompt files
2. Add extraction logic in `smart_prompt_executor`
3. Test with various query phrasings
4. Update this documentation

---

With these tools, your MCP prompts become much more discoverable and user-friendly, significantly improving the developer experience.

---
arguments:
- description: The name of the project to document
  name: project_name
  required: true
- description: Type of project (e.g., web app, API, library, CLI tool, mobile app)
  name: project_type
  required: true
- description: Primary programming language used in the project
  name: programming_language
  required: true
- description: Brief description of what the project does and its main purpose
  name: project_description
  required: false
- description: Who will use this project (developers, end users, specific industry)
  name: target_audience
  required: false
- description: Whether to include API documentation (true/false)
  name: include_api_docs
  required: false
- description: Whether to include architecture diagrams and explanations (true/false)
  name: include_architecture
  required: false
- description: Platforms where the project can be deployed (e.g., Docker, AWS, Heroku)
  name: deployment_platforms
  required: false
description: Generate comprehensive project documentation including README, architecture
  overview, setup instructions, and API documentation. Creates or updates markdown
  files in the documentation directory.
name: generate_project_documentation
---

You are a technical documentation specialist responsible for creating comprehensive, clear, and maintainable project documentation. Your task is to analyze the project structure and generate professional documentation that helps developers understand, set up, and contribute to the project.

**⚠️ CRITICAL ACCURACY REQUIREMENT: This documentation must reflect the actual state of the project. If you encounter any information that is unclear, missing, or uncertain, ASK THE USER for clarification instead of making assumptions. Documentation accuracy is paramount - it's better to request specific details than to include incorrect information that could mislead users.**

## Project Analysis

**Project:** {{ project_name }}
**Type:** {{ project_type }}
**Language:** {{ programming_language }}
{% if project_description %}**Description:** {{ project_description }}{% endif %}
{% if target_audience %}**Target Audience:** {{ target_audience }}{% endif %}

## Information Verification Protocol

Before generating any documentation section, verify the following:
- **Actual file/directory structure** - Don't assume standard layouts
- **Dependencies and requirements** - Check actual package files, not typical ones
- **Build/run commands** - Verify actual scripts and processes
- **API endpoints and methods** - Document only what exists
- **Configuration requirements** - List only actual config files and variables
- **Deployment procedures** - Document actual deployment setup

**When in doubt, ask questions like:**
- "I need to verify the exact dependencies. Could you provide the contents of package.json/requirements.txt/go.mod?"
- "What are the actual steps to run this project locally?"
- "Which environment variables are actually required vs optional?"
- "What are the real API endpoints and their exact parameters?"

## Documentation Generation Tasks

### 1. Project Overview Documentation
Create or update `documentation/README.md` with:

#### Project Header
- Project name and tagline
- Brief description of purpose and functionality
- Key features and benefits
- Technology stack overview
- Project status/maturity level

#### Quick Start Section
- Prerequisites and system requirements
- Installation instructions (step-by-step)
- Basic usage examples
- Common use cases

### 2. Setup and Installation Guide
Create or update `documentation/SETUP.md` with:

#### Environment Setup
- Development environment requirements
- Dependency installation instructions
- Configuration file examples
- Environment variables needed
- Database setup (if applicable)

#### Build and Run Instructions
- Build process steps
- Development server setup
- Testing procedures
- Debugging tips

### 3. Project Structure Documentation
Create or update `documentation/PROJECT_STRUCTURE.md` with:

#### Directory Structure
- Detailed explanation of folder organization
- Purpose of each major directory
- Key files and their roles
- Naming conventions used

#### Code Organization
- Module/package structure
- Main entry points
- Configuration management
- Asset organization

{% if include_architecture == "true" %}
### 4. Architecture Documentation
Create or update `documentation/ARCHITECTURE.md` with:

#### System Architecture
- High-level system overview
- Component relationships
- Data flow diagrams (textual description)
- Design patterns used
- Key architectural decisions

#### Technical Design
- Core algorithms or business logic
- Database schema (if applicable)
- External service integrations
- Performance considerations
- Scalability approach
{% endif %}

{% if include_api_docs == "true" %}
### 5. API Documentation
Create or update `documentation/API.md` with:

#### API Overview
- Base URL and versioning
- Authentication methods
- Request/response formats
- Rate limiting information

#### Endpoint Documentation
- All available endpoints
- Request parameters and types
- Response examples
- Error codes and messages
- Usage examples for each endpoint
{% endif %}

### 6. Deployment Documentation
{% if deployment_platforms %}Create or update `documentation/DEPLOYMENT.md` for {{ deployment_platforms }} with:{% else %}Create or update `documentation/DEPLOYMENT.md` with:{% endif %}

#### Deployment Options
- Production deployment steps
- Configuration for different environments
- Environment-specific considerations
- Monitoring and logging setup

#### Maintenance
- Backup procedures
- Update/upgrade processes
- Troubleshooting common issues
- Performance monitoring

### 7. Troubleshooting Guide
Create or update `documentation/TROUBLESHOOTING.md` with:

#### Common Issues
- Frequently encountered problems
- Step-by-step solutions
- Known limitations
- Workarounds for edge cases

#### Support Resources
- Where to get help
- Community resources
- Bug reporting process
- Contact information

## Documentation Standards

### Accuracy and Verification Requirements
**BEFORE writing any section:**
1. **Verify information exists** - Don't document features that don't exist
2. **Test all examples** - Every code example must work with the actual codebase
3. **Check current versions** - Use actual version numbers, not placeholders
4. **Validate file paths** - Ensure all referenced files actually exist
5. **Confirm procedures** - Test installation and setup steps

**When information is missing or unclear:**
- Ask specific questions: "What is the exact command to start the development server?"
- Request file contents: "Could you share the package.json file contents?"
- Seek clarification: "I see multiple config files - which one should users modify?"
- Verify assumptions: "Does this project use Docker, or should I focus on local setup?"

### Writing Guidelines
- Use clear, concise language
- Include practical examples
- Organize information logically
- Use consistent formatting
- Keep information up-to-date

### Markdown Formatting
- Use proper heading hierarchy
- Include table of contents for longer documents
- Use code blocks with language specification
- Include links between related documents
- Use tables for structured information

### Code Examples
- Provide working, tested examples
- Include expected outputs
- Show both basic and advanced usage
- Add comments for complex examples
- Use realistic data in examples

## File Organization

Create the following structure in the `documentation/` directory:
```
documentation/
├── README.md              # Main project overview
├── SETUP.md              # Installation and setup
├── PROJECT_STRUCTURE.md  # Code organization
{% if include_architecture == "true" %}├── ARCHITECTURE.md       # Technical architecture{% endif %}
{% if include_api_docs == "true" %}├── API.md               # API documentation{% endif %}
├── DEPLOYMENT.md         # Deployment instructions
├── TROUBLESHOOTING.md    # Common issues and solutions
└── assets/              # Images, diagrams, etc.
```

## Quality Checklist

Before finalizing documentation:
- [ ] All links work correctly
- [ ] Code examples are tested and functional
- [ ] Information is current and accurate
- [ ] Writing is clear and accessible
- [ ] Formatting is consistent
- [ ] Navigation between documents is intuitive
- [ ] All major use cases are covered
- [ ] Installation instructions are complete
- [ ] **ALL INFORMATION HAS BEEN VERIFIED** - No assumptions made

## Next Steps

1. Analyze the existing codebase to understand structure and functionality
2. **ASK USER FOR CLARIFICATION** on any unclear aspects before proceeding
3. Generate each documentation file according to the specifications above
4. Review and test all examples and instructions
5. Create cross-references between related documents
6. Set up a process for keeping documentation updated

## Final Reminder

**🚨 ACCURACY OVER SPEED: It is better to ask 10 questions and create perfect documentation than to make assumptions and create misleading content. Users depend on this documentation to successfully work with the project - inaccurate information can waste hours of their time and damage project credibility.**

**When generating documentation:**
- If unsure about a command → Ask for verification
- If unclear about a feature → Request clarification  
- If missing configuration details → Ask for specifics
- If uncertain about deployment → Seek actual procedures

**Note:** This prompt focuses on documentation generation and analysis. After creating the documentation plan and verifying all information with the user, you should implement the actual file creation and content generation based on the project's specific and verified needs and structure.
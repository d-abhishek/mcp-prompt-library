
## Git & GitHub Standards

### Commit Message Format
Use the conventional commit format: `<type>(<scope>): <subject>`

**Valid Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, build changes, dependency updates

**Scope Rules:**
- Optional but recommended
- Name the affected module/component (e.g., auth, api, ui, database)
- Use lowercase, no spaces
- Examples: 
  - `feat(auth): add OAuth integration - Google and GitHub providers`
  - `fix(api): handle null user data - validate before processing`
  - `docs(readme): update installation guide - add Docker setup`

**Subject Rules:**
- Use imperative mood ("add" not "added" or "adds")
- Keep under 50 characters
- No trailing period
- Start with lowercase letter
- Be descriptive but concise
- Use hyphens (-) to create submessages for clarity when needed
- Examples: `add user authentication - OAuth and JWT support`, `fix database connection - handle timeout errors`

**Submessages with Hyphens:**
- Use upto 5 submessages if there are more changes
- Always start submessage in next line
- Use single hyphen (-) with spaces around it to add clarifying details
- Keep total message under 50 characters including submessage
- Submessage should provide specific context or method
- Examples:
  - `feat(auth): add login system - OAuth2 integration - password rules setup`
  - `fix(ui): resolve button alignment - flexbox layout`
  - `docs(api): update endpoint docs - add error codes`
  - `refactor(db): optimize queries - use indexing`

**Body (Optional):**
- Wrap lines at 72 characters
- Explain WHY the change was made, not HOW
- Use complete sentences
- Separate paragraphs with blank lines

**Footer (Optional):**
- Issue references: `Closes #1234`, `Refs #5678`, `Fixes #91011`
- Breaking changes: `BREAKING CHANGE: migration instructions here`

### Branch Naming Conventions
Format: `<type>/<short-description>`

**Valid Types:**
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation updates
- `style` - Code style improvements
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Test additions/updates
- `chore` - Maintenance tasks
- `hotfix` - Critical production fixes
- `release` - Release preparation

**Description Rules:**
- Use lowercase letters
- Separate words with hyphens (kebab-case)
- Be descriptive but concise (under 30 characters)
- No special characters except hyphens
- Examples: `feat/user-authentication`, `fix/memory-leak`, `docs/api-guide`

### Pull Request Standards

**PR Title Requirements:**
- Must mirror commit header format: `<type>(<scope>): <subject>`
- Examples: `feat(auth): add OAuth2 authentication`, `fix(api): resolve user data validation`

**PR Description Template:**
```markdown
## Summary
Brief description of what this PR accomplishes.

## Changes Made
- List key changes
- Highlight important modifications
- Note any breaking changes

## Related Issues
- Closes #123
- Refs #456
- Fixes #789

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed
- [ ] Edge cases considered

## Setup/Migration Steps
List any required setup steps or database migrations.

## Screenshots/Demo
Include relevant visuals if UI changes are involved.

## Checklist
- [ ] Code follows company style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] CI checks passing
```

**Pre-Merge Requirements:**
- All CI checks must pass (tests, linting, security scans, build verification)
- At least one approving code review
- All review comments addressed
- No unresolved conversations
- Code coverage maintained or improved
- No new security vulnerabilities
- Performance impact assessed
- Documentation updated for user-facing changes

## Development Workflow Best Practices

1. **Branch Management:**
   - Create feature branches from main
   - Use descriptive branch names following conventions
   - Keep branches focused on single features/fixes

2. **Commit Practices:**
   - Make small, atomic commits
   - Write descriptive commit messages
   - Commit frequently with logical changesets

3. **Code Review Process:**
   - Create small, focused PRs (one logical change per PR)
   - Provide comprehensive PR descriptions
   - Link related issues and tickets
   - Include appropriate test coverage
   - Update documentation for user-facing changes
   - Address review feedback promptly

4. **Quality Assurance:**
   - Run tests locally before pushing
   - Use automated formatting tools (Prettier, ESLint, Black, etc.)
   - Integrate linting and code quality tools
   - Set up pre-commit hooks for essential checks
   - Ensure CI/CD pipeline passes

## Automation & Tooling Integration

**Recommended Setup:**
- **commitlint**: Validates commit messages
- **husky**: Git hooks for pre-commit checks
- **lint-staged**: Run linters on staged files
- **conventional-changelog**: Generate changelogs
- Automated formatting tools for consistent code style
- Static analysis tools for code quality
- Security scanning tools

**Pre-commit Hook Example:**
```bash
#!/bin/sh
npm run lint
npm run test
npm run build
```
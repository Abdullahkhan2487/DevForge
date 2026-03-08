# Contributing to DevForge

Thank you for your interest in contributing to DevForge! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/DevForge.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add feature X"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

See [SETUP.md](docs/SETUP.md) for detailed setup instructions.

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Use Black for formatting: `black .`
- Use meaningful variable names

```python
# Good
async def create_project(name: str, prompt: str) -> Project:
    """Create a new project with the given name and prompt."""
    pass

# Bad
def cp(n, p):
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Keep components small and focused

```tsx
// Good
interface Props {
    project: Project;
    onUpdate: (project: Project) => void;
}

export default function ProjectCard({ project, onUpdate }: Props) {
    // Component implementation
}

// Bad
export default function ProjectCard(props: any) {
    // Component implementation
}
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Pull Request Guidelines

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug in X`
- `docs: Update documentation`
- `refactor: Refactor component X`
- `test: Add tests for X`

### PR Description

- Describe what changes you made and why
- Reference any related issues
- Include screenshots for UI changes
- List any breaking changes

### Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No console errors
- [ ] Tested locally

## Areas for Contribution

### High Priority

- [ ] Add authentication system
- [ ] Implement rate limiting
- [ ] Add project templates
- [ ] Improve error handling
- [ ] Add integration tests

### Medium Priority

- [ ] Add more agent types
- [ ] Improve UI/UX
- [ ] Add project search
- [ ] Export projects to GitHub
- [ ] Add project sharing

### Low Priority

- [ ] Dark mode improvements
- [ ] Add keyboard shortcuts
- [ ] Add project analytics
- [ ] Add email notifications

## Adding New Agents

To add a new agent:

1. Create file in `backend/agents/`
2. Extend `BaseAgent` class
3. Implement `execute()` method
4. Add to orchestrator pipeline
5. Write tests
6. Update documentation

Example:

```python
from agents.base_agent import BaseAgent, AgentConfig

class MyNewAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="MyNewAgent",
            role="My Role",
            goal="My goal",
            backstory="My backstory"
        )
        super().__init__(config)

    async def execute(self, agent_input):
        # Implementation
        pass
```

## Reporting Bugs

Use GitHub Issues with this template:

**Bug Report**

- Description: Clear description of the bug
- Steps to Reproduce: 1. Go to... 2. Click on... 3. See error
- Expected Behavior: What should happen
- Actual Behavior: What actually happens
- Screenshots: If applicable
- Environment: OS, Browser, Python version, etc.

## Feature Requests

Use GitHub Issues with this template:

**Feature Request**

- Feature Description: What feature you want
- Use Case: Why you need it
- Proposed Solution: How it could work
- Alternatives: Other ways to solve the problem

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, PR will be merged
4. Your contribution will be credited

## Questions?

- Open a GitHub Discussion
- Check existing issues
- Read the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🚀

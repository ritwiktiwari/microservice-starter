# Contributing to Microservice Starter Kit

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Install [uv](https://github.com/astral-sh/uv) and [Pyrefly](https://pyrefly.org):
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.13
uv python install 3.13
```

2. Clone and setup:
```bash
git clone https://github.com/yourusername/microservice-starter.git
cd microservice-starter
uv sync --all-extras
```

3. Start services:
```bash
docker-compose up -d
```

## Code Quality

Before submitting a PR, ensure your code passes all checks:

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test
```

## Code Style

- Use **ruff** for linting and formatting
- Follow **PEP 8** conventions
- Use **type hints** for all functions
- Write **docstrings** for public APIs
- Keep functions small and focused

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use pytest fixtures for common setup
- Test both success and error cases

## Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests
4. Update documentation
5. Run all checks locally
6. Submit PR with clear description
7. Address review feedback

## Questions?

Open an issue for discussion before starting major changes.

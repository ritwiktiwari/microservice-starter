# Development Guide

## Setup

### Install Tools

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Dependencies

```bash
# Install all dependencies including dev tools
uv sync --all-extras

# Install only production dependencies
uv sync
```

### Start Services

```bash
# Start PostgreSQL, Redis, and Jaeger
docker-compose up -d

# Check services are running
docker-compose ps
```

## Development Workflow

### Running the Application

```bash
# Development mode with auto-reload
make dev

# Or manually
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

```bash
# Format code with ruff
make format

# Run all linters
make lint

# Individual checks
uv run ruff check .
uv run ruff format --check .
pyrefly check .
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/test_items.py

# Run specific test
uv run pytest tests/test_items.py::test_create_item -v
```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Add new table"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

## Type Checking with Pyrefly

Pyrefly is configured via `pyrefly.toml` and `pyproject.toml`.

```bash
# Check all files
pyrefly check app/

# Check specific file
pyrefly check app/main.py

# Watch mode (re-check on file changes)
pyrefly watch app/

# Show configuration
pyrefly config
```

### Type Checking Best Practices

- Add type hints to all function signatures
- Use `from typing import` for complex types
- Avoid `Any` when possible
- Use `Optional[T]` for nullable values
- Use `list[T]` instead of `List[T]` (Python 3.9+)
- Use `X | Y` instead of `Union[X, Y]` (Python 3.10+)
- Use `type` statement for type aliases (Python 3.12+)

## Linting with Ruff

Ruff combines multiple tools (black, isort, flake8, etc.) into one fast linter.

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check specific rules
uv run ruff check --select E,F .
```

## VS Code Setup

Install recommended extensions:
- Ruff (charliermarsh.ruff)
- Python (ms-python.python)
- Docker (ms-azuretools.vscode-docker)

Settings are pre-configured in `.vscode/settings.json`.

## Debugging

### VS Code Debug Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

### Debug with pdb

```python
import pdb; pdb.set_trace()
```

### View Logs

```bash
# Application logs (structured JSON)
docker-compose logs -f app

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis
```

## Performance Profiling

```bash
# Install profiling tools
uv pip install py-spy

# Profile running application
py-spy top --pid <pid>

# Generate flame graph
py-spy record -o profile.svg -- python -m uvicorn app.main:app
```

## Load Testing

```bash
# Run load test
locust -f load-tests/locustfile.py --host http://localhost:8000

# Headless mode
locust -f load-tests/locustfile.py \
  --host http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 60s \
  --headless
```

## API Testing with Playwright

```bash
cd tests

# Install dependencies
npm install

# Run tests
npm test

# Run with UI
npm run test:ui

# Run specific test
npx playwright test api.spec.ts
```

## Common Issues

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <pid>
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Type Check Errors

```bash
# Clear Pyrefly cache
rm -rf .pyrefly_cache

# Re-run check
pyrefly check app/
```

## Tips

- Use `make help` to see all available commands
- Run `make lint` before committing
- Keep test coverage above 80%
- Write docstrings for public APIs
- Use structured logging with context
- Add type hints to all functions

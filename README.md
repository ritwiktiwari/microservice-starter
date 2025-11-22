# Microservice Starter Kit

Production-ready FastAPI microservice template with modern Python tooling, observability, and comprehensive testing.

## Features

- **Python 3.13** with latest performance improvements
- **FastAPI** with async/await patterns and SQLAlchemy 2.0
- **Modern Python tooling**: uv, ruff, Pyrefly
- **Database migrations** with Alembic
- **OpenTelemetry** tracing with Jaeger
- **PostgreSQL** with async SQLAlchemy
- **Redis** for caching
- **Structured logging** with structlog
- **Playwright** API tests (TypeScript)
- **Locust** load testing
- **Docker** multi-stage builds
- **Kubernetes** manifests with HPA
- **GitHub Actions** CI/CD

## Project Structure

```
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Config, logging, middleware
│   ├── db/              # Database session management
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── tests/               # Pytest unit tests
├── load-tests/          # Locust load tests
├── k8s/                 # Kubernetes manifests
└── pyproject.toml       # Project dependencies
```

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [Pyrefly](https://pyrefly.org) - Fast type checker
- Docker & Docker Compose (for running services)

### Installation

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras

# Copy environment file
cp .env.example .env
```

### Development

```bash
# Start services (PostgreSQL, Redis, Jaeger)
docker-compose up -d

# Run database migrations
make migrate-up

# Run development server
make dev

# Or manually
uv run uvicorn app.main:app --reload
```

API will be available at http://localhost:8000

- Swagger docs: http://localhost:8000/api/v1/docs
- Jaeger UI: http://localhost:16686

### Database Migrations

```bash
# Create a new migration
make migrate-create MSG="add users table"

# Apply migrations
make migrate-up

# Rollback last migration
make migrate-down
```

### Code Quality

```bash
# Run linters
make lint

# Format code
make format

# Type checking
pyrefly check app/
```

### Testing

```bash
# Run unit tests
make test

# Run with coverage
make test-cov

# Run Playwright API tests
cd tests
npm install
npm test

# Run load tests
locust -f load-tests/locustfile.py --host http://localhost:8000
```

## Deployment

### Docker

```bash
# Build image
docker build -t microservice-starter:latest .

# Run container
docker run -p 8000:8000 microservice-starter:latest
```

### Kubernetes

```bash
# Create secrets (edit secrets.example.yaml first)
kubectl apply -f k8s/secrets.example.yaml

# Deploy application
kubectl apply -f k8s/

# Check status
kubectl get pods
kubectl logs -f deployment/microservice
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for all available options.

Key settings:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OTEL_ENABLED`: Enable/disable OpenTelemetry
- `SECRET_KEY`: Secret key for security features

## Development Tools

- **uv**: Fast Python package manager and resolver
- **ruff**: Extremely fast Python linter and formatter
- **Pyrefly**: Blazing fast static type checker for Python
- **pytest**: Testing framework
- **Playwright**: End-to-end API testing
- **Locust**: Load testing framework

## Architecture Patterns

- **Async/await**: All I/O operations are async
- **Dependency injection**: FastAPI's dependency system
- **Repository pattern**: Database access abstraction
- **Structured logging**: JSON logs with context
- **Health checks**: Kubernetes-ready probes
- **Graceful shutdown**: Proper cleanup on termination

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linters
5. Submit a pull request

## License

MIT License - see LICENSE file for details

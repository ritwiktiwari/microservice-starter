.PHONY: help install dev lint format test test-cov clean docker-build docker-up docker-down migrate-create migrate-up migrate-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Run development server"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make migrate-create MSG='message' - Create new migration"
	@echo "  make migrate-up    - Run migrations"
	@echo "  make migrate-down  - Rollback last migration"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker services"
	@echo "  make docker-down   - Stop Docker services"

install:
	uv sync --all-extras

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	uv run ruff check .
	pyrefly check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	PYTHONPATH=. uv run pytest

test-cov:
	PYTHONPATH=. uv run pytest --cov=app --cov-report=html --cov-report=term

migrate-create:
	uv run alembic revision --autogenerate -m "$(MSG)"

migrate-up:
	uv run alembic upgrade head

migrate-down:
	uv run alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage

docker-build:
	docker build -t microservice-starter:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

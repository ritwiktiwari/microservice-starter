#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h localhost -p 5432 -U postgres; do
  sleep 1
done

echo "Running database migrations..."
uv run alembic upgrade head

echo "Database initialized!"

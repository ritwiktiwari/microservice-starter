# Database Migrations with Alembic

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations.

## Quick Start

### Create a Migration

After modifying your SQLAlchemy models:

```bash
make migrate-create MSG="add new column to users"
```

This will auto-generate a migration file in `alembic/versions/`.

### Apply Migrations

```bash
make migrate-up
```

This runs all pending migrations.

### Rollback

```bash
make migrate-down
```

This rolls back the last migration.

## Manual Commands

### Create Migration (Auto-generate)

```bash
uv run alembic revision --autogenerate -m "description"
```

### Create Empty Migration

```bash
uv run alembic revision -m "description"
```

### Upgrade to Latest

```bash
uv run alembic upgrade head
```

### Upgrade to Specific Revision

```bash
uv run alembic upgrade <revision>
```

### Downgrade

```bash
uv run alembic downgrade -1  # One step back
uv run alembic downgrade <revision>  # To specific revision
uv run alembic downgrade base  # All the way back
```

### Show Current Revision

```bash
uv run alembic current
```

### Show Migration History

```bash
uv run alembic history
```

## Migration File Structure

```python
"""add users table

Revision ID: abc123
Revises: def456
Create Date: 2025-01-13 10:00:00.000000
"""

def upgrade() -> None:
    # Migration code here
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # Rollback code here
    op.drop_table('users')
```

## Best Practices

1. **Always review auto-generated migrations** - Alembic might not catch everything
2. **Test migrations** - Run upgrade and downgrade locally
3. **Keep migrations small** - One logical change per migration
4. **Never edit applied migrations** - Create a new migration instead
5. **Add data migrations carefully** - Consider large datasets
6. **Use transactions** - Migrations run in transactions by default

## Common Operations

### Add Column

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone')
```

### Rename Column

```python
def upgrade() -> None:
    op.alter_column('users', 'name', new_column_name='full_name')

def downgrade() -> None:
    op.alter_column('users', 'full_name', new_column_name='name')
```

### Add Index

```python
def upgrade() -> None:
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade() -> None:
    op.drop_index('ix_users_email', 'users')
```

### Data Migration

```python
from sqlalchemy import table, column

def upgrade() -> None:
    # Define table structure for data migration
    users = table('users',
        column('id', sa.Integer),
        column('status', sa.String)
    )
    
    # Update data
    op.execute(
        users.update()
        .where(users.c.status == 'pending')
        .values(status='active')
    )
```

## Production Deployment

1. **Backup database** before running migrations
2. **Test migrations** in staging environment
3. **Run migrations** before deploying new code
4. **Monitor** for errors during migration
5. **Have rollback plan** ready

### Automated Deployment

```bash
# In CI/CD pipeline
uv run alembic upgrade head
```

### Kubernetes Init Container

```yaml
initContainers:
- name: migrations
  image: microservice-starter:latest
  command: ["uv", "run", "alembic", "upgrade", "head"]
  env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: database-url
```

## Troubleshooting

### Migration Conflicts

If multiple developers create migrations:

```bash
# Merge migrations
uv run alembic merge -m "merge migrations" <rev1> <rev2>
```

### Reset Database

```bash
# Drop all tables and rerun migrations
uv run alembic downgrade base
uv run alembic upgrade head
```

### Stamp Database

If you need to mark database as being at a specific revision:

```bash
uv run alembic stamp head
```

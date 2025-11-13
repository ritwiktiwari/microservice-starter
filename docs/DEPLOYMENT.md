# Deployment Guide

## Local Development

```bash
# Start all services
docker-compose up -d

# Run migrations
uv run alembic upgrade head

# Seed data
uv run python scripts/seed-data.py

# Start dev server
make dev
```

## Docker

### Build

```bash
docker build -t microservice-starter:latest .
```

### Run

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e REDIS_URL=redis://... \
  microservice-starter:latest
```

## Kubernetes

### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- PostgreSQL and Redis (managed or in-cluster)

### Deploy

1. Create secrets:
```bash
kubectl create secret generic app-secrets \
  --from-literal=database-url='postgresql+asyncpg://...' \
  --from-literal=redis-url='redis://...' \
  --from-literal=secret-key='...'
```

2. Run database migrations:
```bash
kubectl apply -f k8s/migration-job.yaml
kubectl wait --for=condition=complete job/db-migration --timeout=300s
```

3. Apply manifests:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

4. Verify:
```bash
kubectl get pods
kubectl logs -f deployment/microservice
```

### Scaling

Manual:
```bash
kubectl scale deployment microservice --replicas=5
```

Auto-scaling is configured via HPA based on CPU usage.

## Cloud Platforms

### AWS EKS

1. Create EKS cluster
2. Setup RDS PostgreSQL
3. Setup ElastiCache Redis
4. Deploy using kubectl

### Google GKE

1. Create GKE cluster
2. Setup Cloud SQL PostgreSQL
3. Setup Memorystore Redis
4. Deploy using kubectl

### Azure AKS

1. Create AKS cluster
2. Setup Azure Database for PostgreSQL
3. Setup Azure Cache for Redis
4. Deploy using kubectl

## Monitoring

### Jaeger (Tracing)

Access Jaeger UI:
```bash
kubectl port-forward svc/jaeger 16686:16686
```

Visit http://localhost:16686

### Logs

View logs:
```bash
kubectl logs -f deployment/microservice
```

Stream logs to external system (Datadog, CloudWatch, etc.)

## CI/CD

GitHub Actions workflow automatically:
- Runs tests and linters
- Builds Docker image
- Pushes to registry
- Deploys to staging (configure)

## Health Checks

- `/health` - Liveness probe
- `/ready` - Readiness probe

## Rollback

```bash
kubectl rollout undo deployment/microservice
```

## Troubleshooting

### Pod not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Database connection issues
- Check DATABASE_URL secret
- Verify network policies
- Check PostgreSQL logs

### High memory usage
- Adjust resource limits
- Check for memory leaks
- Review connection pool sizes

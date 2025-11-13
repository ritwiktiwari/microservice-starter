from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import items, users
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.core.telemetry import setup_telemetry
from app.db.session import close_db_pool, init_db_pool
from app.services.cache import close_cache, init_cache


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    # Startup
    setup_logging()
    await init_db_pool()
    await init_cache()

    yield

    # Shutdown
    await close_cache()
    await close_db_pool()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# Setup middleware and telemetry
setup_middleware(app)
setup_telemetry(app)

# Include routers
app.include_router(items.router, prefix=settings.API_V1_PREFIX, tags=["items"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["users"])


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check endpoint."""
    return {"status": "ready"}

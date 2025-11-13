import json
from typing import Any

from redis.asyncio import ConnectionPool, Redis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

redis_client: Redis | None = None
redis_pool: ConnectionPool | None = None


async def init_cache() -> None:
    """Initialize Redis connection pool."""
    global redis_client, redis_pool

    logger.info("Initializing Redis pool", url=str(settings.REDIS_URL))

    redis_pool = ConnectionPool.from_url(
        str(settings.REDIS_URL),
        max_connections=settings.REDIS_POOL_SIZE,
        decode_responses=False,
    )

    redis_client = Redis(connection_pool=redis_pool)

    # Test connection
    try:
        redis_client.ping()
    except Exception as e:
        raise RuntimeError(f"Redis ping failed: {e}") from e

    logger.info("Redis pool initialized")


async def close_cache() -> None:
    """Close Redis connection pool."""
    global redis_client, redis_pool

    if redis_client:
        logger.info("Closing Redis pool")
        await redis_client.aclose()

    if redis_pool:
        await redis_pool.aclose()

    logger.info("Redis pool closed")


async def get_cache(key: str) -> Any | None:
    """Get value from cache."""
    if redis_client is None:
        return None

    value = await redis_client.get(key)
    if value:
        return json.loads(value)
    return None


async def set_cache(key: str, value: Any, ttl: int = 300) -> None:
    """Set value in cache with TTL."""
    if redis_client is None:
        return

    await redis_client.setex(key, ttl, json.dumps(value))


async def delete_cache(key: str) -> None:
    """Delete value from cache."""
    if redis_client is None:
        return

    await redis_client.delete(key)

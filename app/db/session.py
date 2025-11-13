from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

engine: Any | None = None
async_session_maker: async_sessionmaker[AsyncSession] | None = None


async def init_db_pool() -> None:
    """Initialize database connection pool."""
    global engine, async_session_maker

    logger.info("Initializing database pool", url=str(settings.DATABASE_URL))

    engine = create_async_engine(
        str(settings.DATABASE_URL),
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        echo=False,
    )

    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    logger.info("Database pool initialized")


async def close_db_pool() -> None:
    """Close database connection pool."""
    global engine

    if engine:
        logger.info("Closing database pool")
        await engine.dispose()
        logger.info("Database pool closed")


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Get database session dependency."""
    if async_session_maker is None:
        raise RuntimeError("Database not initialized")

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

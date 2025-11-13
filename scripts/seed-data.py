"""Seed database with sample data."""

import asyncio

from app.db.session import async_session_maker, init_db_pool
from app.models.item import Item
from app.models.user import User


async def seed_data() -> None:
    """Create sample data."""
    await init_db_pool()

    if async_session_maker is None:
        raise RuntimeError("Database not initialized")

    async with async_session_maker() as session:
        # Create users
        users = [
            User(
                email="alice@example.com",
                username="alice",
                full_name="Alice Smith",
            ),
            User(
                email="bob@example.com",
                username="bob",
                full_name="Bob Johnson",
            ),
        ]
        session.add_all(users)
        await session.commit()

        # Create items
        items = [
            Item(name="Laptop", description="MacBook Pro", owner_id=1),
            Item(name="Phone", description="iPhone 15", owner_id=1),
            Item(name="Keyboard", description="Mechanical keyboard", owner_id=2),
        ]
        session.add_all(items)
        await session.commit()

        print("✓ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient) -> None:
    """Test creating an item."""
    response = await client.post(
        "/api/v1/items",
        json={"name": "Test Item", "description": "Test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test description"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test listing items."""
    # Create test items
    item1 = Item(name="Item 1", description="Desc 1", owner_id=1)
    item2 = Item(name="Item 2", description="Desc 2", owner_id=1)
    db_session.add_all([item1, item2])
    await db_session.commit()

    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient, db_session: AsyncSession) -> None:
    """Test getting a single item."""
    item = Item(name="Test Item", description="Test", owner_id=1)
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    response = await client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"


@pytest.mark.asyncio
async def test_get_nonexistent_item(client: AsyncClient) -> None:
    """Test getting a nonexistent item."""
    response = await client.get("/api/v1/items/999")
    assert response.status_code == 404

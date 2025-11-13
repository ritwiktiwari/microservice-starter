import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    """Test creating a user."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_user(client: AsyncClient) -> None:
    """Test creating a duplicate user."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
    }

    # Create first user
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201

    # Try to create duplicate
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 400

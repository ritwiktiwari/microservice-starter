from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()


@router.get("/items", response_model=list[ItemResponse])
async def list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[Item]:
    """List all items with pagination."""
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return list(result.scalars().all())


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Item:
    """Create a new item."""
    item = Item(**item_in.model_dump(), owner_id=1)  # TODO: Get from auth
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Item:
    """Get item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item

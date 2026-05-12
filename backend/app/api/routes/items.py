from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep            
from app.models import Item, ItemCreate, ItemPublic, ItemsPublic

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve current user's items.
    
    Returns a paginated list of items owned by the authenticated user.
    Use skip and limit parameters for pagination.
    """

    count_stmt = (
        select(func.count()).select_from(Item).where(Item.owner_id == current_user.id)
    )
    count = session.exec(count_stmt).one()
    stmt = (
        select(Item).where(Item.owner_id == current_user.id).offset(skip).limit(limit)
    )
    items = session.exec(stmt).all()

    return ItemsPublic(data=items, count=count)


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create a new item.
    
    Creates a new item associated with the authenticated user.
    The item title is required and must be 1-255 characters.
    """
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

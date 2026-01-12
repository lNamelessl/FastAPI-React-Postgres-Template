from typing import Literal

from app.common.types import PaginationParamsType
from app.core.database import AsyncSessionLocal


async def get_session():
    """
    Start a db session
    """
    async with AsyncSessionLocal() as session:  # type: ignore
        yield session
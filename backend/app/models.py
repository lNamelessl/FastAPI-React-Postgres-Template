import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_super_user: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date of creation",
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=72)
    fullname: str | None = Field(default=None, max_length=255)


class UserUpdate(SQLModel):
    fullname: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UserPassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int = Field(description="The total number of users", default=0)


class ItemBase(SQLModel):
    """
    shared properties
    """

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    """
    items creation validation model
    """

    pass


class ItemUpdate(ItemBase):
    """
    Properties to receive on item update
    """

    title: str | None = Field(default=None, min_length=1, max_length=255)


class Item(ItemBase, table=True):
    """
    item database table
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    """
    items list validation model
    """

    data: list[ItemPublic]
    count: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None

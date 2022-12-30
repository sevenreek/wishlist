from sqlmodel import SQLModel, Field, Relationship
from pydantic import FileUrl, EmailStr
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..models import Wishlist
from ..models import UsersWishlists

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    username: str | None = Field(index=True, default=None)
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: FileUrl | None

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str | None = None
    wishlists: list['Wishlist'] = Relationship(
        back_populates='users',
        link_model=UsersWishlists
    )
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int | None


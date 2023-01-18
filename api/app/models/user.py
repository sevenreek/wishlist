from sqlmodel import SQLModel, Field, Relationship
from pydantic import AnyUrl, EmailStr
from typing import TYPE_CHECKING
from uuid import UUID, uuid4


if TYPE_CHECKING:
    from ..models import Wishlist, Reservation
from ..models import UsersWishlists

class UserAnonymousBase(SQLModel):
    uuid: UUID = Field(unique=True, index=True, default_factory=uuid4)

class UserBase(UserAnonymousBase):
    email: EmailStr | None = Field(unique=True, index=True, default=None)
    username: str | None = Field(index=True, default=None)
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: AnyUrl | None = None

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str | None = None
    wishlists: list['Wishlist'] = Relationship(
        back_populates='users',
        link_model=UsersWishlists,
        sa_relationship_kwargs={"cascade": "all,delete"},
    )
    reservations: list['Reservation'] = Relationship(back_populates='reserved_by')

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int


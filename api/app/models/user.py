from sqlmodel import SQLModel, Field, Relationship
from pydantic import FileUrl, EmailStr
from sqlalchemy import delete, select
from typing import TYPE_CHECKING

from app.utils.auth import verify_password, hash_password
from .crud import BaseCRUD

if TYPE_CHECKING:
    from ..models import Wishlist
from ..models import UsersWishlists

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    username: str | None = None
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


class UserCRUD(BaseCRUD):
    async def find_by_email(self, email: str) -> User | None:
        user_coll = await self.s.execute(
            select(User).where(User.email == email)
        )
        return user_coll.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User:
        password_hash = hash_password(data.password)
        u = User(**data.dict(exclude={'password'}), password_hash=password_hash)
        self.s.add(u)
        await self.s.commit()
        await self.s.refresh(u)
        return u
        

        
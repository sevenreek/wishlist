from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from pydantic import FileUrl
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from asyncpg.exceptions import UniqueViolationError

from ..constants import errors
from ..utils.slugs import generate_wishlist_slug, DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
from .crud import BaseCRUD

if TYPE_CHECKING:
    from app.models import Item, User

from .users_wishlists import UsersWishlists

class WishlistBase(SQLModel):
    name: str = Field(index=True)
    image_url: FileUrl | None
    description: str | None
    

class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, default_factory=generate_wishlist_slug)
    items: list['Item'] = Relationship(back_populates='wishlist')
    users: list['User'] = Relationship(
        back_populates='wishlists', 
        link_model=UsersWishlists
    )

class WishlistCreate(WishlistBase):
    pass

class WishlistRead(Wishlist):
    pass

class WishlistCRUD(BaseCRUD):
    async def get(self, id: int) -> Wishlist| None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.id == id).limit(1)
        )
        if result := result.fetchone(): return result
        else: raise HTTPException(status_code = 404, detail=errors.RECORD_NOT_FOUND)

    async def get_by_slug(self, slug: str) -> Wishlist| None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.slug == slug).limit(1)
        )
        if result := result.fetchone(): return result
        else: raise HTTPException(status_code = 404, detail=errors.RECORD_NOT_FOUND)
    
    async def create(self, data: WishlistCreate, user: 'User', *, slug_unique_attempts=DEFAULT_SLUG_UNIQUENESS_ATTEMPTS):
        slug_unique_attempts = slug_unique_attempts if slug_unique_attempts > 0 else 1
        for _ in range(slug_unique_attempts):
            wishlist = Wishlist(**data.dict(), users=[user])
            self.s.add(wishlist)
            try:
                await self.s.commit()
                await self.s.refresh(wishlist)
            except UniqueViolationError:
                continue
            else:
                return wishlist
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=errors.UNIQUE_GENERATION_FAILED)

    async def index_for_user(self, user: 'User') -> list[Wishlist]:
        result = await self.s.execute(
            select(Wishlist).join(UsersWishlists).where(UsersWishlists.user_id == user.id)
        )
        return result.scalars().all()


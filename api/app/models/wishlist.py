from fastapi import HTTPException
from sqlalchemy import delete, select
from pydantic import FileUrl
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from ..utils.slugs import generate_wishlist_slug, DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
from .crud import BaseCRUD

if TYPE_CHECKING:
    from app.models import Item, User

from .users_wishlists import UsersWishlists

class WishlistBase(SQLModel):
    name: str = Field(index=True)
    image_url: FileUrl | None
    description: str | None
    users: 'User' = Relationship(back_populates='wishlists', link_model=UsersWishlists)
    

class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, default_factory=generate_wishlist_slug)
    items: list['Item'] = Relationship(back_populates='wishlist')

class WishlistCreate(WishlistBase):
    pass

class WishlistRead(Wishlist):
    pass

class WishlistCRUD(BaseCRUD):
    async def find(self, id: int) -> WishlistRead | None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.id == id).limit(1)
        )
        if result := result.fetchone(): return result
        else: raise HTTPException(status_code = 404)
    
    async def create(self, data: WishlistCreate, *, slug_unique_attempts=DEFAULT_SLUG_UNIQUENESS_ATTEMPTS):
        slug_unique_attempts = slug_unique_attempts if slug_unique_attempts > 0 else DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
        for _ in range(slug_unique_attempts):
            wishlist = Wishlist(**data.dict(), slug=generate_wishlist_slug())
            self.s.add(wishlist)
            await self.s.commit()
            await self.s.refresh(wishlist)
        return wishlist



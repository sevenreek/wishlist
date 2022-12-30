from fastapi import HTTPException, status
from sqlalchemy import delete, select
from typing import TYPE_CHECKING
from asyncpg.exceptions import UniqueViolationError

from ..constants import errors
from ..utils.slugs import DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
from .crud import BaseCRUD

if TYPE_CHECKING:
    from ..models import User

from ..models import UsersWishlists
from ..models.wishlist import Wishlist, WishlistCreate


class WishlistCRUD(BaseCRUD):
    async def get(self, id: int) -> Wishlist| None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.id == id).limit(1)
        )
        if result := result.fetchone(): return result
        else: raise HTTPException(status_code = 404, detail=errors.RECORD_NOT_FOUND)

    async def get_by_slug(self, slug: str, user: 'User' = None) -> Wishlist| None:
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

    async def can_user_edit(self, wishlist: 'Wishlist', user: 'User'):
        result = await self.s.execute(
            select(UsersWishlists)
                .where(UsersWishlists.user_id == user.id)
                .where(UsersWishlists.wishlist_id == wishlist.id)
        )
        return bool(result.scalar_one_or_none())




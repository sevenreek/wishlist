from fastapi import HTTPException, status, Depends
from sqlalchemy import delete, select
from typing import TYPE_CHECKING, Union
from asyncpg.exceptions import UniqueViolationError

from ..constants import errors
from ..utils.slugs import DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
from .crud import BaseCRUD, NoUser
from ..config import settings
from ..models import UsersWishlists
from ..models.wishlist import Wishlist, WishlistCreate, WishlistPartialUpdate
from ..models.item import Item, ItemCreate, ItemPartialUpdate

if TYPE_CHECKING:
    from ..models import User
UserType = Union['User', type[NoUser]]



class WishlistCRUD(BaseCRUD):
    async def get(self, id: int) -> Wishlist| None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.id == id).limit(1)
        )
        if (result := result.scalar_one_or_none()) is not None: return result
        else: raise HTTPException(status_code = 404, detail=errors.RECORD_NOT_FOUND)

    async def get_by_slug(self, slug: str) -> Wishlist | None:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.slug == slug).limit(1)
        )
        if (result := result.scalar_one_or_none()) is not None: return result
        else: raise HTTPException(status_code = 404, detail=errors.RECORD_NOT_FOUND)
    
    async def create(self, data: WishlistCreate, user: 'User', *, slug_unique_attempts=DEFAULT_SLUG_UNIQUENESS_ATTEMPTS) -> Wishlist:
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

    async def update(self, wishlist: 'Wishlist', data: WishlistPartialUpdate, as_user: UserType = NoUser) -> Wishlist:
        await self._ensure_user_can_modify_wishlist(wishlist, as_user)
        self.s.add(wishlist.copy(update=data.dict(exclude_unset=True)))
        await self.s.commit()
        await self.s.refresh(wishlist)
        return wishlist

    async def _ensure_user_can_modify_wishlist(self, wishlist: 'Wishlist', user: UserType = NoUser) -> None:
        if user is NoUser: return
        result = await self.s.execute(
            select(UsersWishlists)
                .where(UsersWishlists.user_id == user.id) # pyright: ignore // if user is NoUser return on first line
                .where(UsersWishlists.wishlist_id == wishlist.id)
        )
        if result.scalar_one_or_none() is None: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = errors.INSUFFICIENT_ACCESS)


    async def delete(self, wishlist: 'Wishlist', as_user: UserType = NoUser) -> None:
        await self._ensure_user_can_modify_wishlist(wishlist, as_user)
        await self.s.delete(wishlist)
        await self.s.commit()

    # Items
    async def get_item(self, wishlist: 'Wishlist', item_id: int) -> Item | None:
        result = await self.s.execute(
            select(Item).where(Item.wishlist_id == wishlist.id).where(Item.id == item_id)
        )
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.RECORD_NOT_FOUND)
        return result

    async def index_wishlist_items(self, wishlist: 'Wishlist', *, offset=0, limit=settings.wishlist_items_limit, order_by=Item.created_at) -> list['Item']:
        stmt = (select(Item) 
            .where(Item.wishlist_id == wishlist.id)
            .order_by(order_by)
            .offset(offset)
            .limit(limit))
        result = await self.s.execute(stmt)
        return result.scalars().all()

    async def create_item(self, in_wishlist: 'Wishlist', data: 'ItemCreate', as_user: UserType = NoUser) -> 'Item':
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        item = Item(**data.dict(), wishlist=in_wishlist)
        self.s.add(item)
        await self.s.commit()
        await self.s.refresh(item)
        return item
        
    async def update_item(self, in_wishlist: 'Wishlist', item: 'Item', data: 'ItemPartialUpdate', as_user: UserType = NoUser) -> 'Item':
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        self.s.add(item.copy(update=data.dict(exclude_unset=True)))
        await self.s.commit()
        await self.s.refresh(item)
        return item

    async def delete_item(self, in_wishlist: 'Wishlist', item: 'Item', as_user: UserType = NoUser) -> None:
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        await self.s.delete(item)
        await self.s.commit()

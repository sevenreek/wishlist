from fastapi import HTTPException, status, Depends
from sqlalchemy import delete, select, func
from typing import TYPE_CHECKING, Optional, Union
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.orm import selectinload

from app.models.reservation import (
    ReservationCreate,
    ReservationOut,
    ReservationPartialUpdate,
)

from ..constants import errors
from ..utils.slugs import DEFAULT_SLUG_UNIQUENESS_ATTEMPTS
from .crud import BaseCRUD
from ..config import settings
from ..models import UsersWishlists, Reservation
from ..models.wishlist import Wishlist, WishlistCreate, WishlistPartialUpdate
from ..models.item import Item, ItemCreate, ItemPartialUpdate, ItemOut

if TYPE_CHECKING:
    from ..models import User


class WishlistCRUD(BaseCRUD):
    async def get(self, id: int) -> Wishlist:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.id == id).limit(1)
        )
        if (result := result.scalar_one_or_none()) is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail=errors.RECORD_NOT_FOUND)

    async def get_by_slug(self, slug: str) -> Wishlist:
        result = await self.s.execute(
            select(Wishlist).where(Wishlist.slug == slug).limit(1)
        )
        if (result := result.scalar_one_or_none()) is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail=errors.RECORD_NOT_FOUND)

    async def create(
        self,
        data: WishlistCreate,
        user: "User",
        *,
        slug_unique_attempts=DEFAULT_SLUG_UNIQUENESS_ATTEMPTS,
    ) -> Wishlist:
        slug_unique_attempts = slug_unique_attempts if slug_unique_attempts > 0 else 1
        for _ in range(slug_unique_attempts):
            wishlist = Wishlist(**data.dict(), users=[user])
            self.s.add(wishlist)
            try:
                await self.s.flush()
                await self.s.refresh(wishlist)
            except UniqueViolationError:
                continue
            else:
                return wishlist
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=errors.UNIQUE_GENERATION_FAILED,
        )

    async def index_for_user(self, user: "User") -> list[Wishlist]:
        result = await self.s.execute(
            select(Wishlist)
            .join(UsersWishlists)
            .where(UsersWishlists.user_id == user.id)
        )
        return result.scalars().all()

    async def update(
        self, wishlist: "Wishlist", data: WishlistPartialUpdate, as_user: "User"
    ) -> Wishlist:
        await self._ensure_user_can_modify_wishlist(wishlist, as_user)
        wishlist.update(**data.dict(exclude_unset=True))
        self.s.add(wishlist)
        return wishlist

    async def _ensure_user_can_modify_wishlist(
        self, wishlist: "Wishlist", user: "User"
    ) -> None:
        result = await self.s.execute(
            select(UsersWishlists)
            .where(
                UsersWishlists.user_id == user.id
            )  # pyright: ignore // if user is NoUser return on first line
            .where(UsersWishlists.wishlist_id == wishlist.id)
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=errors.INSUFFICIENT_ACCESS
            )

    async def delete(self, wishlist: "Wishlist", as_user: "User") -> None:
        await self._ensure_user_can_modify_wishlist(wishlist, as_user)
        await self.s.delete(wishlist)
        await self.s.flush()

    # Items
    async def get_item(self, wishlist: "Wishlist", item_id: int) -> Item:
        result = await self.s.execute(
            select(Item)
            .options(selectinload(Item.reservations))
            .where(Item.wishlist_id == wishlist.id)
            .where(Item.id == item_id)
        )
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.RECORD_NOT_FOUND
            )
        return result

    async def index_wishlist_items(
        self,
        wishlist: "Wishlist",
        *,
        offset=0,
        limit=settings.wishlist_items_limit,
        order_by=Item.created_at,
    ) -> list["ItemOut"]:
        stmt = (
            select(Item, func.count(Reservation.id).label("reserved"))
            .where(Item.wishlist_id == wishlist.id)
            .order_by(order_by)
            .outerjoin(Reservation)
            .group_by(Item.id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.s.execute(stmt)
        rows = result.all()
        items = [
            ItemOut(**row["Item"].dict(), reserved=row["reserved"]) for row in rows
        ]
        return items

    async def create_item(
        self, in_wishlist: "Wishlist", data: "ItemCreate", as_user: "User"
    ) -> "Item":
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        item = Item(**data.dict(), wishlist=in_wishlist)
        self.s.add(item)
        return item

    async def update_item(
        self,
        in_wishlist: "Wishlist",
        item: "Item",
        data: "ItemPartialUpdate",
        as_user: "User",
    ) -> "Item":
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        self.s.add(item.update(**data.dict(exclude_unset=True)))
        return item

    async def delete_item(
        self, in_wishlist: "Wishlist", item: "Item", as_user: "User"
    ) -> None:
        await self._ensure_user_can_modify_wishlist(in_wishlist, as_user)
        await self.s.delete(item)
        await self.s.flush()

    # Reservation
    async def _ensure_user_can_modify_reservation(
        self, reservation: Reservation, user: "User"
    ) -> None:
        result = await self.s.execute(
            select(Reservation)
            .where(Reservation.id == reservation.id)
            .where(Reservation.reserved_by_id == user.id)  # pyright: ignore
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=errors.INSUFFICIENT_ACCESS
            )

    async def create_reservation(
        self, reservation_data: ReservationCreate, item: Item, as_user: "User"
    ) -> Reservation:
        current_reservation_count = sum((r.count for r in item.reservations))
        if current_reservation_count + reservation_data.count > item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.RESERVATION_INVALID_COUNT,
            )
        reservation = Reservation(
            item=item, reserved_by=as_user, **reservation_data.dict()
        )
        self.s.add(reservation)
        await self.s.flush()
        return reservation

    async def update_reservation(
        self,
        reservation: Reservation,
        data: ReservationPartialUpdate,
        item: Item,
        as_user: "User",
    ) -> Reservation:
        await self._ensure_user_can_modify_reservation(reservation, as_user)
        current_reservation_count = sum((r.count for r in item.reservations))
        new_reservation_count = (
            current_reservation_count - reservation.count + data.count
        )
        if new_reservation_count < 0 or new_reservation_count > item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.RESERVATION_INVALID_COUNT,
            )
        reservation.update(**data.dict(exclude_unset=True))
        self.s.add(reservation)
        await self.s.flush()
        return reservation

    async def delete_reservation(
        self, reservation: Reservation, as_user: "User"
    ) -> None:
        await self._ensure_user_can_modify_reservation(reservation, as_user)
        await self.s.delete(reservation)
        await self.s.flush()

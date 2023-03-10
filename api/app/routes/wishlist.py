from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import BaseModel


from ..utils.deps import get_current_user
from ..models.wishlist import WishlistCreate, WishlistIndexRead, WishlistRead, WishlistPartialUpdate
from ..models.item import ItemCreate, ItemDetailOut, ItemOut, ItemPartialUpdate
from ..models.reservation import (
    ReservationCreate,
    ReservationOut,
    ReservationPartialUpdate,
)
from ..models import User
from ..crud import WishlistCRUD
from ..config import settings
from ..utils import clamp

router = APIRouter(prefix="/lists", tags=["wishlist"])




# Wishlist


@router.get("/{slug}", response_model=WishlistIndexRead)
async def details(
    slug: str,
    page: int = 1,
    limit: int = settings.wishlist_items_limit,
    Wishlists: WishlistCRUD = Depends(),
) -> WishlistIndexRead:

    page = max(1, page)
    limit = clamp(1, limit, settings.wishlist_items_limit_max)
    offset = (page - 1) * limit
    wishlist = await Wishlists.get_by_slug(slug)
    items = await Wishlists.index_wishlist_items(wishlist, offset=offset, limit=limit)
    return WishlistIndexRead(**wishlist.dict(), items=items)


@router.patch("/{slug}", response_model=WishlistRead)
async def update(
    slug: str,
    data: WishlistPartialUpdate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    wishlist = await Wishlists.update(wishlist, data, user)
    await Wishlists.commit()
    return WishlistRead(**wishlist.dict())


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    slug: str,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    await Wishlists.delete(wishlist, user)
    await Wishlists.commit()


@router.post("/", response_model=WishlistRead)
async def create(
    data: WishlistCreate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.create(data, user)
    await Wishlists.commit()
    return WishlistRead(**wishlist.dict())


@router.get("/", response_model=List[WishlistRead])
async def index(
    Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)
):
    return await Wishlists.index_for_user(user)


# Items


@router.get("/{slug}/items/{item_id}", response_model=ItemDetailOut)
async def item_details(slug: str, item_id: int, Wishlists: WishlistCRUD = Depends()):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    return item


@router.post("/{slug}/items", response_model=ItemOut)
async def create_item(
    slug: str,
    data: ItemCreate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.create_item(wishlist, data, user)
    await Wishlists.commit()
    return ItemOut(**item.dict(), reserved=0)


@router.patch("/{slug}/items/{item_id}", response_model=ItemOut)
async def update_item(
    slug: str,
    item_id: int,
    data: ItemPartialUpdate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    item = await Wishlists.update_item(wishlist, item, data, user)
    await Wishlists.commit()
    return ItemOut(**item.dict(), reserved=len(item.reservations))


@router.delete("/{slug}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    slug: str,
    item_id: int,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    await Wishlists.delete_item(wishlist, item, user)
    await Wishlists.commit()


# Reservations


@router.post("/{slug}/items/{item_id}/reservations", response_model=ReservationOut)
async def create_reservation(
    slug: str,
    item_id: int,
    data: ReservationCreate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    reservation = await Wishlists.create_reservation(data, item, user)
    return ReservationOut(**reservation.dict())


@router.delete(
    "/{slug}/items/{item_id}/reservations/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reservation(
    slug: str,
    item_id: int,
    reservation_id: int,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    reservation = await Wishlists.get_reservation(reservation_id)
    await Wishlists.delete_reservation(reservation, user)


@router.patch(
    "/{slug}/items/{item_id}/reservations/{reservation_id}",
    response_model=ReservationOut,
)
async def update_reservation(
    slug: str,
    item_id: int,
    reservation_id: int,
    data: ReservationPartialUpdate,
    Wishlists: WishlistCRUD = Depends(),
    user: User = Depends(get_current_user),
):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    reservation = await Wishlists.get_reservation(reservation_id)
    reservation = await Wishlists.update_reservation(reservation, data, item, user)
    return ReservationOut(**reservation.dict())

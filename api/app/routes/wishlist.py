from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import BaseModel

from ..utils.deps import get_current_user
from ..models.wishlist import WishlistCreate, WishlistRead, WishlistPartialUpdate
from ..models.item import Item, ItemCreate, ItemOut, ItemPartialUpdate
from ..models import User
from ..crud import WishlistCRUD
from ..config import settings
from ..utils import clamp

router = APIRouter(
    prefix='/lists',
    tags=['wishlist']
)

class WishlistContent(BaseModel):
    wishlist : WishlistRead
    items: List[ItemOut]

# Wishlist 

@router.get("/{slug}", response_model=WishlistContent)
async def details(
    slug: str,
    page:int=1,
    limit:int=settings.wishlist_items_limit,
    Wishlists: WishlistCRUD = Depends()
) -> WishlistContent:

    page = max(1, page)
    limit = clamp(1, limit, settings.wishlist_items_limit_max)
    offset = (page-1) * limit 
    wishlist = await Wishlists.get_by_slug(slug)
    items = await Wishlists.index_wishlist_items(wishlist, offset=offset, limit=limit)
    r_wishlist = WishlistRead(**wishlist.dict())
    return WishlistContent(wishlist=r_wishlist, items=items)

@router.patch("/{slug}", response_model=WishlistRead)
async def update(slug: str, data: WishlistPartialUpdate, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    wishlist = await Wishlists.update(wishlist, data, user)
    return WishlistRead(**wishlist.dict())
    
@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(slug: str, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    await Wishlists.delete(wishlist, user)

@router.post("/", response_model=WishlistRead)
async def create(data: WishlistCreate, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.create(data, user)
    return WishlistRead(**wishlist.dict())
    
@router.get("/", response_model=List[WishlistRead])
async def index(Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    return await Wishlists.index_for_user(user)

# Items

@router.get("/{slug}/item/{item_id}", response_model=ItemOut)
async def item_details(slug: str, item_id: int, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    return ItemOut(**item.dict())

@router.post("/{slug}/item", response_model=ItemOut)
async def create_item(slug: str, data: ItemCreate, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.create_item(wishlist, data, user)
    return ItemOut(**item.dict())
    
@router.patch("/{slug}/item/{item_id}", response_model=ItemOut)
async def update_item(slug: str, item_id: int, data: ItemPartialUpdate, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    item = await Wishlists.update_item(wishlist, item, data, user)
    return ItemOut(**item.dict())
    
@router.delete("/{slug}/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(slug: str, item_id: int, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    item = await Wishlists.get_item(wishlist, item_id)
    await Wishlists.delete_item(wishlist, item, user)
   

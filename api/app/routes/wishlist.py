from fastapi import APIRouter, Depends
from typing import List

from ..utils.deps import get_current_user
from ..models.wishlist import Wishlist, WishlistCreate, WishlistRead, WishlistCRUD
from ..models import User

router = APIRouter(
    prefix='/lists',
    tags=['wishlist']
)


@router.get("/{slug}", response_model=WishlistRead)
async def details(slug: str, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.get_by_slug(slug)
    return WishlistRead(**wishlist.dict())
    
@router.post("/", response_model=WishlistRead)
async def create(data: WishlistCreate, Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    wishlist = await Wishlists.create(data, user)
    return WishlistRead(**wishlist.dict())
    
@router.get("/", response_model=List[WishlistRead])
async def index(Wishlists: WishlistCRUD = Depends(), user: User = Depends(get_current_user)):
    return await Wishlists.index_for_user(user)

    
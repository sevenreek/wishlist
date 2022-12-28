from fastapi import APIRouter

from app.models.wishlist import Wishlist, WishlistCreate, WishlistRead, WishlistCRUD

router = APIRouter(
    prefix='/wishlist',
    tags=['wishlist']
)


@router.get("/{slug}")
async def index():
    pass

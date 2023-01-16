from pydantic import AnyUrl
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

from ..utils.slugs import generate_wishlist_slug

if TYPE_CHECKING:
    from app.models import Item, User

from .users_wishlists import UsersWishlists

class WishlistBase(SQLModel):
    name: str = Field(index=True)
    image_url: AnyUrl | None
    description: str | None
    

class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True, default_factory=generate_wishlist_slug)
    items: list['Item'] = Relationship(back_populates='wishlist')
    users: list['User'] = Relationship(
        back_populates='wishlists', 
        link_model=UsersWishlists
    )

class WishlistCreate(WishlistBase):
    pass

class WishlistRead(Wishlist):
    pass

class WishlistPartialUpdate(WishlistBase):
    __annotations__ = {k: Optional[v] for k, v in WishlistBase.__annotations__.items()}

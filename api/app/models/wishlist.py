from pydantic import AnyUrl
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional


from ..utils.slugs import generate_wishlist_slug
from .updateable import Updateable
from app.models.item import ItemOut

if TYPE_CHECKING:
    from app.models import Item, User


from .users_wishlists import UsersWishlists

class WishlistBase(Updateable):
    name: str = Field(index=True)
    image_url: AnyUrl | None
    description: str | None
    

class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True, default_factory=generate_wishlist_slug)
    items: list['Item'] = Relationship(
        back_populates='wishlist',
        sa_relationship_kwargs={"cascade": "all,delete"},
    )
    users: list['User'] = Relationship(
        back_populates='wishlists', 
        link_model=UsersWishlists,
        sa_relationship_kwargs={"cascade": "all,delete"},
    )

class WishlistCreate(WishlistBase):
    id: int

class WishlistRead(WishlistBase):
    id: int
    slug: str

class WishlistIndexRead(WishlistRead):
    items: list['ItemOut']

class WishlistPartialUpdate(WishlistBase):
    __annotations__ = {k: Optional[v] for k, v in WishlistBase.__annotations__.items()}

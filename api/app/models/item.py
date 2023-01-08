from sqlmodel import Field, Relationship
from pydantic import AnyUrl
from typing import TYPE_CHECKING, Optional

from .utils import Timestamped

if TYPE_CHECKING:
    from ..models import Wishlist, Reservation

class ItemBase(Timestamped):
    name: str = Field(index=True)
    image_url: AnyUrl | None
    shop_url: AnyUrl | None
    description: str | None
    quantity: int = 1
    price: int | None = None
    priority: int | None = None

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wishlist_id: int = Field(foreign_key="wishlist.id")
    wishlist: 'Wishlist' = Relationship(back_populates='items')
    reservations: list['Reservation'] = Relationship(back_populates='item')

class ItemCreate(ItemBase):
    pass

class ItemRead(Item):
    pass

class ItemOut(ItemRead):
    reserved: int

class ItemPartialUpdate(ItemBase):
    __annotations__ = {k: Optional[v] for k, v in ItemBase.__annotations__.items()}

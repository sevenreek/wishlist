from sqlmodel import Field, Relationship
from pydantic import AnyUrl
from typing import TYPE_CHECKING, Optional


from .utils import Timestamped

if TYPE_CHECKING:
    from ..models import Wishlist, Reservation
from ..models.reservation import ReservationRead
from ..models.updateable import Updateable

class ItemBase(Timestamped, Updateable):
    name: str = Field(index=True)
    image_url: AnyUrl | None
    shop_url: AnyUrl | None
    description: str | None
    quantity: int = 1
    price: int | None = None
    priority: int | None = Field(default=None, ge=0, le=4) 

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wishlist_id: int = Field(foreign_key="wishlist.id")
    wishlist: 'Wishlist' = Relationship(back_populates='items')
    reservations: list['Reservation'] = Relationship(back_populates='item', sa_relationship_kwargs={"cascade": "all,delete"})

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    reserved: int

class ItemDetailOut(ItemBase):
    id: int
    reservations: list['ReservationRead']

class ItemPartialUpdate(ItemBase):
    __annotations__ = {k: Optional[v] for k, v in ItemBase.__annotations__.items()}

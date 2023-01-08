from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

from .utils import Timestamped

if TYPE_CHECKING:
    from ..models import Item, User

class ReservationBase(Timestamped):
    count: int = 1
    reserved_by_name: str | None = None

class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    item: 'Item' = Relationship(back_populates='reservations')
    reserved_by_id: int = Field(foreign_key="user.id")
    reserved_by: 'User' = Relationship()

class ReservationCreate(ReservationBase):
    wishlist_slug: str
    item_slug: str

class ReservationRead(Reservation):
    pass


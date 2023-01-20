from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional

from .utils import Timestamped
from ..models.updateable import Updateable
if TYPE_CHECKING:
    from ..models import Item, User

class ReservationBase(Timestamped, Updateable):
    count: int = Field(default=1, ge=1)
    reserved_by_name: str | None = None

class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    item: 'Item' = Relationship(back_populates='reservations')
    reserved_by_id: int | None = Field(foreign_key="user.id")
    reserved_by: Optional['User'] = Relationship()

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int

class ReservationPartialUpdate(ReservationBase):
    __annotations__ = {k: Optional[v] for k, v in ReservationBase.__annotations__.items()}

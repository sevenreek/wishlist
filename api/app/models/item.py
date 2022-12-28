from sqlmodel import SQLModel, Field, Relationship
from pydantic import FileUrl
from typing import TYPE_CHECKING

from .crud import BaseCRUD

if TYPE_CHECKING:
    from app.models import Wishlist
class ItemBase(SQLModel):
    name: str = Field(index=True)
    image_url: FileUrl | None
    description: str | None
    quantity: int = 1
    price: int | None = None
    priority: int | None = None

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wishlist_id: int = Field(foreign_key="wishlist.id", primary_key=True)
    wishlist: 'Wishlist' = Relationship(back_populates='items')

class ItemCreate(ItemBase):
    pass

class ItemRead(Item):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemCRUD(BaseCRUD):
    pass
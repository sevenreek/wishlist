from sqlmodel import SQLModel, Field
from crud import BaseCRUD

class ItemBase(SQLModel):
    name: str = Field(index=True)
    description: str | None
    quantity: int = 1
    price: int | None = None
    priority: int | None = None
    reserved: int = 0

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ItemInput(ItemBase):
    pass

class ItemOutput(Item):
    pass

class ItemCRUD(BaseCRUD[Item]):
    pass
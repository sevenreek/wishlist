from pydantic import AnyUrl
from sqlmodel import SQLModel, Field

class WishlistBase(SQLModel):
    name: str = Field(index=True)
    image_url: AnyUrl | None
    description: str | None
    user_id: int = Field(foreign_key=)

class Wishlist(WishlistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class WishlistInput(WishlistBase):
    pass

class WishlistOutput(Wishlist):
    pass
from sqlmodel import SQLModel, Field

class UsersWishlists(SQLModel, table=True):
    user_id: int = Field(foreign_key='user.id', primary_key=True)
    wishlist_id: int = Field(foreign_key='wishlist.id', primary_key=True)

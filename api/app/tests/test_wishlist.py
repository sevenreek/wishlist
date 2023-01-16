import pytest
from sqlalchemy import select

from app.models import Wishlist, Item, UsersWishlists, Reservation
from ..models.item import ItemOut
from ..models.wishlist import WishlistRead
from .fixtures import *
from .factories import *

@pytest.mark.asyncio
async def test_details(aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], Items: ModelFactory[Item]):
    wishlist = await Wishlists.create(items=[])
    items = await Items.create_list(5, wishlist_id=wishlist.id)
    await asession.commit()
    response = await aclient.get(
        f"/lists/{wishlist.slug}"
    )
    assert response.status_code == 200
    data = response.json()
    obtained_wishlist = WishlistRead(**data['wishlist'])
    obtained_items = [ItemOut(**item) for item in data['items']]
    assert obtained_wishlist == wishlist
    for item in obtained_items:
        assert any((ItemOut(**actual_item.dict(), reserved=0) == item for actual_item in items))

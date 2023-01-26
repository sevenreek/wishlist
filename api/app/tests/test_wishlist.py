import pytest
from sqlalchemy import select

from app.models import Wishlist, Item, UsersWishlists, Reservation
from ..models.item import ItemOut
from ..models.wishlist import WishlistRead
from .fixtures import *
from .factories import *

class TestWishlist():
    @pytest.mark.asyncio
    async def test_details(self, aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], Items: ModelFactory[Item]):
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

    @pytest.mark.asyncio
    async def test_details_paging(self, aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], Items: ModelFactory[Item]):
        wishlist = await Wishlists.create(items=[])
        items = await Items.create_list(20, wishlist_id=wishlist.id)
        await asession.commit()
        response = await aclient.get(
            f"/lists/{wishlist.slug}?page=1&limit=5"
        )
        assert response.status_code == 200
        data = response.json()
        obtained_wishlist = WishlistRead(**data['wishlist'])
        obtained_items = [ItemOut(**item) for item in data['items']]
        assert obtained_wishlist == wishlist
        for item in obtained_items:
            assert any((ItemOut(**actual_item.dict(), reserved=0) == item for actual_item in items[:5]))

        response = await aclient.get(
            f"/lists/{wishlist.slug}?page=2&limit=5"
        )
        data = response.json()
        obtained_wishlist = WishlistRead(**data['wishlist'])
        obtained_items = [ItemOut(**item) for item in data['items']]
        assert obtained_wishlist == wishlist
        for item in obtained_items:
            assert any((ItemOut(**actual_item.dict(), reserved=0) == item for actual_item in items[5:10]))

    @pytest.mark.asyncio
    async def test_update(self, aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], user_auth: UserAuth):
        wishlist = await Wishlists.create(users=[user_auth.user])
        await asession.commit()
        update_data={
            'name':'Updated wishlist',
            'image_url': 'https://example.com/modified',
            'description': 'New description',
        }
        response = await aclient.patch(
            f"/lists/{wishlist.slug}",
            json=update_data,
            headers={'Authorization': 'Bearer ' + user_auth.token},
        )
        assert response.status_code == 200
        data = response.json()
        for k in update_data:
            assert data[k] == update_data[k]

    @pytest.mark.asyncio
    async def test_create(self, aclient: AsyncClient, asession: AsyncSession, user_auth: UserAuth):
        create_data={
            'name':'New wishlist',
            'image_url': 'https://example.com/',
            'description': 'New description',
        }
        response = await aclient.post(
            f"/lists",
            json=create_data,
            headers={'Authorization': 'Bearer ' + user_auth.token},
        )
        assert response.status_code == 200
        data = response.json()
        for k in create_data:
            assert data[k] == create_data[k]
        wishlist_in_db = await asession.execute(select(Wishlist))
        wishlist_in_db = wishlist_in_db.one()['Wishlist'].dict()
        for k in create_data:
            assert wishlist_in_db[k] == create_data[k]

    @pytest.mark.asyncio
    async def test_delete(self, aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], user_auth: UserAuth):
        wishlist = await Wishlists.create(users=[user_auth.user])
        await asession.commit()
        response = await aclient.delete(
            f"/lists/{wishlist.slug}",
            headers={'Authorization': 'Bearer ' + user_auth.token},
        )
        assert response.status_code == 204
        db_content = await asession.execute(select(Wishlist))
        assert db_content.fetchone() == None
        db_content = await asession.execute(select(UsersWishlists))
        assert db_content.fetchone() == None

    @pytest.mark.asyncio
    async def test_index(self, aclient: AsyncClient, asession: AsyncSession, Wishlists: ModelFactory[Wishlist], user_auth: UserAuth):
        wishlists = await Wishlists.create_list(10, users=[user_auth.user])
        await asession.commit()
        response = await aclient.get(
            f"/lists",
            headers={'Authorization': 'Bearer ' + user_auth.token},
        )
        assert response.status_code == 200
        data = response.json()
        assert {w.id for w in wishlists} == {w['id'] for w in data}

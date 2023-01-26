import pytest
from sqlalchemy import select
import random

from app.models import Wishlist, Item, UsersWishlists, Reservation
from ..models.item import ItemOut
from ..models.wishlist import WishlistRead
from .fixtures import *
from .factories import *

class TestItems():
    @pytest.mark.asyncio
    async def test_details(
            self,
            aclient: AsyncClient,
            asession: AsyncSession,
            Wishlists: ModelFactory[Wishlist],
            Items: ModelFactory[Item],
            Reservations: ModelFactory[Reservation],
            Users: ModelFactory[User]
        ):
        users = await Users.create_list(2)
        wishlist = await Wishlists.create(items=[])
        item = await Items.create(wishlist_id=wishlist.id, count=3)
        reservations = await Reservations.create_list(2, item=item, user=random.choice(users))
        await asession.commit()
        response = await aclient.get(
            f"/lists/{wishlist.slug}/items/{item.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert item.id == data['id']
        assert {r['id'] for r in data['reservations']} == {r.id for r in reservations}

    @pytest.mark.asyncio
    async def test_create(
            self,
            aclient: AsyncClient,
            asession: AsyncSession,
            Wishlists: ModelFactory[Wishlist],
            user_auth: UserAuth
        ):
        wishlist = await Wishlists.create(users=[user_auth.user])
        await asession.commit()
        input_data={
            'name': 'item',
            'image_url': 'http://example.com',
            'shop_url': 'http://shop.example',
            'description': 'description',
            'quantity': 2,
            'price': 100,
            'priority': 3
        }
        response = await aclient.post(
            f"/lists/{wishlist.slug}/items",
            headers={'Authorization': 'Bearer ' + user_auth.token},
            json=input_data
        )
        assert response.status_code == 200
        output_data = response.json()
        for k in input_data:
            assert input_data[k] == output_data[k]

    @pytest.mark.asyncio
    async def test_update(
            self,
            aclient: AsyncClient,
            asession: AsyncSession,
            Wishlists: ModelFactory[Wishlist],
            Items: ModelFactory[Item],
            user_auth: UserAuth
        ):
        wishlist = await Wishlists.create(users=[user_auth.user], items=[])
        item = await Items.create(wishlist=wishlist)
        await asession.commit()
        input_data={
            'name': 'changed item',
            'image_url': 'http://example.com/2',
            'shop_url': 'http://shop.example/2',
            'description': 'changed description',
            'quantity': 7,
            'price': 900,
            'priority': 1
        }
        response = await aclient.patch(
            f"/lists/{wishlist.slug}/items/{item.id}",
            headers={'Authorization': 'Bearer ' + user_auth.token},
            json=input_data
        )
        assert response.status_code == 200
        output_data = response.json()
        for k in input_data:
            assert input_data[k] == output_data[k]

    @pytest.mark.asyncio
    async def test_delete(
            self,
            aclient: AsyncClient,
            asession: AsyncSession,
            Wishlists: ModelFactory[Wishlist],
            Items: ModelFactory[Item],
            user_auth: UserAuth
        ):
        wishlist = await Wishlists.create(users=[user_auth.user], items=[])
        item = await Items.create(wishlist=wishlist)
        await asession.commit()
        response = await aclient.delete(
            f"/lists/{wishlist.slug}/items/{item.id}",
            headers={'Authorization': 'Bearer ' + user_auth.token}
        )
        assert response.status_code == 204
        item_in_db = await asession.execute(select(Item))
        assert item_in_db.fetchone() is None

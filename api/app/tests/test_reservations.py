import pytest
from sqlalchemy import select
import random

from app.models import Wishlist, Item, UsersWishlists, Reservation
from .fixtures import *
from .factories import *


class TestReservations:
    @pytest.mark.asyncio
    async def test_create(
        self,
        aclient: AsyncClient,
        asession: AsyncSession,
        Wishlists: ModelFactory[Wishlist],
        Items: ModelFactory[Item],
        Users: ModelFactory[User],
        user_auth: UserAuth
    ):
        owner = await Users.create()
        wishlist = await Wishlists.create(users=[owner])
        item = await Items.create(quantity=2, wishlist=wishlist)
        await asession.commit()
        input_data={
            'count': 1,
            'reserved_by_name': 'John Doe'
        }
        response = await aclient.post(
            f"/lists/{wishlist.slug}/items/{item.id}/reservations",
            headers={'Authorization': 'Bearer ' + user_auth.token},
            json=input_data
        )
        assert response.status_code == 200
        output_data = response.json()
        for k,v in input_data.items():
            assert output_data[k] == v
        reservation_db = await asession.execute(
            select(Reservation)
        )
        reservation_db = reservation_db.one()['Reservation'].dict()
        for k,v in input_data.items():
            assert reservation_db[k] == v


    @pytest.mark.asyncio
    async def test_delete(
        self,
        aclient: AsyncClient,
        asession: AsyncSession,
        Wishlists: ModelFactory[Wishlist],
        Items: ModelFactory[Item],
        Reservations: ModelFactory[Reservation],
        Users: ModelFactory[User],
        user_auth: UserAuth
    ):
        owner = await Users.create()
        wishlist = await Wishlists.create(users=[owner])
        item = await Items.create(quantity=2, wishlist=wishlist)
        reservation = await Reservations.create(item=item, reserved_by=user_auth.user)
        await asession.commit()
        response = await aclient.delete(
            f"/lists/{wishlist.slug}/items/{item.id}/reservations/{reservation.id}",
            headers={'Authorization': 'Bearer ' + user_auth.token}
        )
        assert response.status_code == 204
        reservation_db = await asession.execute(
            select(Reservation)
        )
        assert reservation_db.fetchone() == None

    @pytest.mark.asyncio
    async def test_patch(
        self,
        aclient: AsyncClient,
        asession: AsyncSession,
        Wishlists: ModelFactory[Wishlist],
        Items: ModelFactory[Item],
        Users: ModelFactory[User],
        Reservations: ModelFactory[Reservation],
        user_auth: UserAuth
    ):
        owner = await Users.create()
        wishlist = await Wishlists.create(users=[owner])
        item = await Items.create(quantity=10, wishlist=wishlist)
        reservation = await Reservations.create(item=item, reserved_by=user_auth.user)
        await asession.commit()
        input_data={
            'count': 8,
            'reserved_by_name': 'Jane Doe'
        }
        response = await aclient.patch(
            f"/lists/{wishlist.slug}/items/{item.id}/reservations/{reservation.id}",
            headers={'Authorization': 'Bearer ' + user_auth.token},
            json=input_data
        )
        assert response.status_code == 200
        output_data = response.json()
        for k,v in input_data.items():
            assert output_data[k] == v
        reservation_db = await asession.execute(
            select(Reservation)
        )
        reservation_db = reservation_db.one()['Reservation'].dict()
        for k,v in input_data.items():
            assert reservation_db[k] == v

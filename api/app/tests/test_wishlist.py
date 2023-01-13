from typing import AsyncIterable
from uuid import UUID
import pytest
from sqlalchemy import select

from app.models import Wishlist
from .fixtures import *

@pytest.fixture(name="Wishlists")
async def wishlist_factory_fixture(user: User, asession: AsyncSession) -> Wishlist:
    w = Wishlist(
        name="name",
        image_url="http://example.com", #pyright: ignore
        description="description",
        users=[user],
        items=[
        ]
    )
    asession.add(w)
    await asession.commit()
    await asession.refresh(w)
    return w

@pytest.mark.asyncio
async def test_details(aclient: AsyncClient, user: User):
    response = await aclient.post(
        "/auth/login",
        data={
            'grant_type': 'password',
            'username': 'user@example.com',
            'password': 'password',
        }
    )
    assert response.status_code == 200
    data = response.json()
    response_user = UserOut(**data['user'])
    user_in_db = UserOut(**user.dict())
    assert response_user == user_in_db
    assert data['access_token']
    assert data['refresh_token']

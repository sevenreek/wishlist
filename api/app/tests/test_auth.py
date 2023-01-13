from typing import AsyncIterable
from uuid import UUID
import pytest
from sqlalchemy import select

from app.models.user import User, UserOut
from app.utils.auth import hash_password
from .fixtures import *

@pytest.mark.asyncio
async def test_signup(aclient: AsyncClient, asession: AsyncSession):
    response = await aclient.post(
        "/auth/signup",
        json={
            'email': 'mail@mail.com',
            'username': 'username',
            'password': 'password',
            'first_name': 'John',
            'last_name': 'Doe',
            'avatar_url': 'http://example.com/',
        }
    )
    assert response.status_code == 200
    data = response.json()
    user_in_db = await asession.execute(select(User).limit(1))
    user_in_db = user_in_db.fetchone()
    assert user_in_db is not None
    for k,v in {
        'id': 1,
        'email': 'mail@mail.com',
        'username': 'username',
        'first_name': 'John',
        'last_name': 'Doe',
        'avatar_url': 'http://example.com/',
    }.items(): 
        assert data[k] == v
        assert user_in_db['User'].dict()[k] == v
    assert UUID(data['uuid']) 

@pytest.mark.asyncio
async def test_login(aclient: AsyncClient, user: User):
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

@pytest.mark.asyncio
async def test_asignup(aclient: AsyncClient, asession: AsyncSession):
    response = await aclient.post(
        "/auth/asignup"
    )
    assert response.status_code == 200
    response_user = UserOut(**response.json())
    user_in_db = await asession.execute(select(User).limit(1))
    user_in_db = user_in_db.fetchone()
    assert user_in_db is not None
    user_in_db = user_in_db['User'].dict()
    user_in_db = UserOut(**user_in_db)
    assert response_user == user_in_db


@pytest.mark.asyncio
async def test_alogin(aclient: AsyncClient, anon_user: User):
    response = await aclient.post(
        "/auth/alogin",
        json={
            'uuid': str(anon_user.uuid)
        }
    )
    assert response.status_code == 200
    data = response.json()
    response_user = UserOut(**data['user'])
    user_in_db = UserOut(**anon_user.dict())
    assert response_user == user_in_db
    assert data['access_token']
    assert data['refresh_token']


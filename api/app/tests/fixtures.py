from typing import AsyncIterable
import asyncio
import pytest
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..models.user import User
from ..utils.auth import create_access_token, hash_password
from ..main import app
from ..config import settings
from ..db import get_async_session

@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(name="asession")
async def async_session_fixture():
    db_url = settings.get_db_url(test=True)
    async_db_url = settings.get_async_db_url(test=True)

    if not database_exists(db_url):
        create_database(db_url)

    async_engine = create_async_engine(async_db_url, echo=False, future=True)

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    # drop_database(db_url)

@pytest.fixture(name="client")
async def client_fixture(asession: AsyncSession):
    async def get_session_override():
        return asession
    app.dependency_overrides[get_async_session] = get_session_override
    client = TestClient(app)
    yield client 
    app.dependency_overrides.clear() 

@pytest.fixture(name="aclient")
async def async_client_fixture(asession: AsyncSession):
    async def get_session_override():
        return asession
    app.dependency_overrides[get_async_session] = get_session_override
    aclient = AsyncClient(app=app, base_url='http://localhost:8000', follow_redirects=True)
    yield aclient 
    app.dependency_overrides.clear() 

@pytest.fixture(name="anon_auth")
async def anon_user_fixture(asession: AsyncSession) -> tuple[User,str]:
    u = User()
    asession.add(u)
    await asession.commit()
    await asession.refresh(u)
    return u, create_access_token(u.uuid)

@pytest.fixture(name="user_auth")
async def user_fixture(asession: AsyncSession) -> tuple[User,str]:
    u = User(
        email="user@example.com", # pyright: ignore
        username="username",
        first_name="John",
        last_name="Doe",
        password_hash=hash_password("password"),
        avatar_url="http://example.com" # pyright: ignore
    ) 
    asession.add(u)
    await asession.commit()
    await asession.refresh(u)
    return u, create_access_token(u.uuid)



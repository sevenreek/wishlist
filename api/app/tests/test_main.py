import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from .fixtures import *

@pytest.mark.asyncio
async def test_root(aclient: AsyncClient):
    response = await aclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

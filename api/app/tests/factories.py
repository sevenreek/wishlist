import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, TypeVar, Generic, Any
from sqlmodel import SQLModel
from inspect import signature
from faker import Faker
from ..models import Wishlist, User, Item
from ..config import settings
from ..utils.auth import hash_password

ModelType = TypeVar('ModelType')

class ModelFactory(Generic[ModelType]):
    def __init__(self, asession: AsyncSession, model_factory, defaults:dict[str, Any]={}):
        self.s = asession
        self.defaults = defaults
        self.model_factory = model_factory
        self.count = 0

    def __get_next_params(self, **kwargs) -> dict:
        next_params = {}
        for k,v in self.defaults.items():
            if not callable(v):
                next_params[k] = kwargs.get(k, v)
                continue
            param_count = len(signature(v).parameters)
            if param_count == 1:
                next_params[k] = v(self.count)
            elif param_count == 0:
                next_params[k] = v()
            else:
                raise TypeError(f"Default parameter factories must have 0 or 1 arguments. {k} had {param_count}.")
        self.count += 1
        return next_params
                
    async def create(self, **kwargs) -> ModelType:
        instance = self.model_factory(**self.__get_next_params(**kwargs))
        self.s.add(instance)
        await self.s.flush()
        return instance

    async def create_list(self, count, **kwargs) -> list[ModelType]:
        models = []
        for _ in range(count):
            instance = self.model_factory(**self.__get_next_params(**kwargs))
            self.s.add(instance)
            models.append(instance)
        await self.s.flush()
        return models


@pytest.fixture(name="Users")
async def user_factory_fixture(faker: Faker, asession: AsyncSession) -> ModelFactory[User]:
    defaults = {
        'email': lambda i: f"user{i}@mail.com",
        'username': lambda i: f"user{i}",
        'first_name': lambda: faker.first_name(),
        'last_name': lambda: faker.last_name(),
        'avatar_url': lambda i: f"https://picsum.photos/id/{200+i}/256/256",
        'password_hash': hash_password(settings.test_user_password),
    }
    return ModelFactory[User](asession, User, defaults)

@pytest.fixture(name="Wishlists")
async def wishlist_factory_fixture(faker: Faker, asession: AsyncSession) -> ModelFactory[Wishlist]:
    defaults = {
        'name': lambda: faker.word(part_of_speech="adjective").title() + " wishlist",
        'username': lambda i: f"user{i}",
        'first_name': lambda: faker.first_name(),
        'last_name': lambda: faker.last_name(),
        'avatar_url': lambda i: f"https://picsum.photos/id/{200+i}/256/256",
        'password_hash': hash_password(settings.test_user_password),
    }
    return ModelFactory[Wishlist](asession, Wishlist, defaults)

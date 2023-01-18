import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, TypeVar, Generic, Any
from sqlmodel import SQLModel
from inspect import signature
from faker import Faker
from random import randrange

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
        for fieldname in self.model_factory.__fields__.keys():
            default = self.defaults.get(fieldname, None)
            override = kwargs.get(fieldname, None)
            value = override or default
            if not callable(value):
                next_params[fieldname] = value
                continue
            param_count = len(signature(value).parameters)
            if param_count == 1:
                next_params[fieldname] = value(self.count)
            elif param_count == 0:
                next_params[fieldname] = value()
            else:
                raise TypeError(f"Default parameter factories must have 0 or 1 arguments. {fieldname} had {param_count}.")
        self.count += 1
        return kwargs | next_params
                
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
        'avatar_url': lambda i: f"https://picsum.photos/id/{1000+i}/256/256",
        'password_hash': hash_password(settings.test_user_password),
    }
    return ModelFactory[User](asession, User, defaults)

@pytest.fixture(name="Items")
async def item_factory_fixture(faker: Faker, asession: AsyncSession) -> ModelFactory[Item]:
    defaults = {
        'name': lambda: faker.word(part_of_speech="adjective").title() + " " + faker.word(part_of_speech="noun"),
        'image_url': lambda i: f"https://picsum.photos/id/{2000+i}/300/300",
        'description': lambda: faker.paragraph(nb_sentences=1),
        'shop_url': 'https://example.com',
        'price': lambda: randrange(10000),
        'priority': lambda: randrange(5),
    }
    return ModelFactory[Item](asession, Item, defaults)

@pytest.fixture(name="Wishlists")
async def wishlist_factory_fixture(faker: Faker, Items: ModelFactory[Item], asession: AsyncSession) -> ModelFactory[Wishlist]:
    defaults = {
        'name': lambda: faker.word(part_of_speech="adjective").title() + " wishlist",
        'image_url': lambda i: f"https://picsum.photos/id/{3000+i}/300/300",
        'description': lambda: faker.paragraph(),
    }
    return ModelFactory[Wishlist](asession, Wishlist, defaults)


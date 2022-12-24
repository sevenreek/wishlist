from typing import Generic, TypeVar, Self
from fastapi import Depends
from sqlmodel import Session
from app.db import get_async_session

G_SQL = TypeVar('G_SQL')

class BaseCRUD(Generic[G_SQL]):
    def __init__(self, session: Session):
        self.s = session

    @classmethod
    async def async_depend(cls, session: Session = Depends(get_async_session)) -> Self:
        breakpoint()
        return cls(session)

    def find(self, id) -> G_SQL | None:
        pass




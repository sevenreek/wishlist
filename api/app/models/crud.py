from typing import Self
from fastapi import Depends

from app.db import get_async_session, AsyncSession

class BaseCRUD():
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.s = session



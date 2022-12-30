from fastapi import Depends

from ..db import get_async_session, AsyncSession

class BaseCRUD():
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.s = session



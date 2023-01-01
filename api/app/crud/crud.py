from fastapi import Depends

from ..db import get_async_session, AsyncSession

NoUser = object()
class BaseCRUD():
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.s = session



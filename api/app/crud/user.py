from uuid import UUID
from sqlalchemy import select

from ..utils.auth import hash_password
from .crud import BaseCRUD

from ..models.user import UserCreate, User


class UserCRUD(BaseCRUD):
    async def find_by_email(self, email: str) -> User | None:
        user_coll = await self.s.execute(
            select(User).where(User.email == email)
        )
        return user_coll.scalar_one_or_none()

    async def find_by_uuid(self, uuid: str | UUID) -> User | None:
        user_coll = await self.s.execute(
            select(User).where(User.uuid == uuid)
        )
        return user_coll.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User:
        password_hash = hash_password(data.password)
        u = User(**data.dict(exclude={'password'}), password_hash=password_hash)
        self.s.add(u)
        await self.s.flush()
        return u
        
    async def create_anonymous(self) -> User:
        u = User()
        self.s.add(u)
        await self.s.flush()
        return u
        

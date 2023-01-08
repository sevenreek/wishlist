from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Any
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth =  OAuth2PasswordBearer(
    tokenUrl='/login',
    scheme_name='JWT'
)

class BaseToken(BaseModel):
    exp: datetime

class Token(BaseModel):
    content: Any
    exp: datetime

def hash_password(password: str) -> str:
    if not len(password): raise ValueError("Password cannot be empty")
    return password_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_context.verify(password, hashed)

def create_access_token(content: Any, expiry_minutes: int | None = None):
    expiry_minutes = expiry_minutes if expiry_minutes else settings.access_token_expiry
    expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    return jwt.encode(Token(content=content, exp=expiry).dict(), settings.jwt_secret_key, settings.jwt_algorithm)

def create_refresh_token(content: Any, expiry_minutes: int | None = None):
    expiry_minutes = expiry_minutes if expiry_minutes else settings.refresh_token_expiry
    expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    return jwt.encode(Token(content=content, exp=expiry).dict(), settings.jwt_refresh_secret_key, settings.jwt_algorithm)



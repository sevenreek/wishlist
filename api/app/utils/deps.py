from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError
from datetime import datetime, timezone

from ..config import settings
from ..models.user import UserCRUD, User
from ..constants import errors

from .auth import reusable_oauth, Token

async def get_current_user(token: str = Depends(reusable_oauth), Users: UserCRUD = Depends()) -> User:
    try: 
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        token_data = Token(**payload)
        if token_data.exp < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.TOKEN_EXPIRED, headers={"WWW-Authenticate": "Bearer"})
    except(jwt.JWTError, ValidationError) as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errors.CREDENTIALS_INVALID, headers={"WWW-Authenticate": "Bearer"})
    user = await Users.find_by_email(token_data.content)
    if user is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.RECORD_NOT_FOUND)
    return user
    
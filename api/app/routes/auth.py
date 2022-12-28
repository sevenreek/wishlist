from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.user import User, UserOut, UserCreate, UserCRUD
from ..constants import errors
from ..utils.auth import verify_password, create_access_token, create_refresh_token
from ..utils.deps import get_current_user

router = APIRouter(
    tags=['auth']
)

@router.post('/signup', response_model=UserOut)
async def signup(data: UserCreate, Users: UserCRUD = Depends()):
    existing_user = await Users.find_by_email(data.email)
    if existing_user is not None: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.USER_ALREADY_EXISTS)
    new_user = await Users.create_user(data)
    return UserOut(**new_user.dict())

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), Users: UserCRUD = Depends()):
    existing_user = await Users.find_by_email(form_data.username)
    if existing_user is None or not verify_password(form_data.password, existing_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.CREDENTIALS_INVALID)
    return {
        "access_token": create_access_token(existing_user.email),
        "refresh_token": create_refresh_token(existing_user.email),
    }
    
@router.get('/me', response_model=UserOut)
async def show_current_user(current_user: User = Depends(get_current_user)):
    return current_user.dict()



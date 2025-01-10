from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .dao import UsersDAO
from src.auth.dependencies import get_current_user
from src.auth.service import authenticate_user, create_jwt
from .exceptions import IncorrectDataException
from datetime import timedelta
from src.auth.config import TOKEN_EXPIRES_MINUTES
from .schemas import User, UserCreate, Token
from src.exceptions import NoPermissionsException

router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@router.post('/token', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectDataException
    access_token_expires = timedelta(minutes=TOKEN_EXPIRES_MINUTES)
    access_token = await create_jwt({'sub': user.username}, access_token_expires)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/me', response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/register', response_model=User, status_code=201)
async def register(user_data: UserCreate):
    new_user = await UsersDAO.register(user_data)
    return new_user


@router.get('/readers', response_model=list[User])
async def get_readers(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    readers = await UsersDAO.get_readers()
    return readers
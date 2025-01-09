from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from .dependencies import get_current_user
from .service import authenticate_user, create_jwt, hash_password
from .exceptions import IncorrectDataException, NotUniqueException
from datetime import timedelta
from .config import TOKEN_EXPIRES_MINUTES
from .schemas import Token, User, UserInDB
from src.database import async_session
from .models import User as UserOrm

router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectDataException
    access_token_expires = timedelta(minutes=TOKEN_EXPIRES_MINUTES)
    access_token = await create_jwt({'sub': user.username}, access_token_expires)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/me', response_model=User)
async def get_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post('/register', response_model=User)
async def register(new_user: UserInDB):
    try:
        async with async_session() as session:
            hashed_password = hash_password(new_user.hashed_password)
            user = UserOrm(username=new_user.username, hashed_password=hashed_password)
            session.add(user)
            await session.commit()
        return User(**new_user.model_dump())
    except IntegrityError:
        raise NotUniqueException
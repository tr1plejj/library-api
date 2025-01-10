from datetime import timedelta, datetime, timezone
import jwt
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import User
from .config import pwd_context
from .config import SECRET_KEY, ALGORITHM
from src.database import async_session


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    async with async_session() as session:
        query = select(User).filter_by(username=username).options(selectinload(User.books))
        user = await session.execute(query)
        return user.scalar()


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_jwt(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(5)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.dao import BaseDAO
from src.auth.models import User
from src.database import async_session
from src.auth.service import hash_password
from .exceptions import NotUniqueException


class UsersDAO(BaseDAO):

    model = User

    @classmethod
    async def register(cls, user_data):
        try:
            async with async_session() as session:
                async with session.begin():
                    hashed_password = hash_password(user_data.hashed_password)
                    new_user = User(username=user_data.username, hashed_password=hashed_password)
                    session.add(new_user)
                    await session.flush()
                    return jsonable_encoder(new_user)
        except IntegrityError:
            raise NotUniqueException

    @classmethod
    async def get_readers(cls):
        async with async_session() as session:
            query = (
                select(cls.model).
                filter_by(is_admin=False)
            )
            readers = await session.execute(query)
            return readers.scalars().all()
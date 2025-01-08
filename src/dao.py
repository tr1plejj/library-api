from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from .database import async_session
from .exceptions import NotFoundException


class BaseDAO:
    """
    Base Data Access Object to work with all models.
    """

    model = None

    @classmethod
    async def find_all(cls, **filters):
        """
        Finds all objects with filters.

        :return: List of all founded objects.
        """
        async with async_session() as session:
            query = (
                select(cls.model).
                filter_by(**filters)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filters):
        """
        Finds particular object with filters

        :return: Founded object.
        """
        async with async_session() as session:
            query = (
                select(cls.model).
                filter_by(**filters)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data):
        async with async_session() as session:
            async with session.begin():
                new_author = cls.model(**data)
                session.add(new_author)
                await session.flush()
                return jsonable_encoder(new_author)

    @classmethod
    async def delete(cls, object_id: int):
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    delete(cls.model).
                    filter_by(id=object_id)
                )
                await session.execute(stmt)
                return

    @classmethod
    async def update(cls, object_id: int, **values):
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(cls.model).
                    filter_by(id=object_id).
                    values(**values).
                    returning(cls.model.id)
                )
                changed_id = await session.execute(stmt)
                if changed_id.scalar() is None:
                    raise NotFoundException
                return


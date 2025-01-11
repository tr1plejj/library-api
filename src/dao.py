from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from .database import async_session
from .exceptions import NotFoundException, NoDataInsideException


class BaseDAO:
    """Base Data Access Object to work with all models."""

    model = None

    @classmethod
    async def find_all(cls, **filters):
        """
        Find all objects. Can apply filters.

        :param filters: dictionary with needed fields for filter objects
        :return: list of all founded objects
        :rtype: list
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
        Find object. Can apply filters.

        :param filters: dictionary with needed field for object
        :return: founded object
        """
        async with async_session() as session:
            query = (
                select(cls.model).
                filter_by(**filters)
            )
            result = await session.execute(query)
            obj = result.scalar_one_or_none()

            if obj is None:
                raise NotFoundException

            return obj

    @classmethod
    async def create(cls, **data):
        """
        Create new object.

        :param data: dictionary with required fields for object
        :return: new object
        """
        async with async_session() as session:
            async with session.begin():
                new_object = cls.model(**data)
                session.add(new_object)
                await session.flush()
                return jsonable_encoder(new_object)

    @classmethod
    async def delete(cls, object_id: int):
        """
        Delete object with given id.

        :return: void
        :rtype: None
        """
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    delete(cls.model).
                    filter_by(id=object_id).
                    returning(cls.model.id)
                )
                deleted_id = await session.execute(stmt)
                if deleted_id.scalar() is None:
                    raise NotFoundException
                return

    @classmethod
    async def update(cls, object_id: int, **values):
        """
        Update object with given id and values.

        :param values: dictionary with required values for update in object
        :return: void
        :rtype: None
        """
        update_values = {key: value for key, value in values.items() if value is not None}

        if not update_values:
            raise NoDataInsideException

        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(cls.model).
                    filter_by(id=object_id).
                    values(**update_values).
                    returning(cls.model.id)
                )
                changed_id = await session.execute(stmt)
                if changed_id.scalar() is None:
                    raise NotFoundException
                return


from sqlalchemy import select
from .database import async_session

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


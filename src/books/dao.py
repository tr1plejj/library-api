from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dao import BaseDAO
from .models import Book
from src.database import async_session


class BooksDAO(BaseDAO):

    model = Book

    @classmethod
    async def get_all_books(cls):
        async with async_session() as session:
            query = (
                select(cls.model).
                options(selectinload(cls.model.authors))
            )
            books = await session.execute(query)
            return books.scalars().all()

    @classmethod
    async def get_book(cls, book_id: int):
        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(id=book_id)
                .options(selectinload(cls.model.authors))
            )
            book = await session.execute(query)
            return book.scalar()

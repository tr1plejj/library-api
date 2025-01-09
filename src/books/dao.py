from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dao import BaseDAO
from .models import Book
from src.database import async_session
from src.authors import Author
from .exceptions import AuthorsNotFoundException


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

    @classmethod
    async def create_book(cls, **book_data):
        async with async_session() as session:
            async with session.begin():
                authors_ids = book_data.pop('authors_ids', [])
                query = select(Author).where(Author.id.in_(authors_ids))
                authors = await session.execute(query)
                authors = authors.scalars().all()

                if not authors:
                    raise AuthorsNotFoundException

                new_book = cls.model(**book_data)
                new_book.authors = authors

                session.add(new_book)
                await session.flush()
                return jsonable_encoder(new_book)


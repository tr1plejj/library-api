from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from src.dao import BaseDAO
from .models import Book
from src.database import async_session
from src.authors import Author
from .exceptions import AuthorsNotFoundException, UserTookMaxException, NoBooksException, UserAlreadyHasException
from src.exceptions import NoDataInsideException, NotFoundException
from src.models import AuthorBook
from src.users import User


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
        authors_ids = book_data.pop('authors_ids', [])

        async with async_session() as session:
            async with session.begin():

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

    @classmethod
    async def update_book(cls, book_id: int, **book_data):
        authors_ids = book_data.pop('authors_ids', [])
        update_values = {key: value for key, value in book_data.items() if value is not None}

        if not update_values:
            raise NoDataInsideException

        async with async_session() as session:
            async with session.begin():
                await super().update(book_id, **update_values)

                if authors_ids:
                    valid_authors = await session.execute(select(Author.id).where(Author.id.in_(authors_ids)))
                    valid_ids = {row[0] for row in valid_authors}
                    if len(valid_ids) != len(authors_ids):
                        raise AuthorsNotFoundException

                    delete_stmt = delete(AuthorBook).where(AuthorBook.book_id == book_id)
                    await session.execute(delete_stmt)

                    insert_stmt = insert(AuthorBook).values(
                        [{"book_id": book_id, "author_id": author_id} for author_id in authors_ids]
                    )
                    await session.execute(insert_stmt)

                return

    @classmethod
    async def take_book(cls, user_id: int, book_id: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    book_query = (
                        select(cls.model)
                        .where(cls.model.id == book_id)
                        .options(selectinload(cls.model.users))
                        .with_for_update()  # block before end
                    )
                    result = await session.execute(book_query)
                    book = result.scalar_one_or_none()

                    if not book:
                        raise NotFoundException

                    if not book.available > 0:
                        raise NoBooksException

                    user_query = select(User).where(User.id == user_id)
                    user_result = await session.execute(user_query)
                    user = user_result.scalar_one_or_none()

                    if not user:
                        raise NotFoundException

                    if not len(user.books) < 5:
                        raise UserTookMaxException

                    book.available -= 1

                    book.users.append(user)

                    return

        except IntegrityError:
            raise UserAlreadyHasException
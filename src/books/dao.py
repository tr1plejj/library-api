from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from src.dao import BaseDAO
from .models import Book
from src.database import async_session
from src.authors import Author
from .exceptions import AuthorsNotFoundException, UserTookMaxException, NoBooksException, UserAlreadyHasException, NoBookInUserException
from src.exceptions import NoDataInsideException, NotFoundException
from src.models import AuthorBook
from src.auth import User
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='library.log',
    filemode='a'
)


class BooksDAO(BaseDAO):

    model = Book

    @classmethod
    async def get_all_books(cls):
        """
        Find all books and load it authors.

        :return: all founded books with authors in it
        :rtype: list
        """
        async with async_session() as session:
            query = (
                select(cls.model).
                options(selectinload(cls.model.authors))
            )
            books = await session.execute(query)
            return books.scalars().all()

    @classmethod
    async def get_book(cls, book_id: int):
        """
        Find book with given id.

        :return: founded book
        """
        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(id=book_id)
                .options(selectinload(cls.model.authors))
            )
            result = await session.execute(query)
            book = result.scalar_one_or_none()
            if book is None:
                raise NotFoundException
            return book

    @classmethod
    async def create_book(cls, **book_data):
        """
        Create book with given values.

        :param book_data: dictionary with required field for model
        :return: created book
        """
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
        """
        Update book with given id and values.

        :param book_data: dictionary with book values to update
        :return: void
        :rtype: None
        """
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
    async def book_action(cls, user_id: int, book_id: int, action: str): # why if selectinload user can take infinite amount of books
        """
        Make action with book and user.

        :param action: must be 'take' or 'return', needs for particular operation
        :return: void
        :rtype: None
        """
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

                user_query = select(User).where(User.id == user_id).options(selectinload(User.books))
                user_result = await session.execute(user_query)
                user = user_result.scalar_one_or_none()

                if action == 'take':
                    if user in book.users:
                        raise UserAlreadyHasException
                    if not book.available > 0:
                        raise NoBooksException
                    if not len(user.books) < 5:
                        raise UserTookMaxException
                    book.available -= 1
                    book.users.append(user)
                    logging.info(f"Читатель '{user.username} (id: {user_id})' взял книгу '{book.title} (id: {book_id})'.")
                    return

                elif action == 'return':
                    if user not in book.users:
                        raise NoBookInUserException
                    book.available += 1
                    book.users.remove(user)
                    logging.info(f"Читатель '{user.username} (id: {user_id})' вернул книгу '{book.title} (id: {book_id})'.")
                    return

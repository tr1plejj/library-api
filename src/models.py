from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class AuthorBook(Base):
    __tablename__ = 'author_book'

    author_id: Mapped[int] = mapped_column(ForeignKey('author.id', ondelete='CASCADE'), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)
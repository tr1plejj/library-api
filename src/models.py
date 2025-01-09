from datetime import date,timedelta
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class AuthorBook(Base):
    __tablename__ = 'author_book'

    author_id: Mapped[int] = mapped_column(ForeignKey('author.id', ondelete='CASCADE'), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)


class UserBook(Base):
    __tablename__ = 'user_book'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)
    receive_date: Mapped[date] = mapped_column(default=date.today())
    return_date: Mapped[date] = mapped_column(default=(date.today()+timedelta(days=7)))
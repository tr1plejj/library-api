from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date
from src.database import Base


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    publish_date: Mapped[date] = mapped_column(default=date.today())
    genre: Mapped[str]
    available: Mapped[int]
    authors = relationship('Author', back_populates='books', secondary='author_book')
    users = relationship('User', back_populates='books', secondary='user_book')
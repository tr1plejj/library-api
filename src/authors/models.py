from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    biography: Mapped[str]
    birthday: Mapped[date]
    books = relationship('Book', back_populates='authors', secondary='author_book')
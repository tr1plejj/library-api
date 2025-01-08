from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
from src.database import Base


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
    genre: Mapped[str]
    available: Mapped[int]
    authors = relationship('Author', back_populates='books', secondary='author_book')
from pydantic import BaseModel
from src.authors.schemas import AuthorOutput


class BookInput(BaseModel):
    title: str
    description: str
    genre: str
    available: int
    authors: list[AuthorOutput]


class BookOutput(BookInput):
    id: int

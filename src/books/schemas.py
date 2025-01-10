from typing import Optional

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    description: str
    genre: str
    available: int
    authors_ids: list[int]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    available: Optional[int] = None
    authors_ids: Optional[list[int]] = None


class BookOutput(BaseModel):

    class AuthorInBook(BaseModel):
        id: int
        name: str

    id: int
    title: str
    description: str
    genre: str
    available: int
    authors: list[AuthorInBook]


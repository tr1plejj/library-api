from pydantic import BaseModel


class BookCreateUpdate(BaseModel):
    title: str
    description: str
    genre: str
    available: int
    authors_ids: list[int]


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


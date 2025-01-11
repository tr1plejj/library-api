from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):

    class BookInUser(BaseModel):
        title: str

    id: int
    username: str
    is_admin: bool
    books: Optional[list[BookInUser]]


class UserCreate(BaseModel):
    username: str
    password: str
from typing import Optional
from pydantic import BaseModel
from datetime import date


class AuthorInput(BaseModel):
    name: str
    biography: str
    birthday: date


class AuthorOutput(AuthorInput):
    id: int


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birthday: Optional[date] = None
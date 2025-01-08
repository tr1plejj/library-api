from pydantic import BaseModel
from datetime import date

class AuthorInput(BaseModel):
    name: str
    biography: str
    birthday: date

class AuthorOutput(AuthorInput):
    id: int

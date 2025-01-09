from fastapi import FastAPI
from src.authors import authors_router
from src.books import books_router
from src.users import users_router

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(users_router)
from fastapi import FastAPI
from src.authors import authors_router
from src.books import books_router

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)

from typing import Annotated
from fastapi import APIRouter, Path
from .dao import BooksDAO

router = APIRouter(
    tags=['books'],
    prefix='/books'
)


@router.get('/')
async def get_books():
    books = await BooksDAO.get_all_books()
    return books


@router.get('/{book_id}')
async def get_book(book_id: Annotated[int, Path()]):
    book = await BooksDAO.get_book(book_id)
    return book
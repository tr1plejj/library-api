from typing import Annotated
from fastapi import APIRouter, Path
from .dao import BooksDAO
from .schemas import BookInput, BookOutput

router = APIRouter(
    tags=['books'],
    prefix='/books'
)


@router.get('/', response_model=list[BookOutput])
async def get_books():
    books = await BooksDAO.get_all_books()
    return books


@router.get('/{book_id}', response_model=BookOutput)
async def get_book(book_id: Annotated[int, Path()]):
    book = await BooksDAO.get_book(book_id)
    return book


@router.patch('/{book_id}')
async def update_book(
        book_id: Annotated[int, Path()],
        book: BookInput
):
    await BooksDAO.update(book_id, **book.model_dump())
    return {'message': f'book {book_id} updated successfully'}


@router.delete('/{book_id}')
async def delete_book(book_id: Annotated[int, Path()]):
    await BooksDAO.delete(book_id)
    return {'message': f'book {book_id} deleted successfully'}
from typing import Annotated
from fastapi import APIRouter, Path
from .dao import BooksDAO
from .schemas import BookOutput, BookCreate, BookUpdate

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


@router.post('/', response_model=BookOutput, status_code=201)
async def create_book(new_book: BookCreate):
    book = await BooksDAO.create_book(**new_book.model_dump())
    return book


@router.patch('/{book_id}')
async def update_book(
        book_id: Annotated[int, Path()],
        book: BookUpdate
):
    await BooksDAO.update_book(book_id, **book.model_dump())
    return {'message': f'book {book_id} updated successfully'}


@router.delete('/{book_id}')
async def delete_book(book_id: Annotated[int, Path()]):
    await BooksDAO.delete(book_id)
    return {'message': f'book {book_id} deleted successfully'}
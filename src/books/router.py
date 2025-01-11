from typing import Annotated
from fastapi import APIRouter, Path, Depends, Query
from .dao import BooksDAO
from .schemas import BookOutput, BookCreate, BookUpdate
from src.auth.dependencies import get_current_user
from src.exceptions import NoPermissionsException
from src.users.schemas import User

router = APIRouter(
    tags=['books'],
    prefix='/books'
)


@router.get('/', response_model=list[BookOutput])
async def get_books(skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 0):
    books = await BooksDAO.get_all_books()
    if limit == 0:
        return books[skip:]
    else:
        return books[skip:limit]


@router.get('/{book_id}', response_model=BookOutput)
async def get_book(book_id: Annotated[int, Path()]):
    book = await BooksDAO.get_book(book_id)
    return book


@router.post('/', response_model=BookOutput, status_code=201)
async def create_book(new_book: BookCreate, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    book = await BooksDAO.create_book(**new_book.model_dump())
    return book


@router.patch('/{book_id}')
async def update_book(book_id: Annotated[int, Path()], book: BookUpdate, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    await BooksDAO.update_book(book_id, **book.model_dump())
    return {'message': f'book {book_id} updated successfully'}


@router.delete('/{book_id}')
async def delete_book(book_id: Annotated[int, Path()], user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    await BooksDAO.delete(book_id)
    return {'message': f'book {book_id} deleted successfully'}


@router.post("/{book_id}/take")
async def take_book(book_id: Annotated[int, Path()], user: User = Depends(get_current_user)):
    await BooksDAO.book_action(user_id=user.id, book_id=book_id, action='take')
    return {"message": f"user {user.id} successfully took book {book_id}"}


@router.delete('/{book_id}/return')
async def return_book(book_id: Annotated[int, Path()], user: User = Depends(get_current_user)):
    await BooksDAO.book_action(user_id=user.id, book_id=book_id, action='return')
    return {"message": f"user {user.id} successfully returned book {book_id}"}
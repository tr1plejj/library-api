from typing import Annotated
from fastapi import APIRouter, Path, Depends
from .dao import AuthorsDAO
from .schemas import AuthorInput, AuthorOutput, AuthorUpdate
from src.auth.dependencies import get_current_user
from src.exceptions import NoPermissionsException
from src.users.schemas import User

router = APIRouter(
    tags=['authors'],
    prefix='/authors'
)


@router.get('/', response_model=list[AuthorOutput])
async def get_authors():
    authors = await AuthorsDAO.find_all()
    return authors


@router.get('/{author_id}', response_model=AuthorOutput)
async def get_author(author_id: Annotated[int, Path()]):
    author = await AuthorsDAO.find_one_or_none(id=author_id)
    return author


@router.post('/', response_model=AuthorOutput, status_code=201)
async def create_author(author_data: AuthorInput, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    new_author = await AuthorsDAO.create(**author_data.model_dump())
    return new_author


@router.patch('/{author_id}')
async def update_author(author_id: Annotated[int, Path()], author_data: AuthorUpdate, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    await AuthorsDAO.update(author_id, **author_data.model_dump())
    return {'message': f'author {author_id} updated successfully'}


@router.delete('/{author_id}')
async def delete_author(author_id: Annotated[int, Path()], user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise NoPermissionsException
    await AuthorsDAO.delete(author_id)
    return {'message': f'author {author_id} deleted successfully'}
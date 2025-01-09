from typing import Annotated
from fastapi import APIRouter, Path
from .dao import AuthorsDAO
from .schemas import AuthorInput, AuthorOutput, AuthorUpdate

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
async def create_author(author_data: AuthorInput):
    new_author = await AuthorsDAO.create(**author_data.model_dump())
    return new_author


@router.patch('/{author_id}')
async def update_author(
        author_id: Annotated[int, Path()],
        author_data: AuthorUpdate
):
    await AuthorsDAO.update(author_id, **author_data.model_dump())
    return {'message': f'author {author_id} updated successfully'}


@router.delete('/{author_id}')
async def delete_author(author_id: Annotated[int, Path()]):
    await AuthorsDAO.delete(author_id)
    return {'message': f'author {author_id} deleted successfully'}
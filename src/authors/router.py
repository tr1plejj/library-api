from fastapi import APIRouter
from .dao import AuthorsDAO

router = APIRouter(
    tags=['authors'],
    prefix='/authors'
)


@router.get('/')
async def get_authors():
    authors = await AuthorsDAO.find_all()
    return authors
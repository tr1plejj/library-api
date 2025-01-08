from fastapi import HTTPException

NotFoundException = HTTPException(
    status_code=404,
    detail='object not found'
)
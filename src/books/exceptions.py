from fastapi import HTTPException

AuthorsNotFoundException = HTTPException(
    status_code=404,
    detail='authors with this ids not found'
)
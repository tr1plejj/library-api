from fastapi import HTTPException

NotFoundException = HTTPException(
    status_code=404,
    detail='object not found'
)

NoDataInsideException = HTTPException(
    status_code=400,
    detail='no data inside'
)

NoPermissionsException = HTTPException(
    status_code=403,
    detail='you have no permissions to do that'
)
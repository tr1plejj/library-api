from fastapi import HTTPException

AuthorsNotFoundException = HTTPException(
    status_code=404,
    detail='authors with this ids not found'
)

UserTookMaxException = HTTPException(
    status_code=403,
    detail='user already took 5 books'
)

NoBooksException = HTTPException(
    status_code=403,
    detail='there are no books available'
)

UserAlreadyHasException = HTTPException(
    status_code=403,
    detail='user already has this book'
)
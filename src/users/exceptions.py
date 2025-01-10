from fastapi import HTTPException

NotUniqueException = HTTPException(
    status_code=403,
    detail='User with this username already exists'
)

IncorrectDataException = HTTPException(
    status_code=401,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'}
)
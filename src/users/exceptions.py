from fastapi import HTTPException

CredentialsException = HTTPException(
    detail='Could not validate credentials',
    status_code=401,
    headers={'WWW-Authenticate': 'Bearer'}
)

IncorrectDataException = HTTPException(
    status_code=401,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'}
)


NotUniqueException = HTTPException(
    status_code=403,
    detail='User with this username already exists'
)
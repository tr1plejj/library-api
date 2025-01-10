from fastapi import HTTPException

CredentialsException = HTTPException(
    detail='Could not validate credentials',
    status_code=401,
    headers={'WWW-Authenticate': 'Bearer'}
)
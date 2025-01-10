import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from jwt import InvalidTokenError
from .config import ALGORITHM, SECRET_KEY
from .exceptions import CredentialsException
from .schemas import TokenData
from .service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CredentialsException
    user = await get_user(token_data.username)
    if user is None:
        raise CredentialsException
    return user
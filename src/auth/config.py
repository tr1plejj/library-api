from passlib.context import CryptContext

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7' # should be in .env file, but because of test case it is here
ALGORITHM = 'HS256'
TOKEN_EXPIRES_MINUTES = 60
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
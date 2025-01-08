from src.dao import BaseDAO
from .models import Author


class AuthorsDAO(BaseDAO):

    model = Author
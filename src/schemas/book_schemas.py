from typing import Optional
from pydantic import BaseModel

from schemas.author_schemas import AuthorSchema
from utils.enums import GenreEnum


class BookSchema(BaseModel):
    id: int
    title: str
    published_year: int
    genre: GenreEnum
    author: Optional[AuthorSchema] = None

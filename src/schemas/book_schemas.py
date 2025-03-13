from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from schemas.author_schemas import AuthorSchema
from utils.enums import GenreEnum


class BookBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    published_year: int
    genre: GenreEnum

    @field_validator('published_year', mode='after')
    def validate_published_year(cls, v):
        if v is not None and v <= 1800:
            raise ValueError('published_year must be above 1800')
        return v

    @field_validator('title', mode='after')
    def validate_title(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('title cannot be empty')
            if v.isnumeric():
                raise ValueError('title cannot be a number')
        return v


class BookSchema(BookBaseSchema):
    id: int

    author: AuthorSchema
    created_at: datetime
    updated_at: datetime


class BookCreateSchema(BookBaseSchema):
    author_id: int

    @field_validator('author_id', mode='after')
    def validate_author_id(cls, v):
        if v is not None and v < 0:
            raise ValueError('author_id must be above 0')
        return v
    
class BookNewSchema(BookCreateSchema):
    id: int


class BookUpdateSchema(BookBaseSchema):
    title: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[GenreEnum] = None
from typing import Optional
from pydantic import BaseModel, field_validator
from database.models import Book
from utils.enums import GenreEnum

class BookFilterParams(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    author_name: Optional[str] = None
    genre: Optional[GenreEnum] = None

    @field_validator('year', mode='after')
    def validate_year(cls, v):
        if v is not None and v <= 1800:
            raise ValueError('year must be above 1800')
        return v

    @field_validator('title', mode='after')
    def validate_title(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('title cannot be empty')
            if v.isnumeric():
                raise ValueError('title cannot be a number')
        return v

    @field_validator('author_name', mode='after')
    def validate_author_name(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('author_name cannot be empty')
            if v.isnumeric():
                raise ValueError('author_name cannot be a number')
        return v

class BookSortParams(BaseModel):
    order_by: Optional[str] = "id"
    order_desc: bool = False

    @field_validator('order_by', mode='after')
    def validate_order_by(cls, v):
        if v not in Book.__table__.columns:
            raise ValueError(f'order_by must be in [{Book.__table__.columns}]')
        return v
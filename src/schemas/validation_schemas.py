from typing import Optional
from pydantic import BaseModel, field_validator


class BookFilterParams(BaseModel):
    book_id: Optional[int] = None
    title: Optional[str] = None
    year: Optional[int] = None
    author_name: Optional[str] = None

    @field_validator('book_id', mode='after')
    def validate_book_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('book_id must be a positive integer')
        return v

    @field_validator('year', mode='after')
    def validate_year(cls, v):
        if v is not None and v <= 1800:
            raise ValueError('year must be a positive integer')
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
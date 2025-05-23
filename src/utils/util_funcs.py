from typing import Optional
from pydantic import ValidationError

from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.enums import GenreEnum
from utils.validation_funcs import handle_validation_error


def get_filters(
    title: Optional[str] = None,
    published_year: Optional[int] = None,
    author_name: Optional[str] = None,
    genre: Optional[GenreEnum] = None
) -> BookFilterParams:
    try:
        return BookFilterParams(
            title=title,
            published_year=published_year,
            author_name=author_name,
            genre=genre,
        )
    except ValidationError as e:
        handle_validation_error(e)


def get_sorting(
    order_by: Optional[str] = "id",
    order_desc: bool = False
) -> BookSortParams:
    try:
        return BookSortParams(
            order_by=order_by,
            order_desc=order_desc,
        )
    except ValidationError as e:
        handle_validation_error(e)

from typing import Optional
from pydantic import ValidationError

from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.validation_funcs import handle_validation_error


def get_filters(
    book_id: Optional[int] = None,
    title: Optional[str] = None,
    year: Optional[int] = None,
    author_name: Optional[str] = None
) -> BookFilterParams:
    try:
        return BookFilterParams(
            book_id=book_id,
            title=title,
            year=year,
            author_name=author_name,
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

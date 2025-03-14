import csv
from io import StringIO
import json
from typing import Optional
from fastapi import UploadFile
from pydantic import ValidationError

from constants import ALLOWED_FILE_TYPES
from custom_exceptions.book_exceptions import BookBulkImportException
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

def split_into_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


async def parse_file(file: UploadFile):
    if file.content_type == 'application/json':
        return json.loads(await file.read())
    elif file.content_type == 'text/csv':
        content = await file.read()
        decoded_content = content.decode('utf-8')
        csv_reader = csv.DictReader(StringIO(decoded_content))
        return [dict(row) for row in csv_reader]
    else:
        raise BookBulkImportException(f"Unsupported file format. Allowed file types: {', '.join(ALLOWED_FILE_TYPES)}. Got type: {file.content_type}")
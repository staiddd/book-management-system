from fastapi import HTTPException, Path, Query, status
from pydantic import ValidationError

from custom_exceptions.book_exceptions import BookBulkImportException
from schemas.book_schemas import BookCreateSchema
from utils.enums import OnErrorEnum


def handle_validation_error(e: ValidationError):
    errors = []
    for error in e.errors():
        errors.append({
            "field": error["loc"][-1],  
            "message": error["msg"],    
            "type": error["type"],
        })
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=errors,
    )

def validate_book_id(book_id: int = Path(..., gt=0)) -> int:
    if book_id <= 0:
        raise HTTPException(status_code=422, detail="book_id must be greater than 0")
    return book_id

def validate_batch_size(batch_size: int = Query(100, gt=0)) -> int:
    if batch_size <= 0:
        raise HTTPException(status_code=422, detail="batch_size must be greater than 0")
    return batch_size

def validate_book_data(data, on_validation_error):
    required_fields = {"title", "published_year", "genre", "author_id"}
    result = []

    for entry in data:
        try:
            if not required_fields.issubset(entry.keys()):
                raise BookBulkImportException("Missing required fields in data")

            validated_data = BookCreateSchema(**entry)
            result.append(validated_data.model_dump())

        except Exception:
            if on_validation_error == OnErrorEnum.SKIP:
                continue
            raise BookBulkImportException(f"Something went wrong in validation book data: {entry}")
    
    return result
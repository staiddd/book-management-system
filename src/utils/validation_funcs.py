from fastapi import HTTPException, Path, status
from pydantic import ValidationError


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

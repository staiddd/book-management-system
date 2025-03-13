from fastapi import HTTPException, status
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
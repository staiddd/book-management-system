from fastapi import HTTPException, status

class AppException(HTTPException):
    def __init__(self, status_code: status, detail: str):
        super().__init__(status_code=status_code, detail=detail)
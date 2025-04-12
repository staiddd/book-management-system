from fastapi import status
from custom_exceptions.base_exceptions import AppException

class BookException(AppException):
    """Base class for book related errors"""
    pass

class BookCreateException(BookException):
    def __init__(self, detail="Error creating book"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class BookDeleteException(BookException):
    def __init__(self, detail="Error deleting book"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BookGetException(BookException):
    def __init__(self, detail="Error retrieving book(s)"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class BookUpdateException(BookException):
    def __init__(self, detail="Error updating book"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class BookNotFoundException(BookException):
    def __init__(self, detail="Book not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BookDownloadException(BookException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
from fastapi import HTTPException, status


class BookCreateException(HTTPException):
    def __init__(self, detail="Error creating book"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class BookDeleteException(HTTPException):
    def __init__(self, detail="Error deleting book"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BookGetException(HTTPException):
    def __init__(self, detail="Error retrieving book(s)"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class BookUpdateException(HTTPException):
    def __init__(self, detail="Error updating book"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class BookNotFoundException(HTTPException):
    def __init__(self, detail="Book not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
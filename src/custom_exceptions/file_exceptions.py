from fastapi import status
from custom_exceptions.base_exceptions import AppException


class FileException(AppException):
    """Base class for file handling errors"""
    pass

class UnexpectedFileError(FileException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class NoFileFoundException(FileException):
    def __init__(self, detail="No file found!"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UploadingFileException(FileException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class DeletionFileException(FileException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnsupportedFileTypeException(FileException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnsupportedFileSizeException(FileException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
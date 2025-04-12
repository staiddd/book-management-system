import mimetypes
from constants import MAX_FILE_SIZES, SUPPORTED_FILE_TYPES
from fastapi import HTTPException, status

from custom_exceptions.file_exceptions import UnexpectedFileError, UnsupportedFileSizeException, UnsupportedFileTypeException


class FileActionMixin:
    @staticmethod
    def get_file_type(file_name: str) -> str:
        try:
            file_type, _ = mimetypes.guess_type(file_name)
            for file_types in SUPPORTED_FILE_TYPES.values():
                if file_type in file_types:
                    return file_types[file_type]
                
            raise UnsupportedFileTypeException(f'Unsupported file type: {file_type}.')

        except HTTPException:
            raise
        except Exception as e:
            raise UnexpectedFileError(f'Error determining file type: {str(e)}')
        
    @staticmethod
    def validate_file_size(size: int, file_type: str) -> None:
        max_file_size = MAX_FILE_SIZES[file_type]
        if not 0 < size <= max_file_size:
            raise UnsupportedFileSizeException(f'Supported {file_type} file size is 0 - {max_file_size} KB')
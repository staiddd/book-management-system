TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

BOOKS = "books"
BOOK_FOLDER = BOOKS

SUPPORTED_FILE_TYPES = {
    BOOKS: {
        'application/pdf': 'pdf',
        'application/epub+zip': 'epub',
        'application/x-mobipocket-ebook': 'mobi',
        'text/plain': 'txt',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'text/csv': 'csv',
    },
}
    

KB = 1024
MB = 1024 * KB

# file sizes for each type
DEFAULT_MAX_SIZE = 20 * MB  # 20 MB for most types


MAX_FILE_SIZES = {
    "pdf": DEFAULT_MAX_SIZE,
    "epub": DEFAULT_MAX_SIZE,
    "mobi": DEFAULT_MAX_SIZE,
    "txt": DEFAULT_MAX_SIZE,
    "docx": DEFAULT_MAX_SIZE,
    "csv": DEFAULT_MAX_SIZE
}
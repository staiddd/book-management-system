from enum import Enum

class GenreEnum(str, Enum):
    FICTION = "FICTION"
    NONFICTION = "NONFICTION"
    SCIFI = "SCIFI"
    FANTASY = "FANTASY"
    MYSTERY = "MYSTERY"
    BIOGRAPHY = "BIOGRAPHY"
    HISTORY = "HISTORY"
    OTHER = "OTHER"


class OnErrorEnum(str, Enum):
    SKIP = "SKIP"
    RAISE_ERROR = "RAISE_ERROR"
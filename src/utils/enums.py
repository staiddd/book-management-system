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
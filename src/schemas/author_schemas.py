from datetime import datetime
from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
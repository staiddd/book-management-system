from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
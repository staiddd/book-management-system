from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    password_hash: str


class UserIn(UserBase):
    pass


class UserOut(UserBase):
    id: int
    password_hash: bytes
    created_at: datetime


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


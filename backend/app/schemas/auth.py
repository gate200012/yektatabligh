from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

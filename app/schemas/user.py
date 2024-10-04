from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # Only required for password-based registration


class OAuthUserCreate(BaseModel):
    username: str
    email: EmailStr
    oauth_provider: str
    oauth_token: str
    role: Optional[str] = "user"


class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    role: str

    class Config:
        orm_mode = True

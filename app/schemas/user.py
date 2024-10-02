from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Properties for user creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # Only required for password-based registration

# Properties for OAuth user creation
class OAuthUserCreate(BaseModel):
    username: str
    email: EmailStr
    oauth_provider: str
    oauth_token: str
    role: Optional[str] = "user"

# Properties for returning user information
class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    role: str

    class Config:
        orm_mode = True

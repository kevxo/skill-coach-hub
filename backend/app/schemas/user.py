from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str | None ] = None
    last_name: Optional[str | None ] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AvatarUploadResponse(BaseModel):
    upload_url: str
    avatar_url: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
    first_name: str
    last_name: str
    avatar_url: Optional[str]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
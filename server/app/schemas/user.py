from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    is_active: Optional[bool] = True


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Changed from orm_mode = True for Pydantic v2


class User(UserInDBBase):
    # This model can be used for responses where you don't want to expose hashed_password
    pass


class UserInDB(UserInDBBase):
    hashed_password: str

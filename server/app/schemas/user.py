from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Changed from orm_mode = True for Pydantic v2


class User(UserInDBBase):
    # This model can be used for responses where you don't want to expose hashed_password
    pass


# For relationships, you might define simplified schemas to avoid circular imports initially
# Or, use update_forward_refs() if you need to include nested relationships immediately.
# For simplicity, we'll keep project/chat schemas separate for now.

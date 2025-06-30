from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schemas.chat import Chat


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_instructions: str


class ProjectCreate(ProjectBase):
    pass  # No extra fields for creation beyond base


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    base_instructions: Optional[str] = None


class ProjectInDBBase(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Changed from orm_mode = True for Pydantic v2


class Project(ProjectInDBBase):
    chats: List[Chat] = []

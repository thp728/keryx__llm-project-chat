from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    pass
    # Optionally, you can add relationships here for responses, e.g.,
    # owner: Optional[User] = None # Requires handling circular imports or forward_refs
    # chats: List[Chat] = []

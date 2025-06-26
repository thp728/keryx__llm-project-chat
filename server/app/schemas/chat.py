# server/app/schemas/chat.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    project_id: int  # Include project_id for creation


class ChatUpdate(ChatBase):
    title: Optional[str] = None


class ChatInDBBase(ChatBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Changed from orm_mode = True for Pydantic v2


class Chat(ChatInDBBase):
    pass
    # Optionally, you can add relationships here for responses, e.g.,
    # project: Optional[Project] = None # Requires handling circular imports or forward_refs

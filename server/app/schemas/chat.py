from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schemas.message import Message


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    project_id: int  # Include project_id for creation


class ChatUpdate(ChatBase):
    title: Optional[str] = None


class ChatInDBBase(ChatBase):
    id: int
    title: str
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Chat(ChatInDBBase):
    messages: List[Message] = []


class ChatInDB(ChatInDBBase):
    pass

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    role: str = Field(
        ...,
        description="The role of the message sender (e.g., 'user', 'assistant', 'system').",
    )
    content: str = Field(..., description="The actual content of the message.")


class MessageCreate(MessageBase):
    chat_id: int = Field(..., description="The ID of the chat this message belongs to.")


class MessageUpdate(MessageBase):
    role: Optional[str] = Field(
        None,
        description="The role of the message sender (e.g., 'user', 'assistant', 'system').",
    )
    content: Optional[str] = Field(
        None, description="The actual content of the message."
    )


class MessageInDBBase(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass

from pydantic import BaseModel


class UserMessageRequest(BaseModel):
    message_content: str

from typing import Optional
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: Optional[str] = (
        None  # 'sub' typically holds the user identifier (e.g., email or ID)
    )

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    # This schema defines the structure of the *decoded* JWT payload
    sub: Optional[str] = (
        None  # 'sub' typically holds the user identifier (e.g., email or ID)
    )
    # You might add other claims here if needed, e.g., 'exp' for expiration
    # exp: Optional[int] = None # Expiration time as a Unix timestamp

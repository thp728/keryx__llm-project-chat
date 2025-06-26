from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    pass  # Generic CRUD methods are sufficient for now


chat = CRUDChat(Chat)

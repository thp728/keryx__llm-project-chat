from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatCreate, ChatUpdate


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def get_multi_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        return (
            db.query(self.model)
            .filter(Chat.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_project_ids(
        self, db: Session, *, project_ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        """
        Retrieves multiple chats for a list of project IDs.
        """
        return (
            db.query(self.model)
            .filter(Chat.project_id.in_(project_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_message(
        self, db: Session, chat_id: int, role: str, content: str
    ) -> Message:
        """
        Creates a new message record linked to a specific chat.
        """
        db_obj = Message(chat_id=chat_id, role=role, content=content)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


chat = CRUDChat(Chat)

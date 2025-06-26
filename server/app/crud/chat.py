from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chat import Chat
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


chat = CRUDChat(Chat)

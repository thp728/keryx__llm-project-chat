from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from typing import List
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="chats")  # type: ignore
    messages: Mapped[List["Message"]] = relationship(  # type: ignore
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

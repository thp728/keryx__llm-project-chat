from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from typing import List
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    base_instructions = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="projects")  # type: ignore
    chats: Mapped[List["Chat"]] = relationship(  # type: ignore
        "Chat",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Chat.created_at",
    )

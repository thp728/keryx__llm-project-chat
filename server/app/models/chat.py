# server/app/models/chat.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    # The actual chat messages/history will be stored as JSON or similar within the LLM interaction logic,
    # or could be a separate table depending on complexity. For now, we'll keep it simple here.
    # A simple way to store chat history might be a Text field storing JSON string.
    # This design decision would be refined when integrating LangChain.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="chats")

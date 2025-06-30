# Import Base from app.db.base so that all models inherit from it
from app.db.base import Base

# Import all SQLAlchemy models to ensure they are registered with Base
# This is crucial for Alembic to discover them for migrations.
from .user import User
from .project import Project
from .chat import Chat
from .message import Message

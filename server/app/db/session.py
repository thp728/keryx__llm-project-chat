from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings  # Import settings

# Get the application settings, which includes DATABASE_URL
settings = get_settings()

# Create the SQLAlchemy engine
# The pool_pre_ping=True option ensures that connections are still alive before being used.
# This helps prevent issues with stale connections in the pool.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a SessionLocal class
# This will be the actual database session that you use in your code.
# The `autocommit=False` and `autoflush=False` are standard for web applications
# where you want to explicitly commit changes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your ORM models
# All your SQLAlchemy models will inherit from this Base.
Base = declarative_base()


# Dependency to get a database session
def get_db():
    """
    Dependency function to provide a database session.
    It creates a session, yields it, and ensures it's closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

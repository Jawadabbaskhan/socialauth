from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base_class import Base  

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    """
    Provides a database session.

    Yields:
    - Session: A SQLAlchemy database session.

    Ensures:
    - The session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

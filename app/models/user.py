from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Required if you want to support password-based login as well
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)  # E.g., 'google', 'facebook'
    oauth_token = Column(String, nullable=True)  # Stores the OAuth token
    role = Column(String, nullable=True)  # E.g., 'admin', 'user'

from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)
    oauth_token = Column(String, nullable=True)
    role = Column(String, nullable=True)

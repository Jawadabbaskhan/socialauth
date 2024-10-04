from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    """
    Represents a user in the database.

    Attributes:
    - id (int): The primary key of the user.
    - username (str): The username of the user, must be unique.
    - email (str): The email of the user, must be unique.
    - hashed_password (str): The hashed password of the user.
    - is_active (bool): Indicates if the user is active.
    - is_superuser (bool): Indicates if the user has superuser privileges.
    - oauth_provider (str): The OAuth provider used for authentication.
    - oauth_token (str): The OAuth token for the user.
    - role (str): The role of the user.
    """
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

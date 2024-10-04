from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, OAuthUserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    """
    Deletes an existing product by its ID.

    Parameters:
    - db (Session): The database session.
    - product_id (int): The ID of the product to delete.

    Returns:
    - Product or None: The deleted product or None if not found.
    """
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_oauth_user(db: Session, oauth_user: OAuthUserCreate):
    """
    Creates a new OAuth user in the database.

    Parameters:
    - db (Session): The database session.
    - oauth_user (OAuthUserCreate): The OAuth user data to create.

    Returns:
    - User: The created OAuth user.
    """
    db_user = User(
        username=oauth_user.username,
        email=oauth_user.email,
        oauth_provider=oauth_user.oauth_provider,
        oauth_token=oauth_user.oauth_token,
        is_active=True,
        is_superuser=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    """
    Retrieves a user by their email.

    Parameters:
    - db (Session): The database session.
    - email (str): The email of the user to retrieve.

    Returns:
    - User or None: The retrieved user or None if not found.
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session):
    """
    Retrieves all users from the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - list[User]: A list of all users.
    """
    return db.query(User).all()
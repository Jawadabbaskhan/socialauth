from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, OAuthUserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
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
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session):
    return db.query(User).all()
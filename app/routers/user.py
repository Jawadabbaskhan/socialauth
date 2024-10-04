from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request

from app.models.user import User
from app.schemas.user import UserCreate, OAuthUserCreate, UserOut
from app.services.user_service import create_user, create_oauth_user, get_user_by_email
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import verify_token,get_current_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


@router.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.

    Parameters:
    - user (UserCreate): The user data to create.
    - db (Session): The database session dependency.

    Returns:
    - UserOut: The created user.

    Raises:
    - HTTPException: If the email is already registered.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.post("/oauth-register/", response_model=UserOut)
def oauth_register_user(oauth_user: OAuthUserCreate, db: Session = Depends(get_db)):
    """
    Registers a new OAuth user.

    Parameters:
    - oauth_user (OAuthUserCreate): The OAuth user data to create.
    - db (Session): The database session dependency.

    Returns:
    - UserOut: The created OAuth user.

    Raises:
    - HTTPException: If the email is already registered.
    """
    db_user = get_user_by_email(db, email=oauth_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_oauth_user(db=db, oauth_user=oauth_user)


@router.get("/users/")
async def get_users(request: Request, db: Session = Depends(get_db)):
    """
    Retrieves a list of all users.

    Parameters:
    - request (Request): The incoming HTTP request.
    - db (Session): The database session dependency.

    Returns:
    - list[User]: A list of all users.

    Raises:
    - HTTPException: If the user is unauthorized.
    """
    current_user = get_current_user_from_token(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Fetch all users
    users = db.query(User).all()
    return users

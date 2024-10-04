from datetime import timedelta
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.core.auth import create_access_token, create_refresh_token,generate_csrf_token

from app.core.config import settings
from app.core.oauth import oauth
from app.services.user_service import create_oauth_user, get_user_by_email
from app.schemas.user import OAuthUserCreate
from app.db.session import get_db


router = APIRouter()


@router.get("/login/google")
async def google_login(request: Request):
    """
    Initiates the Google OAuth login process.

    Parameters:
    - request (Request): The incoming HTTP request.

    Returns:
    - Response: A redirect response to the Google OAuth authorization URL.
    """
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handles the Google OAuth callback.

    Parameters:
    - request (Request): The incoming HTTP request.
    - db (Session): The database session dependency.

    Returns:
    - JSONResponse: A response with user information and authentication cookies.

    Details:
    - Authorizes the access token using the Google OAuth provider.
    - Retrieves user information from Google.
    - Checks if the user exists in the database; if not, creates a new user.
    - Generates access, refresh, and CSRF tokens.
    - Sets the tokens as HTTP-only cookies in the response.
    - Returns a JSON response with user information.

    Raises:
    - HTTPException: If OAuth authentication fails.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.userinfo(token=token)

        user_email = user_info['email']
        user = get_user_by_email(db, email=user_email)
        if not user:
            oauth_user = OAuthUserCreate(
                username=user_info['name'],
                email=user_info['email'],
                oauth_provider='google',
                oauth_token=token['access_token']
            )
            user = create_oauth_user(db, oauth_user=oauth_user)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email,"role":user.role}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.email,"role":user.role})
        csrf_token = generate_csrf_token()

        response = JSONResponse(
            content={
                "message": "User authenticated successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                },
            }
        )
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            secure=False,
            samesite="Lax",
            path="/" 
        
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=86400,
            secure=False,
            samesite="Lax",
            path="/"
        )

        response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        max_age=1800,
        secure=False,
        samesite="Lax",
        path="/"
        )
        
        return response


    except Exception as e:
        print("OAuth Error:", str(e))
        raise HTTPException(status_code=400, detail="OAuth authentication failed")


@router.post("/logout")
async def logout():
    """
    Logs out the user by deleting authentication cookies.

    Returns:
    - JSONResponse: A response indicating successful logout.
    """
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.oauth import oauth
from app.services.user_service import create_oauth_user, get_user_by_email
from app.schemas.user import OAuthUserCreate
from app.db.session import get_db
from starlette.responses import RedirectResponse

from app.core.auth import create_access_token, create_refresh_token
from datetime import timedelta
from app.core.config import settings

from fastapi.responses import JSONResponse
router = APIRouter()

# OAuth Login with Google
@router.get("/login/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    print("\n\n\n\nRedirect URI:", redirect_uri)  # Debugging line
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")

async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.userinfo(token=token)

        # Check if the user exists in the database
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

        # Generate JWT token for the user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.email})

        response = JSONResponse(
            content={
                "message": "User authenticated successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }
        )
        # Set HTTP-only cookies for access and refresh tokens
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            secure=False,  # Set this to True if using HTTPS
            samesite="Lax",
            path="/"  # Ensure the cookie is accessible to all routes
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=86400,
            secure=False,  # Set this to True if using HTTPS
            samesite="Lax",
            path="/"  # Ensure the cookie is accessible to all routes
        )

        return response


    except Exception as e:
        print("OAuth Error:", str(e))  # Debugging line
        raise HTTPException(status_code=400, detail="OAuth authentication failed")


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

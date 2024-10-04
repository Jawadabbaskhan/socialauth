from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.auth import refresh_access_token
from app.db.session import get_db
from fastapi.responses import JSONResponse
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import Request

@router.post("/refresh-token")
async def refresh_token(request: Request):
    """
    Refreshes the access token using the refresh token from cookies.

    Parameters:
    - request (Request): The incoming HTTP request.

    Returns:
    - JSONResponse: A response indicating the access token has been refreshed.

    Raises:
    - HTTPException: If the refresh token is missing, invalid, or expired.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    new_access_token = refresh_access_token(refresh_token)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    response = JSONResponse(content={"message": "Access token refreshed"})
    response.set_cookie(
        key="access_token", value=new_access_token, httponly=True, max_age=1800, secure=True
    )
    
    return response
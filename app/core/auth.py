import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Request

from app.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire,"role": data.get("role")})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def get_current_user_from_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user_from_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None


def refresh_access_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if payload and payload.get("scope") == "refresh_token":
        new_access_token = create_access_token({"sub": payload["sub"]})
        return new_access_token
    return None


def generate_csrf_token():
    return secrets.token_urlsafe(32)
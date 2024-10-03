from jose import JWTError, jwt
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RoleBasedAccessControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # List of URLs that do not require authorization
        no_auth_urls = [
            "/token",
            "/docs",
            "/openapi.json",
            "/api/v1/oauth/login/google",
            "/api/v1/oauth/callback"
        ]

        # Check if the request URL is in the no_auth_urls list
        if request.url.path in no_auth_urls:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized: Missing token"})

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_email: str = payload.get("sub")
            print("\n\n\n\nUser Email:", user_email)  # Debugging line
            user_role: str = payload.get("role")
            print("\n\n\n\nUser Role:", user_role)  # Debugging line

            if user_email is None or user_role is None:
                raise JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid token"})

            db = next(get_db())
            user = db.query(User).filter(User.email == user_email).first()
            print("\n\n\n\nUser:", user)  # Debugging line
            if user is None:
                raise JSONResponse(status_code=401, content={"detail": "Unauthorized: User not found"})

            request.state.user_role = user_role

            if request.url.path.startswith("/api/v1/products") and request.method == "DELETE":
                if user_role != "admin":
                    return JSONResponse(status_code=403, content={"detail": "Forbidden: Insufficient privileges"})

        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid token"})

        response = await call_next(request)
        return response
from jose import JWTError, jwt
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings


class RoleBasedAccessControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware for role-based access control.

    Methods:
    - dispatch(request: Request, call_next): Handles incoming requests and enforces role-based access control.

    Attributes:
    - no_auth_urls (list): List of URLs that do not require authentication.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Handles incoming requests and enforces role-based access control.

        Parameters:
        - request (Request): The incoming HTTP request.
        - call_next (function): The next middleware or route handler.

        Returns:
        - Response: The HTTP response.

        Details:
        - Allows requests to certain URLs without authentication.
        - Checks for a Bearer token in the Authorization header.
        - Decodes the JWT token and extracts user information.
        - Verifies the user's existence and role.
        - Enforces role-based access control for specific routes.
        """
        no_auth_urls = [
            "/token",
            "/docs",
            "/openapi.json",
            "/api/v1/oauth/login/google",
            "/api/v1/oauth/callback"
        ]

        if request.url.path in no_auth_urls:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized: Missing token"})

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_email: str = payload.get("sub")
            user_role: str = payload.get("role")
            
            if user_email is None or user_role is None:
                raise JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid token"})

            db = next(get_db())
            user = db.query(User).filter(User.email == user_email).first()
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
from fastapi import FastAPI
from app.routers import student
from app.routers import user,oauth

from starlette.middleware.sessions import SessionMiddleware
import os 
from dotenv import load_dotenv


load_dotenv() 
app = FastAPI()
# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Include the student router
# app.include_router(student.router, prefix="/api/students", tags=["students"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(oauth.router, prefix="/api/v1/oauth", tags=["oauth"])

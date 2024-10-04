from fastapi import FastAPI
from app.routers import user,oauth,product

from starlette.middleware.sessions import SessionMiddleware
from app.middleware.authorization import RoleBasedAccessControlMiddleware
import os 
from dotenv import load_dotenv
from app.db.base_class import Base
from app.db.session import engine


load_dotenv() 
app = FastAPI()
# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(RoleBasedAccessControlMiddleware)

Base.metadata.create_all(bind=engine)


app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(oauth.router, prefix="/api/v1/oauth", tags=["oauth"])
app.include_router(product.router, prefix="/api/v1/products", tags=["products"])
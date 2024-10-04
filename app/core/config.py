import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Auth"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    OAUTH_REDIRECT_URI: str = os.getenv("OAUTH_REDIRECT_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


settings = Settings()

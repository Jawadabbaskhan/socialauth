import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app as real_app  # Import the actual app
from app.routers import oauth  # Import your routes

# Create a test app without the custom middleware
test_app = FastAPI()
test_app.include_router(oauth.router)  # Add your routes to the test app

client = TestClient(test_app)

def test_google_login():
    response = client.get("/api/v1/oauth/login/google")
    assert response.status_code == 200

def test_google_callback():
    response = client.get("/api/v1/oauth/callback")
    assert response.status_code == 200

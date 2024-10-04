import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app as real_app
from app.routers import oauth


test_app = FastAPI()
test_app.include_router(oauth.router)

client = TestClient(test_app)

def test_google_login():
    response = client.get("/api/v1/oauth/login/google")
    assert response.status_code == 200

def test_google_callback():
    response = client.get("/api/v1/oauth/callback")
    assert response.status_code == 200

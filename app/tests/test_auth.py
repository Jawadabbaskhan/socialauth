import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import create_access_token, create_refresh_token
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db
    db.close()

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None

def test_create_refresh_token():
    data = {"sub": "testuser"}
    token = create_refresh_token(data)
    assert token is not None

def test_oauth_register_user(db_session: Session):
    response = client.post("/api/v1/users/oauth-register/", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "oauth_provider": "google",
        "oauth_token": "dummy_token"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_refresh_token():
    refresh_token = create_refresh_token({"sub": "testuser"})
    response = client.post("/refresh-token", cookies={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
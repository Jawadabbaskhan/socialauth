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
    """
    Retrieves all users from the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - list[User]: A list of all users.
    """
    db = next(get_db())
    yield db
    db.close()


def test_create_access_token():
    """
    Tests the creation of an access token.

    Asserts:
    - The token is not None.
    """
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None


def test_create_refresh_token():
    """
    Tests the creation of a refresh token.

    Asserts:
    - The token is not None.
    """
    data = {"sub": "testuser"}
    token = create_refresh_token(data)
    assert token is not None


def test_oauth_register_user(db_session: Session):
    """
    Tests the OAuth user registration.

    Parameters:
    - db_session (Session): The database session dependency.

    Asserts:
    - The response status code is 200.
    - The response email matches the expected email.
    """
    response = client.post("/api/v1/users/oauth-register/", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "oauth_provider": "google",
        "oauth_token": "dummy_token"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_refresh_token():
    """
    Tests the refresh token functionality.

    Asserts:
    - The response status code is 200.
    - The response contains an access token.
    """
    refresh_token = create_refresh_token({"sub": "testuser"})
    response = client.post("/refresh-token", cookies={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000/api/v1/products"
HEADERS_NON_ADMIN = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYXdhZGtoYW4zMTg0OUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTcyODAyMzA4OH0.RFCrQ3vCq7sFy7tX8N3MGMrVwq0MRsygwGKbUeyzdwc",
    "Content-Type": "application/json"
}
HEADERS_ADMIN = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYXdhZGtoYW4zMTg0OUBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MjgwMjMwODh9.RFCrQ3vCq7sFy7tX8N3MGMrVwq0MRsygwGKbUeyzdwc",
    "Content-Type": "application/json"
}


def test_create_product():
    """
    Tests the Google OAuth callback endpoint.

    Asserts:
    - The response status code is 200.
    """
    payload = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 10.99
    }
    response = requests.post(BASE_URL, json=payload, headers=HEADERS_ADMIN)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"


def test_get_product():
    """
    Tests the creation of a new product.

    Asserts:
    - The response status code is 201.
    - The response JSON contains the correct product name.
    """
    product_id = 1
    response = requests.get(f"{BASE_URL}/{product_id}", headers=HEADERS_NON_ADMIN)
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_get_products():
    """
    Tests retrieving a product by its ID.

    Asserts:
    - The response status code is 200.
    - The response JSON contains the correct product ID.
    """
    response = requests.get(BASE_URL, headers=HEADERS_NON_ADMIN)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_product_admin():
    """
    Tests retrieving a list of products.

    Asserts:
    - The response status code is 200.
    - The response JSON is a list.
    """
    product_id = 1
    payload = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 12.99
    }
    response = requests.put(f"{BASE_URL}/{product_id}", json=payload, headers=HEADERS_ADMIN)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"


def test_update_product_non_admin():
    """
    Tests updating a product by an admin.

    Asserts:
    - The response status code is 200.
    - The response JSON contains the updated product name.
    """
    product_id = 1
    payload = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 12.99
    }
    response = requests.put(f"{BASE_URL}/{product_id}", json=payload, headers=HEADERS_NON_ADMIN)
    assert response.status_code == 401


def test_delete_product_admin():
    """
    Tests updating a product by a non-admin.

    Asserts:
    - The response status code is 401.
    """
    product_id = 1
    response = requests.delete(f"{BASE_URL}/{product_id}", headers=HEADERS_ADMIN)
    assert response.status_code == 204


def test_delete_product_non_admin():
    """
    Tests deleting a product by an admin.

    Asserts:
    - The response status code is 204.
    """
    product_id = 1
    response = requests.delete(f"{BASE_URL}/{product_id}", headers=HEADERS_NON_ADMIN)
    assert response.status_code == 401
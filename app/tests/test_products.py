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
    payload = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 10.99
    }
    response = requests.post(BASE_URL, json=payload, headers=HEADERS_ADMIN)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_get_product():
    product_id = 1  # Replace with a valid product ID
    response = requests.get(f"{BASE_URL}/{product_id}", headers=HEADERS_NON_ADMIN)
    assert response.status_code == 200
    assert response.json()["id"] == product_id

def test_get_products():
    response = requests.get(BASE_URL, headers=HEADERS_NON_ADMIN)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product_admin():
    product_id = 1  # Replace with a valid product ID
    payload = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 12.99
    }
    response = requests.put(f"{BASE_URL}/{product_id}", json=payload, headers=HEADERS_ADMIN)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_update_product_non_admin():
    product_id = 1  # Replace with a valid product ID
    payload = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 12.99
    }
    response = requests.put(f"{BASE_URL}/{product_id}", json=payload, headers=HEADERS_NON_ADMIN)
    assert response.status_code == 401

def test_delete_product_admin():
    product_id = 1  # Replace with a valid product ID
    response = requests.delete(f"{BASE_URL}/{product_id}", headers=HEADERS_ADMIN)
    assert response.status_code == 204

def test_delete_product_non_admin():
    product_id = 1  # Replace with a valid product ID
    response = requests.delete(f"{BASE_URL}/{product_id}", headers=HEADERS_NON_ADMIN)
    assert response.status_code == 401
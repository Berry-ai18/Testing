import requests
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_token(base_url):
    response = requests.post(f"{base_url}/auth", json={"username": "admin", "password": "password123"})
    response.raise_for_status()
    assert response.status_code == 200
    return response.json().get("token")


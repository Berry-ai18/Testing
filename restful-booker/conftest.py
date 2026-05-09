import requests
import pytest
import os


# Shared fixtures for all restful-booker tests
@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")


@pytest.fixture(scope="session")
def auth_token(base_url):
    response = requests.post(
        f"{base_url}/auth", json={"username": "admin", "password": "password123"})
    response.raise_for_status()
    assert response.status_code == 200
    return response.json().get("token")


@pytest.fixture(scope="session")
def create_post(base_url):
    payload = {
        "firstname": "Patrik",
        "lastname": "Tichy",
        "totalprice": 220,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-04",
            "checkout": "2025-01-12"
        }
    }
    response = requests.post(base_url + '/booking', json=payload)
    data = response.json()
    assert response.status_code == 200
    assert 'bookingid' in data
    booking_id = data['bookingid']
    return booking_id

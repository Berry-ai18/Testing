import pytest
import requests

def test_get_booking(base_url, auth_token):
    response =  requests.get(base_url + '/booking', headers = {'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200

# NOTE: GET /booking is public — no auth required by design.
# In a real application this would ideally return 401 without credentials.
def test_get_booking_noauth(base_url):
    response =  requests.get(base_url + '/booking')
    assert response.status_code == 200
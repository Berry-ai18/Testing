import pytest
import requests

class TestSmoke:

    def test_ping_wakeup(self, base_url):
        response = requests.get(base_url + '/ping')
        assert response.status_code == 201

    # NOTE: GET /booking is public — no auth required by design.
    # In a real application this would ideally return 401 without credentials.
    def test_get_booking_noauth(self,base_url):
        response =  requests.get(base_url + '/booking')
        assert response.status_code == 200

    # NOTE: API returns 200 instead of the expected 201 Created
    # In a properly designed REST API, POST should return 201
    def test_post_booking(self, base_url):
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-01-01",
                "checkout": "2025-01-05"
            }
        }
        response = requests.post(base_url + '/booking', json=payload)
        assert response.status_code == 200
        assert 'bookingid' in response.json()

    
    def test_booking_by_id(self, base_url,create_post):
        response = requests.get(base_url + f'/booking/{create_post}')
        assert response.status_code == 200
        data = response.json()
        assert 'firstname' in data
        assert 'lastname' in data
        assert 'totalprice' in data
        assert 'depositpaid' in data
        assert 'bookingdates' in data
        assert 'checkin' in data['bookingdates']
        assert 'checkout' in data ['bookingdates']


    
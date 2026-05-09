import pytest
import requests
from jsonschema import validate


class TestSmoke:
    def test_ping_wakeup(self, base_url):
        # Verify the API is alive and responding before running other tests
        response = requests.get(base_url + '/ping')
        assert response.status_code == 201

    # NOTE: GET /booking is public — no auth required by design.
    # In a real application this would ideally return 401 without credentials.
    def test_get_booking_noauth(self, base_url):
        # Verify that GET /booking returns a list of bookings without authentication
        response = requests.get(base_url + '/booking')
        assert response.status_code == 200

    # NOTE: API returns 200 instead of the expected 201 Created
    # In a properly designed REST API, POST should return 201
    def test_post_booking(self, base_url):
        # Verify that a booking can be created with valid payload and returns a booking ID
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

    def test_booking_by_id(self, base_url, create_post):
        # Verify that a booking can be retrieved by ID and contains all expected fields
        response = requests.get(base_url + f'/booking/{create_post}')
        assert response.status_code == 200
        data = response.json()
        assert 'firstname' in data
        assert 'lastname' in data
        assert 'totalprice' in data
        assert 'depositpaid' in data
        assert 'bookingdates' in data
        assert 'checkin' in data['bookingdates']
        assert 'checkout' in data['bookingdates']
        assert isinstance(data, dict)

    def test_get_invalid_booking(self, base_url):
        # Verify that requesting a non-existent booking ID returns 404
        response = requests.get(base_url + '/booking/9999999')
        assert response.status_code == 404

    # NOTE: API returns 500 instead of expected 400 Bad Request for missing fields
    # In a properly designed API, missing required fields should return 400
    def test_post_booking_with_missing_fields(self, base_url):
        # Verify API handles incomplete payload — missing bookingdates field
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
        }
        response = requests.post(base_url + '/booking', json=payload)
        assert response.status_code == 500

    def test_update_booking_needs(self, base_url, auth_token, create_post):
        payload_update = {
            "firstname": "Patrik",
            "lastname": "Tichy",
            "totalprice": 220,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-01-04",
                "checkout": "2025-01-12"
            },
            "additionalneeds": "spa"
        }
        response = requests.put(base_url + f"/booking/{create_post}", headers={'Cookie': f'token={auth_token}'},
                                json=payload_update)

        assert response.status_code == 200
        assert 'additionalneeds' in response.json()
        assert 'spa' in response.json()['additionalneeds']

    # NOTE: API returns 403 instead of expected 401 Bad Request for missing fields
    # In a properly designed API, missing required auth should return 401
    def test_put_booking_noauth(self, base_url, create_post):
        payload_update = {
            "firstname": "Patrik",
            "lastname": "Tichy",
            "totalprice": 220,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-01-04",
                "checkout": "2025-01-12"
            },
            "additionalneeds": "spa"
        }
        response = requests.put(
            base_url + f'/booking/{create_post}', json=payload_update)
        assert response.status_code == 403

    def test_patch_booking(self, base_url, create_post, auth_token):
        response = requests.patch(base_url + f"/booking/{create_post}", headers={
                                  'Cookie': f'token={auth_token}'}, json={'firstname': 'Boris', 'lastname': 'Crazy'})
        assert response.status_code == 200
        data = response.json()
        assert 'firstname' in data
        assert 'lastname' in data
        assert 'Boris' in data['firstname']
        assert 'Crazy' in data['lastname']

    def test_patch_noauth(self, base_url, create_post):
        response = requests.patch(
            base_url + f'/booking/{create_post}', json={'firstname': 'Boris', 'lastname': 'Crazy'})
        assert response.status_code == 403

    def test_booking_by_id_json(self, base_url, create_post):
        response = requests.get(base_url + f'/booking/{create_post}')
        assert response.status_code == 200

        schema = {
            "type": "object",
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
            "properties": {
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "integer"},
                "depositpaid": {"type": "boolean"},
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"}
                    }
                }
            }
        }

        validate(instance=response.json(), schema=schema)

    def test_delete_booking(self, base_url, create_post, auth_token):
        response = requests.delete(
            base_url + f"/booking/{create_post}", headers={'Cookie': f'token={auth_token}'})
        assert response.status_code == 201
        verify = requests.get(base_url + f'/booking/{create_post}')
        assert verify.status_code == 404

    def test_delete_booking_noauth(self, base_url, create_post):
        response = requests.delete(base_url + f"/booking/{create_post}")
        assert response.status_code == 403

    def test_delete_booking_invalidid(self, base_url, auth_token):
        response = requests.delete(
            base_url + f"/booking/9999999", headers={'Cookie': f'token={auth_token}'})
        assert response.status_code == 405

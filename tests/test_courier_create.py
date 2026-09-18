import pytest
import requests

from endpoints import CREATE_COURIER
from helpers.courier_helper import generate_courier_data
from endpoints import (
    DUPLICATE_COURIER_MESSAGE,
    REQUIRED_FIELDS_MESSAGE,
)


@pytest.fixture
def courier_cleanup():
    courier_ids = []

    yield courier_ids

    for courier_id in courier_ids:
        requests.delete(f"{CREATE_COURIER}/{courier_id}")


class TestCreateCourier:

    def test_create_courier_success(self, courier_cleanup):
        payload = generate_courier_data()

        response = requests.post(
            CREATE_COURIER,
            json=payload
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = requests.post(
            f"{CREATE_COURIER}/login",
            json={
                "login": payload["login"],
                "password": payload["password"]
            }
        )

        assert login_response.status_code == 200

        courier_id = login_response.json()["id"]
        courier_cleanup.append(courier_id)

    def test_create_duplicate_courier(self, courier_cleanup):
        payload = generate_courier_data()

        first_response = requests.post(
            CREATE_COURIER,
            json=payload
        )

        assert first_response.status_code == 201
        assert first_response.json() == {"ok": True}

        login_response = requests.post(
            f"{CREATE_COURIER}/login",
            json={
                "login": payload["login"],
                "password": payload["password"]
            }
        )

        assert login_response.status_code == 200

        courier_id = login_response.json()["id"]
        courier_cleanup.append(courier_id)

        second_response = requests.post(
            CREATE_COURIER,
            json=payload
        )

        assert second_response.status_code == 409
        assert second_response.json() == {
            "code": 409,
            "message": DUPLICATE_COURIER_MESSAGE
        }

    @pytest.mark.parametrize("field", [
        "login",
        "password"
    ])
    def test_create_courier_without_required_field(self, field):
        payload = generate_courier_data()
        payload.pop(field)

        response = requests.post(
            CREATE_COURIER,
            json=payload
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": REQUIRED_FIELDS_MESSAGE
        }

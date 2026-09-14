import pytest
import requests

from endpoints import CREATE_COURIER
from helpers.courier_helper import generate_courier_data


class TestCreateCourier:

    def test_create_courier_success(self):
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

        requests.delete(f"{CREATE_COURIER}/{courier_id}")

    def test_create_duplicate_courier(self):
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

        courier_id = login_response.json()["id"]

        try:
            second_response = requests.post(
                CREATE_COURIER,
                json=payload
            )

            assert second_response.status_code == 409
            assert second_response.json() == {
                "message": "Этот логин уже используется"
            }
        finally:
            requests.delete(f"{CREATE_COURIER}/{courier_id}")

    @pytest.mark.parametrize("field", [
        "login",
        "password",
        "firstName"
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
            "message": "Недостаточно данных для создания учетной записи"
        }

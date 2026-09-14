import pytest

from helpers.courier_helper import create_courier, delete_courier


@pytest.fixture
def courier():
    response, courier_data = create_courier()

    assert response.status_code == 201
    assert response.json() == {"ok": True}

    login_response = requests.post(
        "https://qa-scooter.education-services.ru/api/v1/courier/login",
        json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
    )

    assert login_response.status_code == 200

    courier_id = login_response.json()["id"]

    yield {
        **courier_data,
        "id": courier_id
    }

    delete_courier(courier_id)

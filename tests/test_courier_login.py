import pytest
import requests

from endpoints import LOGIN_COURIER

# Логин курьера
class TestCourierLogin:

    def test_courier_can_login(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }

        response = requests.post(
            LOGIN_COURIER,
            json=payload
        )

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    # endpoint /api/v1/courier/login не обрабатывает запрос, в котором отсутствует password.
    # Падающий тест здесь фиксирует дефект API. Приходи код 504.
    @pytest.mark.parametrize("field", [
        "login",
        "password"
    ])
    def test_login_without_required_field(self, courier, field):
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }

        payload.pop(field)

        response = requests.post(
            LOGIN_COURIER,
            json=payload
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для входа"
        }

    def test_login_with_wrong_login(self, courier):
        payload = {
            "login": "nonexistent_login",
            "password": courier["password"]
        }

        response = requests.post(
            LOGIN_COURIER,
            json=payload
        )

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }

    def test_login_with_wrong_password(self, courier):
        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }

        response = requests.post(
            LOGIN_COURIER,
            json=payload
        )

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }


import pytest
from helpers.courier_helper import delete_courier


class TestDeleteCourier:

    def test_success_delete_courier(self, courier):
        # Успешный запрос возвращает {"ok": true}
        courier_id = courier["id"]
        response = delete_courier(courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_delete_courier_without_id_returns_error(self):
        # Если отправить запрос без id, вернётся ошибка (404)
        response = delete_courier(courier_id="")

        assert response.status_code == 404

    def test_delete_courier_with_non_existent_id_returns_error(self):
        # Если отправить запрос с несуществующим id, вернётся ошибка 404 и сообщение
        non_existent_id = 99999999
        response = delete_courier(courier_id=non_existent_id)

        assert response.status_code == 404
        assert response.json().get("message") == "Курьера с таким id нет."

    def test_unsuccessful_request_returns_appropriate_error(self):
        # Неуспешный запрос возвращает соответствующую ошибку (проверка структуры ответа)
        non_existent_id = 99999999
        response = delete_courier(courier_id=non_existent_id)

        # Проверяем, что код ответа ошибочный (404) и вернулось корректное тело с текстом ошибки
        assert response.status_code == 404
        assert "message" in response.json()


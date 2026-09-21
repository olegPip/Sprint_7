import pytest
from helpers.courier_helper import create_order, accept_order, get_order_id_by_track


class TestAcceptOrder:

    def test_success_accept_order(self, courier):
        # Успешный запрос возвращает {"ok": true}
        # 1. Создаем новый заказ и получаем track
        order_response = create_order()
        assert order_response.status_code == 201
        track = order_response.json().get("track")

        # 2. Получаем реальный id заказа по его треку
        order_id = get_order_id_by_track(track)
        assert order_id is not None, "Не удалось получить id заказа по треку"

        courier_id = courier["id"]

        # 3. Принимаем заказ курьером
        response = accept_order(order_id, courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_accept_order_without_courier_id_returns_error(self, courier):
        # Если не передать id курьера, запрос вернёт ошибку 400
        order_response = create_order()
        track = order_response.json().get("track")
        order_id = get_order_id_by_track(track)

        # Передаем courier_id=None
        response = accept_order(order_id, courier_id=None)

        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для поиска"

    def test_accept_order_with_invalid_courier_id_returns_error(self):
        # Если передать неверный id курьера, запрос вернёт ошибку 404
        order_response = create_order()
        track = order_response.json().get("track")
        order_id = get_order_id_by_track(track)
        invalid_courier_id = 99999999

        response = accept_order(order_id, courier_id=invalid_courier_id)

        assert response.status_code == 404
        assert response.json().get("message") == "Курьера с таким id не существует"

    def test_accept_order_without_order_id_returns_error(self):
        # Если не передать id заказа, запрос вернёт ошибку 404
        response = accept_order(order_id="", courier_id=123)
        assert response.status_code == 404

    def test_accept_order_with_invalid_order_id_returns_error(self, courier):
        # Если передать неверный id заказа, запрос вернёт ошибку 404
        invalid_order_id = 99999999
        # Передаем РЕАЛЬНОГО курьера из фикстуры, чтобы сервер ругался именно на заказ
        courier_id = courier["id"]

        response = accept_order(order_id=invalid_order_id, courier_id=courier_id)

        assert response.status_code == 404
        assert response.json().get("message") == "Заказа с таким id не существует"


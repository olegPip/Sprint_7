import pytest
import requests
from endpoints import ORDERS
from helpers.courier_helper import create_order


class TestGetOrderByTrack:

    def test_success_get_order_by_track(self):
        # Успешный запрос возвращает объект с заказом (200 OK)
        # 1. Создаем новый заказ, чтобы получить реальный трек-номер
        order_response = create_order()
        assert order_response.status_code == 201
        track = order_response.json().get("track")

        # 2. Отправляем GET-запрос с реальным query-параметром t
        response = requests.get(f"{ORDERS}/track", params={"t": track})

        # 3. Проверяем структуру успешного ответа
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track

    def test_get_order_without_track_returns_error(self):
        # Запрос без номера заказа (без параметра t) возвращает ошибку 400
        # Отправляем query-параметр пустым
        response = requests.get(f"{ORDERS}/track", params={"t": ""})

        # Проверяем код и сообщение об ошибке
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для поиска"

    def test_get_order_with_non_existent_track_returns_error(self):
        # Запрос с несуществующим заказом возвращает ошибку 404
        non_existent_track = 999999999

        # Отправляем GET-запрос с заведомо несуществующим треком
        response = requests.get(f"{ORDERS}/track", params={"t": non_existent_track})

        # Проверяем код 404 и точное сообщение из ТЗ
        assert response.status_code == 404
        assert response.json().get("message") == "Заказ не найден"

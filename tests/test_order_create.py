import pytest
import requests

from endpoints import ORDERS

# Создать заказ
class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_with_color(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-09-20",
            "comment": "Saske, come back to Konoha"
        }

        if color is not None:
            payload["color"] = color

        response = requests.post(
            ORDERS,
            json=payload
        )

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)

import requests

from endpoints import ORDERS

# Список заказов
class TestOrdersList:

    def test_get_orders_returns_list(self):
        response = requests.get(ORDERS)

        assert response.status_code == 200

        body = response.json()

        assert "orders" in body
        assert isinstance(body["orders"], list)

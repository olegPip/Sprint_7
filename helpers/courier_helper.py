import random
import string
import requests
from endpoints import CREATE_COURIER, ORDERS, ACCEPT_ORDER


def generate_random_string(length=10):
    return ''.join(
        random.choice(string.ascii_lowercase)
        for _ in range(length)
    )


def generate_courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }


def create_courier():
    payload = generate_courier_data()

    response = requests.post(
        CREATE_COURIER,
        json=payload
    )

    return response, payload


def delete_courier(courier_id):
    return requests.delete(
        f"{CREATE_COURIER}/{courier_id}"
    )

def create_order():
    # Создает новый тестовый заказ и возвращает ответ сервера
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-10-10",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    return requests.post(ORDERS, json=payload)


def accept_order(order_id, courier_id):
    # Отправляет PUT-запрос на принятие заказа.
    # Конструирует URL: /api/v1/orders/accept/:id?courierId=:courierId
    # Если order_id передан как None или пустой, отправляем запрос на базовый эндпоинт без ID в пути
    if order_id is not None and order_id != "":
        url = f"{ACCEPT_ORDER}/{order_id}"
    else:
        url = f"{ACCEPT_ORDER}/"

    # Формируем query-параметры
    params = {}
    if courier_id is not None:
        params["courierId"] = courier_id

    return requests.put(url, params=params)

def get_order_id_by_track(track):
    """Получает внутренний id заказа по его трек-номеру"""
    response = requests.get(f"{ORDERS}/track", params={"t": track})
    if response.status_code == 200:
        return response.json().get("order", {}).get("id")
    return None

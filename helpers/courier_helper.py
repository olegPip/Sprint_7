import random
import string
import requests

from endpoints import CREATE_COURIER


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

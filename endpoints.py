BASE_URL = "https://qa-scooter.education-services.ru"

CREATE_COURIER = f"{BASE_URL}/api/v1/courier"
LOGIN_COURIER = f"{CREATE_COURIER}/login"
ORDERS = f"{BASE_URL}/api/v1/orders"

DUPLICATE_COURIER_MESSAGE = "Этот логин уже используется. Попробуйте другой."

REQUIRED_FIELDS_MESSAGE = (
    "Недостаточно данных для создания учетной записи"
)

ACCEPT_ORDER = f"{BASE_URL}/api/v1/orders/accept"
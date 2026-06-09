import random
import string
import requests
from config import Config


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Config.COURIER_URL, data=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []


def login_courier_and_return_id(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(f"{Config.COURIER_URL}/login", data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None


def delete_courier(courier_id):
    requests.delete(f"{Config.COURIER_URL}/{courier_id}")


def create_order_and_return_track():
    payload = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Тестовая, д. 1",
        "metroStation": 1,
        "phone": "+79991234567",
        "rentTime": 1,
        "deliveryDate": "2025-12-31",
        "comment": "Тест"
    }
    response = requests.post(Config.ORDERS_URL, data=payload)
    if response.status_code == 201:
        return response.json().get("track")
    return None


def cancel_order(track):
    response = requests.put(f"{Config.ORDERS_URL}/cancel", params={"track": track})
    return response
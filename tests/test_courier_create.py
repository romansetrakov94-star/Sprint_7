import allure
import requests
from config import Config
from helpers import generate_random_string


@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_data):
        assert len(courier_data) == 3

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_data):
        login, password, first_name = courier_data
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(Config.COURIER_URL, data=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get("message", "")

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        payload = {"password": "pass", "firstName": "name"}
        response = requests.post(Config.COURIER_URL, data=payload)
        assert response.status_code == 400

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {"login": "log", "firstName": "name"}
        response = requests.post(Config.COURIER_URL, data=payload)
        assert response.status_code == 400

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_firstname(self):
        login = generate_random_string(10)
        payload = {"login": login, "password": "pass"}
        response = requests.post(Config.COURIER_URL, data=payload)
        assert response.status_code == 201
        assert response.json().get("ok") == True

    @allure.title("Успешный запрос возвращает ok: true")
    def test_create_courier_returns_ok(self):
        login = generate_random_string(10)
        payload = {"login": login, "password": "pass", "firstName": "name"}
        response = requests.post(Config.COURIER_URL, data=payload)
        assert response.status_code == 201
        assert response.json().get("ok") == True
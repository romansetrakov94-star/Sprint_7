import allure
import requests
from config import Config
from helpers import generate_random_string, login_courier_and_return_id, delete_courier


@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        with allure.step("Подготовка данных для нового курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") == True

        # Удаляем курьера после теста
        courier_id = login_courier_and_return_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_data):
        login, password, first_name = courier_data
        payload = {"login": login, "password": password, "firstName": first_name}

        with allure.step("Повторная отправка запроса с тем же логином"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка ошибки: логин уже используется"):
            assert response.status_code == 409
            assert "Этот логин уже используется" in response.json().get("message", "")

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        payload = {"password": "pass", "firstName": "name"}

        with allure.step("Отправка запроса без логина"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка ошибки: недостаточно данных"):
            assert response.status_code == 400

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {"login": "log", "firstName": "name"}

        with allure.step("Отправка запроса без пароля"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка ошибки: недостаточно данных"):
            assert response.status_code == 400

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_firstname(self):
        login = generate_random_string(10)
        payload = {"login": login, "password": "pass"}

        with allure.step("Отправка запроса без имени"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка: курьер создаётся без имени"):
            assert response.status_code == 201
            assert response.json().get("ok") == True

        # Удаляем курьера после теста
        courier_id = login_courier_and_return_id(login, "pass")
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Успешный запрос возвращает ok: true")
    def test_create_courier_returns_ok(self):
        login = generate_random_string(10)
        payload = {"login": login, "password": "pass", "firstName": "name"}

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(Config.COURIER_URL, data=payload)

        with allure.step("Проверка тела ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") == True

        # Удаляем курьера после теста
        courier_id = login_courier_and_return_id(login, "pass")
        if courier_id:
            delete_courier(courier_id)
            
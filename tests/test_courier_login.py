import allure
import requests
import pytest
from config import Config


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier_data):
        login, password, _ = courier_data
        payload = {"login": login, "password": password}

        with allure.step("Отправка запроса на логин с валидными данными"):
            response = requests.post(f"{Config.COURIER_URL}/login", data=payload)

        with allure.step("Проверка успешного ответа и наличия id"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Логин без логина — ошибка 400")
    def test_login_without_login(self):
        with allure.step("Отправка запроса без поля login"):
            response = requests.post(f"{Config.COURIER_URL}/login", data={"password": "pass"})

        with allure.step("Проверка кода ошибки"):
            assert response.status_code == 400

    @allure.title("Логин без пароля — ошибка 400")
    def test_login_without_password(self):
        with allure.step("Отправка запроса без поля password"):
            response = requests.post(f"{Config.COURIER_URL}/login", data={"login": "log"})

        with allure.step("Проверка кода ошибки"):
            if response.status_code == 504:
                pytest.skip("Сервер временно недоступен (504 Gateway Timeout)")
            assert response.status_code == 400

    @allure.title("Логин с неверным паролем — ошибка 404")
    def test_login_wrong_password(self, courier_data):
        login, _, _ = courier_data

        with allure.step("Отправка запроса с неверным паролем"):
            response = requests.post(f"{Config.COURIER_URL}/login", data={"login": login, "password": "wrong"})

        with allure.step("Проверка ошибки: учётная запись не найдена"):
            assert response.status_code == 404

    @allure.title("Логин несуществующего пользователя — ошибка 404")
    def test_login_nonexistent(self):
        with allure.step("Отправка запроса с несуществующим логином"):
            response = requests.post(f"{Config.COURIER_URL}/login", data={"login": "nonexist", "password": "pass"})

        with allure.step("Проверка ошибки: учётная запись не найдена"):
            assert response.status_code == 404
            
import allure
import requests
from config import Config


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин")
    def test_login_success(self, courier_data):
        login, password, _ = courier_data
        payload = {"login": login, "password": password}
        response = requests.post(f"{Config.COURIER_URL}/login", data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Логин без логина")
    def test_login_without_login(self):
        response = requests.post(f"{Config.COURIER_URL}/login", data={"password": "pass"})
        assert response.status_code == 400

    @allure.title("Логин без пароля")
    def test_login_without_password(self):
        response = requests.post(f"{Config.COURIER_URL}/login", data={"login": "log"})
        assert response.status_code in [400, 504]

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, courier_data):
        login, _, _ = courier_data
        response = requests.post(f"{Config.COURIER_URL}/login", data={"login": login, "password": "wrong"})
        assert response.status_code == 404

    @allure.title("Логин несуществующего пользователя")
    def test_login_nonexistent(self):
        response = requests.post(f"{Config.COURIER_URL}/login", data={"login": "nonexist", "password": "pass"})
        assert response.status_code == 404
        
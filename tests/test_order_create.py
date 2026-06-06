import pytest
import allure
import requests
from config import Config
from test_data import OrderTestData


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("color, expected_status", [
        (["BLACK", "GREY"], 201),
        ([], 201)
    ])
    def test_create_order_with_colors_success(self, color, expected_status):
        payload = OrderTestData.BASE_ORDER.copy()
        payload["color"] = color

        with allure.step(f"Отправка запроса на создание заказа с цветом: {color}"):
            response = requests.post(Config.ORDERS_URL, data=payload)

        with allure.step("Проверка успешного ответа и наличия track"):
            assert response.status_code == expected_status
            assert "track" in response.json()

    @allure.title("Создание заказа с одиночным цветом (известный баг)")
    @pytest.mark.xfail(reason="Сервер возвращает 500 на одиночный цвет (известный баг)")
    @pytest.mark.parametrize("color", ["BLACK", "GREY"])
    def test_create_order_with_single_color(self, color):
        payload = OrderTestData.BASE_ORDER.copy()
        payload["color"] = color

        with allure.step(f"Отправка запроса с одиночным цветом: {color}"):
            response = requests.post(Config.ORDERS_URL, data=payload)

        with allure.step("Проверка, что сервер не упал"):
            assert response.status_code == 201
            
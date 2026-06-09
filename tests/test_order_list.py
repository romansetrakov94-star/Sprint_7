import allure
import requests
from config import Config


@allure.feature("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(Config.ORDERS_URL)

        with allure.step("Проверка успешного ответа и наличия списка заказов"):
            assert response.status_code == 200
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)
            
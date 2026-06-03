import allure
import requests
from config import Config


@allure.feature("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(Config.ORDERS_URL)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
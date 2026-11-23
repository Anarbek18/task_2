import allure

import data
import helpers


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Авторизованный пользователь получает свои заказы")
    def test_get_orders_with_auth_returns_user_orders(self, registered_user, ingredient_ids):
        token = registered_user["token"]
        order_number = helpers.create_order({"ingredients": ingredient_ids}, token).json()["order"]["number"]

        response = helpers.get_user_orders(token)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert [order["number"] for order in body["orders"]] == [order_number]
        assert body["orders"][0]["ingredients"] == ingredient_ids

    @allure.title("Неавторизованный пользователь не получает заказы: 401")
    def test_get_orders_without_auth_returns_401(self):
        response = helpers.get_user_orders()

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": data.MSG_UNAUTHORISED}

import allure

import data
import helpers


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("С авторизацией и ингредиентами заказ создаётся")
    def test_create_order_with_auth_and_ingredients_success(self, registered_user, ingredient_ids):
        response = helpers.create_order({"ingredients": ingredient_ids}, registered_user["token"])
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["name"]
        assert isinstance(body["order"]["number"], int)

    @allure.title("Без авторизации, но с ингредиентами заказ создаётся")
    def test_create_order_without_auth_success(self, ingredient_ids):
        response = helpers.create_order({"ingredients": ingredient_ids})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["name"]
        assert isinstance(body["order"]["number"], int)

    @allure.title("Без ингредиентов заказ не создаётся: 400")
    def test_create_order_without_ingredients_returns_400(self, registered_user):
        response = helpers.create_order({"ingredients": []}, registered_user["token"])

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": data.MSG_NO_INGREDIENTS}

    @allure.title("С неверным хешем ингредиента заказ не создаётся: 500")
    def test_create_order_with_invalid_ingredient_hash_returns_500(self, registered_user):
        response = helpers.create_order(
            {"ingredients": [data.INVALID_INGREDIENT_HASH]}, registered_user["token"]
        )

        assert response.status_code == 500
        assert "Internal Server Error" in response.text

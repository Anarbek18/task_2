import allure
import pytest

import data
import helpers


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Можно залогиниться под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        payload = registered_user["payload"]

        response = helpers.login_user({"email": payload["email"], "password": payload["password"]})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {"email": payload["email"], "name": payload["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Неверные данные ({wrong_data}) -> 401")
    @pytest.mark.parametrize("wrong_data", ["email", "password", "email and password"])
    def test_login_with_wrong_credentials_returns_401(self, registered_user, wrong_data):
        payload = registered_user["payload"]
        credentials = {"email": payload["email"], "password": payload["password"]}
        if "email" in wrong_data:
            credentials["email"] = helpers.generate_user_payload()["email"]
        if "password" in wrong_data:
            credentials["password"] = helpers.generate_random_string(12)

        response = helpers.login_user(credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": data.MSG_INCORRECT_CREDENTIALS}

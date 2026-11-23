import allure
import pytest

import data
import helpers


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("С авторизацией можно изменить поле '{field}'")
    @pytest.mark.parametrize("field", ["email", "name"])
    def test_update_field_with_auth_success(self, registered_user, field):
        new_payload = helpers.generate_user_payload()
        payload = {**registered_user["payload"], field: new_payload[field]}

        response = helpers.update_user(payload, registered_user["token"])
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {"email": payload["email"], "name": payload["name"]}

    @allure.title("С авторизацией можно изменить пароль")
    def test_update_password_with_auth_success(self, registered_user):
        payload = {**registered_user["payload"], "password": helpers.generate_random_string(12)}

        update_response = helpers.update_user(payload, registered_user["token"])
        login_response = helpers.login_user(
            {"email": payload["email"], "password": payload["password"]}
        )

        assert update_response.status_code == 200
        assert update_response.json()["success"] is True
        assert login_response.status_code == 200

    @allure.title("Без авторизации нельзя изменить поле '{field}': 401")
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_field_without_auth_returns_401(self, registered_user, field):
        new_payload = helpers.generate_user_payload()
        payload = {**registered_user["payload"], field: new_payload[field]}

        response = helpers.update_user(payload)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": data.MSG_UNAUTHORISED}

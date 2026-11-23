import allure
import pytest

import data
import helpers


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Можно создать уникального пользователя")
    def test_create_unique_user_success(self, user_payload, user_cleanup):
        response = helpers.create_user(user_payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {"email": user_payload["email"], "name": user_payload["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Нельзя создать уже зарегистрированного пользователя")
    def test_create_existing_user_returns_403(self, registered_user):
        response = helpers.create_user(registered_user["payload"])

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": data.MSG_USER_EXISTS}

    @allure.title("Без обязательного поля '{missing_field}' возвращается 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_returns_403(self, user_payload, missing_field):
        payload = {key: value for key, value in user_payload.items() if key != missing_field}

        response = helpers.create_user(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": data.MSG_REQUIRED_FIELDS}

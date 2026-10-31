import pytest

import helpers


@pytest.fixture
def user_payload():
    """Данные нового пользователя (без регистрации)."""
    return helpers.generate_user_payload()


@pytest.fixture
def user_cleanup(user_payload):
    """Удаляет пользователя после теста (после ассертов), если он был создан."""
    yield
    helpers.cleanup_user(user_payload)


@pytest.fixture
def registered_user(user_payload):
    """Зарегистрированный пользователь: данные и токен. Удаляется после теста."""
    response = helpers.create_user(user_payload)
    assert response.status_code == 200, "Не удалось подготовить пользователя для теста"
    token = response.json()["accessToken"]
    yield {"payload": user_payload, "token": token}
    helpers.delete_user(token)


@pytest.fixture
def ingredient_ids():
    """Хеши двух существующих ингредиентов."""
    response = helpers.get_ingredients()
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    return [ingredient["_id"] for ingredient in response.json()["data"][:2]]

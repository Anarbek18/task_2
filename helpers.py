import random
import string

import allure
import requests

import data

TIMEOUT = 15


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_user_payload():
    return {
        "email": f"{generate_random_string()}@yandex.ru",
        "password": generate_random_string(),
        "name": generate_random_string(),
    }


def auth_headers(token):
    return {"Authorization": token}


@allure.step("Создать пользователя")
def create_user(payload):
    return requests.post(data.REGISTER_URL, json=payload, timeout=TIMEOUT)


@allure.step("Авторизовать пользователя")
def login_user(payload):
    return requests.post(data.LOGIN_URL, json=payload, timeout=TIMEOUT)


@allure.step("Изменить данные пользователя")
def update_user(payload, token=None):
    headers = auth_headers(token) if token else None
    return requests.patch(data.USER_URL, json=payload, headers=headers, timeout=TIMEOUT)


@allure.step("Удалить пользователя")
def delete_user(token):
    return requests.delete(data.USER_URL, headers=auth_headers(token), timeout=TIMEOUT)


@allure.step("Получить список ингредиентов")
def get_ingredients():
    return requests.get(data.INGREDIENTS_URL, timeout=TIMEOUT)


@allure.step("Создать заказ")
def create_order(payload, token=None):
    headers = auth_headers(token) if token else None
    return requests.post(data.ORDERS_URL, json=payload, headers=headers, timeout=TIMEOUT)


@allure.step("Получить заказы пользователя")
def get_user_orders(token=None):
    headers = auth_headers(token) if token else None
    return requests.get(data.ORDERS_URL, headers=headers, timeout=TIMEOUT)


def cleanup_user(payload):
    """Удаляет пользователя, если он существует (логинимся и удаляем по токену)."""
    response = requests.post(
        data.LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
        timeout=TIMEOUT,
    )
    if response.status_code == 200:
        delete_user(response.json()["accessToken"])

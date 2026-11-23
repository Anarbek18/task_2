BASE_URL = "https://stellarburgers.education-services.ru"

REGISTER_URL = f"{BASE_URL}/api/auth/register"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
USER_URL = f"{BASE_URL}/api/auth/user"
INGREDIENTS_URL = f"{BASE_URL}/api/ingredients"
ORDERS_URL = f"{BASE_URL}/api/orders"

# Тексты ошибок из документации API
MSG_USER_EXISTS = "User already exists"
MSG_REQUIRED_FIELDS = "Email, password and name are required fields"
MSG_INCORRECT_CREDENTIALS = "email or password are incorrect"
MSG_UNAUTHORISED = "You should be authorised"
MSG_NO_INGREDIENTS = "Ingredient ids must be provided"

INVALID_INGREDIENT_HASH = "invalid_ingredient_hash"

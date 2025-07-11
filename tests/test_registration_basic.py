import requests
from dotenv import load_dotenv
import os
import random

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

send_code_url = f"{BASE_URL}/authorization/sendVerificationCode"
register_url = f"{BASE_URL}/registration/basic"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}


def generate_unique_phone():
    return {
        "countryCode": "7",
        "number": f"900{random.randint(1000000, 9999999)}"
    }


def test_successful_registration():
    phone = generate_unique_phone()

    send_payload = {"phone": phone}
    send_response = requests.post(send_code_url, headers=headers, json=send_payload)
    assert send_response.status_code == 200, "Не удалось отправить код"

    send_data = send_response.json()
    token = send_data.get("result", {}).get("token")
    assert token, "token отсутствует в ответе"

    verification_code = "1234"

    register_payload = {
        "token": token,
        "verificationCode": verification_code,
        "user": {
            "name": "Тестовый"
        }
    }

    response = requests.post(register_url, headers=headers, json=register_payload)
    assert response.status_code == 200, f"❌ Ожидали 200, получили {response.status_code}"

    data = response.json()
    assert "result" in data, "В ответе нет поля result"
    user = data["result"].get("user")
    assert user is not None, "В ответе нет информации о пользователе"
    assert user.get("name") == "Тестовый", "Имя пользователя не совпадает"

    access = data["result"].get("access")
    assert access is not None, "В ответе нет информации о токене доступа"
    assert "token" in access, "В ответе нет access.token"
    assert "expire" in access, "В ответе нет access.expire"
    assert "refresh" in access, "В ответе нет access.refresh"


def test_registration_with_wrong_code():
    phone = generate_unique_phone()

    send_payload = {"phone": phone}
    send_response = requests.post(send_code_url, headers=headers, json=send_payload)
    assert send_response.status_code == 200, "Не удалось отправить код"

    send_data = send_response.json()
    token = send_data.get("result", {}).get("token")
    assert token, "token отсутствует в ответе"

    wrong_code = "1233"
    payload = {
        "token": token,
        "verificationCode": wrong_code,
        "user": {
            "name": "Тестовый"
        }
    }

    response = requests.post(register_url, headers=headers, json=payload)
    assert response.status_code == 403, f"❌ Ожидали 403, получили {response.status_code}"

    data = response.json()
    error = data.get("error")
    assert error is not None, "В ответе нет поля error"
    assert all(k in error for k in ("type", "message", "debugMessage")), "Ошибка не содержит нужных полей"

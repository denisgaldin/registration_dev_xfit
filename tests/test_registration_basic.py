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
    print(f"📡 Ответ на отправку кода (status {send_response.status_code}): {send_response.text}")
    assert send_response.status_code == 200, "Не удалось отправить код"

    send_data = send_response.json()
    token = send_data.get("result", {}).get("token")

    assert token, "token отсутствует в ответе"

    # TODO: Подставь здесь реальный verificationCode, который приходит в тестовом окружении
    verification_code = "1234"

    register_payload = {
        "token": token,
        "verificationCode": verification_code,
        "user": {
            "name": "Тестовый"
        }
    }

    response = requests.post(register_url, headers=headers, json=register_payload)

    print(f"📡 Status Code: {response.status_code}")
    print(f"📨 Response Body: {response.text}")

    assert response.status_code == 200, f"❌ Ожидали 200, получили {response.status_code}"

import uuid
import time
import httpx


BASE_URL = "http://backend:8000"
CONFIG_PATH = "./xray/config.json"


def test_add_and_remove_user():
    test_user = {
        "email": f"{uuid.uuid4()}@example.com",
        "uuid": str(uuid.uuid4()),
    }
    response = httpx.post(f"{BASE_URL}/user/add", json=test_user)
    assert response.status_code == 200
    print("Добавление прошло успешно:", response.json())
    time.sleep(1)
    response = httpx.post(f"{BASE_URL}/user/remove", json=test_user)
    assert response.status_code == 200
    print("Удаление прошло успешно:", response.json())

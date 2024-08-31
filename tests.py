import requests
import json

# Базовый URL вашего API
BASE_URL = "http://127.0.0.1:8000"

# Пример API-ключа, если используется авторизация
API_KEY = "user6_api_key"

# Заголовки для запросов
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def test_post_note():
    # Данные для POST запроса
    data = {
        "id": 1,
        "name": "Josh",
        "note": "Привет, как дела? Что желаешь?"
    }

    # Выполняем POST запрос
    response = requests.post(f"{BASE_URL}/users", json=data, headers=HEADERS)

    # Проверяем, что запрос был успешен
    assert response.status_code == 200
    # Проверяем, что ответ содержит ожидаемые данные
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Josh"
    assert response_data["note"] == "Привет, как дела? Что желаешь?"

def test_get_note():
    # Выполняем GET запрос для получения заметки по ID
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS)

    # Проверяем, что запрос был успешен
    assert response.status_code == 200

    # Декодируем содержимое ответа из JSON
    response_data = json.loads(response.content.decode('utf-8'))

    # Предполагаем, что данные возвращаются в виде списка
    assert isinstance(response_data, list)

    # Проверяем содержимое первого элемента списка
    if response_data:
        first_note = response_data[0]  # Работаем с первым элементом списка
        assert first_note["id"] == 1
        assert first_note["name"] == "Josh"
        assert first_note["note"] == "Привет, как дела? Что желаешь?"

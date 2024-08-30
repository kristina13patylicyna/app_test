from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import json
from typing import List
import requests
from fastapi.security import APIKeyHeader



app = FastAPI()
file_path = "users.json" # файл с данными

# API ключи пользователей (для примера)
API_KEYS = {
    "user1_api_key": "user1",
    "user2_api_key": "user2",
    "user3_api_key": "kristina",
    "user4_api_key": "alena",
    "user5_api_key": "dmitriy"
}

# Зависимость для получения API ключа
api_key_header = APIKeyHeader(name="X-API-Key")

# класс юзера(pydantic)
class User(BaseModel):
    id: int
    name: str
    note: str

# Функция чтения получает путь до файла и читает его
def read_data(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)

# Функция записи данных: получает путь до файла и данные,которые нужно записать
def write_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Функция для проверки орфографии с использованием Яндекс.Спеллер
def check_spelling(note: str):
    response = requests.get(
        "https://speller.yandex.net/services/spellservice.json/checkText", # используем api сайта и метод checkText
        params={"note": note}
    )
    errors = response.json() # сохраняем найденные ошибки

    errors_messages: list = []
    if errors:
        for error in errors:
            errors_messages.append("У вас ошибка в слове:" + error['word'])

        raise HTTPException(status_code=400, detail=errors_messages)



# Функция для получения заметок текущего пользователя
def get_user_data(api_key: str):
    username = API_KEYS.get(api_key)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    data_file = read_data(file_path)
    # Возвращаем данные только для текущего пользователя
    return [user for user in data_file if user.get("username") == username]  # уточнить моментик



# GET запрос для получения всех заметок пользователя
@app.get("/users", response_model=List[User])
async def get_users(api_key: str = Depends(api_key_header)):
    return get_user_data(api_key)

# POST запрос для добавления новой записи
@app.post("/users", response_model=User)
async def add_user(user: User, api_key: str = Depends(api_key_header)):
    username = API_KEYS.get(api_key)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    data = read_data(file_path)

    # Проверка орфографии в заметке
    check_spelling(user.note)

    # Добавление новой записи с привязкой к пользователю
    user_dict = user.model_dump()
    user_dict["username"] = username
    data.append(user_dict)

    write_data(data)

    return user

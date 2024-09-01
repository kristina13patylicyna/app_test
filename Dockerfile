# Используем официальный образ Python 3.9
FROM python:3.12.2

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы приложения в рабочую директорию
COPY requirements.txt .
COPY tests.py .
COPY users.json .


RUN pip install -r requirements.txt

COPY app/ .

# Указываем команду запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Используем тот же базовый образ
FROM python:3.11-slim

# Установка необходимых системных зависимостей (например, для компиляции асинхронных библиотек)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем зависимости
# Убедитесь, что aiogram здесь
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Команда запуска: просто запускаем основной скрипт Python
# Этот процесс будет контролироваться Docker Compose и политикой restart: always
CMD ["python", "main.py"]

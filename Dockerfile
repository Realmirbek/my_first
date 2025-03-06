# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt перед установкой зависимостей
COPY ./requirements.txt /app/requirements.txt


# Обновляем pip и устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Копируем весь проект (включая manage.py)
COPY mysite /app/

# Открываем порт 8000
EXPOSE 8000
# Устанавливаем переменную окружения, чтобы вывод не был буферизован


# Запускаем сервер Django
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]


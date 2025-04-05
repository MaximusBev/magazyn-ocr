# Базовий образ із підтримкою Python і системних бібліотек
FROM python:3.11-slim

# Встановлення системних залежностей
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Створення робочої директорії
WORKDIR /app

# Копіюємо проєкт
COPY . .

# Встановлення Python-залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт
EXPOSE 8000

# Команда запуску (через gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

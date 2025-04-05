# Вихідний образ з Python та apt
FROM python:3.11-slim

# Оновлення системи і встановлення Tesseract + залежностей
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файли в контейнер
WORKDIR /app
COPY . .

# Встановлюємо Python залежності
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Відкриваємо порт
EXPOSE 5000

# Запускаємо додаток
CMD ["python", "app.py"]

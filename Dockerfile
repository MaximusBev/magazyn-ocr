FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1-mesa-glx tesseract-ocr-pol && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

FROM python:3.11-slim
WORKDIR /app

# Установка clamav и зависимостей
RUN apt-get update \
    && apt-get install -y clamav clamav-daemon \
    && freshclam \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY virus-scan-service .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

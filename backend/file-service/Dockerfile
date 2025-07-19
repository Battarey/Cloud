FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt

RUN apt-get update \
    && apt-get install -y clamav clamav-daemon netcat-openbsd \
    && freshclam \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY file-service .
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
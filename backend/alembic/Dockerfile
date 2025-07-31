FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем alembic и конфиг
COPY alembic ./alembic
COPY alembic/alembic.ini ./alembic.ini

# Копируем весь file_service и user_service
COPY file_service ./file_service
COPY user_service ./user_service


# Копируем entrypoint.sh
COPY ../entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app
CMD ["alembic", "upgrade", "head"]
 
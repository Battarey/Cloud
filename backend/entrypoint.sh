#!/bin/sh

# Ждем, пока Postgres станет доступен
while ! nc -z postgres 5432; do
  echo "Ожидание Postgres..."
  sleep 5
done

# Применяем миграции Alembic
alembic upgrade head


# Если переданы аргументы — выполнить их, иначе запустить uvicorn
if [ $# -eq 0 ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000
else
  exec "$@"
fi

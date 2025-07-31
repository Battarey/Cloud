#!/bin/sh

# Ждем, пока Postgres станет доступен
while ! nc -z postgres 5432; do
  echo "Ожидание Postgres..."
  sleep 2
done

# Если нужно дождаться появления самой базы (для alembic)
if [ "$1" = "alembic" ]; then
  shift
  DB_NAME="${POSTGRES_DB:-cloud_db}"
  DB_USER="${POSTGRES_USER:-clouduser}"
  DB_PASS="${POSTGRES_PASSWORD:-cloudpass}"
  until PGPASSWORD="$DB_PASS" psql -h postgres -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; do
    echo "Ожидание создания базы данных $DB_NAME..."
    sleep 2
  done
  echo "База данных $DB_NAME готова!"
  alembic upgrade head
  echo "Миграции успешно применены"
  exit 0
fi

# Если переданы аргументы — выполнить их, иначе запустить uvicorn
if [ $# -eq 0 ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000
else
  exec "$@"
fi

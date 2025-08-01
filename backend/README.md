# Backend для облачного хранилища

## Описание
Микросервисный backend для облачного хранилища на Python (FastAPI).

## Архитектура backend
```
backend
├── alembic/                     # сервис для применения alembic миграций к БД
├── file-service/                # сервис для работы с файлами
├── gateway/                     # API Gateway, единая точка входа
├── user-service/                # сервис для работы с пользователем 
├── .env                         # переменные окружения 
├── docker-compose.yml           # оркестрация сервисов и инфраструктуры 
├── entrypoint.sh                # скрипт для применения alembic миграций (более подробно ниже)
├── README.md
└── requirements.txt             # файл с основными зависимостями для backend
```

## Запуск
```
docker compose up --build
```

## Применение Alembic миграций (На данный момент не актуально)
Сначала исправить .env, убрать из DATABASE_URL символы "+asyncpg"
- User-serive:
```
-
```
- File-service:
```
docker compose run --rm --workdir /app/file-service file-service alembic -c alembic.ini upgrade head
```
Добавить обратно "+asyncpg" в DATABASE_URL 

## Используемые инструменты
- PostgreSQL
- MinIO
- Redis
- ClamAV

## Переменные окружения
- .env — настройки БД, MinIO и др.

## Безопасность
- JWT, CORS, HTTPS, лимиты, защита от инъекций, проверка файлов (Не покрыто пока что полностью)

## entrypoint.sh
Файл для того, чтобы скрипт ждал запуска контейнера с postgre, после чего к postgre применяются alembic миграции, после чего активируются file_service и user_service.

## TODO
- Реализация сервисов
- Документация API
- Тесты: e2e, нагрузочные
- Подтверждение почты при регистрации
- Создание собственного API
- Система шифрования
- 2х факторная аунтефикация
- Реферальная программа

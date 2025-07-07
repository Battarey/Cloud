# Backend для облачного хранилища

## Описание
Микросервисный backend для облачного хранилища на Python (FastAPI).

## Архитектура backend
```
backend
├── file-service/                # сервис для работы с файлами
├── gateway/                     # API Gateway, единая точка входа
├── user-service/                # сервис для работы с пользователем 
├── virus-scan-service/          # сервис проверки файлов на вирусы (ClamAV)
├── .env.example                 # переменные окружения 
├── docker-compose.yml           # оркестрация сервисов и инфраструктуры 
├── README.md
└── requirements.txt             # файл с основными зависимостями для backend
```

## Запуск
```
docker compose up --build
```

## Используемые инструменты
- PostgreSQL
- MinIO
- Redis
- ClamAV

## Переменные окружения
- .env — настройки БД, MinIO и др.

## Безопасность
- JWT, CORS, HTTPS, лимиты, защита от инъекций, проверка файлов

## TODO
- Реализация сервисов
- Документация API
- Тесты: интеграционные, unit, e2e, нагрузочные

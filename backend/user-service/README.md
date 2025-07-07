# user-service

## Описание
Микросервис для управления пользователями: регистрация, авторизация, профиль, статистика, удаление аккаунта, работа с токенами и сессиями.

## Архитектура user-service
```
user-service
├── alembic/            # папка для alembic миграций
├── authorization/      # авторизация (логин, refresh, получение текущего пользователя)
├── delete_account/     # удаление аккаунта
├── logout/             # выход из аккаунта (revoke refresh token)
├── models/             # модели БД
├── registration/       # регистрация пользователей
├── schemas/            # Pydantic-схемы
├── security/           # безопасность: токены, пароли, лимитеры
├── statistics/         # статистика пользователя
├── alembic.ini         # файл для работы с alembic
├── database.py         # подключение к БД
├── Dockerfile
├── main.py
└── README.md
```

## TODO
- Покрытие тестами
- Рефакторинг

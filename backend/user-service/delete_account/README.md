# delete_account

## Описание
Модуль для удаления аккаунта пользователя.

## Архитектура
```
delete_account/
├── router.py   # роут удаления аккаунта
├── service.py  # бизнес-логика удаления
└── README.md
```

## Основные задачи
- Удаление аккаунта пользователя

## API

### DELETE /delete_account
Удаление пользователя

Заголовок: Authorization: Bearer <access_token>

Успешный ответ:
204 No Content

Ошибки:
- 401 Unauthorized — если токен невалиден
- 404 Not Found — если пользователь не найден

# logout

## Описание
Модуль выхода пользователя из аккаунта (logout, отзыв refresh токена).

## Архитектура
```
logout/
├── router.py   # роут logout
├── service.py  # бизнес-логика выхода
└── README.md
```

## Основные задачи
- Logout пользователя (revoke refresh token)

## API

### POST /logout
Выход из аккаунта (отзыв refresh-токена)

Запрос:
```
{
  "refresh_token": "..."
}
```
Заголовок: Content-Type: application/json

Успешный ответ:
204 No Content

Ошибки:
- 401 Unauthorized — если refresh_token невалиден или истёк
- 400 Bad Request — если формат запроса неверный

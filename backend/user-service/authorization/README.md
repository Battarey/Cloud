# authorization

## Описание
Модуль авторизации: логин, refresh токен, получение текущего пользователя (me).

## Архитектура
```
authorization/
├── router.py   # роуты авторизации
├── service.py  # бизнес-логика авторизации
└── README.md
```

## Основные задачи
- Логин пользователя
- Обновление access/refresh токена
- Получение информации о текущем пользователе

## API


### POST /auth/login
Вход пользователя

Запрос:
```
{
  "email": "user@example.com",
  "password": "string"
}
```
Заголовок: Content-Type: application/json

Успешный ответ:
```
{
  "access_token": "...",
  "refresh_token": "..."
}
```

Ошибки:
- 401 Unauthorized — неверный email или пароль
- 400 Bad Request — некорректный формат запроса

### POST /auth/refresh
Обновление access-токена

Запрос:
```
{
  "refresh_token": "..."
}
```
Заголовок: Content-Type: application/json

Успешный ответ:
```
{
  "access_token": "..."
}
```

Ошибки:
- 401 Unauthorized — refresh_token невалиден или истёк
- 400 Bad Request — некорректный формат запроса

### GET /profile/me
Получение профиля текущего пользователя

Заголовок: Authorization: Bearer <access_token>

Успешный ответ:
```
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Имя"
}
```

Ошибки:
- 401 Unauthorized — невалидный или отсутствует access_token

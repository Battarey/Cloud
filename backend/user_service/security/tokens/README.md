# tokens

## Описание
Работа с JWT и refresh токенами.

## Архитектура
```
tokens/
├── jwt.py      # JWT-токены
├── refresh.py  # refresh-токены
└── README.md
```

## API

### JWT токены
- Генерация access и refresh токенов для авторизации пользователей.
- Валидация токенов при каждом запросе к защищённым эндпоинтам.

Ошибки:
- 401 Unauthorized — невалидный или истёкший токен
- 400 Bad Request — некорректный формат токена

### Пример
- Access token: срок жизни 15 минут.
- Refresh token: срок жизни 30 дней.
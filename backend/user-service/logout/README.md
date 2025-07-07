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

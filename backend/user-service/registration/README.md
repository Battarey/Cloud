# registration

## Описание
Модуль регистрации пользователей.

## Архитектура
```
registration/
├── router.py   # роут регистрации
├── service.py  # бизнес-логика регистрации
└── README.md
```

## Основные задачи
- Регистрация нового пользователя
- Валидация данных

## API


### POST /registration/register
Регистрация нового пользователя

Запрос:
```
{
  "email": "user@example.com",
  "password": "string",
  "name": "Имя"
}
```
Заголовок: Content-Type: application/json

Успешный ответ:
```
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Имя"
}
```

Ошибки:
- 400 Bad Request — некорректные данные или email уже занят

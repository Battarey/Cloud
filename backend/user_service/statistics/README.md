# statistics

## Описание
Модуль для работы со статистикой пользователя (количество файлов, общий размер, свободное место).

## Архитектура
```
statistics/
├── router.py   # роут статистики
├── service.py  # бизнес-логика статистики
└── README.md
```

## API


### POST /user-stat/update
Обновление статистики пользователя

Запрос:
```
{
  "user_id": "uuid",
  "action": "upload|delete",
  "file_size": 12345
}
```
Заголовок: Content-Type: application/json

Успешный ответ:
```
{
  "status": "ok",
  "files_count": 10,
  "files_size": 123456,
  "free_space": 987654
}
```

Ошибки:
- 404 Not Found — пользователь не найден
- 400 Bad Request — некорректные данные или действие

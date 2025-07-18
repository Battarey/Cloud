# list_files

## Описание
Модуль получения списка файлов и папок пользователя.

## Архитектура
```
list_files/
├── router.py   # роут списка файлов
├── service.py  # бизнес-логика получения списка
└── README.md
```

## API

### GET /files/
Получение списка файлов и папок пользователя
Параметры: folder_id, name, created_from, created_to, size_min, size_max, file_type
Заголовок: Authorization: Bearer <access_token>
Ответ: массив объектов FileRead

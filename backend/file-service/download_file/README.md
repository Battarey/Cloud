# download_file

## Описание
Модуль скачивания файлов пользователями (загрузка из MinIO, проверка прав доступа).

## Архитектура
```
download_file/
├── router.py   # роут скачивания файла
├── service.py  # бизнес-логика скачивания
└── README.md
```

## API

### GET /files/{file_id}
Скачивание файла пользователем
Заголовок: Authorization: Bearer <access_token>
Ответ: файл в бинарном виде, заголовок Content-Disposition: attachment; filename="file.txt"

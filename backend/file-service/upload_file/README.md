# upload_file

## Описание
Модуль загрузки файлов пользователями (upload, сохранение в MinIO, запись метаданных в БД).

## Архитектура
```
upload_file/
├── README.md
├── router.py   # роут загрузки файлов
└── service.py  # бизнес-логика загрузки
```

## API

### POST /files/upload
Загрузка файла пользователем
Запрос: multipart/form-data, поле upload
Заголовок: Authorization: Bearer <access_token>
Ответ:
```
{
  "id": "uuid",
  "filename": "file.txt",
  "size": 12345,
  "content_type": "text/plain",
  "created_at": "2025-07-18T12:00:00"
}
```

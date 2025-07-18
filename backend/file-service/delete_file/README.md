# delete_file

## Описание
Модуль удаления файлов пользователями (удаление из MinIO и из БД).

## Архитектура
```
delete_file/
├── router.py   # роут удаления файла
├── service.py  # бизнес-логика удаления
└── README.md
```

## API

### DELETE /files/{file_id}
Удаление файла пользователем
Заголовок: Authorization: Bearer <access_token>
Ответ:
```
{
  "status": "deleted"
}
```

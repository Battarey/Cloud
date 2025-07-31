# delete_folder

## Описание
Модуль удаления папки пользователем (удаление папки и всех файлов внутри из MinIO и БД).

## Архитектура
```
delete_folder/
├── router.py   # роут удаления папки
├── service.py  # бизнес-логика удаления
└── README.md
```

## API

### DELETE /folders/{folder_id}
Удаление папки и всех файлов внутри пользователем
Заголовок: Authorization: Bearer <access_token>
Ответ:
```
{
  "status": "deleted"
}
```

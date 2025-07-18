# rename_file

## Описание
Модуль переименования файлов и папок пользователем.

## Архитектура
```
rename_file/
├── router.py   # роут переименования файла/папки
├── service.py  # бизнес-логика переименования
└── README.md
```

## API

### PATCH /files/{file_id}
Переименование файла пользователем
Запрос:
```
{
  "new_name": "new_file.txt"
}
```
Заголовок: Authorization: Bearer <access_token>
Ответ: объект FileRead

### PATCH /folders/{folder_id}
Переименование папки пользователем
Запрос:
```
{
  "new_name": "new_folder"
}
```
Заголовок: Authorization: Bearer <access_token>
Ответ: объект FileRead

# create_folder

## Описание
Модуль создания папки пользователем (создание записи в БД, структура для хранения файлов).

## Архитектура
```
create_folder/
├── router.py   # роут создания папки
├── service.py  # бизнес-логика создания
└── README.md
```

## API

### POST /folders/create
Создание новой папки пользователем
Запрос:
```
{
  "folder_name": "new_folder"
}
```
Заголовок: Authorization: Bearer <access_token>
Ответ:
```
{
  "id": "uuid",
  "name": "new_folder",
  "status": "created"
}
```

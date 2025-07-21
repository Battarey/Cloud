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


## Chunked upload (загрузка файла по частям)

### Когда используется chunked upload?
- Если размер файла превышает 5 МБ, используйте загрузку по частям (endpoint `/files/upload/chunk`).
- Для файлов ≤ 5 МБ используйте обычный endpoint `/files/upload`.
- Если попытаться загрузить большой файл через обычный upload, сервис вернёт ошибку с советом использовать chunked upload.

### Endpoint
`POST /files/upload/chunk`

**Параметры запроса:**
- `chunk` (UploadFile, form-data) — содержимое части файла
- `chunk_number` (int, query) — номер чанка (начиная с 1)
- `total_chunks` (int, query) — общее количество чанков
- `upload_id` (str, query) — уникальный идентификатор загрузки (UUID или строка)
- `filename` (str, query) — имя файла
- `user_id` (str, query) — идентификатор пользователя

**Ограничения:**
- Максимальный размер одного чанка: 5 МБ
- Если загрузка не обновлялась более 4 часов, временные файлы автоматически удаляются

**Пример (cURL):**
```
curl -X POST "http://localhost:8000/files/upload/chunk?chunk_number=1&total_chunks=3&upload_id=some-uuid&filename=bigfile.bin&user_id=..." \
  -F "chunk=@part1.bin"
```

### Логика выбора способа загрузки
- На фронте: если файл > 5 МБ — разбить на чанки и отправлять через `/files/upload/chunk`
- На бэке: если файл > 5 МБ и используется обычный upload — возвращается ошибка 413 с советом использовать chunked upload

---

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

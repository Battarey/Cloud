# scan

## Описание
Модуль проверки файлов на вирусы с помощью ClamAV.

## Архитектура
```
scan/
├── router.py   # роут для проверки файла (POST /scan)
├── service.py  # бизнес-логика проверки через clamscan
└── README.md
```

## API

### POST /scan
Проверка файла на вирусы
Запрос: multipart/form-data, поле file
Ответ (чистый):
```
{
  "clean": true
}
```
Ответ (заражён):
```
{
  "clean": false,
  "detail": "...вывод clamscan..."
}
```

Ошибки:
- 400 Bad Request — некорректный файл
- 500 Internal Server Error — ошибка ClamAV или сервиса

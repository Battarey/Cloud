# filtration

## Описание
Модуль фильтрации файлов и папок по различным параметрам (имя, дата создания, размер, тип и др.).

## Архитектура
```
filtration/
├── __init__.py
├── README.md
├── schemas.py   # схемы фильтрации (pydantic)
└── service.py   # бизнес-логика фильтрации
```

## Основные задачи
- Фильтрация файлов/папок по имени (частичное совпадение)
- Фильтрация по дате создания (от/до)
- Фильтрация по размеру (min/max)
- Фильтрация по типу файла (content_type/folder)
- Поддержка фильтрации только по одному параметру за раз (приоритет: name, created_from, created_to, size_min, size_max, file_type)

# Unit-тесты file-service

## Команда для запуска всех unit тестов
```
docker compose run --rm file-service pytest tests/unit/
```

## Команда для запуска одного файла с unit тестами:
```
docker compose run --rm file-service pytest tests/unit/NAME_TEST.py
```

## Команда для запуска одной функции в файле с unit тестами
```
docker compose run --rm file-service pytest tests/unit/NAME_TEST.py::NAME_FUNCTION
```

## Структура и статистика тестов:
```
- test_create_folder.py      # Пройден
- test_delete_file.py        # Пройден
- test_delete_folder.py      # Пройден
- test_download_file.py      # Пройден
- test_filtration.py         # Пройден
- test_list_files.py         # Пройден
- test_minio_utils.py        # Пройден
- test_models.py             # Пройден
- test_rename.py             # Пройден
- test_schemas.py            # Пройден
- test_security.py           # Пройден
- test_statistics.py         # Пройден
- test_upload_file.py        # Пройден
```

## Подсказка
Если тесты не работают и ты решил внести изменения - перезапусти все сервисы
(CTRL + C в консоли, где запущен docker-compose, это сработает только если запущено без пометки -d, т.е ты запустил docker-compose с выводом логов)

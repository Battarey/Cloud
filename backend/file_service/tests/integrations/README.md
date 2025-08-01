# Интеграционные тесты для file-service

## Директория
Тесты запускать из папки backend

## Команда для запуска (запускать тесты по одному)
```
docker compose run --rm file-service pytest tests/integrations/NAME_TEST.py
```

## Команда для запуска одной функции в файле с интеграционными тестами
```
docker compose run --rm file-service pytest tests/integrations/NAME_TEST.py::NAME_FUNCTION
```

## Структура и статистика тестов:
```
test_chunk_upload.py              # Пройден
test_create_folder.py             # Пройден
test_crypto_flow.py               # Не пройден
test_delete_file.py               # Пройден
test_delete_folder.py             # Пройден
test_download_file.py             # Не пройден
test_generate_link.py             # Не пройден
test_list_files.py                # Пройден
test_rename.py                    # Пройден
test_upload_file.py               # Не пройден
```

## Подсказка
Если тесты не работают и ты решил внести изменения - перезапусти все сервисы
(CTRL + C в консоли, где запущен docker-compose, это сработает только если запущено без пометки -d, т.е ты запустил docker-compose с выводом логов)

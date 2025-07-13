# Интеграционные тесты для file-service


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
test_create_folder.py             # Пройден, 1 предупреждение
test_delete_file.py               # Пройден, 1 предупреждение
test_delete_folder.py             # Пройден, 1 предупреждение
test_download_file.py             # Пройден, 1 предупреждение
test_list_files.py                # Пройден, 1 предупреждение
test_rename.py                    # Пройден, 1 предупреждение
test_upload_file.py               # Не пройден
```

## Подсказка
Если тесты не работают и ты решил внести изменения - перезапусти все сервисы
(CTRL + C в консоли, где запущен docker-compose, это сработает только если запущено без пометки -d, т.е ты запустил docker-compose с выводом логов)

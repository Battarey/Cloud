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
test_create_folder_integration.py         # Не пройден
test_delete_file_integration.py           # Не пройден
test_delete_folder_integration.py         # Не пройден
test_download_file_integration.py         # Не пройден
test_list_files_integration.py            # Не пройден
test_rename_integration.py                # Не пройден
test_upload_file_integration.py           # Не пройден
```

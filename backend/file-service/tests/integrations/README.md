# Интеграционные тесты для user-service

## Команда для запуска (запускать тесты по одному)
```
docker compose run --rm user-service pytest tests/integrations/NAME_TEST.py
```

## Команда для запуска одной функции в файле с интеграционными тестами
```
docker compose run --rm user-service pytest tests/integrations/NAME_TEST.py::NAME_FUNCTION
```

## Структура и статистика тестов:
```
- later
```

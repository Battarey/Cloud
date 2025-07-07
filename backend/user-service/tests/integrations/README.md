# Интеграционные тесты для user-service

## Команда для запуска (запускать тесты по одному)
```
docker compose run --rm user-service pytest user-service/tests/integrations/NAME_TEST.py
```

## Команда для запуска одной функции в файле с интеграционными тестами
```
docker compose run --rm user-service pytest user-service/tests/integrations/NAMET_EST.py::NAME_FUNCTION
```

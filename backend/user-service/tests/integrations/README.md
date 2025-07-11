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
- test_authorization_integration          # Пройден
- test_delete_account_integration         # Пройден
- test_limiter_integration                # Пройден
- test_logout_integration                 # Пройден
- test_registration_integration           # Пройден
- test_security_integration               # Пройден
- test_statistics_integration             # Пройден
```

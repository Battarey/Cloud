# Интеграционные тесты для user-service

## Директория
Тесты запускать из папки backend

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
- test_authorization               # Пройден
- test_delete_account              # Пройден
- test_limiter                     # Пройден
- test_logout                      # Пройден
- test_registration                # Пройден
- test_security                    # Пройден
- test_statistics                  # Пройден
```

## Подсказка
Если тесты не работают и ты решил внести изменения - перезапусти все сервисы
(CTRL + C в консоли, где запущен docker-compose, это сработает только если запущено без пометки -d, т.е ты запустил docker-compose с выводом логов)

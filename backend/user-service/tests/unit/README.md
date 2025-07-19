# Unit тесты для user-service

## Команда для запуска всех unit тестов
```
docker compose run --rm user-service pytest tests/unit/
```

## Команда для запуска одного файла с unit тестами
```
docker compose run --rm user-service pytest tests/unit/NAME_TEST.py
```

## Команда для запуска одной функции в файле с unit тестами
```
docker compose run --rm user-service pytest tests/unit/NAME_TEST.py::NAME_FUNCTION
```

## Структура и статистика тестов:
```
- test_authorization.py        # Пройден
- test_delete_account.py       # Пройден
- test_jwt.py                  # Пройден
- test_limiter.py              # Пройден
- test_logout.py               # Пройден
- test_password.py             # Пройден
- test_refresh.py              # Пройден
- test_registration.py         # Пройден
- test_sample.py               # Пройден
- test_statistics_service.py   # Пройден
- test_statistics.py           # Пройден
```

## Подсказка
Если тесты не работают и ты решил внести изменения - перезапусти все сервисы
(CTRL + C в консоли, где запущен docker-compose, это сработает только если запущено без пометки -d, т.е ты запустил docker-compose с выводом логов)

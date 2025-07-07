# Unit тесты для user-service

## Команда для запуска всех unit тестов
```
docker compose run --rm user-service pytest user-service/tests/unit/
```

## Команда для запуска одного файла с unit тестами
```
docker compose run --rm user-service pytest user-service/tests/unit/NAME_TEST.py
```

## Команда для запуска одной функции в файле с unit тестами
```
docker compose run --rm user-service pytest user-service/tests/unit/NAME_TEST.py::NAME_FUNCTION
```

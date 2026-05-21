# Виджет банковских операций

Проект для демонстрации банковских транзакций в личном кабинете.

## Функциональность

- Маскировка номеров карт и счетов (`src.masks`)
- Фильтрация операций по статусу (`src.processing.filter_by_state`)
- Сортировка операций по дате (`src.processing.sort_by_date`)

## Установка

```bash
poetry install
```

## Модуль 'generators'

Содержит генераторы для эффективной обработки списков транзакций.

### `filter_by_currency(transactions, currency_code)`

Итератор, возвращающий транзакции с заданной валютой.

```python
from src.generators import filter_by_currency

for transaction in filter_by_currency(transactions, "USD"):
    print(transaction)
```

## Декоратор `log`

Модуль `decorators` предоставляет декоратор `log` для автоматического логирования вызовов функций.

### Использование

```python
from src.decorators import log

@log(filename="log.txt")
def my_func(x, y):
    return x + y

my_func(1, 2)   # запись в файл: my_func ok

@log()          # логирование в консоль
def divide(a, b):
    return a / b

divide(10, 0)   # вывод: divide error: ZeroDivisionError. Inputs: (10, 0), {}
```
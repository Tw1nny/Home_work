"""
Тесты для модуля generators.
"""
import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура с типовыми транзакциями
@pytest.fixture
def sample_transactions() -> list:
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"amount": "100.50", "currency": {"code": "USD", "name": "USD"}},
        },
        {
            "id": 2,
            "description": "Оплата услуг",
            "operationAmount": {"amount": "50.00", "currency": {"code": "EUR", "name": "EUR"}},
        },
        {
            "id": 3,
            "description": "Покупка билетов",
            "operationAmount": {"amount": "200.00", "currency": {"code": "USD", "name": "USD"}},
        },
        {
            "id": 4,
            "description": "Перевод другу",
            "operationAmount": {"amount": "30.00", "currency": {"code": "RUB", "name": "RUB"}},
        },
    ]


def test_filter_by_currency_usd(sample_transactions: list) -> None:
    """Фильтрация по USD должна вернуть 2 транзакции."""
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_eur(sample_transactions: list) -> None:
    """Фильтрация по EUR."""
    result = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_currency_no_match(sample_transactions: list) -> None:
    """Нет транзакций с указанной валютой."""
    result = list(filter_by_currency(sample_transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_list() -> None:
    """Пустой список транзакций."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions(sample_transactions: list) -> None:
    """Проверка генератора описаний."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = ["Перевод организации", "Оплата услуг", "Покупка билетов", "Перевод другу"]
    assert descriptions == expected


def test_transaction_descriptions_missing_description() -> None:
    """Если в транзакции нет поля 'description', выдаётся пустая строка."""
    transactions = [{"id": 1}, {"id": 2, "description": "Есть описание"}]
    result = list(transaction_descriptions(transactions))
    assert result == ["", "Есть описание"]


def test_card_number_generator_range_start_stop() -> None:
    """Генерация номеров для небольшого диапазона."""
    gen = card_number_generator(1, 5)
    numbers = list(gen)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert numbers == expected


def test_card_number_generator_large_number() -> None:
    """Генерация с большим числом, проверка форматирования."""
    gen = card_number_generator(1234567890123456, 1234567890123456)
    number = next(gen)
    assert number == "1234 5678 9012 3456"


def test_card_number_generator_start_equal_stop() -> None:
    """Один номер."""
    gen = card_number_generator(42, 42)
    assert next(gen) == "0000 0000 0000 0042"
    with pytest.raises(StopIteration):
        next(gen)


# Параметризация для различных диапазонов
@pytest.mark.parametrize(
    "start,stop,expected_first",
    [
        (1, 1, "0000 0000 0000 0001"),
        (10, 10, "0000 0000 0000 0010"),
        (9999, 9999, "0000 0000 0000 9999"),
        (10000, 10000, "0000 0000 0001 0000"),
    ],
)
def test_card_number_generator_parametrized(start: int, stop: int, expected_first: str) -> None:
    """Параметризованный тест граничных значений."""
    gen = card_number_generator(start, stop)
    assert next(gen) == expected_first

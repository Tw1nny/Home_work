"""
Тесты для модуля processing.
"""
import pytest
from src.processing import filter_by_state, sort_by_date


# Фикстура с набором транзакций
@pytest.fixture
def transaction_list() -> list:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
        {"id": 4, "state": "PENDING", "date": "2021-01-01T00:00:00"},
    ]


# Фикстура для пустого списка
@pytest.fixture
def empty_list() -> list:
    return []


# Параметризация для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("NONEXISTENT", []),
    ],
)
def test_filter_by_state(transaction_list: list, state: str, expected_ids: list) -> None:
    """Тест фильтрации по различным статусам."""
    filtered = filter_by_state(transaction_list, state)
    assert [item["id"] for item in filtered] == expected_ids


def test_filter_by_state_default(transaction_list: list) -> None:
    """Тест со значением state по умолчанию."""
    filtered = filter_by_state(transaction_list)
    assert [item["id"] for item in filtered] == [1, 3]


def test_filter_by_state_empty_list(empty_list: list) -> None:
    """Тест на пустом списке."""
    assert filter_by_state(empty_list) == []
    assert filter_by_state(empty_list, "EXECUTED") == []


# Параметризация для sort_by_date
@pytest.mark.parametrize(
    "descending, expected_ids",
    [
        (True, [4, 3, 1, 2]),  # убывание: самые новые сначала
        (False, [2, 1, 3, 4]),  # возрастание: самые старые сначала
    ],
)
def test_sort_by_date(transaction_list: list, descending: bool, expected_ids: list) -> None:
    """Тест сортировки по дате."""
    sorted_list = sort_by_date(transaction_list, descending=descending)
    assert [item["id"] for item in sorted_list] == expected_ids


def test_sort_by_date_default(transaction_list: list) -> None:
    """Тест сортировки по умолчанию (убывание)."""
    sorted_list = sort_by_date(transaction_list)
    assert [item["id"] for item in sorted_list] == [4, 3, 1, 2]


def test_sort_by_date_same_dates() -> None:
    """Тест: одинаковые даты – порядок должен сохраняться как у sorted (стабильная сортировка)."""
    data = [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "date": "2019-01-01"},
        {"id": 3, "date": "2020-01-01"},
    ]
    sorted_desc = sort_by_date(data, descending=True)
    assert [item["id"] for item in sorted_desc] == [1, 3, 2]
    sorted_asc = sort_by_date(data, descending=False)
    assert [item["id"] for item in sorted_asc] == [2, 1, 3]


def test_sort_by_date_empty_list(empty_list: list) -> None:
    """Тест на пустом списке."""
    assert sort_by_date(empty_list) == []

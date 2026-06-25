import pytest

from src.transaction_operations import count_operations_by_categories, search_by_description


@pytest.fixture
def sample_transactions():
    return [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Оплата услуг", "amount": 200},
        {"description": "Перевод с карты на карту", "amount": 300},
        {"description": "Открытие вклада", "amount": 400},
        {"description": "Перевод организации", "amount": 500},
    ]


def test_search_by_description_found(sample_transactions):
    result = search_by_description(sample_transactions, "перевод")
    assert len(result) == 3
    assert all("перевод" in t["description"].lower() for t in result)


def test_search_by_description_not_found(sample_transactions):
    result = search_by_description(sample_transactions, "пополнение")
    assert result == []


def test_search_by_description_empty_string(sample_transactions):
    result = search_by_description(sample_transactions, "")
    assert result == sample_transactions


def test_search_by_description_case_insensitive(sample_transactions):
    result = search_by_description(sample_transactions, "ОТКРЫТИЕ")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"


def test_count_operations_by_categories(sample_transactions):
    categories = ["Перевод организации", "Оплата услуг", "Открытие вклада"]
    result = count_operations_by_categories(sample_transactions, categories)
    expected = {"Перевод организации": 2, "Оплата услуг": 1, "Открытие вклада": 1}
    assert result == expected


def test_count_operations_by_categories_no_matches(sample_transactions):
    categories = ["Несуществующая"]
    result = count_operations_by_categories(sample_transactions, categories)
    assert result == {"Несуществующая": 0}

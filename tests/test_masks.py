"""
Тесты для модуля masks.
"""
import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстуры с валидными данными
@pytest.fixture
def valid_card_number() -> str:
    return "7000792289606361"


@pytest.fixture
def valid_account_number() -> str:
    return "73654108430135874305"


# Параметризация для функции маскировки карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Тест корректной маскировки для валидных номеров карт."""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_with_fixture(valid_card_number: str) -> None:
    """Тест с использованием фикстуры."""
    assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"


def test_get_mask_card_number_invalid_length() -> None:
    """Тест: номер карты не из 16 цифр -> ValueError."""
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр"):
        get_mask_card_number("1234567890")
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567")


def test_get_mask_card_number_non_digit() -> None:
    """Тест: номер карты содержит не цифры."""
    with pytest.raises(ValueError):
        get_mask_card_number("7000abcd89606361")


# Параметризация для маскировки счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("0000", "**0000"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str) -> None:
    """Тест корректной маскировки для валидных номеров счетов."""
    assert get_mask_account(account_number) == expected


def test_get_mask_account_with_fixture(valid_account_number: str) -> None:
    """Тест с фикстурой."""
    assert get_mask_account(valid_account_number) == "**4305"


def test_get_mask_account_too_short() -> None:
    """Тест: номер счета короче 4 цифр."""
    with pytest.raises(ValueError, match="Номер счета должен содержать не менее 4 цифр"):
        get_mask_account("123")
    with pytest.raises(ValueError):
        get_mask_account("")


def test_get_mask_account_non_digit() -> None:
    """Тест: номер счета содержит не цифры."""
    with pytest.raises(ValueError):
        get_mask_account("7365abcd4305")

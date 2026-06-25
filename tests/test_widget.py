"""
Тесты для модуля widget.
"""
import pytest

from src.widget import get_date, mask_account_card


# Фикстуры для данных
@pytest.fixture
def card_info() -> str:
    return "Visa Platinum 7000792289606361"


@pytest.fixture
def account_info() -> str:
    return "Счет 73654108430135874305"


# Параметризация для mask_account_card
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 12345", "Счет **2345"),
    ],
)
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    """Тест корректного маскирования для карт и счетов."""
    assert mask_account_card(input_str) == expected


def test_mask_account_card_with_fixtures(card_info: str, account_info: str) -> None:
    """Тест с фикстурами."""
    assert mask_account_card(card_info) == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card(account_info) == "Счет **4305"


def test_mask_account_card_invalid_format() -> None:
    """Тест на неправильный формат ввода (нет пробела)."""
    with pytest.raises(ValueError, match="Неверный формат"):
        mask_account_card("VisaPlatinum7000792289606361")
    with pytest.raises(ValueError):
        mask_account_card("Счет")


def test_mask_account_card_unknown_title() -> None:
    """Тест: неизвестный тип (не "Счет" и не что-то с пробелом)."""
    # Любой текст с пробелом, но не начинающийся со "Счет", будет трактоваться как карта
    result = mask_account_card("Unknown 1234567890123456")
    assert result == "Unknown 1234 56** **** 3456"


# Параметризация для get_date
@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00", "01.01.2020"),
        ("1999-12-31T23:59:59", "31.12.1999"),
    ],
)
def test_get_date_valid(date_str: str, expected: str) -> None:
    """Тест преобразования даты."""
    assert get_date(date_str) == expected


def test_get_date_no_time() -> None:
    """Тест: строка без времени (только дата)."""
    assert get_date("2025-05-05") == "05.05.2025"


def test_get_date_malformed() -> None:
    """Тест: некорректный формат (вызовет ошибку при split)."""
    with pytest.raises(ValueError):
        get_date("2024/03/11")

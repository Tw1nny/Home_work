"""
Тесты для модуля file_reader.
"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.file_reader import read_transactions_from_csv, read_transactions_from_excel


# Фикстура с примером данных для CSV
@pytest.fixture
def sample_csv_data() -> list:
    return [
        {"id": "1", "state": "EXECUTED", "date": "2023-01-01", "amount": "100"},
        {"id": "2", "state": "CANCELED", "date": "2023-01-02", "amount": "200"},
    ]


# Фикстура для mock DataFrame
@pytest.fixture
def mock_df(sample_csv_data):
    return pd.DataFrame(sample_csv_data)


def test_read_transactions_from_csv_success(mock_df):
    """Успешное чтение CSV."""
    with patch("pandas.read_csv", return_value=mock_df) as mock_read:
        result = read_transactions_from_csv("dummy.csv")
        mock_read.assert_called_once_with("dummy.csv", sep=";", encoding="utf-8")
        assert result == mock_df.to_dict(orient="records")


def test_read_transactions_from_csv_empty(mock_df):
    """Пустой CSV -> пустой список."""
    empty_df = pd.DataFrame()
    with patch("pandas.read_csv", return_value=empty_df):
        result = read_transactions_from_csv("empty.csv")
        assert result == []


def test_read_transactions_from_csv_file_not_found():
    """Файл не найден -> пустой список."""
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv("missing.csv")
        assert result == []


def test_read_transactions_from_csv_parser_error():
    """Ошибка парсинга -> пустой список."""
    with patch("pandas.read_csv", side_effect=pd.errors.ParserError):
        result = read_transactions_from_csv("bad.csv")
        assert result == []


def test_read_transactions_from_excel_success(mock_df):
    """Успешное чтение Excel."""
    with patch("pandas.read_excel", return_value=mock_df) as mock_read:
        result = read_transactions_from_excel("dummy.xlsx")
        mock_read.assert_called_once_with("dummy.xlsx", sheet_name=0, engine="openpyxl")
        assert result == mock_df.to_dict(orient="records")


def test_read_transactions_from_excel_empty(mock_df):
    """Пустой Excel -> пустой список."""
    empty_df = pd.DataFrame()
    with patch("pandas.read_excel", return_value=empty_df):
        result = read_transactions_from_excel("empty.xlsx")
        assert result == []


def test_read_transactions_from_excel_file_not_found():
    """Файл не найден -> пустой список."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel("missing.xlsx")
        assert result == []


def test_read_transactions_from_excel_general_exception():
    """Любая другая ошибка -> пустой список."""
    with patch("pandas.read_excel", side_effect=Exception("Something went wrong")):
        result = read_transactions_from_excel("bad.xlsx")
        assert result == []

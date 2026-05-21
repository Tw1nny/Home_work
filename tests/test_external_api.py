import pytest
from unittest.mock import patch, MagicMock
from src.external_api import convert_to_rub

# Фикстура с транзакцией USD
@pytest.fixture
def usd_transaction():
    return {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "USD", "name": "USD"}
        }
    }

@pytest.fixture
def eur_transaction():
    return {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"code": "EUR", "name": "EUR"}
        }
    }

@pytest.fixture
def rub_transaction():
    return {
        "operationAmount": {
            "amount": "2000",
            "currency": {"code": "RUB", "name": "RUB"}
        }
    }

def test_convert_usd_to_rub(usd_transaction):
    """Конвертация USD -> RUB с моком API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}

    with patch("src.external_api.requests.get", return_value=mock_response):
        result = convert_to_rub(usd_transaction)
    assert result == 100.50 * 90.5  # 9095.25

def test_convert_eur_to_rub(eur_transaction):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 98.2}}

    with patch("src.external_api.requests.get", return_value=mock_response):
        result = convert_to_rub(eur_transaction)
    assert result == 50.00 * 98.2  # 4910.0

def test_convert_rub(rub_transaction):
    """Для RUB конвертация не требуется."""
    result = convert_to_rub(rub_transaction)
    assert result == 2000.0

def test_api_failure(usd_transaction):
    """Если API вернул ошибку, должно быть исключение."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = Exception("API error")
        with pytest.raises(RuntimeError, match="Currency conversion failed"):
            convert_to_rub(usd_transaction)

def test_missing_api_key(usd_transaction):
    """Отсутствие переменной окружения."""
    with patch("src.external_api.API_KEY", None):
        with pytest.raises(ValueError, match="API key.*missing"):
            convert_to_rub(usd_transaction)
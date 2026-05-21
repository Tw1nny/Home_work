"""
Модуль для конвертации валют с использованием внешнего API.
"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Параметры:
        transaction (Dict[str, Any]): словарь с данными транзакции.
            Ожидается структура с ключами "operationAmount" -> "amount" и "currency" -> "code".
            Или альтернативно "amount" и "currency".

    Возвращает:
        float: сумма в рублях.
    """
    # Определяем структуру. Пробуем получить amount и код валюты
    amount = None
    currency_code = None

    # Вариант 1: вложенный operationAmount
    if "operationAmount" in transaction:
        op_amount = transaction["operationAmount"]
        amount = float(op_amount.get("amount", 0))
        currency_code = op_amount.get("currency", {}).get("code")
    # Вариант 2: прямые поля amount и currency
    elif "amount" in transaction and "currency" in transaction:
        amount = float(transaction["amount"])
        currency_code = transaction["currency"]

    if amount is None or currency_code is None:
        # Если не удалось определить, возвращаем 0 или логируем ошибку
        return 0.0

    if currency_code == "RUB":
        return amount

    if currency_code not in ("USD", "EUR"):
        # Если другая валюта, возвращаем 0 (можно расширить)
        return 0.0

    # Запрос курса к API
    if not API_KEY:
        raise ValueError("API key for Exchange Rates Data is missing. Set EXCHANGE_RATES_API_KEY in .env")

    headers = {"apikey": API_KEY}
    params = {"base": currency_code, "symbols": "RUB"}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            raise RuntimeError("RUB rate not found in API response")
        return round(amount * rate, 2)
    except (requests.RequestException, KeyError, ValueError) as e:
        # В случае ошибки API можно либо пробросить исключение, либо вернуть 0.
        # По заданию: если не удалось конвертировать, можно вернуть исходную сумму? Лучше raise.
        raise RuntimeError(f"Currency conversion failed: {e}")
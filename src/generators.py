"""
Модуль с генераторами для обработки банковских транзакций.
"""

from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Принимает список транзакций и код валюты, возвращает итератор,
    который выдает транзакции, где валюта соответствует заданной.

    Параметры:
        transactions: список словарей с данными о транзакциях.
        currency_code: код валюты (например, 'USD', 'EUR').

    Возвращает:
        Iterator[Dict[str, Any]]: итератор по отфильтрованным транзакциям.
    """
    for transaction in transactions:
        # Проверяем наличие поля operationAmount и currency
        if (transaction.get("operationAmount") and
            transaction["operationAmount"].get("currency") and
            transaction["operationAmount"]["currency"].get("code") == currency_code):
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Принимает список транзакций, возвращает генератор, который
    по очереди выдаёт описания каждой операции (поле "description").

    Параметры:
        transactions: список словарей с транзакциями.

    Возвращает:
        Iterator[str]: генератор строк с описаниями.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX
    для чисел в диапазоне от start до stop включительно.

    Параметры:
        start: начальное значение (целое число, минимум 1).
        stop: конечное значение (целое число, максимум 9999999999999999).

    Возвращает:
        Iterator[str]: генератор строк с номерами карт.
    """
    for number in range(start, stop + 1):
        # Форматируем как 16-значное число с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        formatted = " ".join([card_str[i:i+4] for i in range(0, 16, 4)])
        yield formatted
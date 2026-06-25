"""
Модуль для поиска по описанию и подсчёта категорий транзакций.
"""

import re
from collections import Counter
from typing import Any, Dict, List


def search_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится заданная строка (без учёта регистра).

    Параметры:
        transactions: список словарей с транзакциями.
        search_string: строка для поиска.

    Возвращает:
        список транзакций, у которых в описании есть искомая строка.
    """
    if not search_string:
        return transactions
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]


def count_operations_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям (точное совпадение описания).

    Параметры:
        transactions: список словарей с транзакциями.
        categories: список категорий (строк).

    Возвращает:
        словарь с ключами-категориями и значениями-количеством операций.
    """
    counter = Counter()
    for t in transactions:
        desc = t.get("description", "")
        if desc in categories:
            counter[desc] += 1
    return {cat: counter.get(cat, 0) for cat in categories}

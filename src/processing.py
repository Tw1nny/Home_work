"""
Модуль обработки списка банковских операций: фильтрация по статусу, сортировка по дате.
"""

from typing import List, Dict, Any, Optional

def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Параметры:
        data (List[Dict[str, Any]]): список словарей, каждый должен содержать ключ 'state'.
        state (str): значение для фильтрации (по умолчанию 'EXECUTED').

    Возвращает:
        List[Dict[str, Any]]: новый список, содержащий словари с указанным состоянием.
    """
    return [item for item in data if item.get("state") == state]

def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.

    Параметры:
        data (List[Dict[str, Any]]): список словарей, каждый должен содержать ключ 'date' в формате ISO (строка).
        descending (bool): порядок сортировки. True — по убыванию (сначала новые), False — по возрастанию.

    Возвращает:
        List[Dict[str, Any]]: новый отсортированный список.
    """
    # Используем sorted с ключом, извлекая дату; если даты нет, выбрасываем исключение (можно обработать)
    return sorted(data, key=lambda x: x["date"], reverse=descending)
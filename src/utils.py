"""
Модуль для работы с JSON-файлами банковских операций.
"""

import json
from typing import Any, Dict, List


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.

    Параметры:
        file_path (str): путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: список словарей с данными транзакций.
        Если файл пуст, содержит не список или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []

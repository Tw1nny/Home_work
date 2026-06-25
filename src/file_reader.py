"""
Модуль для чтения финансовых транзакций из CSV и Excel-файлов.
"""

from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл с транзакциями и возвращает список словарей.

    Параметры:
        file_path (str): путь к CSV-файлу.

    Возвращает:
        List[Dict[str, Any]]: список транзакций.
        В случае ошибки (пустой файл, неверный формат) возвращает пустой список.
    """
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        # Удаляем пустые строки (если есть)
        df = df.dropna(how="all")
        if df.empty:
            return []
        # Преобразуем DataFrame в список словарей
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл (xlsx) с транзакциями и возвращает список словарей.

    Параметры:
        file_path (str): путь к Excel-файлу.

    Возвращает:
        List[Dict[str, Any]]: список транзакций.
        В случае ошибки возвращает пустой список.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")
        # Удаляем пустые строки
        df = df.dropna(how="all")
        if df.empty:
            return []
        return df.to_dict(orient="records")
    except (FileNotFoundError, ValueError, Exception):
        return []

"""Модуль для работы с JSON-файлами банковских операций."""

import json
import logging
import os
from typing import Any, Dict, List

# Создаём логгер для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Убеждаемся, что папка logs существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка file_handler с перезаписью при каждом запуске (mode='w')
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат лога: время - имя модуля - уровень - сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем handler, если его ещё нет
if not logger.handlers:
    logger.addHandler(file_handler)


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.

    Параметры:
        file_path (str): путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: список словарей с данными транзакций.
        Если файл пуст, содержит не список или не найден, возвращает пустой список.
    """
    logger.debug(f"Попытка открыть файл: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            logger.info(f"Файл успешно загружен, количество транзакций: {len(data)}")
            return data
        else:
            logger.error(f"Файл {file_path} содержит не список (тип {type(data).__name__}), возвращаем пустой список")
            return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка значения при чтении файла {file_path}: {e}")
        return []

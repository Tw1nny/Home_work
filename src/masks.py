"""Модуль с функциями маскировки номеров карт и счетов."""

import logging
import os
from logging.handlers import RotatingFileHandler

# Создаём логгер для модуля masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Убеждаемся, что папка logs существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка file_handler с перезаписью при каждом запуске (mode='w')
file_handler = logging.FileHandler(os.path.join(log_dir, "masks.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат лога: время - имя модуля - уровень - сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем handler, если его ещё нет
if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты (строка из 16 цифр) и возвращает маску в формате XXXX XX** **** XXXX.

    Пример:
    >>> get_mask_card_number("7000792289606361")
    '7000 79** **** 6361'
    """
    try:
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Номер карты должен состоять из 16 цифр")
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Успешная маскировка карты: входной номер {card_number} -> {masked}")
        return masked
    except ValueError as e:
        logger.error(f"Ошибка маскировки карты: {e}. Входные данные: {card_number}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Принимает номер счета (строка цифр) и возвращает маску в формате **XXXX.

    Пример:
    >>> get_mask_account("73654108430135874305")
    '**4305'
    """
    try:
        if len(account_number) < 4 or not account_number.isdigit():
            raise ValueError("Номер счета должен содержать не менее 4 цифр")
        masked = f"**{account_number[-4:]}"
        logger.info(f"Успешная маскировка счета: входной номер {account_number} -> {masked}")
        return masked
    except ValueError as e:
        logger.error(f"Ошибка маскировки счета: {e}. Входные данные: {account_number}")
        raise

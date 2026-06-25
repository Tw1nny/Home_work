"""Модуль с функциями маскировки номеров карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты (строка из 16 цифр) и возвращает маску в формате XXXX XX** **** XXXX.

    Пример:
    >>> get_mask_card_number("7000792289606361")
    '7000 79** **** 6361'
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Принимает номер счета (строка цифр) и возвращает маску в формате **XXXX.

    Пример:
    >>> get_mask_account("73654108430135874305")
    '**4305'
    """
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать не менее 4 цифр")
    return f"**{account_number[-4:]}"

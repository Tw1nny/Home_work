from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Принимает строку вида "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".
    Возвращает строку с замаскированным номером.
    """
    parts = account_info.rsplit(" ", 1)
    if len(parts) != 2:
        raise ValueError("Неверный формат")
    title, number = parts
    if title.lower() == "счет":
        return f"{title} {get_mask_account(number)}"
    else:
        return f"{title} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """
    Принимает строку "2024-03-11T02:26:18.671407".
    Возвращает "11.03.2024".
    """
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"

import sys
from typing import List, Dict, Any

from src.utils import get_transactions_from_json
from src.file_reader import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.transaction_operations import search_by_description


def get_amount_and_currency(transaction: Dict[str, Any]) -> tuple:
    """
    Извлекает сумму и код валюты из транзакции, поддерживая разные структуры.
    Возвращает (amount, currency_code) или (0, "") если не найдено.
    """
    # Пробуем плоскую структуру (CSV/Excel)
    if "amount" in transaction and "currency_code" in transaction:
        return transaction.get("amount", 0), transaction.get("currency_code", "")
    # Пробуем вложенную структуру operationAmount (JSON)
    op_amount = transaction.get("operationAmount")
    if op_amount and isinstance(op_amount, dict):
        amount = op_amount.get("amount", 0)
        currency = op_amount.get("currency", {})
        if isinstance(currency, dict):
            code = currency.get("code", "")
        else:
            code = currency
        return amount, code
    return 0, ""


def format_transaction(transaction: Dict[str, Any]) -> str:
    """
    Форматирует одну транзакцию для вывода в консоль.
    """
    date_str = get_date(transaction.get("date", ""))
    description = transaction.get("description", "Без описания")
    amount, currency = get_amount_and_currency(transaction)

    if currency and currency.upper() == "RUB":
        amount_str = f"{amount} руб."
    else:
        amount_str = f"{amount} {currency}" if currency else f"{amount}"

    from_str = transaction.get("from")
    to_str = transaction.get("to")
    from_masked = mask_account_card(from_str) if from_str else ""
    to_masked = mask_account_card(to_str) if to_str else ""

    if from_masked and to_masked:
        transfer_info = f"{from_masked} -> {to_masked}"
    elif from_masked:
        transfer_info = from_masked
    elif to_masked:
        transfer_info = to_masked
    else:
        transfer_info = ""

    lines = [f"{date_str} {description}"]
    if transfer_info:
        lines.append(transfer_info)
    lines.append(f"Сумма: {amount_str}")
    return "\n".join(lines)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор (1/2/3): ").strip()

    transactions = []
    if choice == "1":
        file_path = "data/operations.json"
        print("Для обработки выбран JSON-файл.")
        transactions = get_transactions_from_json(file_path)
    elif choice == "2":
        file_path = "data/transactions.csv"
        print("Для обработки выбран CSV-файл.")
        transactions = read_transactions_from_csv(file_path)
    elif choice == "3":
        file_path = "data/transactions_excel.xlsx"
        print("Для обработки выбран XLSX-файл.")
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор. Завершаем работу.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте наличие файла и его формат.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                       "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").strip().upper()
        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered_by_state = filter_by_state(transactions, status)
    print(f"Операции отфильтрованы по статусу \"{status}\"")

    if not filtered_by_state:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = input("\nОтсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice in ("да", "д", "yes", "y"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        descending = order not in ("по возрастанию", "возрастанию", "asc", "возрастания")
        filtered_by_date = sort_by_date(filtered_by_state, descending)
    else:
        filtered_by_date = filtered_by_state

    # Фильтрация по рублю
    rub_choice = input("\nВыводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_choice in ("да", "д", "yes", "y"):
        filtered_by_rub = []
        for t in filtered_by_date:
            _, currency = get_amount_and_currency(t)
            if currency and currency.upper() == "RUB":
                filtered_by_rub.append(t)
        filtered_by_date = filtered_by_rub
        if not filtered_by_date:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return

    # Поиск по описанию
    search_choice = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    if search_choice in ("да", "д", "yes", "y"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_by_search = search_by_description(filtered_by_date, search_word)
            if not filtered_by_search:
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                return
            filtered_by_date = filtered_by_search

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_by_date)}")
    for t in filtered_by_date:
        print()
        print(format_transaction(t))


if __name__ == "__main__":
    main()
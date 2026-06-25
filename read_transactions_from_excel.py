from src.file_reader import read_transactions_from_excel

transactions = read_transactions_from_excel("data/transactions_excel.xlsx")
print(len(transactions))
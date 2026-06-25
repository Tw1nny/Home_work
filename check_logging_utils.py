from src.utils import get_transactions_from_json

# Пример 1: попытка прочитать несуществующий файл (должна быть ошибка)
print("=== Тест 1: файл не существует ===")
result = get_transactions_from_json("nonexistent.json")
print(f"Результат: {result}\n")

import json

# Пример 2: создадим временный JSON-файл с корректными данными
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".json") as tmp:
    json.dump([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}], tmp)
    tmp_path = tmp.name

print("=== Тест 2: корректный JSON-файл ===")
result = get_transactions_from_json(tmp_path)
print(f"Результат: {result}")

# Очистка
import os

os.unlink(tmp_path)

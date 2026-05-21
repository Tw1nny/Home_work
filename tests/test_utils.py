import json
import os
import tempfile

from src.utils import get_transactions_from_json


def test_get_transactions_valid() -> None:
    """Чтение корректного JSON со списком."""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f:
        json.dump([{"id": 1}, {"id": 2}], f)
        path = f.name
    result = get_transactions_from_json(path)
    assert result == [{"id": 1}, {"id": 2}]
    import os

    os.unlink(path)


def test_get_transactions_empty_list() -> None:
    """Файл содержит пустой список."""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f:
        json.dump([], f)
        path = f.name
    result = get_transactions_from_json(path)
    assert result == []
    os.unlink(path)


def test_get_transactions_not_a_list() -> None:
    """Файл содержит не список (например, словарь)."""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f:
        json.dump({"key": "value"}, f)
        path = f.name
    result = get_transactions_from_json(path)
    assert result == []
    os.unlink(path)


def test_get_transactions_file_not_found() -> None:
    """Файл не существует."""
    result = get_transactions_from_json("nonexistent.json")
    assert result == []


def test_get_transactions_invalid_json() -> None:
    """Некорректный JSON."""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f:
        f.write("not a json")
        path = f.name
    result = get_transactions_from_json(path)
    assert result == []
    os.unlink(path)

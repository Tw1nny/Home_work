import os
import tempfile

import pytest

from src.decorators import log

# ... другие тесты ...


def test_log_to_file_success() -> None:
    """Логирование успешного вызова в файл."""
    # Создаём временный файл, который не будет заблокирован
    fd, path = tempfile.mkstemp(text=True)
    os.close(fd)  # Закрываем дескриптор, чтобы файл можно было открыть повторно
    try:

        @log(filename=path)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)
        assert result == 20

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == "multiply ok\n"
    finally:
        os.unlink(path)  # Удаляем временный файл


def test_log_to_file_error() -> None:
    """Логирование ошибки в файл."""
    fd, path = tempfile.mkstemp(text=True)
    os.close(fd)
    try:

        @log(filename=path)
        def faulty_function(msg: str) -> None:
            raise ValueError(msg)

        with pytest.raises(ValueError, match="boom"):
            faulty_function("boom")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        assert "faulty_function error: ValueError. Inputs: ('boom',), {}" in content
    finally:
        os.unlink(path)

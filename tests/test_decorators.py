"""
Тесты для декоратора log.
"""

import pytest
import tempfile
from src.decorators import log


def test_log_to_console_success(capsys: pytest.CaptureFixture) -> None:
    """Логирование успешного вызова в консоль."""
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)
    captured = capsys.readouterr()
    assert result == 8
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys: pytest.CaptureFixture) -> None:
    """Логирование ошибки в консоль."""
    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_log_to_file_success() -> None:
    """Логирование успешного вызова в файл."""
    with tempfile.NamedTemporaryFile(mode="r+", encoding="utf-8") as tmp_file:
        @log(filename=tmp_file.name)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)
        assert result == 20

        tmp_file.seek(0)
        content = tmp_file.read()
        assert content == "multiply ok\n"


def test_log_to_file_error() -> None:
    """Логирование ошибки в файл."""
    with tempfile.NamedTemporaryFile(mode="r+", encoding="utf-8") as tmp_file:
        @log(filename=tmp_file.name)
        def faulty_function(msg: str) -> None:
            raise ValueError(msg)

        with pytest.raises(ValueError, match="boom"):
            faulty_function("boom")

        tmp_file.seek(0)
        content = tmp_file.read().strip()
        assert "faulty_function error: ValueError. Inputs: ('boom',), {}" in content


def test_log_preserves_function_metadata() -> None:
    """Декоратор не должен терять имя и документацию функции."""
    @log()
    def sample(x: int) -> int:
        """Возвращает квадрат."""
        return x ** 2

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Возвращает квадрат."
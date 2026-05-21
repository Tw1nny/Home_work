"""
Модуль с декоратором log для логирования вызовов функций.
"""

import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор, логирующий вызов функции и её результат (или ошибку).

    Параметры:
        filename (Optional[str]): если указано, логи пишутся в файл,
                                   иначе выводятся в консоль.

    Возвращает:
        Callable: обёрнутую функцию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)
                raise  # повторно поднимаем исключение, чтобы не менять поведение

        return wrapper

    return decorator
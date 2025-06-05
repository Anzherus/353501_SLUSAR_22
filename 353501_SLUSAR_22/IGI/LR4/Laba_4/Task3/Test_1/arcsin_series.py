"""
Модуль для расчета арксинуса с использованием разложения в степенной ряд
"""

import math
from typing import Tuple, List


def log_execution(func):
    """Декоратор для регистрации выполнения функции"""

    def wrapper(*args, **kwargs):
        print(f"\nExecuting {func.__name__} with x = {args[0]}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} completed with result {result}")
        return result

    return wrapper


def calculate_arcsin_series(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int, List[float]]:
    """
   Вычислите arcsin(x), используя расширение степенного ряда.
Возвращает кортеж: (result, n, sequence_terms)
    """
    if abs(x) >= 1:
        raise ValueError("|x| must be < 1 for series convergence")

    result = 0.0
    term = x
    n = 0
    sequence_terms = []

    while abs(term) > eps and n < max_iter:
        result += term
        sequence_terms.append(term)
        n += 1
        term = term * (x ** 2) * (2 * n - 1) ** 2 / (2 * n * (2 * n + 1))

    if n == max_iter:
        print(f"Reached maximum iterations ({max_iter})")

    return result, n, sequence_terms


@log_execution
def math_arcsin(x: float) -> float:
    """
  Вычислите arcsin(x), используя математический модуль для сравнения.
    """
    return math.asin(x)
"""
Модуль методов инициализации данных
"""

import random
from input_utils import input_float

def initialize_from_input() -> float:
    """
    Инициализируйте значение x из введенного пользователем значения.
    """
    return input_float("Enter x value (|x| < 1): ", -1.0, 1.0)

def initialize_from_generator() -> float:
    """
Инициализируйте значение x с помощью генератора случайных чисел.
    """
    return random.uniform(-0.99, 0.99)
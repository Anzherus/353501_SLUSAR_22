"""
Модуль для безопасной обработки пользовательского ввода
"""

def _get_float_input(prompt: str) -> float:
    """Вспомогательная функция для получения плавающего ввода с обработкой ошибок"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number")
        except KeyboardInterrupt:
            print("\nInput interrupted by user")
            raise

def input_float(prompt: str, min_val: float = -1.0, max_val: float = 1.0) -> float:
    """
    Безопасное чтение числа с плавающей точкой из пользовательского ввода в пределах [min_val, max_val].
    """
    while True:
        value = _get_float_input(prompt)
        if min_val <= value <= max_val:
            return value
        print(f"Error: Value must be between {min_val} and {max_val}")

def input_eps() -> float:
    """
    Считайте положительное значение эпсилон от пользователя.
    """
    while True:
        eps = _get_float_input("Enter calculation precision (eps > 0): ")
        if eps > 0:
            return eps
        print("Error: Precision must be positive")
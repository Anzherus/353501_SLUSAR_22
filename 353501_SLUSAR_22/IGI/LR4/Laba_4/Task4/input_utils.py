def input_float(prompt: str, min_val: float = 0.1) -> float:
    """Безопасный ввод чисел с плавающей точкой"""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"Значение должно быть больше {min_val}")
                continue
            return value
        except ValueError:
            print("Ошибка: введите число")

def input_shape_choice() -> str:
    """Выбор типа фигуры"""
    print("\nВыберите фигуру:")
    print("1 - Прямоугольник")
    print("2 - Круг")
    print("0 - Выход")
    return input("Ваш выбор (0-2): ").strip()
import numpy as np
from matrix_operations import create_random_matrix, find_min_anti_diagonal, get_anti_diagonal
from statistical_operations import calculate_variance_standard, calculate_variance_manual, calculate_statistics


def main():
    # Параметры матрицы
    n, m = 5, 5  # Для работы с диагональю делаем квадратную матрицу

    # 1. Создание и вывод матрицы
    A = create_random_matrix(n, m)
    print("Сгенерированная матрица A:")
    print(A)

    # 2. Демонстрация возможностей NumPy
    print("\nДемонстрация возможностей NumPy:")
    # a.1 Создание массивов
    arr = np.array([1, 2, 3, 4, 5])
    print("\nСозданный массив:", arr)

    # a.2 Специальные массивы
    print("\nМассив нулей 2x3:\n", np.zeros((2, 3)))
    print("Массив единиц 3x2:\n", np.ones((3, 2)))

    # a.3 Индексирование
    print("\nЭлемент A[0,1]:", A[0, 1])
    print("Срез первой строки:", A[0, :])

    # a.4 Поэлементные операции
    print("\nМатрица умноженная на 2:\n", A * 2)

    # 3. Работа с побочной диагональю
    anti_diag = get_anti_diagonal(A)
    print("\nЭлементы побочной диагонали:", anti_diag)

    # 4. Нахождение минимального элемента
    min_element = find_min_anti_diagonal(A)
    print("\nНаименьший элемент на побочной диагонали:", min_element)

    # 5. Вычисление дисперсии
    variance_std = calculate_variance_standard(anti_diag)
    variance_manual = calculate_variance_manual(anti_diag)
    print("\nДисперсия (стандартная функция):", round(variance_std, 2))
    print("Дисперсия (по формуле):", round(variance_manual, 2))

    # 6. Другие статистические показатели
    stats = calculate_statistics(anti_diag)
    print("\nДругие статистические показатели:")
    print(f"Среднее: {stats['mean']}")
    print(f"Медиана: {stats['median']}")
    print(f"Стандартное отклонение: {stats['std']}")

    if stats['corrcoef'] is not None:
        print("\nМатрица корреляции:")
        print(stats['corrcoef'])


if __name__ == "__main__":
    main()
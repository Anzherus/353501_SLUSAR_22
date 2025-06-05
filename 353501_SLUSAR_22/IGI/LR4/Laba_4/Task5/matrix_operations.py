import numpy as np

def create_random_matrix(n, m):
    """Создание случайной целочисленной матрицы"""
    return np.random.randint(0, 100, size=(n, m))

def get_anti_diagonal(matrix):
    """Получение элементов побочной диагонали"""
    return np.diag(np.fliplr(matrix))

def find_min_anti_diagonal(matrix):
    """Нахождение минимального элемента на побочной диагонали"""
    anti_diag = get_anti_diagonal(matrix)
    return np.min(anti_diag)